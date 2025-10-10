import ansys.fluent.core as pyfluent
import numpy as np

from GUI_SubClasses.GUI_BoundaryConditions import Boundary_conditions_sett
from GUI_SubClasses.GUI_Simulation import SimulationSett
from GUI_SubClasses.GUI_General import GeneralSett
from GUI_SubClasses.GUI_Postprocess import PostprocessSett
from GUI_SubClasses.GUI_Tunnel import TunnelSett

#density = 1.15

def load_fan_curve_from_txt(Fan_2D_curve_Path):
        data_points = []
        with open(Fan_2D_curve_Path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue  # skip empty or commented lines
                try:
                    parts = line.split()
                    velocity = float(parts[0])
                    pressure = float(parts[1])
                    data_points.append({'item': velocity, 'value': pressure})
                except (ValueError, IndexError):
                    print(f"Skipping invalid line: {line}")
        return data_points


def FindPart(Name, list):
    '''
    Function for finding a part in a list
    '''
    for part in list:
        print(part)
        print(part.find(Name))
        if part.find(Name)!= -1:
            return part
    return None    

def CalculatePressure(height):
    P_b = 101325 #Pa
    M = 0.0289644
    g_0 = 9.80665
    R =  8.3144598
    T = 288.15
    P = P_b*np.exp((-g_0*M*(height))/(R*T))
    return P

def CalculateDensity(Press, Temp):
    Rho_b = 1.2250
    T_b = 288.15
    P_b = 101325
    Temp = Temp+273.15
    
    Rho = Rho_b*Press/Temp*T_b/P_b
    return Rho

def CalculateViscosity(Temp):
    b = 1.458*10**-6
    S = 110.4
    T = Temp+273.15
    Mi = (b*T**(3/2))/(T+S)
    return Mi

def StartFluentSolver(BoundarySett: Boundary_conditions_sett, 
                      SolvSett:SimulationSett,   
                      TurnSett:TunnelSett,                   
                      MSH_Objects, 
                      SettGen:GeneralSett, 
                      PostproSett:PostprocessSett,
                      MeshPath = None):
    '''
    Start of a function containing whole solver workflow
    Inputs:
    BoundarySett - SolverSettings object containing settings for a solver
    Meshing - Fluent Instance returned from Meshing function
    workingDirectory - A path to a working directory#
    MSH_Object - list of all meshing objects that contains info about scopesizing, object type, prism settings etc.
    Returns:
    A fluent instance
    '''
    work_Directory = SettGen.workingDirectory

    #solve = Meshing.switch_to_solver() #Switches to a solver workflow
    solve = pyfluent.launch_fluent(mode= pyfluent.FluentMode.SOLVER,
                                     product_version= SettGen.Version,
                                     precision = SettGen.DoublePrecision,
                                     processor_count=int(SettGen.IntCoreCount),  #2, ...když chceš aby byl počet jader podle GUI
                                     ui_mode= SettGen.GUI, 
                                     cleanup_on_exit= True, 
                                     py = SettGen.PyConsole, 
                                     cwd= SettGen.workingDirectory,
                                     additional_arguments='-mpi=intel',
                                     gpu= SettGen.GPU,
                                     env={"FLUENT_WEBSERVER_TOKEN":'12345', "STARTED_BY_SIMBA":True},
                                     )

    if MeshPath == None:
        solve.settings.file.read_mesh(file_name = SettGen.CAD_Path)    
    else:
        
        solve.settings.file.read_mesh(file_name = MeshPath)
    
    '''
    Web Server
    '''
    if SettGen.WebServer:
        solve.tui.server.start_web_server()
    '''
    Setup a material properties
    '''
    density = CalculateDensity(CalculatePressure(SolvSett.Height), SolvSett.Temperature)
    solve.settings.setup.materials.fluid['air'].density.value = density #change density of air
    
    viscosity = CalculateViscosity(SolvSett.Temperature)
    solve.settings.setup.materials.fluid['air'].viscosity.value = viscosity
    '''
    Setup of reference values
    '''
    solve.settings.setup.reference_values.density = density
    solve.settings.setup.reference_values.area = 0.5
    solve.settings.setup.reference_values.pressure = 0
    solve.settings.setup.reference_values.temperature = SolvSett.Temperature
    solve.settings.setup.reference_values.velocity = BoundarySett.velocity

    '''
    Energy equation 
    '''
    if BoundarySett.Fan_2D_check:
        solve.settings.setup.models.energy.enabled = True

    '''
    Turbulence model 
    '''
    solve.settings.setup.models.viscous.model = SolvSett.Turbulence_model
    solve.settings.setup.models.viscous.options.curvature_correction = True
    solve.settings.setup.models.viscous.options.production_kato_launder_enabled = True
    
    if SolvSett.Turbulence_model == 'k-epsilon':
        solve.settings.setup.models.viscous.k_epsilon_model = 'realizable'
        solve.settings.setup.models.viscous.near_wall_treatment.wall_treatment = SolvSett.Wall_function
    else:
        solve.settings.setup.models.viscous.options.corner_flow_correction = True
    
    '''
    2D fan zone 
    '''
    if BoundarySett.Fan_2D_check:
        solve.settings.setup.boundary_conditions.set_zone_type(zone_list=["*rotor*"],new_type="fan",) #change of BC from interior to fan
        fan_1_name = FindPart('rotor', list(solve.settings.setup.boundary_conditions.fan.keys())) #find name of front wheel part
        fan_1 = solve.settings.setup.boundary_conditions.fan[str(fan_1_name)]
        fan_1.pressure_jump_specification.reverse_fan_direction = True #fan direction specification
        '''
        Piecewise-linear pressure jump [normal velocity/pressure]
        '''
        
        fan_1.pressure_jump_specification.pressure_jump.option = 'piecewise-linear'
        fan_1.pressure_jump_specification.pressure_jump.piecewise_linear.function_of = 'normal-velocity'
        fan_curve_path = BoundarySett.Fan_2D_curve_Path  # Path stored in Boundary_conditions_sett
        fan_curve_data = load_fan_curve_from_txt(fan_curve_path)
        fan_1.pressure_jump_specification.pressure_jump.piecewise_linear.data_points = fan_curve_data #[{'item': 0, 'value': 0}, {'item': 1, 'value': 1}, {'item': 2, 'value': 4}, {'item': 3, 'value': 8}]
        '''
        Constant pressure jump [Pa] 
        '''
        #fan_1.pressure_jump_specification.profile_specification_of_pressure_jump = True #fan curve specification
        #fan_1.pressure_jump_specification.pressure_jump_profile.value = 2000           #fixed pressure jump [Pa]
        '''
        Polynomial pressure jump [normal velocity/pressure]
        '''
        #fan_1.pressure_jump_specification.pressure_jump.option = 'polynomial'
        #fan_1.pressure_jump_specification.pressure_jump.polynomial.function_of = 'normal-velocity'
        #fan_1.pressure_jump_specification.pressure_jump.polynomial.coefficients = [1, 2, 3, 4, 5, 6, 7, 8] #polynomial pressure jump specification

    
    '''
    Porous media setup
    '''
    if BoundarySett.Radiator_check:
        #solve.settings.mesh.modify_zones.sep_face_zone_angle(face_zone_name = "*radiator*region-1*", angle = 90, move_faces = False)
        #solve.settings.mesh.modify_zones.sep_face_zone_angle(face_zone_name = "*radiator*radiator-1*", angle = 90, move_faces = False)
        solve.tui.mesh.modify_zones.sep_face_zone_angle('*radiator*region-1*', 90, 'yes')
        solve.tui.mesh.modify_zones.sep_face_zone_angle('*radiator*radiator-1*', 90, 'yes')
        #solve.settings.setup.mesh_interfaces.create_manually(name = "radiator1", zone_list_1 = ["*radiator*region-1"], zone_list_2 = ["*radiator*radiator-1"])
        #solve.settings.setup.mesh_interfaces.create_manually(name = "radiator2", zone_list_1 = ["*radiator*region-1:*"], zone_list_2 = ["*radiator*radiator-1:*"])
        solve.settings.setup.mesh_interfaces.create_manually(name = 'radiator-interface', zone_list_1 = ['*radiator*region-1*'], zone_list_2 = ['*radiator*radiator-1*']) 

        solve.settings.setup.mesh_interfaces.delete_interfaces_with_small_overlap(delete = True, overlapping_percentage_threshold = 10)
        radiator_1 = solve.settings.setup.cell_zone_conditions.fluid['radiator-1']
        radiator_1.porous_zone.porous = True
        radiator_1.porous_zone.viscous_resistance = [0, 211100000, 211100000]
        radiator_1.porous_zone.power_law_c0 = BoundarySett.power_law_c_0
        radiator_1.porous_zone.power_law_c1 = BoundarySett.power_law_c_1
        radiator_1.porous_zone.porosity = BoundarySett.porosity



    '''
    3D fan zone ///in construction...
    '''
    #if BoundarySett.Fan_check:
        
        #fan_1 = solve.settings.setup.cell_zone_conditions.fluid['fan-1']
        #fan_1.fan_zone.fan_zone = True
        #fan_1.fan_zone.fan_hub_rad = 1
        #fan_1.fan_zone.fan_tip_rad = 2
        #fan_1.fan_zone.fan_thickness = 3
        #fan_1.fan_zone.fan_origin = [1, 2, 3]
        #fan_1.fan_zone.fan_rot_dir = 'positive'
        #fan_1.fan_zone.fan_opert_angvel = 300
        #fan_1.fan_zone.axial_source_term = True
        #fan_1.fan_zone.fan_axial_source_method = 'fan curve'

    '''
    BoundarySett a inlet BC
    '''
    inlet = solve.settings.setup.boundary_conditions.velocity_inlet['tunnel-xmin']
    
    
   


    if TurnSett.turn_check == 1:
        inlet.momentum.velocity = 0
        inlet.momentum.reference_frame = 'Relative to Adjacent Cell Zone'
        
        '''
        BoundarySett a road BC
        '''
        road = solve.settings.setup.boundary_conditions.wall['tunnel-zmin']
        road.momentum.wall_motion = 'Moving Wall'
        road.momentum.rotating = True
        road.momentum.rotation_speed =  BoundarySett.velocity/TurnSett.radius
        road.momentum.rotation_axis_origin = [0,TurnSett.radius,0]
        road.momentum.rotation_axis_direction = [0,0,1]
        
        '''
        Cell zone movement
        '''
        
        zone = solve.settings.setup.cell_zone_conditions['fluid-region-1']
        zone.reference_frame.frame_motion = True
        zone.reference_frame.mrf_omega = BoundarySett.velocity/TurnSett.radius
        zone.reference_frame.reference_frame_axis_origin = [0,TurnSett.radius,0]
        zone.reference_frame.reference_frame_axis_direction = [0,0,1]
        
    
    else: 
        inlet.momentum.velocity = BoundarySett.velocity
        
        '''
        BoundarySett a road BC
        '''
        road = solve.settings.setup.boundary_conditions.wall['tunnel-zmin']
        road.momentum.wall_motion = 'Moving Wall'
        road.momentum.speed = BoundarySett.velocity
        road.momentum.direction = [1,0,0]
    
    #list of all surfaces on a car
    wall_list = list(solve.settings.setup.boundary_conditions.wall.keys()) #list of all wall BC surfaces
    for wall in wall_list:
        if wall.find(r'tunnel-zmin') != -1: #exclude road surface
            wall_list.remove(wall)
    
    '''
    Setting of a Wheel BC
    '''
    #front wheels
    f_wheel_name = FindPart('front_tyre', list(solve.settings.setup.boundary_conditions.wall.keys())) #find name of front wheel part
    f_wheel = solve.settings.setup.boundary_conditions.wall[str(f_wheel_name)] 
    f_wheel.momentum.wall_motion = 'Moving Wall'
    f_wheel.momentum.rotating = True #sett the wall motion as rotating
    f_wheel.momentum.rotation_speed = -BoundarySett.velocity/BoundarySett.WheelDiameter*2 #calculate rotaional speed [rad/s]
    f_wheel.momentum.rotation_axis_origin = [BoundarySett.f_w_axis_x,BoundarySett.f_w_axis_y, BoundarySett.f_w_axis_z]
    f_wheel.momentum.rotation_axis_direction = [0,1,0]
    
    #rear wheels
    r_wheel_name = FindPart('rear_tyre', list(solve.settings.setup.boundary_conditions.wall.keys()))
    print(r_wheel_name)
    r_wheel = solve.settings.setup.boundary_conditions.wall[str(r_wheel_name)]
    r_wheel.momentum.wall_motion = 'Moving Wall'
    r_wheel.momentum.rotating = True
    r_wheel.momentum.rotation_speed = -BoundarySett.velocity/BoundarySett.WheelDiameter*2
    r_wheel.momentum.rotation_axis_origin = [BoundarySett.r_w_axis_x,BoundarySett.r_w_axis_y, BoundarySett.r_w_axis_z]
    r_wheel.momentum.rotation_axis_direction = [0,1,0]
    
    '''
    Solver method setting
    '''
    solve.settings.solution.methods.high_order_term_relaxation.enable = True #enabling high order term relaxation
    solve.settings.solution.methods.p_v_coupling.flow_scheme = SolvSett.Coupling    
    '''
    Report definitions and plots
    '''
    Report_def_list = []
    #setup a drag rep. def. on whole car
    solve.settings.solution.report_definitions.drag['Drag'] = {} #report definition initialisation
    Drag_rep = solve.settings.solution.report_definitions.drag['Drag']
    Drag_rep.zones = wall_list #assigning surfaces to the report definition
    Drag_rep.report_output_type =  'Drag Force' #setting a tyoe os definition ('Drag Force' or 'Drag Coefficionet')
    Drag_rep.force_vector = [1,0,0]
    
    solve.settings.solution.monitor.report_plots["Drag-plot"] = {}
    Drag_plot = solve.settings.solution.monitor.report_plots["Drag-plot"]
    Drag_plot_list = ["Drag"]
    Report_def_list.append("Drag")
    Drag_plot.print = True
    

    #setup a lift rep. def. on whole car
    solve.settings.solution.report_definitions.lift['Lift'] = {}
    Lift_rep = solve.settings.solution.report_definitions.lift['Lift']
    Lift_rep.zones = wall_list
    Lift_rep.report_output_type =  'Lift Force'
    Lift_rep.force_vector = [0,0,1]
    
    solve.settings.solution.monitor.report_plots["Lift-plot"] = {}
    Lift_plot = solve.settings.solution.monitor.report_plots["Lift-plot"]
    Lift_plot_list  =["Lift"]
    Report_def_list.append("Lift")
    #Lift_plot.print = True
    
    #setup a moment rep. def. on whole car
    solve.settings.solution.report_definitions.moment['f_axis_moment'] = {}
    f_mom_rep = solve.settings.solution.report_definitions.moment['f_axis_moment']
    f_mom_rep.zones =wall_list
    f_mom_rep.report_output_type = 'Moment'
    f_mom_rep.mom_center = [0,0,-0.2]
    f_mom_rep.mom_axis = [0,1,0]
    
    solve.settings.solution.monitor.report_plots["Moment-plot"] = {}
    Moment_plot = solve.settings.solution.monitor.report_plots["Moment-plot"]
    Moment_plot.report_defs = 'f_axis_moment'
    Report_def_list.append('f_axis_moment')
    Moment_plot.print = True
    if BoundarySett.Radiator_check:
        #setup a mass flow rate rep. def. on radiator
        solve.settings.solution.report_definitions.flux['Radiator'] = {}
        Mass_flow_rep = solve.settings.solution.report_definitions.flux['Radiator']
        Mass_flow_rep.boundaries = list(solve.settings.setup.boundary_conditions.interface.keys())[0]

        
        solve.settings.solution.monitor.report_plots["Radiator-plot"] = {}
        Radiator_plot = solve.settings.solution.monitor.report_plots["Radiator-plot"]
        Radiator_plot.report_defs = 'Radiator'
        Report_def_list.append('Radiator')
        Radiator_plot.print = True
        
    '''
    looping for report definitions on individual subassemblies
    '''
    for Obj in MSH_Objects['vehicle']: #loop through all MSH objects
        obj_wall_list = Obj._findParts(MSH_Objects['vehicle'], list(solve.settings.setup.boundary_conditions.wall.keys())) #find all parts for given subassembly
        
        solve.settings.solution.report_definitions.drag['Drag-'+Obj.Name] = {} 
        Drag_rep = solve.settings.solution.report_definitions.drag['Drag-'+Obj.Name]
        Drag_rep.zones = obj_wall_list
        Drag_rep.report_output_type =  'Drag Force'
        Drag_rep.force_vector = [1,0,0]
        Drag_plot_list.append('Drag-'+Obj.Name) #append created report definition to a drag plot for all drag reports
        Report_def_list.append('Drag-'+Obj.Name)
        '''
        solve.settings.solution.monitor.report_plots['Drag-plot-'+Obj.Name] = {}
        Drag_plot = solve.settings.solution.monitor.report_plots['Drag-plot-'+Obj.Name]
        Drag_plot.report_defs = 'Drag-'+Obj.Name
        Drag_plot.print = True
        '''
        
        solve.settings.solution.report_definitions.lift['Lift-'+Obj.Name] = {}
        Lift_rep = solve.settings.solution.report_definitions.lift['Lift-'+Obj.Name]
        Lift_rep.zones = obj_wall_list
        Lift_rep.report_output_type =  'Lift Force'
        Lift_rep.force_vector = [0,0,1]
        Lift_plot_list.append('Lift-'+Obj.Name)
        Report_def_list.append('Lift-'+Obj.Name)
        '''
        solve.settings.solution.monitor.report_plots['Lift-plot-'+Obj.Name] = {}
        Lift_plot = solve.settings.solution.monitor.report_plots['Lift-plot-'+Obj.Name]
        Lift_plot.report_defs = 'Lift-'+Obj.Name
        Lift_plot.print = True
        '''

    Lift_plot.report_defs = Lift_plot_list

    Drag_plot.report_defs = Drag_plot_list

    if BoundarySett.Fan_2D_check:
        #setup a mass flow rate rep. def. on fan and delete its force report
        solve.tui.solve.report_definitions.delete('"Drag-rotor"')
        solve.tui.solve.report_definitions.delete('"Lift-rotor"')
        #solve.settings.solution.report_definitions.flux['rotor'] = {}
        #Mass_flow_rep_fan = solve.settings.solution.report_definitions.flux['rotor']
        #Mass_flow_rep_fan.boundaries = list(solve.settings.setup.boundary_conditions.interior.keys())[0]

        
        #solve.settings.solution.monitor.report_plots["rotor-plot"] = {}
        #Fan_plot = solve.settings.solution.monitor.report_plots["rotor-plot"]
        #Fan_plot.report_defs = 'rotor'
        #Report_def_list.append('rotor')
        #Fan_plot.print = True
    
    solve.settings.solution.report_definitions.volume['Max-p'] = {}
    Max_P_rep = solve.settings.solution.report_definitions.volume['Max-p']
    Max_P_rep.cell_zones = 'fluid-region-1'
    Max_P_rep.report_type = 'volume-max'
    Max_P_rep.field = 'total-pressure'
    
    solve.settings.solution.monitor.report_plots["Max-p-plot"] = {}
    Max_P_plot = solve.settings.solution.monitor.report_plots["Max-p-plot"]
    Max_P_plot.report_defs = "Max-p"
    Report_def_list.append("Max-p")
    Max_P_plot.print = True

    solve.settings.solution.monitor.report_files["Rep-file"] = {}
    Report_file = solve.settings.solution.monitor.report_files["Rep-file"]

    #Report_file.report_defs = Report_def_list
    valid_names = []
    for rep_type in solve.settings.solution.report_definitions:
        valid_names.extend(dir(solve.settings.solution.report_definitions[rep_type]))
    valid_report_defs = [r for r in Report_def_list if r in valid_names]
    Report_file.report_defs = valid_report_defs

    solve.tui.file.write_case(SettGen.workingDirectory+r'\Pred_compute.cas.h5')
    

    solve.settings.solution.initialization.initialization_type = 'hybrid'
    solve.settings.solution.initialization.initialize()

    #print(sorted(solve.settings.monitors.get_monitor_set_names()))
    solve.settings.solution.monitor.residual.options.criterion_type = 'none'


    solve.settings.setup.general.solver.time = SolvSett.Transient
    
    if SolvSett.Transient == 'steady': 
        if SolvSett.Coupling == 'Coupled':
            solve.settings.solution.methods.pseudo_time_method.formulation.coupled_solver = 'global-time-step'
            solve.settings.solution.run_calculation.pseudo_time_settings.time_step_method.time_step_size_scale_factor = SolvSett.TimeStep
        solve.settings.solution.run_calculation.iter_count = SolvSett.iter_count-PostproSett.Iteration_averaging
    else:
        solve.settings.solution.run_calculation.transient_controls.time_step_count = int(SolvSett.Time/SolvSett.TimeStep)
        solve.settings.solution.run_calculation.transient_controls.time_step_size = SolvSett.TimeStep
        solve.settings.solution.run_calculation.transient_controls.max_iter_per_time_step = SolvSett.iter_count
    
    ''' 
    Relaxation factors
    '''
    if SolvSett.Transient == 'steady': 
        if SolvSett.Coupling == 'Coupled':
            solve.settings.solution.controls.p_v_controls.explicit_momentum_under_relaxation = 0.5
        else:
            solve.settings.solution.controls.under_relaxation["mom"] = 0.5

    #solve.tui.file.write_case(SettGen.workingDirectory+r'\Pred_compute.cas.h5')
    
    ''' 
    First number of iterations before report definition is created
    '''    
    solve.tui.solve.iterate()

    ''' 
    Data smpling
    '''   
    solve.settings.solution.run_calculation.data_sampling.enabled = True
    solve.settings.solution.run_calculation.data_sampling.sampling_interval = 5
    solve.settings.solution.run_calculation.data_sampling.wall_statistics = True
    solve.settings.solution.run_calculation.data_sampling.force_statistics = True  

    # solve.settings.solution.run_calculation.data_sampling_options.add_datasets(
    #     zone_names = wall_list, 
    #     quantities = ['pressure-coefficient', 'x-wall-shear', 'total-pressure', 'vorticity-mag', 'pressure','velocity-magnitude'], 
    #     moving_average = True, 
    #     average_over = 200
    #     )

    solve.tui.solve.iterate(PostproSett.Iteration_averaging)
    
    solve.settings.solution.run_calculation.calculate()
    #print(sorted(solve.monitors.get_monitor_set_names()))
    
    
    solve.tui.file.write_case_data(SettGen.workingDirectory+r'\Results.cas.h5')
    return str(SettGen.workingDirectory+r'\Results.cas.h5')


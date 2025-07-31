import ansys.fluent.core as pyfluent
import numpy as np
import pandas as pd
import os
import openpyxl
import openpyxl.workbook


from GUI_SubClasses.GUI_BoundaryConditions import Boundary_conditions_sett
from GUI_SubClasses.GUI_General import GeneralSett
from GUI_SubClasses.GUI_Postprocess import PostprocessSett



front_view = {
    'up_vector': [0,0,1],
    'position' : [-3,0,0.4],
    'target' : [0,0,0.4],
    'width': 1.5,
    'height':1.5,
}

side_view = {
    'up_vector': [0,0,1],
    'position' : [0.9, 4, 0.68],
    'target' : [0.9,0,0.68],
    'width': 2.2,
    'height':2.2,
}

top_view = {
    'up_vector': [0,-1,0],
    'position' : [0.9, 0, 4],
    'target' : [0.9,0,0.5],
    'width': 2.5,
    'height':2.5,
}

def create_contour(root, name:str, field:str, surfaces_list:list,range ):
    '''
    Function for quick creating of contour objects.
    Inputs:
    root - Fluent instance
    name - Name of the contour [string]
    field - 
    surfaces_list - List of surfaces on which the contour shlould be shown on [list[string]]
    range - Min and Max values of the contour [list[float]]
    Returns:
    Object of created contour
    '''
    graphics = root.results.graphics
    
    graphics.contour.create(name)
    
    graphics.contour[name] = {"coloring": {
        "option": "banded",
        "smooth": False,
    },
    "field": field,
    "filled": True, 
    'surfaces_list': surfaces_list,
    }
    
    graphics.contour[name].range_option.option = 'auto-range-off'
    graphics.contour[name].range_option.auto_range_off.minimum = range[0]
    graphics.contour[name].range_option.auto_range_off.maximum = range[1]
    graphics.contour[name].coloring.option = 'smooth'

    
    
    return graphics.contour[name]

def create_lic(root, name:str, field:str,vector_field:str,  plane:str, range):
    '''
    Function for quick line integral convolutoion creation.
    Input:
    rooot - Fluent Instance
    name - LICs name [string]
    field - field to be visualised [string]
    vector_field - field used for vector directions [string]
    plane - plane on which to show the LIC [string]
    range - Min and Max values range [list[float]]
    Returns:
    Object of created LICs
    '''
    lic = root.results.graphics.lic
    lic.create(name)
    
    lic[name].field = field
    lic[name].vector_field = vector_field
    lic[name].surfaces_list = plane
    lic[name].range_option.option = 'auto-range-off'
    lic[name].range_option.auto_range_off.minimum = range[0]
    lic[name].range_option.auto_range_off.maximum = range[1]
    lic[name].lic_intensity_factor = 1 #intensity factor for created lics 
    lic[name].texture_size = 50  #detail of created LICs
    lic[name].lic_image_filter = 'Mild Sharpen' #image filter (mild sharpen causes higher contrast)
    return lic[name]

def create_plane(root, name:str, plane:str, value:float):
    '''
    creates a plane in either YZ, ZX or XY plane
    plane parameter dictate in which plane the surface will be created
    'plane' allowed values  - 'YZ', 'ZX', 'XY'
    returns the created surface object
    '''
    surfaces =  root.results.surfaces
    surfaces.plane_surface[name] = {}
    if plane == 'YZ':
        surfaces.plane_surface[name].x = value
    elif plane == 'ZX':
        surfaces.plane_surface[name].y = value
    elif plane == 'XY':
        surfaces.plane_surface[name].z = value
    else:
        return None
    return surfaces.plane_surface[name]

def create_iso_surface(root, name:str, field:str, value:float):
    '''
    creates Iso-surface based on field and its value
    Input:
    root - Fluent instance
    name - created iso-surface name [string]
    field - field from which to create the iso-surface [string]
    value - field value for iso-surface [float]
    Returns:
    Object of created iso-surface
    '''
    surfaces =  root.results.surfaces
    surfaces.iso_surface[name] = {}
    
    surfaces.iso_surface[name].field = field
    surfaces.iso_surface[name].iso_values = value

    return surfaces.iso_surface[name]

def create_histogram(root, name:str, field:str):
    plot = root.results.plot
    plot.histogram[name] = {}
    

def change_camera(root, view):
    '''
    Changes camera positions based on predefined camera views
    Input:
    root - Fluent instance
    view - Dictionary with predefined camera views [dict[list[float]]]
    '''
    root.results.graphics.views.camera.up_vector(xyz =  [1,1,1]) #defines upward vector of camera
    root.results.graphics.views.camera.position(xyz =  view['position']) #defines camera position
    root.results.graphics.views.camera.target(xyz = view['target']) #defines position of target on which the camera points
    root.results.graphics.views.camera.up_vector(xyz =  view['up_vector'])
    root.results.graphics.views.camera.field(width = view['width'], height = view['height']) #defines camera field of view

def save_avz(root, filename, workDir):
    root.tui.display.save_picture(workDir+'/Results/pictures/'+filename)

def create_mesh(root, name:str, zones, colour:str):
    '''
    Creates visualisation of a mesh
    Input:
    root - Fluent instance
    name - Name of created mesh [string]
    zones - Areas which to visualise [list[string]]
    colour - colour of created surface [string]
    '''
    graphics = root.results.graphics
    
    graphics.mesh.create(name)
    
    graphics.mesh[name].surfaces_list = zones
    graphics.mesh[name].coloring.option = 'manual'
    graphics.mesh[name].coloring.manual.faces = colour
    
    graphics.mesh[name].display()
    
    return graphics.mesh[name]

def StartPostprocessing(solverPath ,
                        GeneralSett:GeneralSett , 
                        SolvSett:Boundary_conditions_sett, 
                        PostproSett:PostprocessSett,
                        MSH_Objects):

    '''
    Main function for postporcessing of fluent case

    '''

    
    root = pyfluent.launch_fluent(mode= pyfluent.FluentMode.SOLVER,
                                     product_version=GeneralSett.Version,
                                     precision = pyfluent.Precision.SINGLE,
                                     processor_count=int(GeneralSett.IntCoreCount),
                                     ui_mode= GeneralSett.GUI, 
                                     cleanup_on_exit= False, 
                                     py = GeneralSett.PyConsole, 
                                     case_data_file_name= solverPath,
                                     cwd= GeneralSett.workingDirectory,
                                     additional_arguments='-mpi=intel',
                                     gpu= False,
                                     )
    
    if GeneralSett.Data_Path != '':
       root.file.read_data(file_name = GeneralSett.Data_Path) 
    
    '''
    Create folders to which save all generated pictures and files
    '''
    work_Directory = GeneralSett.workingDirectory
    
    if not os.path.exists(work_Directory+'/Results'):
        os.makedirs(work_Directory+'/Results')
        # os.makedirs(work_Directory+'/pictures/slices/pressure_coefficient')
        # os.makedirs(work_Directory+'/pictures/slices/pressure_coefficient/XY')
        # os.makedirs(work_Directory+'/pictures/slices/pressure_coefficient/XZ')
        # os.makedirs(work_Directory+'/pictures/slices/pressure_coefficient/YZ')
        if PostproSett.Mean_Press_cuts:
            os.makedirs(work_Directory+'/Results/pictures/slices/static_pressure')
            os.makedirs(work_Directory+'/Results/pictures/slices/static_pressure/XY')
            os.makedirs(work_Directory+'/Results/pictures/slices/static_pressure/XZ')
            os.makedirs(work_Directory+'/Results/pictures/slices/static_pressure/YZ')
        if PostproSett.Total_Press_cuts:
            os.makedirs(work_Directory+'/Results/pictures/slices/total_pressure')
            os.makedirs(work_Directory+'/Results/pictures/slices/total_pressure/XY')
            os.makedirs(work_Directory+'/Results/pictures/slices/total_pressure/XZ')
            os.makedirs(work_Directory+'/Results/pictures/slices/total_pressure/YZ')
        if PostproSett.Vel_Mag_cuts:    
            os.makedirs(work_Directory+'/Results/pictures/slices/velocity')
            os.makedirs(work_Directory+'/Results/pictures/slices/velocity/XY')
            os.makedirs(work_Directory+'/Results/pictures/slices/velocity/XZ')
            os.makedirs(work_Directory+'/Results/pictures/slices/velocity/YZ')
        if PostproSett.Vorticity_cuts:    
            os.makedirs(work_Directory+'/Results/pictures/slices/vorticity')
            os.makedirs(work_Directory+'/Results/pictures/slices/vorticity/XY')
            os.makedirs(work_Directory+'/Results/pictures/slices/vorticity/XZ')
            os.makedirs(work_Directory+'/Results/pictures/slices/vorticity/YZ')
        if PostproSett.Vel_LIC_cuts:
            os.makedirs(work_Directory+'/Results/pictures/slices/LICs')
            os.makedirs(work_Directory+'/Results/pictures/slices/LICs/XY')
            os.makedirs(work_Directory+'/Results/pictures/slices/LICs/XZ')
            os.makedirs(work_Directory+'/Results/pictures/slices/LICs/YZ')
    
    '''
    Find a list of all surfaces on a car
    '''    
    wall_list = list(root.setup.boundary_conditions.wall.keys())
    for wall in wall_list:
        if wall.find(r'tunnel-zmin') != -1:
            wall_list.remove(wall)
    
    
    if PostproSett.Excell and os.path.isfile(work_Directory+'\Rep-file.out'):
        '''
        Initiliasing excell sheet creation
        '''
        excell_workbook = openpyxl.Workbook()
        sheet = excell_workbook.active
        
        '''
        Extracting lift, drag and moment data from report definitions
        '''
        data  = pd.read_table(work_Directory+'\Rep-file.out', sep= ' ', header=2)
        Lift_data = data['Lift'].to_list()
        Drag_data = data['Drag'].to_list()
        Moment_data = data['f_axis_moment'].to_list()
        if 'Radiator' in list(data.columns):
            MassFlowRate_data = data['Radiator'].to_list()
        
        '''
        Create excell sheet for values for whole car
        '''
        sheet['A1'] = 'Part'
        sheet['A2'] = 'Car'
        sheet['B2'] = 'Lift [N]'

        if len(Lift_data) > PostproSett.Iteration_averaging: #case when there is enough iteration
            Lift = float(np.average(data['Lift'].to_list()[- PostproSett.Iteration_averaging:-1]))*2 #average data over last 200 iterations
            sheet['C2'] = Lift
            sheet['B3'] = 'Drag [N]'
            Drag = float(np.average(data['Drag'].to_list()[- PostproSett.Iteration_averaging:-1]))*2
            sheet['C3'] = Drag
            l_f = abs(float(np.average((data['f_axis_moment'].to_list()[- PostproSett.Iteration_averaging:-1]))*2)/Lift) #calculate length of moment arm
            if 'Radiator' in list(data.columns):
                MassFlowRate = float(np.average(data['Radiator'].to_list()[- PostproSett.Iteration_averaging:-1]))
        else: #case for when there is not enough iterations
            Lift = float(np.average(data['Lift'].to_list()))*2
            sheet['C2'] = Lift
            sheet['B3'] = 'Drag [N]'
            Drag = float(np.average(data['Drag'].to_list()))*2
            sheet['C3'] = Drag
            l_f = abs(float(np.average((data['f_axis_moment'].to_list()))*2)/Lift)
            if 'Radiator' in list(data.columns):
                MassFlowRate = float(np.average(data['Radiator'].to_list()))
        sheet['B4'] = 'Cl/Cd [~]'
        sheet['C4'] = Lift/Drag #calculate lift/drag ratio  
        sheet['B5'] = 'Balance [%]'
        sheet['C5'] = l_f/(SolvSett.r_w_axis_x)*100   #calculate position of center of pressure
        if 'Radiator' in list(data.columns):
            sheet['A41'] = 'Radiator'
            sheet['B41'] = 'Mass flow rate [kg/s]'
            sheet['C41'] = MassFlowRate


        '''
        start loop for writing of data for all defined subassemblies
        '''
        i = 6
        for obj in MSH_Objects['vehicle']:
            
            sheet['A'+str(i)] = obj.Name
            if len(data['Lift-'+obj.Name].to_list()) >  PostproSett.Iteration_averaging:
                Curr_Lift = float(np.average(data['Lift-'+obj.Name].to_list()[- PostproSett.Iteration_averaging:-1]))*2
                sheet['C'+str(i)] = Curr_Lift
                sheet['B'+str(i)] = 'Lift [N]'
                Curr_Drag = float(np.average(data['Drag-'+obj.Name].to_list()[- PostproSett.Iteration_averaging:-1]))*2
                sheet['C'+str(i+1)] = Curr_Drag
                sheet['B'+str(i+1)] = 'Drag [N]'
            else:
                Curr_Lift = float(np.average(data['Lift-'+obj.Name].to_list()))*2
                sheet['C'+str(i)] = Curr_Lift
                sheet['B'+str(i)] = 'Lift [N]'
                Curr_Drag = float(np.average(data[1]['Drag-'+obj.Name].to_list()))*2
                sheet['C'+str(i+1)] = Curr_Drag
                sheet['B'+str(i+1)] = 'Drag [N]'
            #sheet['D'+str(i)] = Curr_Lift/Curr_Drag
            i = i+2
        
        excell_workbook.save(filename=work_Directory+"/Results/Results_excel.xlsx") #saves the created excell file into work directory
        

    graphics = root.results.graphics
    surfaces =  root.results.surfaces
    picture = graphics.picture
    
    root.tui.views.camera.projection('orthographic') #change the view to orthographic projection
    root.tui.preferences.appearance.graphics_view('"Orthographic"')
    
    # use_window_resolution option not active inside containers or Ansys Lab environment
    if picture.use_window_resolution.is_active():
        picture.use_window_resolution = False
    picture.x_resolution = 3840
    picture.y_resolution = 2160
    
    #turns on/off lights
    graphics.lighting.lights_on = True

    #removes grid lines, reflections and shadows    
    root.tui.preferences.graphics.graphics_effects.grid_plane_enabled('no')
    root.tui.preferences.graphics.graphics_effects.reflections_enabled('no')
    root.tui.preferences.graphics.graphics_effects.simple_shadows_enabled('no')
    
    #defines a plane for mirroring of pictures
    root.tui.views.mirror_zones('tunnel-ymin')
    
    if PostproSett.Create_report_file:
        '''
        Creating a report file
        '''

        root.results.report.simulation_reports.generate_simulation_report(report_name="Simulation Report")
        #root.results.report.simulation_reports.add_histogram_to_report('y-plus', '#f', 0, 100, 50, 'no',wall_list)
        root.results.report.simulation_reports.export_simulation_report_as_pdf(report_name = "Simulation Report", file_name = work_Directory + '/Results/SimulationReport.pdf')

    if PostproSett.Save_AVZ:
        '''
        Create contours of mean pressure coefficient on car surface and saves as AVZ
        '''
        cp_1 =  create_contour(root, 'Cp_mean', 'mean-pressure-coefficient', wall_list, [-3.5, 1])
        cp_1.color_map.color = 'bgr' #change the colormap settings
        cp_1.display() #display the contour
        root.results.graphics.picture.driver_options.hardcopy_format = "avz" # has to be set after some mesh or contour is displayed in graphical window (can not save .avz of graph)
        save_avz(root, 'Cp_mean_AVZ', work_Directory) 

        '''
        Create contours of pressure coefficient on car surface and saves as AVZ
        '''
        cp_2 =  create_contour(root, 'Cp_cont', 'pressure-coefficient', wall_list, [-3.5, 1])
        cp_2.color_map.color = 'bgr' #change the colormap settings
        cp_2.display() #display the contour
        root.results.graphics.picture.driver_options.hardcopy_format = "avz" # has to be set after some mesh or contour is displayed in graphical window (can not save .avz of graph)
        save_avz(root, 'Cp_AVZ', work_Directory) 

        '''
        Create contours of RMSE static pressure on car surface and saves as AVZ
        '''
        rmse_sp =  create_contour(root, 'RMSE_stat_p', 'rmse-pressure', wall_list, [0, 70])
        rmse_sp.color_map.color = 'field-velocity' #change the colormap settings
        rmse_sp.display() #display the contour
        root.results.graphics.picture.driver_options.hardcopy_format = "avz" # has to be set after some mesh or contour is displayed in graphical window (can not save .avz of graph)
        save_avz(root, 'RMSE_Stat_Pressure_AVZ', work_Directory)

        '''
        Create contours of wall shear stress in x direction on car surfaces and saves as AVZ
        '''
        wall_shear_x =  create_contour(root, 'x-wall-shear-stress-mean','x-wall-shear',wall_list, [-1, 1])
        root.scheme_eval.scheme_eval('(cxsetvar '+'\''+'cmap-list (cons '+'\''+'("x-wall-shear-colormap" (4 (0 1 0 0) (0.5 1 0 0) (0.501 0 0 1)(1 0 0 1))) (cxgetvar '+'\'cmap-list)))') #custom colormap definition
        wall_shear_x.color_map.color = 'x-wall-shear-colormap'
        wall_shear_x.display()
        #save_avz(root, 'wall_shear_x_AVZ', work_Directory)  
        
        '''
        Create contours of wall shear stress in x direction on car surfaces and saves as AVZ
        ''' 
        root.results.graphics.pathline["oil_flow"]={}
        root.results.graphics.pathline["oil_flow"].options.oil_flow=True
        root.results.graphics.pathline["oil_flow"].step=80
        root.results.graphics.pathline["oil_flow"].skip=8
        root.results.graphics.pathline["oil_flow"].range.option = "clip-to-range"
        root.results.graphics.pathline["oil_flow"].range.clip_to_range.min_value = 0
        root.results.graphics.pathline["oil_flow"].range.clip_to_range.max_value = 0.1
        root.scheme_eval.scheme_eval('(cxsetvar '+'\''+'cmap-list (cons '+'\''+'("oilflow-colormap" (2 (0 0.565 0.565 0.565) (1 0.565 0.565 0.565))) (cxgetvar '+'\'cmap-list)))')
        root.results.graphics.pathline["oil_flow"].color_map.color = "oilflow-colormap"
        root.results.graphics.pathline["oil_flow"].release_from_surfaces = wall_list
        root.results.graphics.pathline["oil_flow"].onzone = wall_list
        print(wall_list)
        root.results.graphics.pathline.add_to_graphics(object_name="oil_flow")
        save_avz(root, 'wall_shear_x_AVZ', work_Directory) 

        '''
        Create contours of wall y plus on car surfaces and saves as AVZ
        '''
        wall_y_plus =  create_contour(root, 'wall_y_plus_mean', 'y-plus', wall_list, [0, 300])
        root.scheme_eval.scheme_eval('(cxsetvar '+'\''+'cmap-list (cons '+'\''+'("y-plus-colormap" (9 (0 0 0.666 0) (0.015 0 1 0) (0.01501 1 0.666 0) (0.0367 1 0 0) (0.1 1 0.666 0) (0.1001 0 0.666 1) (0.5 0 0 1) (0.99 0 0.666 1) (1 1 0 0))) (cxgetvar '+'\'cmap-list)))')
        wall_y_plus.color_map.color = 'y-plus-colormap'
        wall_y_plus.display()
        save_avz(root, 'wall_y_plus_AVZ', work_Directory)   

        '''
        Create an iso-surface of q-criterion and show a velocity contour on this iso-survace.
        '''
        root.tui.surface.iso_surface('q-criterion', 'q-crit-iso-surf', '()', '()', 10) #tui command for iso-surface cration
        vel_mag_on_q_crit = create_contour(root, 'vel-on-q-crit_cont', 'velocity-magnitude', 'q-crit-iso-surf', [0,35])
        vel_mag_on_q_crit.color_map.color = 'field-velocity'
        car_mesh = create_mesh(root, 'vehicle_mesh', wall_list, 'light gray')
        root.results.scene['q_crit_scene'] = {} #creating a new scene for combining a contour and car mesh
        root.results.scene['q_crit_scene'].graphics_objects['vel-on-q-crit_cont'] = {} #adding graphic objects to the scene
        root.results.scene['q_crit_scene'].graphics_objects['vehicle_mesh'] = {}
        root.results.scene['q_crit_scene'].display()
        save_avz(root, 'q_crit_AVZ', work_Directory) 

        '''
        Create an iso-surface of total pressure
        '''
        # root.tui.surface.iso_surface('total-pressure', 'p-tot-iso-surf', '()', '()', 0)
        # p_tot_mesh = create_mesh(root, 'p_tot_mesh','p-tot-iso-surf', 'yellow')
        # root.results.scene['p_tot_scene'] = {}
        # root.results.scene['p_tot_scene'].graphics_objects['p_tot_mesh'] = {}
        # root.results.scene['p_tot_scene'].graphics_objects['vehicle_mesh'] = {}
        # root.results.scene['p_tot_scene'].display()
        # save_avz(root, 'p_tot_AVZ', work_Directory)
        

    '''
    Create cut planes for contour display in all major planes
    '''
    xy_spacing = (PostproSett.End_coord_XY - PostproSett.Start_coord_XY)/(PostproSett.Number_of_cuts_XY-1)
    xz_spacing = (PostproSett.End_coord_XZ - PostproSett.Start_coord_XZ)/(PostproSett.Number_of_cuts_XZ-1)
    yz_spacing = (PostproSett.End_coord_YZ - PostproSett.Start_coord_YZ)/(PostproSett.Number_of_cuts_YZ-1)
                                            #plane creation method, start coordinate,     name of created places, number of surfaces, surface spacing
    surfaces.create_multiple_plane_surfaces(method = 'xy-plane', z =PostproSett.Start_coord_XY, name_format = 'XY{z:+.3f}',surfaces = PostproSett.Number_of_cuts_XY, spacing = xy_spacing)
    surfaces.create_multiple_plane_surfaces(method = 'zx-plane', y =PostproSett.Start_coord_XZ, name_format = 'ZX{y:+.3f}',surfaces = PostproSett.Number_of_cuts_XZ, spacing = xz_spacing)
    surfaces.create_multiple_plane_surfaces(method = 'yz-plane', x =PostproSett.Start_coord_YZ, name_format = 'ZY{x:+.3f}',surfaces = PostproSett.Number_of_cuts_YZ, spacing = yz_spacing)
    
    graphics.lighting.lights_on = False #turns off the lighting
    
    root.results.graphics.picture.driver_options.hardcopy_format = "png" #changes the file format to .png

    #disable ruler
    root.tui.preferences.appearance.ruler('yes')
    root.tui.preferences.appearance.ruler('no')

    '''
    A loop for creating and saving contours in all XY planes
    '''
    change_camera(root, top_view)
    for pic in range(PostproSett.Number_of_cuts_XY):    #24 #number of surfaces to be looped
        pict_number = (PostproSett.Start_coord_XY+pic*xy_spacing) #starting coordinate plus number of looped plane times plane spacing
        if pict_number < 0: #formating of picture number based on wheter its negative or positive
            pict_number = '{:1.3f}'.format(pict_number)
        else:
            pict_number = '+{:1.3f}'.format(pict_number)
        pict_number.replace('.',  ',')
        file_number = '{:02d}'.format(pic)

        #create pressure coefficient contour
        # coef_press = create_contour(root, 'cp-xy-'+pict_number, 'pressure-coefficient', 'xy'+pict_number,  [-3.5, 1])
        # coef_press.color_map.color = 'bgr'
        # coef_press.color_map.position = 0
        # coef_press.display()
        # graphics.picture.save_picture(file_name = work_Directory+'/Results/pictures/slices/pressure_coefficient/XY/press-coeff-'+'xy'+file_number+'.png')
        #create mean static pressure coefficient contour
        if PostproSett.Mean_Press_cuts:
            stat_press = create_contour(root, 'stat-p-xy-'+pict_number, 'mean-pressure', 'xy'+pict_number,  [-400, 140])
            stat_press.color_map.color = 'bgr'
            stat_press.color_map.position = 0
            stat_press.display()
            graphics.picture.save_picture(file_name = work_Directory+'/Results/pictures/slices/static_pressure/XY/stat-press-'+'xy'+file_number+'.png')
        #create total pressure contour
        if PostproSett.Total_Press_cuts:
            tot_press = create_contour(root, 'tot-press-xy-'+pict_number, 'total-pressure', 'xy'+ pict_number,  [-200, 200])
            tot_press.color_map.color = 'field-velocity'
            tot_press.color_map.position = 0
            tot_press.display()
            graphics.picture.save_picture(file_name = work_Directory+'/Results/pictures/slices/total_pressure/XY/tot-press-'+file_number+'.png')
    
        #create mean velocity contour
        if PostproSett.Vel_Mag_cuts:
            velocity = create_contour(root, 'velocity-xy-'+pict_number, 'mean-velocity-magnitude', 'xy'+pict_number, [0,35])
            velocity.color_map.color = 'field-velocity'
            velocity.color_map.position = 0
            velocity.display()
            graphics.picture.save_picture(file_name = work_Directory+'/Results/pictures/slices/velocity/XY/velocity-'+file_number+'.png')
        #create vorticity contour
        if PostproSett.Vorticity_cuts:
            vorticity = create_contour(root, 'vorticity-xy-'+pict_number, 'vorticity-mag', 'xy'+pict_number,  [0,200])
            vorticity.color_map.color = 'sequential-inferno'
            vorticity.color_map.position = 0
            vorticity.display()
            graphics.picture.save_picture(file_name = work_Directory+'/Results/pictures/slices/vorticity/XY/vorticity-'+'xy'+'%.3d'%pic+'.png')
        
        if PostproSett.Vel_LIC_cuts:
            lic = create_lic(root=root, name='LIC-xy-'+pict_number, field= 'mean-velocity-magnitude', vector_field= 'velocity', plane='xy'+pict_number,range= [0,35])
            lic.color_map.color = 'field-velocity'
            lic.color_map.position = 0
            lic.display()
            graphics.picture.save_picture(file_name = work_Directory+'/Results/pictures/slices/LICs/XY/LIC-'+file_number+'.png')

        
    '''
    A loop for creating and saving contours and LICs in XZ plane
    '''
    change_camera(root, side_view)
    for pic in range(PostproSett.Number_of_cuts_XZ):    #20
        pict_number = (PostproSett.Start_coord_XZ+pic*xz_spacing)
        if pict_number < 0:
            pict_number = '{:1.3f}'.format(pict_number)
        else:
            pict_number = '+{:1.3f}'.format(pict_number)
        pict_number.replace('.',  ',')
        file_number = '{:02d}'.format(pic)
        # coef_press = create_contour(root, 'cp-zx-'+pict_number, 'pressure-coefficient', 'zx'+pict_number,  [-3.5, 1])
        # coef_press.color_map.color = 'bgr'
        # coef_press.color_map.position = 0
        # coef_press.display()
        # graphics.picture.save_picture(file_name = work_Directory+'/Results/pictures/slices/pressure_coefficient/XZ/press-coeff-'+file_number+'.png')
        if PostproSett.Mean_Press_cuts:
            stat_press = create_contour(root, 'stat-p-zx-'+pict_number, 'mean-pressure', 'zx'+pict_number,  [-400, 140])
            stat_press.color_map.color = 'bgr'
            stat_press.color_map.position = 0
            stat_press.display()
            graphics.picture.save_picture(file_name = work_Directory+'/Results/pictures/slices/static_pressure/XZ/stat-press-'+'zx'+file_number+'.png')
        
        if PostproSett.Total_Press_cuts:
            tot_press = create_contour(root, 'tot-press-zx-'+pict_number, 'total-pressure', 'zx'+pict_number,  [-200, 200])
            tot_press.color_map.color = 'field-velocity'
            tot_press.color_map.position = 0
            tot_press.display()
            graphics.picture.save_picture(file_name = work_Directory+'/Results/pictures/slices/total_pressure/XZ/tot-press-'+file_number+'.png')
        
        if PostproSett.Vel_Mag_cuts:
            velocity = create_contour(root, 'velocity-zx-'+pict_number, 'mean-velocity-magnitude', 'zx'+pict_number, [0,35])
            velocity.color_map.color = 'field-velocity'
            velocity.color_map.position = 0
            velocity.display()
            graphics.picture.save_picture(file_name = work_Directory+'/Results/pictures/slices/velocity/XZ/velocity-'+file_number+'.png')
        
        if PostproSett.Vorticity_cuts:
            vorticity = create_contour(root, 'vorticity-zx-'+pict_number, 'vorticity-mag', 'zx'+pict_number, [0,200])
            vorticity.color_map.color = 'sequential-inferno'
            vorticity.color_map.position = 0
            vorticity.display()
            graphics.picture.save_picture(file_name = work_Directory+'/Results/pictures/slices/vorticity/XZ/vorticity-'+'zx'+'%.3d'%pic+'.png')
        
        if PostproSett.Vel_LIC_cuts:
            lic = create_lic(root=root, name='LIC-zx-'+pict_number, field= 'mean-velocity-magnitude', vector_field= 'velocity', plane='zx'+pict_number,range= [0,35])
            lic.color_map.color = 'field-velocity'
            lic.color_map.position = 0
            lic.display()
            graphics.picture.save_picture(file_name = work_Directory+'/Results/pictures/slices/LICs/XZ/LIC-'+file_number+'.png')

    '''
    A loop for creating and saving contours and LICs in ZY plane
    '''
    change_camera(root, front_view)
    for pic in range(PostproSett.Number_of_cuts_YZ):    #67
        pict_number = (PostproSett.Start_coord_YZ+pic*yz_spacing)
        if pict_number < 0:
            pict_number = '{:1.3f}'.format(pict_number)
        else:
            pict_number = '+{:1.3f}'.format(pict_number)
        pict_number.replace('.',  ',')
        file_number = '{:02d}'.format(pic)
        # coef_press = create_contour(root, 'cp-zy-'+pict_number, 'pressure-coefficient', 'zy'+pict_number, [-3.5, 1])
        # coef_press.color_map.color = 'bgr'
        # coef_press.color_map.position = 0
        # coef_press.display()
        # graphics.picture.save_picture(file_name = work_Directory+'/Results/pictures/slices/pressure_coefficient/YZ/press-coeff-'+file_number+'.png')
        
        if PostproSett.Mean_Press_cuts:
            stat_press = create_contour(root, 'stat-p-zy-'+pict_number, 'mean-pressure', 'zy'+pict_number,  [-400, 140])
            stat_press.color_map.color = 'bgr'
            stat_press.color_map.position = 0
            stat_press.display()
            graphics.picture.save_picture(file_name = work_Directory+'/Results/pictures/slices/static_pressure/YZ/stat-press-'+'yz'+file_number+'.png')
        
        if PostproSett.Total_Press_cuts:
            tot_press = create_contour(root, 'tot-press-zy-'+pict_number, 'total-pressure', 'zy'+pict_number, [-200, 200])
            tot_press.color_map.color = 'field-velocity'
            tot_press.color_map.position = 0
            tot_press.display()
            graphics.picture.save_picture(file_name = work_Directory+'/Results/pictures/slices/total_pressure/YZ/tot-press-'+'yz'+file_number+'.png')
       
        if PostproSett.Vel_Mag_cuts:
            velocity = create_contour(root, 'velocity-zy-'+pict_number, 'mean-velocity-magnitude', 'zy'+pict_number, [0,35])
            velocity.color_map.color = 'field-velocity'
            velocity.color_map.position = 0
            velocity.display()
            graphics.picture.save_picture(file_name = work_Directory+'/Results/pictures/slices/velocity/YZ/velocity-'+file_number+'.png')
        
        if PostproSett.Vorticity_cuts:
            vorticity = create_contour(root, 'vorticity-zy-'+pict_number, 'vorticity-mag', 'zy'+pict_number, [0,200])
            vorticity.color_map.color = 'sequential-inferno'
            vorticity.color_map.position = 0
            vorticity.display()
            graphics.picture.save_picture(file_name = work_Directory+'/Results/pictures/slices/vorticity/YZ/vorticity-'+file_number+'.png')
        
        if PostproSett.Vel_LIC_cuts:
            lic = create_lic(root=root, name='LIC-zy-'+pict_number, field= 'mean-velocity-magnitude', vector_field= 'velocity', plane='zy'+pict_number,range= [0,35])
            lic.color_map.color = 'field-velocity'
            lic.color_map.position = 0
            lic.display()
            graphics.picture.save_picture(file_name = work_Directory+'/Results/pictures/slices/LICs/YZ/LIC-'+file_number+'.png')
        
    
    root.tui.file.write_case_data(work_Directory+r'\Results.cas.h5')

#SolverSett = Solver.SolverSettings(16, 0.4, [0, 0.75, 0], [1.53, 0.75, 0], 250)       
#StartPostprocessing(1, r'D:\plesnik\PyFluent\Versions\Beta06_19_09_24\BetaTest2', SolverSett)
import ansys.fluent.core as pyfluent
import Support_scripts.MeshObjects as MeshObjects
import os
'''
Fault tolerant meshing workflow for car external aero simulations
This automatic workflow takes as inputs a objects of general settings, scope/prism settings, BOI settings 
and CAD file of a vehicle and automatically generates volume mesh suitable for simulation.
date: 29.07.2024
v:0.05
author:Jan Plesnik
contact: plesnik.honza@seznam.cz 
'''

from GUI_SubClasses.GUI_BoundaryConditions import Boundary_conditions_sett
from GUI_SubClasses.GUI_Tunnel import TunnelSett
from GUI_SubClasses.GUI_General import GeneralSett

def get_selection_id(Self, Obj_list, meshing):
    if Self.Name == 'vehicle':
        Sel_id = meshing.meshing_utilities.get_face_zones(filter ='*'+Self.Name+'*')
    else:
        Sel_id = meshing.meshing_utilities.get_face_zones(filter ='*'+Self.Parent+'-'+Self.Name+'*')
    print(Sel_id)
    included_obj_list = []
    for obj in Obj_list:
        if  (obj.Parent.find(Self.Parent) != -1 or obj.Parent == '') and obj.Parent.find(Self.Name) != -1 and obj.MSH_ID != Self.MSH_ID:
            included_obj_list.append(obj)
            curr_obj_id_list = meshing.meshing_utilities.get_face_zones(filter ='*'+obj.Parent+'-'+obj.Name+'*')
            if curr_obj_id_list != None:
                for curr_obj in curr_obj_id_list:
                    if Sel_id != None: 
                        if curr_obj in Sel_id:
                            Sel_id.remove(curr_obj)
    print(Sel_id)
    return Sel_id
            
'''
Start of function containing whole mshing workflow
Inputs into this function are:
MSH_Obj_List: list of all meshing objects that contains info about scopesizing, object type, prism settings etc.
work_Directory: string path to a working directory
General_Settings: an object containing info about general settings of fluent meshing and solver#
Tunnel_Settings: an object containing info about external aero tunnel
'''
def StartFluentMeshing(MSH_Obj_List,General_Settings:GeneralSett, Tunnel_Settings:TunnelSett, Boundary_settings:Boundary_conditions_sett):

    def _taskObjectResultPrint(b : bool, taskObjectName : str) -> None:
        """Helper function for obtaining information about whether the given task was completed (prints INFO to console) or not (raises Error).
        """

        if b:

            print("\nINFO, %s Task was successful!" % taskObjectName)

        else:
            
            return False



    '''
    Fluent launcher that creates a fluent instance, here we set number of cores, precision, CPU or GPU and other startup settings
    '''
    meshing = pyfluent.launch_fluent(mode= pyfluent.FluentMode.MESHING,
                                     product_version='25.1',
                                     precision = General_Settings.DoublePrecision,
                                     processor_count=int(General_Settings.IntCoreCount),
                                     ui_mode= General_Settings.GUI, 
                                     start_transcript=True,
                                     cleanup_on_exit= True, 
                                     py = General_Settings.PyConsole, 
                                     cwd= General_Settings.workingDirectory,
                                     additional_arguments='-mpi=intel',
                                     gpu= General_Settings.GPU,
                                     )


    '''
    Fluent core classes shosrtcuts
    '''
    workf = meshing.workflow
    mesh = meshing.meshing
    quer = meshing.meshing_utilities
    tui = meshing.tui
    
    tui.beta_feature_access('yes', 'ok')
    
    #tui.file.read_case(work_Directory+'/Po_autonodemove.msh.h5')

    #return meshing

    '''
    Import of cad file as CAD Assembly 
    '''
    tui.file.import_.cad_options.one_object_per('body')
    tui.file.import_.cad_options.create_cad_assemblies('yes')
    print(General_Settings.CAD_Path)
    #tui.file.import_.cad_options.tessellation('cad-faceting', 0.1, 10)
    tui.file.import_.cad_options.tessellation('cfd-surface-mesh', 'no', 1, 30, 25, 'yes', 1, 'no')
    tui.file.import_.cad('yes',General_Settings.CAD_Path , 'no', 'yes', 'mm', 'ok')

    '''
    GUI scheme commands to create mesh objects from cad assembly in order to have cad assembly tree path included in mesh objects names
    '''
    meshing.scheme_eval.scheme_eval('(cx-gui-do cx-set-list-tree-selections "NavigationPane*Frame2*Table1*List_Tree2" (list "Mesh Generation|Model|CAD Assemblies"))')
    meshing.scheme_eval.scheme_eval('(cx-gui-do cx-activate-item "MenuBar*TreeSubMenu*Selection Helper")')
    meshing.scheme_eval.scheme_eval('(cx-gui-do cx-set-list-selections "Selection Helper*Frame1*DropDownList2(Filter)" \'( 1))')
    meshing.scheme_eval.scheme_eval('(cx-gui-do cx-activate-item "Selection Helper*PanelButtons*PushButton3(Select)")')
    meshing.scheme_eval.scheme_eval('(cx-gui-do cx-activate-item "MenuBar*ObjectSubMenu*Create")')
    meshing.scheme_eval.scheme_eval('(cx-gui-do cx-set-toggle-button2 "Create Object*Frame1(Properties)*Table1*CheckButton4(One Object per CAD object selection)" #t)')
    meshing.scheme_eval.scheme_eval('(cx-gui-do cx-activate-item "Create Object*PanelButtons*PushButton3(Create)")')
    
    '''
    Writing mesh in order to be read into fault-tollerant workflow
    '''
    meshing.tui.file.write_mesh(General_Settings.workingDirectory+r'\AssemblyMesh.msh.gz')
    
    '''
    Fault-tolerant meshing workflow initialization
    '''
    b = workf.InitializeWorkflow(WorkflowType = r"Fault-tolerant Meshing")

    if b:
        print("\nINFO, Initialization of Fault-tolerant meshing workflow was successful!")

    else:

        raise Exception("\nERROR, Initialization of Fault-tolerant meshing workflow FAILED!")
   
   
    '''
    Import of previously created mesh object into workflow
    '''
    importGeoAndPartManagementObj = workf.TaskObject["Import CAD and Part Management"]
    importGeoAndPartManagementObj.Arguments = {

        "FMDFileName" : General_Settings.workingDirectory + r'\AssemblyMesh.msh.gz',   #path to geometry (cad or mesh) file 
        "LengthUnit" : "mm",    #length unit in which the geometry was created
        "CreateObjectPer" : "One per part",     # "One per part", "Custom"
        "Route" : 'MSH',    # "Native", "FM", "SCDM", "Workbench"
        "PartPerBody" : True,   #Create object per cad part (False), or per cad object(like bodies)(True)
        "RemoveEmptyParts" : True,  
        "FeatureAngle" : 40,    # [deg] Angle at which fluent will detect meshing and 
        "EdgeExtraction" : "auto", # "auto", "yes", "no"
        "OneZonePer" : "object", # "object", "body", "face"
        
        "FileLoaded": "yes",

    }
    b = importGeoAndPartManagementObj.Execute()
    if b:
        print("\nINFO, Initialization of Fault-tolerant meshing workflow was successful!")

    else:
        raise Exception("\nERROR, Import to Fault-tolerant meshing workflow FAILED!")

    os.remove(General_Settings.workingDirectory+r'\AssemblyMesh.msh.gz')
    
    '''
    Deleting prefix and suffix for cleaner object names
    '''
    
    Obj_list = quer.get_all_objects()
    for obj in Obj_list:
        if obj.find(':')==-1 or obj.find('.stp') != -1:
            meshing.tui.objects.delete(obj)
        else:
            meshing.tui.objects.rename_object(obj, obj[obj.find(':')+1::])
   
    '''
    Query for list of all object names
    '''
    Obj_list = quer.get_all_objects()
    print(Obj_list)


    '''
    Workflow task for geometry description
    '''
    describe_geom = workf.TaskObject["Describe Geometry and Flow"]
    describe_geom.Arguments.set_state(
        {
            "AddEnclosure": "Yes",  #specify adding of enclosure for extaernal aero (tunnel)
            "CloseCaps": "No",  #enclosing inlets and outlets for internal aero
            "DescribeGeometryAndFlowOptions": {
                "AdvancedOptions": True,
                "CloseLeakages": "No",  #task for leakage closing (mostly for internal aero, just have good cad model)
                r'EnablePrimeWrapper': r'Yes',
                "ExtractEdgeFeatures": "Yes",    #creating edge features from ceartain degree and object intersections
            },
            "FlowType": "External flow around object",
            r'LocalRefinementRegions': r'Yes',
        }
    )
    describe_geom.UpdateChildTasks(SetupTypeChanged=False)
    b=describe_geom.Execute()
    if b:
        print("\nINFO, Describe geometry was successful!")

    else:
        raise Exception("\nERROR, Describe geometry FAILED!")

    '''
    Creation of tunnel
    '''

    create_tunnel = workf.TaskObject['Create External Flow Boundaries']
    create_tunnel.Arguments.set_state(
        {
            r'BoundingBoxObject': 
            {
                r'SizeRelativeLength': 
                r'Directly specify coordinates',
                    r'Xmax': Tunnel_Settings.x_max,
                    r'Xmin': Tunnel_Settings.x_min,
                    r'Ymax': Tunnel_Settings.y_max,
                    r'Ymin': Tunnel_Settings.y_min,
                    r'Zmax': Tunnel_Settings.z_max,
                    r'Zmin': Tunnel_Settings.z_min,
                    
            },
            r'CreationMethod': r'Create new boundary',
            r'ExtractionMethod': r'wrap',   #method for geometry extraction (wrapping is reliable method)
        }
    )

    b = create_tunnel.Execute()
    if b:
        print("\nINFO, Tunnel creation was successful!")

    else:
        raise Exception("\nERROR, Tunnel creation FAILED!")
    

    for obj in MSH_Obj_List['BOI'][1::]:
        LocalRefinement = workf.TaskObject['Create Local Refinement Regions']
        LocalRefinement.Arguments.set_state(
            {
            r'BOIMaxSize': obj.Max_Size,
            r'BoundingBoxObject': 
                {r'Xmax': 1077.7900390625,r'Xmin': -2155.580078125,r'Ymax': 5969.453857421875,r'Ymin': 1680.1064453125,r'Zmax': 2779.164794921875,r'Zmin': 716.55419921875,},
            r'CreationMethod': r'Existing',
            r'ObjectSelectionList': [r'bois-'+obj.Name],
            r'ObjectSelectionSingle': [r'bois-'+obj.Name],
            r'SelectionType': r'object',
            }
            )
        b = LocalRefinement.AddChildAndUpdate(DeferUpdate=False)
        if b:
            print("\nINFO, Local refinement region added!")

        else:
            raise Exception("\nERROR, Local refinement region FAILED!")

    '''
    Edge extraction task
    '''
    extr_edges = workf.TaskObject['Extract Edge Features']
    extr_edges.Arguments.set_state(
        {
        r'ExtractMethodType': r'Intersection Loops',    #extraction method
        r'ObjectSelectionList': r'vehicle|tunnel',      #extraction sellection (alle objects with vehicle or tunnel in their name)
        r'SelectionType': r'object',
        }
    )
    extr_edges.AddChildAndUpdate(DeferUpdate=False)
    extr_edges.Arguments.set_state(
        {
        r'ObjectSelectionList': r'vehicle|tunnel',
        }
    )
    b = extr_edges.AddChildAndUpdate(DeferUpdate=False)
    if b:
        print("\nINFO, Edge extraction was successful!")

    else:
        raise Exception("\nERROR, Edge extraction FAILED!")

    '''
    Fluid object identification
    a.k.a creation of material point
    '''
    identify_region = workf.TaskObject['Identify Regions']
    identify_region.Arguments.set_state(
        {
        r'AddChild': r'yes',
        r'GraphicalSelection': False,
        r'MaterialPointsName': r'fluid-region-1',    #material point name (will also be a created fluid region name)
        r'MptMethodType': r'Numerical Inputs',
        r'NewRegionType': r'fluid',  #type of region
        r'ShowCoordinates': True,  r'X': -2500,r'Y': 2000,r'Z': 1000,   #coordinates of material point inside fluid domain
        }
    )
    b = identify_region.AddChildAndUpdate(DeferUpdate=False)
    if b:
        print("\nINFO, Region identification was successful!")

    else:
        raise Exception("\nERROR, Region identification FAILED!")

    if Boundary_settings.Radiator_check == True:
        '''
        Identification of radiator fluid region
        '''

        identify_region = workf.TaskObject['Identify Regions']
        identify_region.Arguments.set_state(
            {
            r'AddChild': r'yes',
            r'GraphicalSelection': False,
            r'MaterialPointsName': r'radiator-1',    #material point name (will also be a created fluid region name)
            r'MptMethodType': r'Centroid of Objects',
            r'NewRegionType': r'fluid',  #type of region
            r'ObjectSelectionList': r'*radiator*',  
            }
        )
        b = identify_region.AddChildAndUpdate(DeferUpdate=False)
        if b:
            print("\nINFO, Region identification was successful!")

        else:
            raise Exception("\nERROR, Region identification FAILED!")
    '''
    Region selection Settings
    Choosing of extraction method of region and its cell type
    '''
    update_regions = workf.TaskObject['Update Region Settings']
    update_regions.Arguments.set_state(
        {
            r'FilterCategory': r'Identified Regions',   #filter for only created region from material points
            r'MainFluidRegion': r'fluid-region-1',   #name of fluid region
            r'OldRegionLeakageSizeList': [r''],
            r'OldRegionMeshMethodList': [r'wrap'],
            r'OldRegionNameList': [r'fluid-region-1'],
            r'OldRegionOversetComponenList': [r'no'],
            r'OldRegionTypeList': [r'fluid'],
            r'OldRegionVolumeFillList': [r'hexcore'],
            r'RegionLeakageSizeList': [r''],    #no leakage defined
            r'RegionMeshMethodList': [r'wrap'], #geometry extraction nmethod for region
            r'RegionNameList': [r'fluid-region-1'],  #fluid region name again
            r'RegionOversetComponenList': [r'no'],  #no overset mesh defined
            r'RegionTypeList': [r'fluid'],  #region type ('fluid', 'solid, 'dead')
            r'RegionVolumeFillList': [r'poly-hexcore'], #Type of cells in region ('poly', 'tet', 'hexcore', 'poly-hexcore')
        }
    )
    b = update_regions.Execute()
    if b:
        print("\nINFO, Region update was successful!")

    else:
        raise Exception("\nERROR, Region update FAILED!")

    '''
    Mesh controlls
    mainly for Wrap target size
    '''
    mesh_contr_opt = workf.TaskObject['Choose Mesh Control Options']
    mesh_contr_opt.Arguments.set_state(
        {
        r'CreationMethod': r'Custom',
        r'MeshControlOptions': {r'WrapTargetSizeFieldRatio': Tunnel_Settings.Wrap_ratio,},
        }
    )
    mesh_contr_opt.UpdateChildTasks(SetupTypeChanged=False)
    mesh_contr_opt.Arguments.set_state(
        {r'CreationMethod': r'Custom',
        r'MeshControlOptions': 
            {
            r'AdvancedOptions': True,
            r'WrapTargetBothOptions': r'Both Wrap And Target',
            r'WrapTargetSizeFieldRatio': Tunnel_Settings.Wrap_ratio,
            },
        }
    )
    b =  mesh_contr_opt.Execute()
    if b:
        print("\nINFO, Mesh Control update successful!")

    else:
        raise Exception("\nERROR, Mesh Control update FAILED!")

    '''
    Creation of Default Local Sizings
    '''
    '''
    Tunnel local sizing
    '''
    scope_size_tunnel_max = workf.TaskObject['Add Local Sizing']
    scope_size_tunnel_max.Arguments.set_state(
        {
            r'LocalSettingsName': r'tunnel-max',#region name
            r'LocalSizeControlParameters': 
                {r'CellsPerGap': 3, #proximity settings (0 if ignored)
                r'CurvatureNormalAngle': 18,    #curvature settings (0 if ignored)
                r'GrowthRate': 1.2, #cell geometric growth rate
                r'IgnoreSelf': True,    #option to ignore self in this sizing
                r'MaxSize': Tunnel_Settings.Cell_size,   #maximum cell size
                r'MinSize': Tunnel_Settings.Cell_size,  #minimum cell size (unless overriden)
                r'ScopeProximityTo': r'faces-and-edges',    #geometry type to which local sizing will be applied ('faces', 'edges', 'faces-and-edges')
                r'SizingType': r'soft',     #type of local sizing
                r'WrapCellsPerGap': 3,
                r'WrapCurvatureNormalAngle': 18,
                r'WrapGrowthRate': 1.2,
                r'WrapMax': 250,
                r'WrapMin': 375,
                },
            r'ObjectSelectionList': [r'tunnel'],
            r'SelectionType': r'object',
            r'ValueChanged': r'DefaultButChanged',
        }
    )
    b = scope_size_tunnel_max.AddChildAndUpdate(DeferUpdate=False)
    if b:
        print("\nINFO, Add Local Sizing successful!")

    else:
        raise Exception("\nERROR, Add Local Sizing FAILED!")

    '''
    Default curvature local sizing
    '''
    scope_size_def_curv = workf.TaskObject['Add Local Sizing']
    scope_size_def_curv.Arguments.set_state(
        {
            r'LocalSettingsName': r'default-curvature',
            r'LocalSizeControlParameters': 
                {
                r'CellsPerGap': 3 ,
                r'CurvatureNormalAngle': 30,
                r'GrowthRate': 1.2,
                r'IgnoreSelf': True,
                r'MaxSize': 200,
                r'MinSize': 20,
                r'ScopeProximityTo': r'faces-and-edges',
                r'SizingType': r'curvature',
                r'WrapCellsPerGap': 3,
                r'WrapCurvatureNormalAngle': 30,
                r'WrapGrowthRate': 1.2,
                r'WrapMax': 150,
                r'WrapMin': 15,
                },
            r'ObjectSelectionList': r'vehicle*',
            r'SelectionType': r'object',
            r'ValueChanged': r'DefaultButChanged',
        }
    )
    b = scope_size_def_curv.AddChildAndUpdate(DeferUpdate=False)
    if b:
        print("\nINFO, Add Local Sizing successful!")

    else:
        raise Exception("\nERROR, Add Local Sizing FAILED!")
    
    '''
    Default proximity local sizing
    '''
    '''
    scope_size_def_prox = workf.TaskObject['Add Local Sizing']
    scope_size_def_prox.Arguments.set_state(
        {
            r'LocalSettingsName': r'default-proximity',
            r'LocalSizeControlParameters': 
                {
                r'CellsPerGap': 1,
                r'CurvatureNormalAngle': 18,
                r'GrowthRate': 1.2,
                r'IgnoreSelf': True,
                r'MaxSize': 200,
                r'MinSize': 20,
                r'ScopeProximityTo': r'edges',
                r'SizingType': r'proximity',
                r'WrapCellsPerGap': 1,
                r'WrapCurvatureNormalAngle': 18,
                r'WrapGrowthRate': 1.2,
                r'WrapMax': 150,
                r'WrapMin': 15,
                },
            r'ObjectSelectionList': r'vehicle*',
            r'SelectionType': r'object',
            r'ValueChanged': r'DefaultButChanged',
        }
    )
    scope_size_def_prox.AddChildAndUpdate(DeferUpdate=False)
    '''
    
    '''
    Task loop for automatical creation of local scoped sizing 
    based on provided custm Size Field list file.
    '''
    Obj_list = quer.get_all_objects()  #querry list of all active  object names 
    print(Obj_list)

    #MSH_Obj_List = MeshObjects.ReadObjectList(Size_field_text_file)
    print(MSH_Obj_List)
    for obj in MSH_Obj_List['vehicle']:    #start of local sizing creation loop
        scope_size = workf.TaskObject['Add Local Sizing']
        print('Init. local sizing')
        if float(obj.Curvature) !=0:   #case for if Scoped sizing applies for curvature
            scope_size.Arguments.set_state(
                {
                r'CompleteObjectSelectionList': obj._findParts(MSH_Obj_List['vehicle'] ,Obj_list),     #list of all parts for which current size settings apply
                r'LocalSettingsName': obj.Name + '-curv',
                r'LocalSizeControlParameters': 
                    {
                    r'AdvancedOptions': True,
                    r'CellsPerGap': 1,
                    r'CurvatureNormalAngle': int(obj.Curvature),
                    r'GrowthRate': float(obj.Growth_Rate),
                    r'IgnoreSelf': obj.Ignore_self,
                    r'InitialSizeControl': False,
                    r'MaxSize': float(obj.Max_Size),
                    r'MinSize': float(obj.Min_Size),
                    r'ScopeProximityTo': obj.Scope_To_Curv,
                    r'SizingType': 'curvature',
                    r'TargetSizeControl': False,
                    r'WrapCellsPerGap': 1,
                    r'WrapCurvatureNormalAngle':int(obj.Curvature),
                    r'WrapGrowthRate': float(obj.Growth_Rate),
                    r'WrapMax': float(float(obj.Max_Size)*4/5),
                    r'WrapMin': float(float(obj.Min_Size)*4/5),
                    },
                r'ObjectSelectionList': obj._findParts(MSH_Obj_List['vehicle'] ,Obj_list),
                r'SelectionType': r'object',
                r'ValueChanged': r'NotDefault',
                }
            )
            print('Arguments set')
            b= scope_size.AddChildAndUpdate(DeferUpdate=False)
            if b:
                print("\nINFO, Add Local Sizing successful!")

            else:
                raise Exception("\nERROR, Add Local Sizing FAILED!")
            print('Local  sizing updated')
        if float(obj.Cells_Per_Gap) > 0:  #case for if Scoped sizing applies for proximity
            scope_size.Arguments.set_state(
                {
                r'CompleteObjectSelectionList': obj._findParts(MSH_Obj_List['vehicle'] ,Obj_list),
                r'LocalSettingsName': obj.Name + '-prox',
                r'LocalSizeControlParameters': 
                    {
                    r'AdvancedOptions': True,
                    r'CellsPerGap': int(obj.Cells_Per_Gap),
                    r'CurvatureNormalAngle': 30,
                    r'GrowthRate': float(obj.Growth_Rate),
                    r'IgnoreSelf': obj.Ignore_self,
                    r'InitialSizeControl': False,
                    r'MaxSize': float(obj.Max_Size),
                    r'MinSize': float(obj.Min_Size),
                    r'ScopeProximityTo': obj.Scope_To_Prox,
                    r'SizingType': 'proximity',
                    r'TargetSizeControl': False,
                    r'WrapCellsPerGap': int(obj.Cells_Per_Gap),
                    r'WrapCurvatureNormalAngle':30,
                    r'WrapGrowthRate': float(obj.Growth_Rate),
                    r'WrapMax': float(float(obj.Max_Size)*4/5),
                    r'WrapMin': float(float(obj.Min_Size)*4/5),
                    },
                r'ObjectSelectionList': obj._findParts(MSH_Obj_List['vehicle'] ,Obj_list),
                r'SelectionType': r'object',
                r'ValueChanged': r'NotDefault',
                }
            )
            print('Arguments set')
            b = scope_size.AddChildAndUpdate(DeferUpdate=False)
            if b:
                print("\nINFO, Add Local Sizing successful!")

            else:
                raise Exception("\nERROR, Add Local Sizing FAILED!")
            print('Local  sizing updated')
            

    for obj in MSH_Obj_List['BOI'][1::]:    #start of local sizing creation loop
        scope_size = workf.TaskObject['Add Local Sizing']
        print('Init. local sizing')
        scope_size.Arguments.set_state(
                {
                r'LocalSettingsName': obj.Name,
                r'LocalSizeControlParameters': 
                    {
                    r'AdvancedOptions': False,
                    r'CellsPerGap': 3,
                    r'CurvatureNormalAngle': 18,
                    r'GrowthRate': float(obj.Growth_Rate),
                    r'IgnoreSelf': True,
                    r'InitialSizeControl': False,
                    r'MaxSize': float(obj.Max_Size),
                    r'MinSize': float(obj.Max_Size),
                    r'ScopeProximityTo': r'faces',
                    r'SizingType': r'boi',
                    r'TargetSizeControl': False,
                    r'WrapCellsPerGap': 3,
                    r'WrapCurvatureNormalAngle': 18,
                    r'WrapGrowthRate': float(obj.Growth_Rate),
                    r'WrapMax': float(obj.Max_Size),
                    r'WrapMin': float(obj.Max_Size),
                    },
                r'SelectionType': r'zone',
                r'ValueChanged': r'NotDefault',
                r'ZoneSelectionList': r'*'+obj.Name+r'*',
                }
            )
        print('Arguments set')
        b = scope_size.AddChildAndUpdate(DeferUpdate=False)
        if b:
            print("\nINFO, Add Local Sizing successful!")

        else:
            raise Exception("\nERROR, Add Local Sizing FAILED!")
        print('Local  sizing updated')

    '''
    Creation of surface Mesh
    '''
    generate_surf_mesh = workf.TaskObject['Generate the Surface Mesh']
    generate_surf_mesh.Arguments.set_state({r'AdvancedOptions': True,r'SurfaceQuality': 0.7,})
    b = generate_surf_mesh.Execute()
    if b:
        print("\nINFO, Surface Mesh Creation successful!")

    else:
        raise Exception("\nERROR, Surface Mesh Creation FAILED!")

    '''
    Changing of boundary types for tunnel face zones
    '''
    update_boundary = workf.TaskObject['Update Boundaries']
    update_boundary.Arguments.set_state(
        {r'BoundaryZoneList': [r'tunnel-ymin', r'tunnel-xmax', r'tunnel-ymax', r'tunnel-xmin', r'tunnel-zmax'],
        r'BoundaryZoneTypeList': [r'symmetry', r'pressure-outlet', r'symmetry', r'velocity-inlet', r'symmetry'],
        r'OldBoundaryZoneList': [r'tunnel-ymin', r'tunnel-xmax', r'tunnel-ymax', r'tunnel-xmin', r'tunnel-zmax'],
        r'OldBoundaryZoneTypeList': [r'wall', r'wall', r'wall', r'wall', r'wall'],})
    b=update_boundary.Execute()
    if b:
        print("\nINFO, Update Boundaries successful!")

    else:
        raise Exception("\nERROR, Update Boundaries FAILED!")
    
    '''
    Querry for getting a list of all face zone names
    '''

    #face_zone_id_list = str(tuple(quer.get_face_zones_of_object(region_type = 'fluid', objects = quer.get_all_objects(), object_name = 'fluid-region-1'))).replace(",", "")
    print('Printing face zones!!!!! \n')
    print(quer.get_face_zones_of_object(object_name = 'fluid-region-1'))
    face_zone_id_list = str(tuple(quer.get_face_zones_of_object(object_name = 'fluid-region-1'))).replace(",", "")
    Zone_name_list = meshing.scheme_eval.scheme_eval("(tgapi-util-convert-zone-ids-to-name-strings '%s)" % face_zone_id_list)
   
    '''
    Dictionary of mesh zones belonging to their prism settings
    '''
    Prism_dict = MeshObjects.MakeBoundaryLayerDict2(MSH_Obj_List['vehicle'], Obj_list, Zone_name_list)
    '''
    Loop for setting prisms
    '''

    for MSH_obj in MSH_Obj_List['vehicle']:
        
        #print(vars(MSH_obj))
        print(MeshObjects.MakePrismWildcard(MSH_obj, MSH_Obj_List['vehicle']))
        if MSH_obj.Boundary_Type == 'uniform' and get_selection_id(MSH_obj,MSH_Obj_List['vehicle'], meshing) != []: #setting of uniform prisms type
            add_prisms = workf.TaskObject['Add Boundary Layers']
            add_prisms.Arguments.set_state(
                {
                    r'AddChild': r'yes',
                    r'BLControlName': MSH_obj.Name, #name of the prism controll
                    r'BLRegionList': [r'radiator-1', r'fluid-region-1'], #fluid region name where prism layer will be created,
                    r'FaceScope': 
                        {
                        r'GrowOn': r'selected-zones',
                        r'RegionsType': r'named-fluid-regions',
                        },
                    r'FirstHeight': float(MSH_obj.First_Aspect_Ratio),   #first prism layer height
                    r'LocalPrismPreferences': {r'Continuous': r'Stair Step',},  #prism creation method
                    r'NumberOfLayers': int(float(MSH_obj.Number_Of_Layers)),   #total number of prism layers
                    r'OffsetMethodType': r'uniform',     #prism growth method
                    r'Rate': float(MSH_obj.Pism_Growth_Rate),   #prism geometric growtH rate
                    r'RegionScope': [r'fluid-region-1'],
                    r'ZoneSelectionList': MeshObjects.MakePrismWildcard(MSH_obj, MSH_Obj_List['vehicle']), #list of all face zone names to which the prism settins will be aplied
                    }
                )
            b = add_prisms.AddChildAndUpdate(DeferUpdate=False)
            if b:
                print("\nINFO, Prism Creation successful!")

            else:
                raise Exception("\nERROR, Prism Creation FAILED!")
            

        elif MSH_obj.Boundary_Type == 'aspect-ratio' and get_selection_id(MSH_obj,MSH_Obj_List['vehicle'], meshing) != []:
            add_prisms.Arguments.set_state(
                {
                r'AddChild': r'yes',
                r'BLControlName': MSH_obj.Name,
                r'BLRegionList': [r'radiator-1', r'fluid-region-1'],
                r'FaceScope': 
                    {
                    r'GrowOn': r'selected-zones',
                    r'RegionsType': r'named-fluid-regions',
                    },
                r'FirstAspectRatio': float(MSH_obj.First_Aspect_Ratio),
                r'FirstHeight': r'5',
                r'LocalPrismPreferences': {r'Continuous': r'Stair Step',},
                r'NumberOfLayers': int(float(MSH_obj.Number_Of_Layers)),
                r'OffsetMethodType': MSH_obj.Boundary_Type,
                r'Rate': float(MSH_obj.Pism_Growth_Rate),
                r'RegionScope': [r'fluid-region-1'],
                r'ZoneSelectionList':MeshObjects.MakePrismWildcard(MSH_obj, MSH_Obj_List['vehicle']),
                }
            )
            b = add_prisms.AddChildAndUpdate(DeferUpdate=False)
            if b:
                print("\nINFO, Prism Creation successful!")

            else:
                raise Exception("\nERROR, Prism Creation FAILED!")
        
        

    
    '''
    Prism layer settings for undeclared face zones
    '''
    
    add_rest_prisms = workf.TaskObject['Add Boundary Layers']
    add_rest_prisms.Arguments.set_state(
            {
            r'AddChild': r'yes',
            r'BLControlName': r'rest',
            r'FaceScope': 
                {
                r'FaceScopeMeshObject': r'',
                r'GrowOn': r'selected-zones',
                r'RegionsType': r'fluid-regions',
                },
            r'FirstAspectRatio': 10,
            r'FirstHeight': 0.2,
            r'InvalidAdded': r'no',
            r'LocalPrismPreferences': 
                {
                r'AdditionalIgnoredLayers': 0,  
                r'AllowedTangencyAtInvalidNormals': 0.98,
                r'Continuous': r'Stair Step',
                r'IgnoreBoundaryLayers': r'yes',
                r'ModifyAtInvalidNormals': r'no',
                r'NumberOfSplitLayers': 3,
                r'RemeshAtInvalidNormals': r'no',
                r'ShowLocalPrismPreferences': False,
                r'SphereRadiusFactorAtInvalidNormals': 0.8,
                r'SplitPrism': r'No',
                },
            r'MaxLayerHeight': 0,
            r'NumberOfLayers': 4,
            r'OffsetMethodType': r'aspect-ratio',
            r'Rate': 1.25,
            r'ReadPrismControlFile': r'',
            r'TransitionRatio': 0.272,
            r'ZoneSelectionList': r'tunnel-zmin',
            }
        )
    b=add_rest_prisms.AddChildAndUpdate(DeferUpdate=False)
    
    if b:
        print("\nINFO, Prism Creation successful!")

    else:
        raise Exception("\nERROR, Prism Creation FAILED!")

    
    '''
    Generate Volume Mesh
    '''
    generate_vol_mesh=workf.TaskObject['Generate the Volume Mesh']
    generate_vol_mesh.Arguments.set_state(
        {
            r'OrthogonalQuality': 0.1,
            "EnableParallel": True,
        })
    b = generate_vol_mesh.Execute()
    if b:
        print("\nINFO, Volume Mesh Creation successful!")

    else:
        raise Exception("\nERROR, Volume Mesh Creation FAILED!")

    meshing.tui.mesh.modify.auto_node_move('*', '()', '*', '()', 0.1, 50, 100, 'yes', 10)
    meshing.tui.mesh.modify.auto_node_move('*', '()', '*', '()', 0.05, 50, 50, 'yes', 15)
    meshing.tui.mesh.modify.auto_node_move('*', '()', '*', '()', 0.13, 50, 100, 'no', 3)
    meshing.tui.mesh.modify.auto_node_move('*', '()', '*', '()', 0.07, 50, 70, 'no', 10)
    meshing.tui.mesh.modify.auto_node_move('*', '()', '*', '()', 0.1, 50, 100, 'no', 10)
    
    meshing.tui.file.write_mesh(General_Settings.workingDirectory+r'\Po_autonodemove.msh.h5')        
    
    
    return str(General_Settings.workingDirectory+r'\Po_autonodemove.msh.h5')










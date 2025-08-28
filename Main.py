
import threading
import time
import copy
import sys
import json
import os
import customtkinter as ctk
from PIL import Image
from tkinter import ttk
from tkinter import filedialog
from typing import  Tuple

import Support_scripts.MeshObjects as MeshObjects
import Fluent_scripts.Solver as Solver
import Fluent_scripts.Postproces as Postproces
import Fluent_scripts.Mesher as Mesher


'''
A code for custom app used to set a fluent simulation settings without the need
for user to know in depth fluent settings and with a basic understanding of CFD
start automatically producing high quality external aero simulations.
This code uses mainly Custom TKinter library for GUI creation trough which the user 
can change the simulation settings and start simulation in other custom libraries.
date: 14.01.2024
v:0.11
version update: Added queue and in app console log
author:Jan Plesnik
contact: plesnik.honza@seznam.cz 
'''
from GUI_SubClasses.GUI_General import General, GeneralSett
       
from GUI_SubClasses.GUI_SopeSizing import ScopeSizing

from GUI_SubClasses.GUI_Tunnel import Tunnel, TunnelSett

from GUI_SubClasses.GUI_Simulation import Simulation, SimulationSett

from GUI_SubClasses.GUI_BoundaryConditions import BoundaryConditions, Boundary_conditions_sett

from GUI_SubClasses.GUI_Postprocess import Postprocessing, PostprocessSett

from GUI_SubClasses.GUI_Prisms import Prisms

from GUI_SubClasses.GUI_Parametrization import Parameters, ParametrizationSett
        
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")    



Debug_Console = False        

class SimulationClass:
    '''
    Class containing all of simulation settings and responsible for starting individual simulation 
    steps as individual threads.
    '''
    
    _registry = []
    states = {
      
        'wait': 'Waiting', 
        'msh':  'Meshing',
        'msh_dn': 'Meshing done!',
        'slv': 'Solving',  
        'slv_dn': 'Solved', 
        'post': 'Postprocessing', 
        'dn' : 'Done!', 
        'err': 'Error!!!'
        
    }
    '''
    Shotcuts fow various possible simulation states.
    '''
    def __init__(self, simGeneralObject, simMeshObjectList,simTunnelObject,simSolverSett, simBoundarySett, simPostproSett, simParametersSett, simName, simStat = 'wait'):
        '''
        Constructs a simulation class with simulation settings as its atributes.
        '''
        self.simGeneralObject = simGeneralObject
        self.simMeshObjectList = simMeshObjectList
        self.simTunnelObject = simTunnelObject
        self.simSolverSett = simSolverSett    
        self.simBoundarySett = simBoundarySett
        self.simPostproSett = simPostproSett
        self.simParametersSett = simParametersSett
        self.simName = simName
    
        
        self.SimID = self.findSimID()
        self._registry.append(self)
        self.SimStat = simStat
        self.meshPath = None
        self.SimThread = None
        self.solverPath = ''#"D:\plesnik\PyFluent\Versions\Beta18v1_14_01_25\TestSim1\Results.cas.h5"

    def findSimID(self):
        '''
        This function will automatically find a closest aviable ID number for simulation.
        
        :returns: (Int) ID number of simulation
        '''
        simID = 0
        if self._registry == []:
            return 1
        for sim in self._registry:
            if sim.SimID >= simID:
                simID = sim.SimID
                
        return simID+1
    
    def startMeshing(self):
        '''
        Changes the simulation status to 'Meshing' and pushes the simulation settings to 
        Mesher.StartFluentMeshing function which takes care of entire meshing workflow.
        
        After meshing changes the simulation status to 'Meshing Done'.
        
        :returns: (String) path to saved volumetric mesh
        '''
        self.SimStat = 'msh'
        MeshingPath = Mesher.StartFluentMeshing(self.simMeshObjectList,
                                  General_Settings= self.simGeneralObject,
                                  Tunnel_Settings = self.simTunnelObject,
                                  Boundary_settings= self.simBoundarySett,
                                  Parameters_settings= self.simParametersSett                               
                                  )
        
        self.meshPath = MeshingPath
        self.SimStat = 'msh_dn'
        self.SimThread = None
        return str(MeshingPath)
    
    def startMeshingThread(self):
        '''
        Starts SimulationClass.startMeshing() method in new thread.
        
        :returns: (Thread)
        '''
        tMesh = threading.Thread(target=self.startMeshing, args=())
        tMesh.start()
        return tMesh

    def startSolver(self):
        '''
        Changes the simulation status to 'Solving' and pushes the simulation settings to 
        Solver.StartFluentSolver function which takes care of entire solver workflow.
        
        After solving changes the simulation status to 'Solver Done'.
        
        :returns: (String) path to saved case file
        '''
        self.SimStat = 'slv'
        SolverPath = Solver.StartFluentSolver(self.simBoundarySett, 
                                               self.simSolverSett, 
                                               self.simMeshObjectList, 
                                               self.simGeneralObject,
                                               self.simPostproSett,
                                               self.meshPath)
        self.solverPath = SolverPath
        self.SimStat = 'slv_dn'
        self.SimThread = None
        return str(SolverPath)
        
    
    def startSolverThread(self):
        '''
        Starts SimulationClass.startSolver() method in new thread.
        
        :returns: (Thread)
        '''
        tSolv = threading.Thread(target=self.startSolver, args=())
        tSolv.start()
        return tSolv

    def startPostpro(self):
        '''
        Changes the simulation status to 'Postprocessing' and pushes the simulation settings to 
        Postproces.StartPostprocessing() function which takes care of entire postprocessing workflow.
        
        After postprocessing changes the simulation status to 'Done'.
        
        :returns: True
        '''
        self.SimStat = 'post'
        if self.solverPath == '':
            self.solverPath = self.simGeneralObject.CAD_Path
        Postproces.StartPostprocessing(self.solverPath,
                                       GeneralSett= self.simGeneralObject,
                                       SolvSett= self.simBoundarySett, 
                                       PostproSett= self.simPostproSett,
                                       MSH_Objects= self.simMeshObjectList)
        self.SimStat = 'dn'
        self.SimThread = None
        return True
    
    def startPostproThread(self):
        '''
        Starts SimulationClass.startPostpro() method in new thread.
        
        :returns: (Thread)
        '''
        tPost = threading.Thread(target=self.startPostpro, args=())
        tPost.start()
        return tPost

   
class MainMenuButtons(ctk.CTkScrollableFrame):
    '''
    class that initialises the main menu buttons which redirect the user to given 
    subcategories.
    '''
    def __init__(self, master):
        super().__init__(master ,width= 720, height=60, orientation='horizontal')
        self.button = ctk.CTkButton(self, text="General" ,command=lambda : MainApp.show_frame(master, General))
        self.button.grid(row=0, column=0, padx=10, pady=20, sticky="ew")
        
        self.button = ctk.CTkButton(self, text="Scope Sizings", command=lambda : MainApp.show_frame(master, ScopeSizing))
        self.button.grid(row=0, column=1, padx=10, pady=20, sticky="ew")
        
        self.button = ctk.CTkButton(self, text="Tunnel", command=lambda : MainApp.show_frame(master, Tunnel))
        self.button.grid(row=0, column=2, padx=10, pady=20, sticky="ew")
        
        self.button = ctk.CTkButton(self, text="Prisms", command=lambda : MainApp.show_frame(master, Prisms))
        self.button.grid(row=0, column=3, padx=10, pady=20, sticky="ew")
        
        self.button = ctk.CTkButton(self, text="Simulation", command=lambda : MainApp.show_frame(master, Simulation))
        self.button.grid(row=0, column=4, padx=10, pady=20, sticky="ew")
        
        self.button = ctk.CTkButton(self, text="Boundary Conditions", command=lambda : MainApp.show_frame(master, BoundaryConditions))
        self.button.grid(row=0, column=5, padx=10, pady=20, sticky="ew")
        
        self.button = ctk.CTkButton(self, text="Postprocessing", command=lambda : MainApp.show_frame(master, Postprocessing))
        self.button.grid(row=0, column=6, padx=10, pady=20, sticky="ew")

        self.button = ctk.CTkButton(self, text="Parametrization", command=lambda : MainApp.show_frame(master, Parameters))
        self.button.grid(row=0, column=7, padx=10, pady=20, sticky="ew")
        

class Queue(ctk.CTkFrame):
    '''
    Queue class manages the order of simulations in queue as well as a visualisation of queue in GUI.
    '''
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.treeText = ctk.CTkTextbox(self, height = 20, width = 150, fg_color = 'transparent',)
        self.treeText.grid(row=0, column=0, padx=10, pady=(10, 0) ,sticky="we")
        self.treeText.insert("0.0", 'Solution Queue')
        
        self.treeview = ttk.Treeview(self, height=27, columns= ('state', 'id'))
        self.treeview.column("#0", width=150)
        self.treeview.heading("#0", text="Name")
        self.treeview.column("state", width=70)
        self.treeview.heading("state", text="State")
        self.treeview.column("id", width=20)
        self.treeview.heading("id", text="ID")
        self.treeview.grid(row=1, column=0, padx=10, pady=(20, 20), sticky="w", rowspan= 10)

    def updateSims(self, simList:list[SimulationClass]):
        '''
        This method checks all simulations in queue and and assigns a propper status and colour based 
        on simulation status.
        '''
        treeChildren = self.treeview.get_children() #gets all the entries from queue tree
        for treeChild in treeChildren:
            matchSimID = self.treeview.item(treeChild)['values'][1] #gets ID in tree entry
            for sim in simList:
                if matchSimID == sim.SimID: #matches the tree entry ID with SimulationClass SimID
                    matchSim = sim
    
            self.treeview.item(treeChild, values = [matchSim.states[matchSim.SimStat], matchSim.SimID]) #assigns propper simulation status to queue tree
            self.treeview.item(treeChild,  tags = [matchSim.SimID])
        self.updateColour(simList)
           

    def insertSim(self, sim:SimulationClass):
        '''
        Inserts a new simulation (SimulationClass) to queue.
        '''
        self.treeview.insert(parent='', index=sim.SimID,iid=str(sim.SimID) , text= sim.simName, values=[sim.states[sim.SimStat], sim.SimID], tags = sim.SimID)
        #self.treeview.tag_configure(sef)
        self.updateSims(self.master.queue_list)

    def updateColour(self, simList:list[SimulationClass]):
        '''
        Assigns a proper colour in queue based on simulation status.
        '''
        treeChildren = self.treeview.get_children()
        colour = 'none'
        for treeChild in treeChildren:
            matchSimID = self.treeview.item(treeChild)['values'][1]
            for sim in simList:
                if matchSimID == sim.SimID:
                    matchSim = sim
            colour = 'none'
            #print(self.treeview.item(treeChild)['values'][0])
            match matchSim.SimStat:
                case 'wait':
                    colour = 'orange'
                case 'msh':
                    colour = 'yellow'
                case 'slv':
                    colour = 'blue'
                case 'post':
                    colour = 'purple'
                case 'dn':
                    colour = 'green'
                case 'err':#
                    colour = 'red'
            if colour != 'none':
                self.treeview.tag_configure(self.treeview.item(treeChild)['tags'][0], background= colour)
                #print(self.treeview.item(treeChild)['tags'][0])


class PrintLogger(object):  # create file like object
    '''
    File like objects for redirected terminal view.
    '''
    def __init__(self, textbox):  #: pass reference to text widget
        self.textbox = textbox  # keep ref

    def write(self, text):
        '''
        Writes into a Logger.
        '''
        self.textbox.configure(state="normal")  # make field editable
        self.textbox.insert("end", text)  # write text to textbox
        self.textbox.see("end")  # scroll to end
        self.textbox.configure(state="disabled")  # make field readonly

    def flush(self):  # needed for file like object
        pass


class MainApp(ctk.CTk):
    '''
    A main CTKinter class that services all other TKinter classes and pushes simulation settings into queue.
    '''
    def __init__(self, fg_color: str | Tuple[str, str] | None = None,*args,  **kwargs):
        
        super().__init__(fg_color,*args, **kwargs)

        '''
        App title and resolution
        '''
        self.title('CFD AutoSolver V0.05')
        self.geometry('1480 x1300')
        
        '''
        Initialisation of al needed mesh objects that will be handled to
        fluent automatization
        '''
        if not hasattr(self, 'GeneralObject'):
            print('Does not have objects initialised' )
            self.GeneralObject = GeneralSett()
            self.TunnelObject = TunnelSett()
            self.BoundarySett = Boundary_conditions_sett(15, 0.4, 0, 0.75, 0, 1.53, 0.75, 0,True, 372.1198, 1.5744, 0.7)
            self.SolverSett = SimulationSett()
            self.PostproSett = PostprocessSett()
            self.SettingsPath = ''
            self.ParametersSett = ParametrizationSett()
        else:
            print('Has objects initialised' )
        
        self.windows_init()
        

        

        queueLoopThread  = threading.Thread(target=self.QueueLoop, args= ())
        queueLoopThread.start()
 
        #self.checkbox_frame = MainAppCheckBoxFrame(self)
        #self.checkbox_frame.grid(row=2, column=0, padx=10, pady=(10, 10), sticky="w")
        self.segmentState = 'Meshing'
        self.segment_level = ctk.CTkSegmentedButton(self,values= ['Meshing', 'Solver', 'Postprocess'], command= self.changeSegment)
        self.segment_level.grid(row=3, column=0, padx=10, pady=(10, 10), sticky="we", columnspan = 2)
        self.segment_level.set('Meshing')
        
        self.button = ctk.CTkButton(self, text="Start simulation", command=self.Start)
        self.button.grid(row=5, column=4, padx=10, pady=10, sticky="ew", columnspan = 2)
        
        self.LoadSettingsText = ctk.CTkTextbox(self, height=5,  width= 130,  fg_color = 'transparent',)
        self.LoadSettingsText.grid(row=4, column=2, padx=(30, 10), pady=(10, 0) ,sticky="e")
        self.LoadSettingsText.insert("0.0", 'Load setting:')
        
        self.LoadSettingsButt = ctk.CTkButton(self,height=30,width= 100, text= 'Load...', command=self.browseJsonFiles)
        self.LoadSettingsButt.grid(row=4, column=3 , padx=10, pady=(10, 0), sticky="we")
        
        self.SaveSettingsText = ctk.CTkTextbox(self, height=5,  width= 130,  fg_color = 'transparent',)
        self.SaveSettingsText.grid(row=4, column=4, padx=(30, 10), pady=(10, 0) ,sticky="e")
        self.SaveSettingsText.insert("0.0", 'Save settings:')
        
        self.SaveSettingsButt = ctk.CTkButton(self,height=30,width= 100, text= 'Save...', command=self.getJsonSavePath)
        self.SaveSettingsButt.grid(row=4, column=5 , padx=10, pady=(10, 0), sticky="we")
        
        self.WorkDirText = ctk.CTkTextbox(self, height=5,  width= 130,  fg_color = 'transparent',)
        self.WorkDirText.grid(row=4, column=0, padx=10, pady=(10, 0) ,sticky="we", columnspan = 1)
        self.WorkDirText.insert("0.0", 'Working directory')
        
        self.WorkDirBox = ctk.CTkTextbox(self, height=20,  width= 290,)
        self.WorkDirBox.grid(row=5, column=0, padx=10, pady=(10, 10) ,sticky="we",columnspan = 4)
        self.WorkDirBox.insert("0.0", r'D:\work\directory')
        
        self.WorkDirButt = ctk.CTkButton(self,height=30,width= 100, text= 'Open...', command=self.browseFolders)
        self.WorkDirButt.grid(row=4, column=1 , padx=10, pady=(10, 0), sticky="we", columnspan = 1)
        
        self.console_text = ctk.CTkTextbox(self, width=650, height=120)
        self.console_text.grid(row=6, column=0 , padx=10, pady=(10, 10), sticky='we', columnspan  = 10) #Anchor the console box to the middle of the screen and add some padding
        self.console_text.configure(scrollbar_button_color="", scrollbar_button_hover_color="") #Make scroll-bar invisible
        if not Debug_Console:
            self.redirect_logging()
        
    def windows_init(self):
        '''
        Initialises the Options Menus top scrolls buttons and inserts a ctk.CTkFrame class of options menu to each button.
        
        If new options menu is desired, its ctk.CTkFrame class needs to be inserted into container bellow.
        '''
        container = ctk.CTkFrame(self)  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        container.grid(row=1, column=0, padx=10, pady=2, sticky="ew", columnspan = 7)
        #container.pack(side = "top", fill = "both", expand = True) 

        
        self.main_buttons_frame = MainMenuButtons(self)
        self.main_buttons_frame.grid(row=0, column=0, padx=(10,10), pady=2, sticky="ew", columnspan = 6)

        # initializing frames to an empty array
        self.frames = {}  
        
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (General, ScopeSizing, Tunnel, Prisms, Simulation, BoundaryConditions,  Postprocessing, Parameters):
  
            frame = F(container, self)
  
             #initializing frame of that object from
            # startpage, page1, page2 respectively with 
            # for loop
            self.frames[F] = frame 
  
            frame.grid(row = 1, column = 0, sticky ="nsew")
  
        self.show_frame(General)
            
    def reset_logging(self):
        '''
        Resets the terminal redirecting back to python terminal.
        '''
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def redirect_logging(self):
        '''
        Redirects the python terminal into a GUI terminal (read only).
        '''
        logger = PrintLogger(self.console_text)
        sys.stdout = logger
        sys.stderr = logger
    
     
    def browseFolders(self):
        '''
        Opens the explorer window and puts the selected folder into a GeneralObject.workingDirectory attribute.
        '''
        self.GeneralObject.workingDirectory = filedialog.askdirectory(initialdir = self.WorkDirBox.get('1.0'),
                                            title = "Select a Folder",
                                            )  
        self.WorkDirBox.delete('0.0', 'end')
        self.WorkDirBox.insert("0.0", self.GeneralObject.workingDirectory)   
        
    def changeSegment(self, a):
        '''
        Changes the simulation starting point and activates the GUI_Subclasses/GUI_General.General.activateDataInput() method.
        '''
        self.segmentState = self.segment_level.get() #gets the segment state from segment button
        self.frames[General].activateDataInput()
        print(self.segmentState)
     
    '''       
    def copyObject(self, oldObject):
        match type(oldObject):
            case MeshObjects.GeneralSett:
                newObject =MeshObjects.GeneralSett()
            case MeshObjects.TunnelSett:
                newObject =MeshObjects.TunnelSett()
            case Solver.SolverSettings:
                newObject =Solver.SolverSettings()
        
        for x in vars(oldObject).keys(): #iterating through all dictionary keys
            vars(newObject)[x] = vars(oldObject)[x]
        
        return newObject         
    '''
    def Start(self):
        '''
        Creates the SimulationsClass from current settings and pushes the simulation into a simulation queue.
        '''

    # Nebuď dement Trigger
        if self.GeneralObject.Version == 'STAR CCM+':
            try:
                 # Get the directory where the current script is located
                script_dir = os.path.dirname(os.path.abspath(__file__))
                image_path = os.path.join(script_dir, "star.png")

                # Open the image
                img = Image.open(image_path)
                img.show()
                print("Nebuď dement triggered!")
                return  # Exit early to skip running a simulation
            except Exception as e:
                print(f"Error opening easter egg image: {e}")
                return

    # Normal simulation execution
        print('\n General Settings \n')
        print(vars(self.GeneralObject.TransferFromTKinter()))
    
        print('\n Tunnel Settings \n')
        print(vars(self.TunnelObject.TransferFromTKinter()))

        print('\n Simulation Settings \n')
        print(vars(self.SolverSett.TransferFromTKinter()))

        print('\n Boundary Settings \n')
        print(vars(self.BoundarySett.TransferFromTKinter()))

        print('\n Postpro Settings \n')
        print(vars(self.PostproSett.TransferFromTKinter()))

        print('\n Boundary Settings \n')
        print(vars(self.ParametersSett.TransferFromTKinter()))



        #print('\n General Settings \n')
        #print(vars(self.GeneralObject.TransferFromTKinter()))
        
        #print('\n Tunnel Settings \n')
        #print(vars(self.TunnelObject.TransferFromTKinter()))
    
        #print('\n Simulation Settings \n')
        
        #print(vars(self.SolverSett.TransferFromTKinter()))

        #print('\n Boundary Settings \n')
        #print(vars(self.BoundarySett.TransferFromTKinter()))
        
        #print('\n Postpro Settings \n')
        #print(vars(self.PostproSett.TransferFromTKinter()))
        
        
        
        
        
        self.GeneralObject.workingDirectory = self.WorkDirBox.get('0.0', 'end')
        self.GeneralObject.workingDirectory = self.GeneralObject.workingDirectory.replace('\n', '')
        self.GeneralObject.IntCoreCount = int(self.GeneralObject.CoreCount.get())
        #self.TransformTunnelToFloat()
        #self.TransformSolverSettToFloat()
        print(self.GeneralObject.CAD_Path)
        print(self.GeneralObject.workingDirectory)
        for MSH_Obj in self.MeshObjList['vehicle']:
            MSH_Obj.Ignore_self = bool(int(MSH_Obj.Ignore_self))
            print(vars(MSH_Obj))
        if self.segment_level.get() == 'Solver':
            sim_state = 'msh_dn'
        elif self.segment_level.get() == 'Postprocess':
            sim_state = 'slv_dn'
        else:
            sim_state = 'wait'
        sim = SimulationClass(
                              simGeneralObject=  self.GeneralObject.TransferFromTKinter(),
                              simMeshObjectList= copy.deepcopy(self.MeshObjList),
                              simTunnelObject= self.TunnelObject.TransferFromTKinter(), 
                              simSolverSett= self.SolverSett.TransferFromTKinter(),
                              simBoundarySett = self.BoundarySett.TransferFromTKinter(),
                              simPostproSett= self.PostproSett.TransferFromTKinter(),
                              simParametersSett= self.ParametersSett.TransferFromTKinter(),
                              simName= self.GeneralObject.workingDirectory[self.GeneralObject.workingDirectory.rfind('/')+1::],
                              simStat= sim_state)
        self.queue_list.append(sim)
        self.queue.insertSim(sim)
        
        #print(self.queue_list[0].SimID)#simSett.TunnelObject.Cell_size)
        #print(self.queue_list[1].SimID)#simSett.TunnelObject.Cell_size)
        # sim1.startMeshing()
        '''
        MeshingObj = Mesher.StartFluentMeshing(self.MeshObjList,
                                  General_Settings= self.GeneralObject,
                                  Tunnel_Settings = self.TunnelObject
                                  )
        
        
        #MeshingObj =1
        SolverObj = Solver.StartFluentSolver(self.SolverSett, MeshingObj, self.MeshObjList)
        
        Postproces.StartPostprocessing(SolverObj,SolvSett= self.SolverSett, MSH_Objects= self.MeshObjList)
        
    '''
    '''
    def StartThread(self):
        t1 = threading.Thread(target= self.Start, args= () )
        #t2 = threading.Thread(target= self.Start, args=())
        
        t1.start()
        #t2.start()
    '''
    def QueueLoop(self):
        '''
        Loop responsible for pushing simulations in the queue.
        '''

        def SimListStatCheck(simList, state):
            '''
            Checks if a simulation with given simulation state exists within provided list (Queue).
            '''
            for sim in simList:
                if state == sim.SimStat:
                    return True
            return False    
        self.queue = Queue(master = self)
        self.queue.grid(row=0, column=9, padx=10, pady=8, sticky="ew", rowspan = 5)

        def PrintSimStats(simList):
            simStatDict = {}
            for sim in simList:
                simStatDict[sim.simName] = sim.SimStat
            print (simStatDict)
            
            
        self.queue_list = []        
        while True:
            #self.queue.updateSims(self.queue_list)
            self.queue.update()
            if self.queue_list == []:
                time.sleep(1)
            else:
                time.sleep(1)
                #self.queue.updateSims(self.queue_list)
                self.queue.update()
                for Sim in self.queue_list:
                    #print('##Sim State##')
                    #print(Sim.simName)
                    #PrintSimStats(self.queue_list)
                    #print(SimListStatCheck(self.queue_list, 'msh'))
                    
                    self.queue.updateSims(self.queue_list)
                    time.sleep(3)
                    
                    if  Sim.SimThread != None:
                        if Sim.SimThread.is_alive()!=True:
                            Sim.SimStat = 'err'
                    match Sim.SimStat:
                        case 'wait':
                            if SimListStatCheck(self.queue_list, 'msh') == False:
                                Sim.SimStat = 'msh'
                                Sim.SimThread = Sim.startMeshingThread()
                                #Sim.SimStat = 'post'
                                #Sim.SimThread = Sim.startPostproThread()
                                
                                #Sim.SimStat = 'slv'
                                #Sim.meshPath = 'D:\plesnik\PyFluent\Versions\Beta18v1_14_01_25\TestSim1\Po_autonodemove.msh.h5'
                                #Sim.SimThread = Sim.startSolverThread()
                        case 'msh_dn':
                            if SimListStatCheck(self.queue_list, state= 'slv') == False:
                                Sim.SimStat = 'slv'
                                Sim.SimThread = Sim.startSolverThread()

                        case 'slv_dn':
                            if SimListStatCheck(self.queue_list, state= 'post') == False:
                                Sim.SimStat = 'post'
                                Sim.SimThread = Sim.startPostproThread()
                        case 'post':
                            True
                        case 'dn':
                            True
                        case 'err':
                            True        
        
    '''
    def TransformTunnelToFloat(self):
        for x in vars(self.TunnelObject).keys():
            if type(vars(self.TunnelObject)[x]) != float:
                vars(self.TunnelObject)[x] = float(vars(self.TunnelObject)[x].get())
                
    def TransformSolverSettToFloat(self):
        for x in vars(self.SolverSett).keys():
            print(x)
            if type(vars(self.SolverSett)[x]) != float and type(vars(self.SolverSett)[x]) != list:
                print('A')
                vars(self.SolverSett)[x] = float(vars(self.SolverSett)[x].get())
            elif type(vars(self.SolverSett)[x]) == list:
                print('B')
                print(vars(self.SolverSett)[x][0])
                print(type(vars(self.SolverSett)[x][0]))
                if type(vars(self.SolverSett)[x][0]) != float:
                    for i in range(len(vars(self.SolverSett)[x])):                
                        vars(self.SolverSett)[x][i] = float(vars(self.SolverSett)[x][i].get())
                        print(vars(self.SolverSett)[x][i])
    '''
    
        
    def show_frame(self, cont):
        '''
        Shows a frame of given ctk.CTkFrame class options menu.
        '''
        frame = self.frames[cont]
        frame.tkraise()
        if cont == Prisms:
            print('Loading Prisms')
            Prisms.LoadTree(frame)
         
    def getJsonSavePath(self):
        '''
        Gets a .json file path from opened explorer window and writes current simulation settings 
        into newly created .json file.
        '''
        self.writeFilename = filedialog.asksaveasfilename(initialdir = self.WorkDirText.get('1.0'),
                                          title = "Select a File",
                                          filetypes=[('JSON Files', '*.json'),('Text Files', '*.txt'), ('All Files', '*.*')],
                                          defaultextension='.json'
            )
            #MeshObjects.WriteObjToFile(self.controller.MeshObjList, self.writeFilename)
        self.WriteSettToJson([self.GeneralObject.TransferFromTKinter(), 
                               self.TunnelObject.TransferFromTKinter(), 
                               self.SolverSett.TransferFromTKinter(), 
                               self.BoundarySett.TransferFromTKinter(), 
                               self.PostproSett.TransferFromTKinter(),
                               self.ParametersSett.TransferFromTKinter() ], 
                              self.writeFilename)
            #print(self.writeFilename)
           
    def WriteSettToJson(self,Obj_list, file_path):
        '''
        Writes all the provided Settings objects into a provided .json file.
        '''
        with open(file_path, mode = 'w', encoding= 'utf-8') as write_file:
            Obj_dict = {'GeneralSett':[], 'TunnelSett':[], 'SimulationSett':[], 'Boundary_conditions_sett':[],  'PostprocessSett':[],  'ParametrizationSett':[]}
            for Obj in Obj_list:

                print(str(type(Obj))[str(type(Obj)).rfind('.',)+1:str(type(Obj)).find('\'',-1)-1])
            for Obj in Obj_list:
                Obj_dict[str(type(Obj))[str(type(Obj)).rfind('.')+1:str(type(Obj)).find('\'',-1)-1]].append(vars(Obj))                 
            print(Obj_dict)
            json.dump(Obj_dict, write_file , indent=2)  

    def browseJsonFiles(self):
        '''
        Opens the explorer window and reads the selected .json settings file.
        '''
        self.filename = filedialog.askopenfilename(initialdir = self.WorkDirBox.get('1.0'),
                                          title = "Select a File",
                                          filetypes = (("JSON files",
                                                        "*.json*"),
                                                       ("Text files",
                                                        "*.txt*"),
                                                       ("all files",
                                                        "*.*")))     
        
        self.SettingsPath = self.filename
        self.ReadSettJson(self.filename)
    
    def ReadSettJson(self, File_path):
        '''
        Reads a provided .json file and loads the values into settings objects.        
        '''
        with open(File_path, mode = 'r', encoding= 'utf-8') as read_file:
            scope_data = json.load(read_file)
        print(scope_data)
        self.GeneralObject._ValueReadJson(scope_data['GeneralSett'])      
        self.TunnelObject._ValueReadJson(scope_data['TunnelSett'])
        self.SolverSett._ValueReadJson(scope_data['SimulationSett'])
        self.BoundarySett._ValueReadJson(scope_data['Boundary_conditions_sett'])
        self.PostproSett._ValueReadJson(scope_data['PostprocessSett'])
        self.ParametersSett._ValueReadJson(scope_data['ParametrizationSett'])
        self.windows_init()
       
            

if __name__ == '__main__':  
    app = MainApp()
    app.mainloop()

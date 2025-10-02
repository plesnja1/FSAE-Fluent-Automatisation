import tkinter
import customtkinter as ctk
from tkinter import filedialog


class Setting:
    '''
    A parent class for every settings object. Makes settings import and copy creations easier.
    '''
    
    def TransferFromTKinter(self):
        '''
        Creates a copy of the object.
        
        :returns: type(self)
        '''
        CopyObject = type(self)()
        for key in vars(self).keys():
            if type(vars(self)[key]) ==  (tkinter.StringVar or tkinter.IntVar or tkinter.DoubleVar or tkinter.BooleanVar):
                vars(CopyObject)[key] = type(vars(CopyObject)[key])(vars(self)[key].get())
                
            else: 
                vars(CopyObject)[key] =(vars(self)[key])
            

        return CopyObject
    
    def _ValueReadJson(self, Settings_dir):
        '''
        Reads a values from .json file.
        
        :meta public:
        '''
        for var in vars(self).keys():
                vars(self)[var] = Settings_dir[0][var]   
        print(type(self))
        print(vars(self))     
 

class GeneralSett(Setting):
    '''
    Class containing general settings of meshing and simulation
    (precision of solver, number of processes, GPU or CPU solver, etc.).
    '''
    def __init__(self):
        '''
        Assigns default values.
        '''
        self.DoublePrecision = 'single'
        self.CoreCount = '20'
        self.IntCoreCount = 20
        self.GPU = True
        self.Mode = 'Meshing'
        self.PyConsole = True
        self.CAD_Path = ''
        self.Data_Path = ''
        self.GUI = 'gui'
        self.workingDirectory = 'D:/work' 
        self.Version = '25.1'
        self.RemovePart = ''  
        self.DefaultMeshPath = ''
        self.FullAssembly = False
        self.WebServer = True
            
class General(ctk.CTkFrame):
    '''
    ctk.CTkFrame class servicing the General settings menu.
    '''
    
    
    def __init__(self, parent, controller):
        '''
        Frame initialisation and features placement.
        '''
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.DoublePrecisionText = ctk.CTkTextbox(self, height= 20, width= 130)
        self.DoublePrecisionText.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        self.DoublePrecisionText.insert("0.0", 'Solver Precision')
        
        self.DoublePrecisionCombo = ctk.CTkComboBox(self, values=['Single Precision', 'Double Precision'], command= self.DoublePrecisionChange )
        self.DoublePrecisionCombo.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="w")

        self.VersionText = ctk.CTkTextbox(self, height=20,  width= 130)
        self.VersionText.grid(row=0, column=2, padx=10, pady=(10, 0), sticky="w")
        self.VersionText.insert("0.0", 'Version')
    
        self.VersionCombo = ctk.CTkComboBox(self, values=['25.1','25.2','24.2','STAR CCM+'], command= self.VersionChange)
        self.VersionCombo.grid(row=0, column=3, padx=10, pady=(10, 0), sticky="w")
    
        self.GPUText = ctk.CTkTextbox(self, height=20,  width= 130)
        self.GPUText.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")
        self.GPUText.insert("0.0", 'GPU or CPU Solver')
    
        self.GPUCombo = ctk.CTkComboBox(self, values=['GPU', 'CPU'], command= self.GPUChange)
        self.GPUCombo.grid(row=1, column=1, padx=10, pady=(10, 0), sticky="w")
        
        self.NCoresText = ctk.CTkTextbox(self, height= 20,width= 130)
        self.NCoresText.grid(row=2 ,column=0, padx=10, pady=(10, 0), sticky="w")
        self.NCoresText.insert("0.0", 'Solver Processes')
        
        self.controller.GeneralObject.CoreCount = ctk.StringVar(None, str(self.controller.GeneralObject.CoreCount))
        self.CoreEntry = ctk.CTkEntry(self ,textvariable=self.controller.GeneralObject.CoreCount,width= 30, placeholder_text= '4')
        self.CoreEntry.grid(row=2, column=1, padx=10, pady=(10, 0), sticky="w")
        
        self.PyConsoleText = ctk.CTkLabel(self, text='Turn on Python Console?')
        self.PyConsoleText.grid(row=3, column=0, padx=10, pady=(10, 10), sticky="nw")

        self.PyConsoleVarCheck = ctk.BooleanVar()
        self.PyConsoleCheck = ctk.CTkCheckBox(self, text="",variable=self.PyConsoleVarCheck,onvalue=True, offvalue=False, command=self.PyConsoleChange)
        self.PyConsoleCheck.grid(row=3, column=1, padx=10, pady=(10, 10), sticky="nw")

        self.WebServerText = ctk.CTkLabel(self, text='Start Web Server?')
        self.WebServerText.grid(row=3, column=2, padx=10, pady=(10, 10), sticky="nw")

        self.WebServerVarCheck = ctk.BooleanVar()
        self.WebServerCheck = ctk.CTkCheckBox(self, text="",variable=self.WebServerVarCheck,onvalue=True, offvalue=False, command=self.WebServerChange)
        self.WebServerCheck.select()
        self.WebServerCheck.grid(row=3, column=3, padx=10, pady=(10, 0), sticky="nw")

        self.PyConsoleText = ctk.CTkLabel(self, text='Start with GUI?')
        self.PyConsoleText.grid(row=4, column=0, padx=10, pady=(10, 10), sticky="nw")

        self.GUIVarCheck = ctk.IntVar()
        self.GUICheck = ctk.CTkCheckBox(self, text="",variable=self.GUIVarCheck,onvalue=1, offvalue=0, command=self.GUIChange)
        self.GUICheck.grid(row=4, column=1, padx=10, pady=(10, 10), sticky="nw")
        self.GUICheck.select()

        self.MeshText = ctk.CTkLabel(self, text='Load Entry .msh.h5 file...')
        self.MeshText.grid(row=5, column=0, padx=10, pady=(10, 10), sticky="nw")

        self.MeshFileText =ctk.CTkTextbox(self, width= 370, height=15)
        self.MeshFileText.grid(row=5, column=1, padx=10, pady=(10, 10), sticky="nw", columnspan = 4)
        self.MeshFileText.insert('0.0', r'D:\work\scopefiles')

        self.MeshFileButt = ctk.CTkButton(self,height=30,width= 100, text= 'Open...', command=self.browseFilesMesh)
        self.MeshFileButt.grid(row=5, column=4 , padx=10, pady=(10, 10), sticky="nw")   

        self.PartText = ctk.CTkLabel(self, text='Parts to be replaced (*example*)...')
        self.PartText.grid(row=6, column=0, padx=10, pady=(10, 10), sticky="nw")  

        self.controller.GeneralObject.RemovePart = ctk.StringVar(None, str(self.controller.GeneralObject.RemovePart))
        self.PartEntry = ctk.CTkEntry(self ,textvariable=self.controller.GeneralObject.RemovePart,width= 370, placeholder_text= '4')
        self.PartEntry.grid(row=6, column=1, padx=10, pady=(10, 0), sticky="w")

        self.CadText = ctk.CTkLabel(self, text='Load .stp CAD file...')
        self.CadText.grid(row=7, column=0, padx=10, pady=(10, 10), sticky="nw")
        
        self.CadFileText =ctk.CTkTextbox(self, width= 370, height=15)
        self.CadFileText.grid(row=7, column=1, padx=10, pady=(10, 10), sticky="nw", columnspan = 4)
        self.CadFileText.insert('0.0', r'D:\work\scopefiles')

        self.FullAssemblyText = ctk.CTkLabel(self, text='Load full assembly .stp CAD file...')
        self.FullAssemblyText.grid(row=7, column=2, padx=10, pady=(10, 10), sticky="nw")
        
        self.FullAssembly_Check = ctk.IntVar(value=0)
        self.FullAssembly_Check_Box = ctk.CTkCheckBox(self, text="",variable=self.FullAssembly_Check,onvalue=1, offvalue=0, command=self.FullAssemblyChange)
        self.FullAssembly_Check_Box.grid(row=7  , column=3, padx=10, pady=(10, 0), sticky="w")
        
        self.CadFileButt = ctk.CTkButton(self,height=30,width= 100, text= 'Open...', command=self.browseFiles)
        self.CadFileButt.grid(row=7, column=4 , padx=10, pady=(10, 10), sticky="nw")
        
        self.DataText = ctk.CTkLabel(self, text='Load .dat Fluent data file...')
        self.DataText.grid(row=8, column=0, padx=10, pady=(10, 10), sticky="nw")
        
        self.DataFileText =ctk.CTkTextbox(self, width= 370, height=15)
        self.DataFileText.grid(row=8, column=1, padx=10, pady=(10, 10), sticky="nw", columnspan = 4)
        self.DataFileText.insert('0.0', r'D:\work\scopefiles')
        self.DataFileText.configure(state = 'disabled')
        self.DataFileText.configure(fg_color = 'grey')
        
        self.DataFileButt = ctk.CTkButton(self,height=30,width= 100, text= 'Open...', command=self.browseFilesData)
        self.DataFileButt.grid(row=8, column=4 , padx=10, pady=(10, 10), sticky="nw")        
        self.DataFileButt.configure(state = 'disabled')
        self.DataFileButt.configure(fg_color = 'PaleGreen4')
        
       
    def browseFiles(self):
        '''
        Open an explorer window and put a selected path to a CAD file into a GeneralSett.CAD_Path attribute.
        '''
        self.CADfilename = filedialog.askopenfilename(initialdir = self.CadFileText.get('1.0'),
                                          title = "Select a File",
                                          filetypes = (("Sumulation files",
                                                        ["*.stp*", "*.msh*", "*.cas*"]),
                                                        ("Step files",
                                                        "*.stp*"),
                                                       ("Mesh files",
                                                        "*.msh*"),
                                                       ("Case files",
                                                        "*.cas*"),
                                                       ("all files",
                                                        "*.*")))
             
        self.CadFileText.delete('0.0', 'end')
        self.CadFileText.insert('0.0', self.CADfilename)
        self.controller.GeneralObject.CAD_Path = self.CADfilename
        print(self.controller.GeneralObject.CAD_Path)
        
    def browseFilesData(self):
        '''
        Open an explorer window and put a selected path to a .DAT fluent data file into a GeneralSett.Data_Path attribute.
        '''
        self.Datafilename = filedialog.askopenfilename(initialdir = self.DataFileText.get('1.0'),
                                          title = "Select a File",
                                          filetypes = (("Data files",
                                                        "*.dat*"),
                                                       ("all files",
                                                        "*.*")))
             
        self.DataFileText.delete('0.0', 'end')
        self.DataFileText.insert('0.0', self.Datafilename)
        self.controller.GeneralObject.Data_Path = self.Datafilename
        print(self.controller.GeneralObject.Data_Path)
         
    def browseFilesMesh(self):
        '''
        Open an explorer window and put a selected path to a .msh fluent mesh file into a GeneralSett.DefaultMeshPath attribute.
        '''
        self.DefaultMesh_filename = filedialog.askopenfilename(initialdir = self.MeshFileText.get('1.0'),
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.msh.h5*"),
                                                       ("all files",
                                                        "*.*")))
             
        self.MeshFileText.delete('0.0', 'end')
        self.MeshFileText.insert('0.0', self.DefaultMesh_filename)
        self.controller.GeneralObject.DefaultMeshPath = self.DefaultMesh_filename
        print(self.controller.GeneralObject.DefaultMeshPath)

    def PyConsoleChange(self):
        '''
        Switches between Python and tui console in Fluent GUI.
        '''
        if self.PyConsoleVarCheck.get():

            self.controller.GeneralObject.PyConsole = True 
            print('Py Console Check State:')    
            print(self.controller.GeneralObject.PyConsole) 
        else:
            self.controller.GeneralObject.PyConsole = False 
            print('Py Console Check State:')   
            print(self.controller.GeneralObject.PyConsole)    

    def WebServerChange(self):
        '''
        Start a remote web server.
        '''
        if self.WebServerVarCheck.get():

            self.controller.GeneralObject.WebServer = True 
            print('WebServer Check State:')    
            print(self.controller.GeneralObject.WebServer) 
        else:
            self.controller.GeneralObject.WebServer = False 
            print('WebServer Check State:')   
            print(self.controller.GeneralObject.WebServer) 
            
    def GUIChange(self):
        '''
        Start with Fluent GUI.
        '''
        print('GUI Check State:') 
        print(self.GUIVarCheck.get())
        if self.GUIVarCheck.get() == 1:
            self.controller.GeneralObject.GUI = 'gui'   
            print('GUI Var State:')    
            print(self.controller.GeneralObject.GUI)    
        else:
            self.controller.GeneralObject.GUI = 'no_gui_or_graphics'
            print('GUI Var State:')    
            print(self.controller.GeneralObject.GUI)   
    
    def DoublePrecisionChange(self, select):
        '''
        Changes the preccision solver setting.
        '''
        if select == 'Single Precision':
            self.controller.GeneralObject.DoublePrecision =  'single' #pyfluent.Precision.SINGLE
            print('Precision Check State:\n')
            print(self.controller.GeneralObject.DoublePrecision)
        else:
            self.controller.GeneralObject.DoublePrecision = 'double'#pyfluent.Precision.DOUBLE
            print('Precision Check State:\n')
            print(self.controller.GeneralObject.DoublePrecision)

    def VersionChange(self, select):
        '''
        Slection of Fluent version.
        '''
        if select == '24.2':
            self.controller.GeneralObject.Version =  '24.2'
            print('Version Check State:\n')
            print(self.controller.GeneralObject.Version)
           
        elif select == '25.1':
            self.controller.GeneralObject.Version =  '25.1'
            print('Version Check State:\n')
            print(self.controller.GeneralObject.Version)
            
        else:
            self.controller.GeneralObject.Version =  'STAR CCM+'
            print('Version Check State:\n')
            print(self.controller.GeneralObject.Version)        
    
    def GPUChange(self, select):
        '''
        Select CPU or GPU solver.
        '''
        if select == 'CPU':
            self.controller.GeneralObject.GPU = False
            print(self.controller.GeneralObject.GPU)
        else:
            self.controller.GeneralObject.GPU = True
            print(self.controller.GeneralObject.GPU)
        
    def activateDataInput(self):
        '''
        Sets the initial simulation stage based on Segment Button. Also alters button and text windows states based on selected stage.
        '''
        if self.controller.segmentState == 'Postprocess':
            self.DataFileText.configure(state = 'normal')
            self.DataFileText.configure(fg_color = 'grey23')
            self.DataFileButt.configure(state = 'normal')
            self.DataFileButt.configure(fg_color = 'medium sea green')       
            self.CadText.configure(text = 'Load .cas Fluent case file...')
            self.MeshFileText.configure(state = 'disabled')
            self.MeshFileText.configure(fg_color = 'grey')
            self.PartEntry.configure(state = 'disabled')
            self.PartEntry.configure(fg_color = 'grey')
            self.MeshFileButt.configure(state = 'disabled')
            self.MeshFileButt.configure(fg_color = 'PaleGreen4')

        elif self.controller.segmentState == 'Solver':
            self.DataFileText.configure(state = 'disabled')
            self.DataFileText.configure(fg_color = 'grey')
            self.DataFileButt.configure(state = 'disabled')
            self.DataFileButt.configure(fg_color = 'PaleGreen4')
            self.CadText.configure(text = 'Load .msh Fluent mesh file...')
            self.MeshFileText.configure(fg_color = 'grey')
            self.PartEntry.configure(state = 'disabled')
            self.PartEntry.configure(fg_color = 'grey')
            self.MeshFileButt.configure(state = 'disabled')
            self.MeshFileButt.configure(fg_color = 'PaleGreen4')
            
        else:
            self.DataFileText.configure(state = 'disabled')
            self.DataFileText.configure(fg_color = 'grey')
            self.DataFileButt.configure(state = 'disabled')
            self.DataFileButt.configure(fg_color = 'PaleGreen4')
            self.CadText.configure(text = 'Load .stp CAD file...')
            self.PartEntry.configure(state = 'normal')
            self.PartEntry.configure(fg_color = 'grey23')
            self.MeshFileButt.configure(state = 'normal')
            self.MeshFileButt.configure(fg_color = 'medium sea green')
            self.MeshFileText.configure(state = 'normal')
            self.MeshFileText.configure(fg_color = 'grey23')


    def FullAssemblyChange(self):
        '''
        Wether only part of the assembly or whole assembly is loaded.
        '''
        print('Full Assembly Check State:') 
        print(self.FullAssembly_Check.get())

        if self.FullAssembly_Check.get() == 1:
            self.controller.GeneralObject.FullAssembly = True
            print('Full Assembly Var State:')    
            print(self.controller.GeneralObject.FullAssembly)    
            self.MeshFileText.configure(state='disabled')
            self.MeshFileText.configure(fg_color='grey')
            self.MeshFileButt.configure(state='disabled')
            self.MeshFileButt.configure(fg_color='PaleGreen4')
            self.PartEntry.configure(state='disabled')
            self.PartEntry.configure(fg_color='grey')
        else:
            self.controller.GeneralObject.FullAssembly = False
            print('Full Assembly Var State:')    
            print(self.controller.GeneralObject.FullAssembly)
            self.MeshFileText.configure(state='normal')
            self.MeshFileText.configure(fg_color='grey23')
            self.MeshFileButt.configure(state='normal')
            self.MeshFileButt.configure(fg_color='medium sea green')
            self.PartEntry.configure(state='normal')
            self.PartEntry.configure(fg_color='grey23')
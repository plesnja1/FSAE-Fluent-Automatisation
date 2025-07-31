import customtkinter as ctk
from tkinter import filedialog
from tkinter import ttk
from GUI_SubClasses.GUI_General import Setting

class SimulationSett(Setting):
    def __init__(self):
        self.Turbulence_model = 'k-omega'
        self.Wall_function = 'enhanced-wall-treatment'
        self.Coupling = 'Coupled'
        self.Transient = 'steady'
        self.iter_count = 1500
        self.TimeStep = 1 #[s]
        self.Time = 1 #[s]
        self.Temperature = 34.24 #[°C]
        self.Height = 0 #[m]
        
        
class Simulation(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        
        self.Turb_mod_text = ctk.CTkLabel(self, text='Turbulence model')
        self.Turb_mod_text.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="w")
        
        self.Turb_mod_combo = ctk.CTkComboBox(self, values=['SST k-Omega', 'k-Epsilon'], command= self.Turb_mod_change )
        self.Turb_mod_combo.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="w")
        
        self.Wall_funct_text = ctk.CTkLabel(self, text='Wall function')
        self.Wall_funct_text.grid(row=1, column=0, padx=10, pady=(10, 10), sticky="w")
        
        self.Wall_funct_combo = ctk.CTkComboBox(self, values=[ 'Enhanced', 'Standard', 'Non-Equilibrium'], command= self.Wall_funct_change )
        self.Wall_funct_combo.grid(row=1, column=1, padx=10, pady=(10, 0), sticky="w")
 
        self.Coupling_text = ctk.CTkLabel(self, text='Pressure-Veopcity Coupling')
        self.Coupling_text.grid(row=2, column=0, padx=10, pady=(10, 10), sticky="w")
        
        self.Coupling_combo = ctk.CTkComboBox(self, values=['Coupled', 'SIMPLE'], command= self.Coupling_change )
        self.Coupling_combo.grid(row=2, column=1, padx=10, pady=(10, 0), sticky="w")
               
        self.Transient_text = ctk.CTkLabel(self, text='Time')
        self.Transient_text.grid(row=3, column=0, padx=10, pady=(10, 10), sticky="w")
        
        self.Transient_combo = ctk.CTkComboBox(self, values=['Steady', 'Transient'], command= self.Transient_change )
        self.Transient_combo.grid(row=3, column=1, padx=10, pady=(10, 0), sticky="w")
       
        self.Iter_count_text = ctk.CTkLabel(self, text='Number of iterations')
        self.Iter_count_text.grid(row=4, column=0, padx=30, pady=(10, 10), sticky="w")
        # 
        controller.SolverSett.iter_count = ctk.StringVar(None, str(controller.SolverSett.iter_count))
        self.Iter_count_Entry = ctk.CTkEntry(self ,textvariable=controller.SolverSett.iter_count,width= 60, placeholder_text= 100)
        self.Iter_count_Entry.grid(row=4  , column=1, padx=10, pady=(10, 0), sticky="w") 
        
        self.Time_step_text = ctk.CTkLabel(self, text='Pseudo-time step [-]')
        self.Time_step_text.grid(row=5, column=0, padx=30, pady=(10, 10), sticky="w")
        # 
        controller.SolverSett.TimeStep = ctk.StringVar(None, str(controller.SolverSett.TimeStep))
        self.Time_step_Entry = ctk.CTkEntry(self ,textvariable=controller.SolverSett.TimeStep,width= 60, placeholder_text= '100')
        self.Time_step_Entry.grid(row=5  , column=1, padx=10, pady=(10, 0), sticky="w") 

        self.Time_text = ctk.CTkLabel(self, text='End time of simulation [s]')
        self.Time_text.grid(row=5, column=2, padx=10, pady=(10, 10), sticky="w")
        # 
        controller.SolverSett.Time = ctk.StringVar(None, str(controller.SolverSett.Time))
        self.Time_Entry = ctk.CTkEntry(self ,textvariable=controller.SolverSett.Time,width= 60, placeholder_text= '100')
        self.Time_Entry.grid(row=5  , column=3, padx=10, pady=(10, 0), sticky="w") 
        self.Time_Entry.configure(state = 'disabled')
        self.Time_Entry.configure(fg_color = 'gray')
        
        self.Temperature_text = ctk.CTkLabel(self, text='Air temperature [°C]')
        self.Temperature_text.grid(row=6, column=0, padx=10, pady=(10, 10), sticky="w")
        # 
        controller.SolverSett.Temperature = ctk.StringVar(None, str(controller.SolverSett.Temperature))
        self.Temperature_Entry = ctk.CTkEntry(self ,textvariable=controller.SolverSett.Temperature,width= 60, placeholder_text= '100')
        self.Temperature_Entry.grid(row=6  , column=1, padx=10, pady=(10, 0), sticky="w") 
        
        self.Height_text = ctk.CTkLabel(self, text='Altitude [m]')
        self.Height_text.grid(row=7, column=0, padx=10, pady=(10, 10), sticky="w")
        # 
        controller.SolverSett.Height = ctk.StringVar(None, str(controller.SolverSett.Height))
        self.Height_Entry = ctk.CTkEntry(self ,textvariable=controller.SolverSett.Height,width= 60, placeholder_text= '100')
        self.Height_Entry.grid(row=7  , column=1, padx=10, pady=(10, 0), sticky="w") 
       
    def Turb_mod_change(self, select):
        if select == 'SST k-Omega':
            self.controller.SolverSett.Turbulence_model =  'k-omega'
            print('Turbulence Check State:\n')
            print(self.controller.SolverSett.Turbulence_model)
            self.Wall_funct_combo.configure(state = 'disabled')
            self.Wall_funct_combo.configure(fg_color = 'gray')
        else:
            self.controller.SolverSett.Turbulence_model =  'k-epsilon'
            print('Turbulence Check State:\n')
            print(self.controller.SolverSett.Turbulence_model)
            self.Wall_funct_combo.configure(state = 'normal')
            self.Wall_funct_combo.configure(fg_color = 'gray24')
            
    def Wall_funct_change(self, select):
        if select == 'Enhanced':
            self.controller.SolverSett.Wall_function =  'enhanced-wall-treatment'
            print('Wall Function Check State:\n')
            print(self.controller.SolverSett.Wall_function)
           
        elif select == 'Standard':
            self.controller.SolverSett.Wall_function =  'standard-wall-fn'
            print('Wall Function Check State:\n')
            print(self.controller.SolverSett.Wall_function)
            
        else:
            self.controller.SolverSett.Wall_function =  'non-equilibrium-wall-fn'
            print('Wall Function Check State:\n')
            print(self.controller.SolverSett.Wall_function)
            
    def Coupling_change(self, select):
        if select == 'Coupled':
            self.controller.SolverSett.Coupling = 'Coupled'
            print('Coupling Check State:\n')
            print(self.controller.SolverSett.Coupling)

        else:
            self.controller.SolverSett.Coupling = 'SIMPLE'
            print('Coupling Check State:\n')
            print(self.controller.SolverSett.Coupling)
            
    def Transient_change(self, select):
        if select == 'Steady':
            self.controller.SolverSett.Transient = 'steady'
            print('Transient Check State:\n')
            print(self.controller.SolverSett.Transient)
            self.Time_Entry.configure(state = 'disabled')
            self.Time_Entry.configure(fg_color = 'gray')
            self.Time_step_text.configure(text = 'Pseudo-time step ')
            self.Iter_count_text.configure(text = 'Number of iteration ')

        else:
            self.controller.SolverSett.Transient = 'unsteady-2nd-order'
            print('Transient Check State:\n')
            print(self.controller.SolverSett.Transient)
            self.Time_Entry.configure(state = 'normal')
            self.Time_Entry.configure(fg_color = 'gray24')
            self.Time_step_text.configure(text = 'Time step size [s]')
            self.Iter_count_text.configure(text = 'Iterations per time step ')
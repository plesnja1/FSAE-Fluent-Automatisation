import customtkinter as ctk
from tkinter import filedialog
from tkinter import ttk
from GUI_SubClasses.GUI_General import Setting

class Boundary_conditions_sett(Setting):
    def __init__(self, velocity = 0, WheelDiameter = 0, f_w_axis_x = 0, f_w_axis_y = 0,f_w_axis_z = 0,r_w_axis_x = 0,r_w_axis_y = 0,r_w_axis_z = 0,rad_check = True,  c_0 = 0, c_1 = 0, porosity = 0, Fan_2D_check = True):
        self.velocity = float(velocity) #inlet velocity
        self.WheelDiameter = float(WheelDiameter) #diameter of wheels
        self.f_w_axis_x = float(f_w_axis_x) #position of front axis
        self.f_w_axis_y = float(f_w_axis_y) #position of front axis
        self.f_w_axis_z = float(f_w_axis_z) #position of front axis
        self.r_w_axis_x = float(r_w_axis_x) #position of rear axis
        self.r_w_axis_y = float(r_w_axis_y) #position of rear axis
        self.r_w_axis_z = float(r_w_axis_z) #position of rear axis
        
        self.Radiator_check = bool(rad_check)
        self.power_law_c_0 = float(c_0)
        self.power_law_c_1 = float(c_1)
        self.porosity = float(porosity)

        self.Fan_2D_check = bool(Fan_2D_check)
        self.Fan_2D_curve_Path = ''
        self.workingDirectory = 'D:/work' 
        


class BoundaryConditions(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        
        self.Vel_text = ctk.CTkLabel(self, text='Inlet velocity [m/s]')
        self.Vel_text.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="w")
        
        controller.BoundarySett.velocity = ctk.StringVar(None, str(controller.BoundarySett.velocity))
        self.Vel_Entry = ctk.CTkEntry(self ,textvariable=controller.BoundarySett.velocity,width= 60, placeholder_text= '16')
        self.Vel_Entry.grid(row=0  , column=1, padx=10, pady=(10, 0), sticky="nw")
        
        self.W_diam_text = ctk.CTkLabel(self, text='Wheel diameter [m]')
        self.W_diam_text.grid(row=0, column=2, padx=10, pady=(10, 10), sticky="w")
        
        controller.BoundarySett.WheelDiameter = ctk.StringVar(None, str(controller.BoundarySett.WheelDiameter))
        self.W_diam_Entry = ctk.CTkEntry(self ,textvariable=controller.BoundarySett.WheelDiameter,width= 60, placeholder_text= '0.91')
        self.W_diam_Entry.grid(row=0  , column=3, padx=10, pady=(10, 0), sticky="nw")

        self.F_W_Axis_text = ctk.CTkLabel(self, text='Front wheel axis origin [m]')
        self.F_W_Axis_text.grid(row=1, column=0, padx=10, pady=(10, 10),columnspan= 2, sticky="w")
     
        self.F_W_X_Axis_text = ctk.CTkLabel(self, text='X')
        self.F_W_X_Axis_text.grid(row=2, column=0, padx=10, pady=(10, 10), sticky="")
        
        controller.BoundarySett.f_w_axis_x = ctk.StringVar(None, str(controller.BoundarySett.f_w_axis_x))
        self.F_W_X_Axis_Entry = ctk.CTkEntry(self ,textvariable=controller.BoundarySett.f_w_axis_x,width= 60, placeholder_text= '-1')
        self.F_W_X_Axis_Entry.grid(row=2  , column=1, padx=10, pady=(10, 0), sticky="w")   

        self.F_W_Y_Axis_text = ctk.CTkLabel(self, text='Y')
        self.F_W_Y_Axis_text.grid(row=3, column=0, padx=10, pady=(10, 10), sticky="")
        
        controller.BoundarySett.f_w_axis_y = ctk.StringVar(None, str(controller.BoundarySett.f_w_axis_y))
        self.F_W_Y_Axis_Entry = ctk.CTkEntry(self ,textvariable=controller.BoundarySett.f_w_axis_y,width= 60, placeholder_text= '0')
        self.F_W_Y_Axis_Entry.grid(row=3  , column=1, padx=10, pady=(10, 0), sticky="w")     
        
        self.F_W_Z_Axis_text = ctk.CTkLabel(self, text='Z')
        self.F_W_Z_Axis_text.grid(row=4, column=0, padx=10, pady=(10, 10), sticky="")
        
        controller.BoundarySett.f_w_axis_z = ctk.StringVar(None, str(controller.BoundarySett.f_w_axis_z))
        self.F_W_Z_Axis_Entry = ctk.CTkEntry(self ,textvariable=controller.BoundarySett.f_w_axis_z,width= 60, placeholder_text= '0.447')
        self.F_W_Z_Axis_Entry.grid(row=4  , column=1, padx=10, pady=(10, 0), sticky="w") 
        
        self.R_W_Axis_text = ctk.CTkLabel(self, text='Rear wheel axis origin [m]')
        self.R_W_Axis_text.grid(row=1, column=2, padx=10, pady=(10, 10),columnspan= 2, sticky="w")
     
        self.R_W_X_Axis_text = ctk.CTkLabel(self, text='X')
        self.R_W_X_Axis_text.grid(row=2, column=2, padx=10, pady=(10, 10), sticky="")
        
        controller.BoundarySett.r_w_axis_x = ctk.StringVar(None, str(controller.BoundarySett.r_w_axis_x))
        self.R_W_X_Axis_Entry = ctk.CTkEntry(self ,textvariable=controller.BoundarySett.r_w_axis_x,width= 60, placeholder_text= '-1')
        self.R_W_X_Axis_Entry.grid(row=2  , column=3, padx=10, pady=(10, 0), sticky="w")   

        self.R_W_Y_Axis_text = ctk.CTkLabel(self, text='Y')
        self.R_W_Y_Axis_text.grid(row=3, column=2, padx=10, pady=(10, 10), sticky="")
        
        controller.BoundarySett.r_w_axis_y = ctk.StringVar(None, str(controller.BoundarySett.r_w_axis_y))
        self.R_W_Y_Axis_Entry = ctk.CTkEntry(self ,textvariable=controller.BoundarySett.r_w_axis_y,width= 60, placeholder_text= '0')
        self.R_W_Y_Axis_Entry.grid(row=3  , column=3, padx=10, pady=(10, 0), sticky="w")     
        
        self.R_W_Z_Axis_text = ctk.CTkLabel(self, text='Z')
        self.R_W_Z_Axis_text.grid(row=4, column=2, padx=10, pady=(10, 10), sticky="")
        
        controller.BoundarySett.r_w_axis_z = ctk.StringVar(None, str(controller.BoundarySett.r_w_axis_z))
        self.R_W_Z_Axis_Entry = ctk.CTkEntry(self ,textvariable=controller.BoundarySett.r_w_axis_z,width= 60, placeholder_text= '0.447')
        self.R_W_Z_Axis_Entry.grid(row=4  , column=3, padx=10, pady=(10, 0), sticky="w") 

        self.Radiator_check_text = ctk.CTkLabel(self, text='Simulate radiators? ')
        self.Radiator_check_text.grid(row=5, column=0, padx=10, pady=(10, 10), sticky="")
                
        self.Radiator_Var_Check = ctk.IntVar(value=1)
        self.Radiator_Check_Box = ctk.CTkCheckBox(self, text="",variable=self.Radiator_Var_Check,onvalue=1, offvalue=0, command=self.Radiator_var_change)
        self.Radiator_Check_Box.grid(row=5  , column=1, padx=10, pady=(10, 0), sticky="w")

        self.Power_law_c_0_text = ctk.CTkLabel(self, text='Radiator C 0')
        self.Power_law_c_0_text.grid(row=6, column=0, padx=10, pady=(10, 10), sticky="")
     
        controller.BoundarySett.power_law_c_0 = ctk.StringVar(None, str(controller.BoundarySett.power_law_c_0))
        self.Power_law_c_0_Entry = ctk.CTkEntry(self ,textvariable=controller.BoundarySett.power_law_c_0,width= 60, placeholder_text= '100')
        self.Power_law_c_0_Entry.grid(row=6  , column=1, padx=10, pady=(10, 0), sticky="w") 
        
        self.Power_law_c_1_text = ctk.CTkLabel(self, text='Radiator C 1')
        self.Power_law_c_1_text.grid(row=6, column=2, padx=10, pady=(10, 10), sticky="")
     
        controller.BoundarySett.power_law_c_1 = ctk.StringVar(None, str(controller.BoundarySett.power_law_c_1))
        self.Power_law_c_1_Entry = ctk.CTkEntry(self ,textvariable=controller.BoundarySett.power_law_c_1,width= 60, placeholder_text= '100')
        self.Power_law_c_1_Entry.grid(row=6  , column=3, padx=10, pady=(10, 0), sticky="w")

        self.Porosity_text = ctk.CTkLabel(self, text='Porosity')
        self.Porosity_text.grid(row=6, column=4, padx=10, pady=(10, 10), sticky="")
     
        controller.BoundarySett.porosity = ctk.StringVar(None, str(controller.BoundarySett.porosity))
        self.Porosity_Entry = ctk.CTkEntry(self ,textvariable=controller.BoundarySett.porosity,width= 60, placeholder_text= '100')
        self.Porosity_Entry.grid(row=6  , column=5, padx=10, pady=(10, 0), sticky="w")

        self.Fan_2D_check_text = ctk.CTkLabel(self, text='Simulate fan? ')
        self.Fan_2D_check_text.grid(row=7, column=0, padx=10, pady=(10, 10), sticky="")
                
        self.Fan_2D_Var_Check = ctk.IntVar(value=1)
        self.Fan_2D_Check_Box = ctk.CTkCheckBox(self, text="",variable=self.Fan_2D_Var_Check,onvalue=1, offvalue=0, command=self.Fan_2D_var_change)
        self.Fan_2D_Check_Box.grid(row=7  , column=1, padx=10, pady=(10, 0), sticky="w")

        self.Fan_2D_curve_text = ctk.CTkLabel(self, text='Fan curve .txt (max 50 points!)')
        self.Fan_2D_curve_text.grid(row=7, column=2, padx=10, pady=(10, 10), sticky="")
     
        self.Fan_2D_FileText =ctk.CTkTextbox(self, width= 370, height=15)
        self.Fan_2D_FileText.grid(row=7, column=3, padx=10, pady=(10, 10), sticky="nw", columnspan = 4)
        self.Fan_2D_FileText.insert('0.0', r'D:\work\scopefiles')

        self.Fan_2DButt = ctk.CTkButton(self,height=30,width= 100, text= 'Open...', command=self.browseFilesData)
        self.Fan_2DButt.grid(row=7, column=7 , padx=10, pady=(10, 10), sticky="nw")  
        self.Fan_2DButt.configure(state = 'enabled')
        self.Fan_2DButt.configure(fg_color = 'medium sea green')      
        
        


        #self.DataText = ctk.CTkLabel(self, text='Load .txt fan curve...')
        #self.DataText.grid(row=8, column=0, padx=10, pady=(10, 10), sticky="nw")
        
        #self.DataFileText =ctk.CTkTextbox(self, width= 370, height=15)
        #self.DataFileText.grid(row=8, column=1, padx=10, pady=(10, 10), sticky="nw", columnspan = 4)
        #self.DataFileText.insert('0.0', r'D:\work\scopefiles')
        
        #self.DataFileButt = ctk.CTkButton(self,height=30,width= 100, text= 'Open...', command=self.browseFilesData)
        #self.DataFileButt.grid(row=8, column=4 , padx=10, pady=(10, 10), sticky="nw") 
        
        
    def Radiator_var_change(self):
            print('Radiator Check State:') 
            print(self.Radiator_Var_Check.get())
            if self.Radiator_Var_Check.get() == 1:
                self.controller.BoundarySett.Radiator_check = True   
                print('Radiator Var State:')    
                print(self.controller.BoundarySett.Radiator_check)    
                
                self.Power_law_c_0_Entry.configure(state = 'normal')
                self.Power_law_c_0_Entry.configure(fg_color = 'gray24')
                self.Power_law_c_1_Entry.configure(state = 'normal')
                self.Power_law_c_1_Entry.configure(fg_color = 'gray24')
                self.Porosity_Entry.configure(state = 'normal')
                self.Porosity_Entry.configure(fg_color = 'gray24')
            else:
                self.controller.BoundarySett.Radiator_check = False
                print('Radiator Var State:')    
                print(self.controller.BoundarySett.Radiator_check)   
                self.Power_law_c_0_Entry.configure(state = 'disabled')
                self.Power_law_c_0_Entry.configure(fg_color = 'grey')
                self.Power_law_c_1_Entry.configure(state = 'disabled')
                self.Power_law_c_1_Entry.configure(fg_color = 'grey')
                self.Porosity_Entry.configure(state = 'disabled')
                self.Porosity_Entry.configure(fg_color = 'grey')

    def Fan_2D_var_change(self):
            print('Fan Check State:') 
            print(self.Fan_2D_Var_Check.get())
            if self.Fan_2D_Var_Check.get() == 1:
                self.controller.BoundarySett.Fan_2D_check = True   
                print('2D Fan Var State:')    
                print(self.controller.BoundarySett.Fan_2D_check)    
                
                self.Fan_2D_FileText.configure(state = 'normal')
                self.Fan_2D_FileText.configure(fg_color = 'gray24')
                self.Fan_2DButt.configure(state = 'normal')
                self.Fan_2DButt.configure(fg_color = 'medium sea green') 
            else:
                self.controller.BoundarySett.Fan_2D_check = False
                print('Fan Var State:')    
                print(self.controller.BoundarySett.Fan_2D_check)   

                self.Fan_2D_FileText.configure(state = 'disabled')
                self.Fan_2D_FileText.configure(fg_color = 'gray')
                self.Fan_2DButt.configure(state = 'disabled')
                self.Fan_2DButt.configure(fg_color = 'PaleGreen4')

    def browseFilesData(self):
        
        self.Fan_2D_filename = filedialog.askopenfilename(initialdir = self.Fan_2D_FileText.get('1.0'),
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.txt*"),
                                                       ("all files",
                                                        "*.*")))
             
        self.Fan_2D_FileText.delete('0.0', 'end')
        self.Fan_2D_FileText.insert('0.0', self.Fan_2D_filename)
        self.controller.BoundarySett.Fan_2D_curve_Path = self.Fan_2D_filename
        print(self.controller.BoundarySett.Fan_2D_curve_Path)

    
    
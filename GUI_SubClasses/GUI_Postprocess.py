import customtkinter as ctk
from tkinter import filedialog
from tkinter import ttk
from GUI_SubClasses.GUI_General import Setting
 
class PostprocessSett(Setting):
    '''
    Class containing posprocessing settings of exported data ad pictures.
    (Excell table, .AVZ scenes, contour cuts, etc.).
    '''
    def __init__(self):
        '''
        Assigns default values.
        '''
        self.Excell = True
        self.Excell_path = ''
        self.Iteration_averaging = 300
        self.Create_report_file = True
        self.Save_AVZ = True
        self.Start_coord_XY = -0.18
        self.Number_of_cuts_XY = 24
        self.End_coord_XY = 1.02
        self.Start_coord_XZ = 0.01
        self.Number_of_cuts_XZ = 20
        self.End_coord_XZ = 0.81
        self.Start_coord_YZ = -0.95
        self.Number_of_cuts_YZ = 67
        self.End_coord_YZ = 2.65
        self.Vel_Mag_cuts = True
        self.Vel_LIC_cuts = True
        self.Mean_Press_cuts = True
        self.Total_Press_cuts = True
        self.Vorticity_cuts = False
        
        
class Postprocessing(ctk.CTkFrame):
    '''
    ctk.CTkFrame class servicing the Postprocessing settings menu.
    '''
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        
        self.Excell_check_text = ctk.CTkLabel(self, text='Export forces to excel file? ')
        self.Excell_check_text.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="w")
                
        self.Excell_Var_Check = ctk.IntVar(value=controller.PostproSett.Excell)
        self.Excell_Check_Box = ctk.CTkCheckBox(self, text="",variable=self.Excell_Var_Check,onvalue=1, offvalue=0, command=self.Excell_var_change)
        self.Excell_Check_Box.grid(row=0  , column=1, padx=10, pady=(10, 10), sticky="w")
        
        self.Iteration_averaging_text = ctk.CTkLabel(self, text='Iteration averaging ')
        self.Iteration_averaging_text.grid(row=0, column=2, padx=10, pady=(10, 10), sticky="w")
        
        controller.PostproSett.Iteration_averaging = ctk.StringVar(None, str(controller.PostproSett.Iteration_averaging))
        self.Iteration_averaging_Entry = ctk.CTkEntry(self ,textvariable=controller.PostproSett.Iteration_averaging,width= 60, placeholder_text= '100')
        self.Iteration_averaging_Entry.grid(row=0  , column=3, padx=10, pady=(10, 10), sticky="w") 
        
        self.Report_check_text = ctk.CTkLabel(self, text='Create report file? ')
        self.Report_check_text.grid(row=1, column=0, padx=10, pady=(10, 10), sticky="w")
                
        self.Report_Var_Check = ctk.IntVar(value=controller.PostproSett.Create_report_file)
        self.Report_Check_Box = ctk.CTkCheckBox(self, text="",variable=self.Report_Var_Check,onvalue=1, offvalue=0, command=self.Report_var_change)
        self.Report_Check_Box.grid(row=1  , column=1, padx=10, pady=(10, 10), sticky="w")
        
        self.AVZ_check_text = ctk.CTkLabel(self, text='Create AVZ files?')
        self.AVZ_check_text.grid(row=1, column=2, padx=10, pady=(10, 10), sticky="w")
                
        self.AVZ_Var_Check = ctk.IntVar(value=controller.PostproSett.Save_AVZ)
        self.AVZ_Check_Box = ctk.CTkCheckBox(self, text="",variable=self.AVZ_Var_Check,onvalue=1, offvalue=0, command=self.AVZ_var_change)
        self.AVZ_Check_Box.grid(row=1  , column=3, padx=10, pady=(10, 10), sticky="w")
        
        self.Cut_plane_text = ctk.CTkLabel(self, text='Cut plane settings')
        self.Cut_plane_text.grid(row=2, column=0, padx=10, pady=(10, 10), sticky="w")
        
        self.XY_plane_text = ctk.CTkLabel(self, text='XY')
        self.XY_plane_text.grid(row=2, column=1, padx=10, pady=(10, 10), sticky="")
        
        self.XZ_plane_text = ctk.CTkLabel(self, text='XZ')
        self.XZ_plane_text.grid(row=2, column=2, padx=10, pady=(10, 10), sticky="")
        
        self.YZ_plane_text = ctk.CTkLabel(self, text='YZ')
        self.YZ_plane_text.grid(row=2, column=3, padx=10, pady=(10, 10), sticky="")
        
        self.Start_plane_text = ctk.CTkLabel(self, text='Starting coordinate [m]:')
        self.Start_plane_text.grid(row=3, column=0, padx=30, pady=(10, 10), sticky="w")
        
        controller.PostproSett.Start_coord_XY = ctk.StringVar(None, str(controller.PostproSett.Start_coord_XY))
        self.XY_plane_start_Entry = ctk.CTkEntry(self ,textvariable=controller.PostproSett.Start_coord_XY,width= 60, placeholder_text= '100')
        self.XY_plane_start_Entry.grid(row=3  , column=1, padx=10, pady=(10, 10), sticky="") 
        
        controller.PostproSett.Start_coord_XZ = ctk.StringVar(None, str(controller.PostproSett.Start_coord_XZ))
        self.XZ_plane_start_Entry = ctk.CTkEntry(self ,textvariable=controller.PostproSett.Start_coord_XZ,width= 60, placeholder_text= '100')
        self.XZ_plane_start_Entry.grid(row=3  , column=2, padx=10, pady=(10, 10), sticky="") 
        
        controller.PostproSett.Start_coord_YZ = ctk.StringVar(None, str(controller.PostproSett.Start_coord_YZ))
        self.YZ_plane_start_Entry = ctk.CTkEntry(self ,textvariable=controller.PostproSett.Start_coord_YZ,width= 60, placeholder_text= '100')
        self.YZ_plane_start_Entry.grid(row=3  , column=3, padx=10, pady=(10, 10), sticky="") 
        
        self.End_plane_text = ctk.CTkLabel(self, text='End coordinate [m]:')
        self.End_plane_text.grid(row=4, column=0, padx=30, pady=(10, 10), sticky="w")
        
        controller.PostproSett.End_coord_XY = ctk.StringVar(None, str(controller.PostproSett.End_coord_XY))
        self.XY_plane_end_Entry = ctk.CTkEntry(self ,textvariable=controller.PostproSett.End_coord_XY,width= 60, placeholder_text= '100')
        self.XY_plane_end_Entry.grid(row=4  , column=1, padx=10, pady=(10, 10), sticky="") 
        
        controller.PostproSett.End_coord_XZ = ctk.StringVar(None, str(controller.PostproSett.End_coord_XZ))
        self.XZ_plane_end_Entry = ctk.CTkEntry(self ,textvariable=controller.PostproSett.End_coord_XZ,width= 60, placeholder_text= '100')
        self.XZ_plane_end_Entry.grid(row=4  , column=2, padx=10, pady=(10, 10), sticky="") 
        
        controller.PostproSett.End_coord_YZ = ctk.StringVar(None, str(controller.PostproSett.End_coord_YZ))
        self.YZ_plane_end_Entry = ctk.CTkEntry(self ,textvariable=controller.PostproSett.End_coord_YZ,width= 60, placeholder_text= '100')
        self.YZ_plane_end_Entry.grid(row=4  , column=3, padx=10, pady=(10, 10), sticky="") 
        
        self.Number_cut_text = ctk.CTkLabel(self, text='Number of cuts:')
        self.Number_cut_text.grid(row=5, column=0, padx=30, pady=(10, 10), sticky="w")
        
        controller.PostproSett.Number_of_cuts_XY = ctk.StringVar(None, str(controller.PostproSett.Number_of_cuts_XY))
        self.XY_plane_number_Entry = ctk.CTkEntry(self ,textvariable=controller.PostproSett.Number_of_cuts_XY,width= 60, placeholder_text= '100')
        self.XY_plane_number_Entry.grid(row=5  , column=1, padx=10, pady=(10, 10), sticky="") 
        
        controller.PostproSett.Number_of_cuts_XZ = ctk.StringVar(None, str(controller.PostproSett.Number_of_cuts_XZ))
        self.XZ_plane_number_Entry = ctk.CTkEntry(self ,textvariable=controller.PostproSett.Number_of_cuts_XZ,width= 60, placeholder_text= '100')
        self.XZ_plane_number_Entry.grid(row=5  , column=2, padx=10, pady=(10, 10), sticky="") 
        
        controller.PostproSett.Number_of_cuts_YZ = ctk.StringVar(None, str(controller.PostproSett.Number_of_cuts_YZ))
        self.YZ_plane_number_Entry = ctk.CTkEntry(self ,textvariable=controller.PostproSett.Number_of_cuts_YZ,width= 60, placeholder_text= '100')
        self.YZ_plane_number_Entry.grid(row=5  , column=3, padx=10, pady=(10, 10), sticky="") 
        
        '''
        Check Buttons for chooosing which contours are to be included in generated cut planes
        '''
        
        '''
        Velocity magnitude contours
        '''
        self.VelMag_check_text = ctk.CTkLabel(self, text='Velocity Magnitude cuts:')
        self.VelMag_check_text.grid(row=6, column=0, padx=30, pady=(10, 10), sticky="w")
                
        self.VelMag_Var_Check = ctk.IntVar(value=controller.PostproSett.Vel_Mag_cuts)
        self.VelMag_Check_Box = ctk.CTkCheckBox(self, text="",variable=self.VelMag_Var_Check,onvalue=1, offvalue=0, command=self.VelMag_var_change)
        self.VelMag_Check_Box.grid(row=6  , column=1, padx=10, pady=(10, 10), sticky="")
        
        '''
        Veocity Line Integral Convolitions
        '''
        self.VelLIC_check_text = ctk.CTkLabel(self, text='Velocity LIC cuts:')
        self.VelLIC_check_text.grid(row=6, column=2, padx=10, pady=(10, 10), sticky="w")
                
        self.VelLIC_Var_Check = ctk.IntVar(value=controller.PostproSett.Vel_LIC_cuts)
        self.VelLIC_Check_Box = ctk.CTkCheckBox(self, text="",variable=self.VelLIC_Var_Check,onvalue=1, offvalue=0, command=self.VelLIC_var_change)
        self.VelLIC_Check_Box.grid(row=6  , column=3, padx=10, pady=(10, 10), sticky="")
        
        '''
        Mean Pressure contours
        '''
        self.MeanPress_check_text = ctk.CTkLabel(self, text='Mean Static Pressure cuts:')
        self.MeanPress_check_text.grid(row=7, column=0, padx=30, pady=(10, 10), sticky="w")
                
        self.MeanPress_Var_Check = ctk.IntVar(value=controller.PostproSett.Mean_Press_cuts)
        self.MeanPress_Check_Box = ctk.CTkCheckBox(self, text="",variable=self.MeanPress_Var_Check,onvalue=1, offvalue=0, command=self.MeanPress_var_change)
        self.MeanPress_Check_Box.grid(row=7  , column=1, padx=10, pady=(10, 10), sticky="")
        
        '''
        Total Pressure contours
        '''
        self.TotPress_check_text = ctk.CTkLabel(self, text='Total Pressure cuts:')
        self.TotPress_check_text.grid(row=7, column=2, padx=10, pady=(10, 10), sticky="w")
                
        self.TotPress_Var_Check = ctk.IntVar(value=controller.PostproSett.Total_Press_cuts)
        self.TotPress_Check_Box = ctk.CTkCheckBox(self, text="",variable=self.TotPress_Var_Check,onvalue=1, offvalue=0, command=self.TotPress_var_change)
        self.TotPress_Check_Box.grid(row=7  , column=3, padx=10, pady=(10, 10), sticky="")
        
        '''
        Vorticity contours
        '''
        self.Vorticity_check_text = ctk.CTkLabel(self, text='Vorticity cuts:')
        self.Vorticity_check_text.grid(row=8, column=0, padx=30, pady=(10, 10), sticky="w")
                
        self.Vorticity_Var_Check = ctk.IntVar(value=controller.PostproSett.Vorticity_cuts)
        self.Vorticity_Check_Box = ctk.CTkCheckBox(self, text="",variable=self.Vorticity_Var_Check,onvalue=1, offvalue=0, command=self.Vorticity_var_change)
        self.Vorticity_Check_Box.grid(row=8  , column=1, padx=10, pady=(10, 10), sticky="")
        
    def Excell_var_change(self):
            '''
            Enable or disable Excell data file generation.
            '''
            print('Excell Check State:') 
            print(self.Excell_Var_Check.get())
            if self.Excell_Var_Check.get() == 1:
                self.controller.PostproSett.Excell = True   
                print('Excell State:')    
                print(self.controller.PostproSett.Excell)    
                
                self.Iteration_averaging_Entry.configure(state = 'normal')
                self.Iteration_averaging_Entry.configure(fg_color = 'gray24')
                
            else:
                self.controller.PostproSett.Excell = False
                print('Excell Var State:')    
                print(self.controller.PostproSett.Excell)   
                self.Iteration_averaging_Entry.configure(state = 'disabled')
                self.Iteration_averaging_Entry.configure(fg_color = 'grey')
                
    def Report_var_change(self):
            '''
            Enable or disable report file generation.
            '''
            print('Report Check State:') 
            print(self.Report_Var_Check.get())
            if self.Report_Var_Check.get() == 1:
                self.controller.PostproSett.Create_report_file = True   
                print('Report State:')    
                print(self.controller.PostproSett.Create_report_file)    

            else:
                self.controller.PostproSett.Create_report_file = False   
                print('Report State:')    
                print(self.controller.PostproSett.Create_report_file)    
                
                
    def AVZ_var_change(self):
            '''
            Enable or disable .AVZ scene file generation.
            '''
            print('AVZ Check State:') 
            print(self.AVZ_Var_Check.get())
            if self.AVZ_Var_Check.get() == 1:
                self.controller.PostproSett.Save_AVZ = True   
                print('AVZ State:')    
                print(self.controller.PostproSett.Save_AVZ)    

            else:
                self.controller.PostproSett.Save_AVZ = False   
                print('AVZ State:')    
                print(self.controller.PostproSett.Save_AVZ)    
                
    def VelMag_var_change(self):
            '''
            Enable or disable velocity magnitude contour cuts generation.
            '''
            print('VelMag Check State:') 
            print(self.VelMag_Var_Check.get())
            if self.VelMag_Var_Check.get() == 1:
                self.controller.PostproSett.Vel_Mag_cuts = True   
                print('VelMag State:')    
                print(self.controller.PostproSett.Vel_Mag_cuts)    

            else:
                self.controller.PostproSett.Vel_Mag_cuts = False   
                print('VelMag State:')    
                print(self.controller.PostproSett.Vel_Mag_cuts)    
                
    def VelLIC_var_change(self):
            '''
            Enable or disable velocity Line Integral Convolution cuts generation.
            '''
            print('VelLIC Check State:') 
            print(self.VelLIC_Var_Check.get())
            if self.VelLIC_Var_Check.get() == 1:
                self.controller.PostproSett.Vel_LIC_cuts = True   
                print('VelLIC State:')    
                print(self.controller.PostproSett.Vel_LIC_cuts)    

            else:
                self.controller.PostproSett.Vel_LIC_cuts = False   
                print('VelLIC State:')    
                print(self.controller.PostproSett.Vel_LIC_cuts)    
                
    def MeanPress_var_change(self):
            '''
            Enable or disable mean pressure contour cuts generation.
            '''
            print('Mean Pressure Check State:') 
            print(self.MeanPress_Var_Check.get())
            if self.MeanPress_Var_Check.get() == 1:
                self.controller.PostproSett.Mean_Press_cuts = True   
                print('Mean_Press State:')    
                print(self.controller.PostproSett.Mean_Press_cuts)    

            else:
                self.controller.PostproSett.Mean_Press_cuts = False   
                print('Mean_Press State:')    
                print(self.controller.PostproSett.Mean_Press_cuts)    
                
                
    def TotPress_var_change(self):
            '''
            Enable or disable total pressure contour cuts generation.
            '''
            print('Total Pressure Check State:') 
            print(self.TotPress_Var_Check.get())
            if self.TotPress_Var_Check.get() == 1:
                self.controller.PostproSett.Total_Press_cuts = True   
                print('Total_Press State:')    
                print(self.controller.PostproSett.Total_Press_cuts)    

            else:
                self.controller.PostproSett.Total_Press_cuts = False   
                print('Total_Press State:')    
                print(self.controller.PostproSett.Total_Press_cuts)  
                
    def Vorticity_var_change(self):
            '''
            Enable or disable vorticity contour cuts generation.
            '''
            print('Vorticity Check State:') 
            print(self.Vorticity_Var_Check.get())
            if self.Vorticity_Var_Check.get() == 1:
                self.controller.PostproSett.Vorticity_cuts = True   
                print('Vorticity State:')    
                print(self.controller.PostproSett.Vorticity_cuts)    

            else:
                self.controller.PostproSett.Vorticity_cuts = False   
                print('Vorticity State:')    
                print(self.controller.PostproSett.Vorticity_cuts)      
import tkinter
import customtkinter as ctk
from tkinter import filedialog
from GUI_SubClasses.GUI_General import Setting
from PIL import Image
import os

class ParametrizationSett(Setting):
    '''
    Class containing parametrization settings of yaw, roll and ride height.
    '''
    def __init__(self):
        '''
        Assigns default values.
        '''
        self.FrontRHCount = 35   
        self.RearRHCount = 35
        self.RollAngleCount = 0
        self.YawAngleCount = 0
        self.RollPivotCount = -121
        self.YawPivotCount = 1200

        self.Pitch_check = False
        self.Roll_check = False
        self.Yaw_check = False
        
        
class Parameters(ctk.CTkFrame):
    '''
    ctk.CTkFrame class servicing the Parametrization settings menu.
    '''
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        self.controller = controller
        self.PitchText = ctk.CTkLabel(self, text='Pitch')
        self.PitchText.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="nw")

        self.Pitch_Var_Check = ctk.IntVar(value=0)
        self.Pitch_Check_Box = ctk.CTkCheckBox(self, text="",variable=self.Pitch_Var_Check,onvalue=1, offvalue=0, command=self.Pitch_var_change)
        self.Pitch_Check_Box.grid(row=0  , column=1, padx=10, pady=(10, 0), sticky="w")

        self.FrontRHText = ctk.CTkLabel(self, text='Front RH (mm)')
        self.FrontRHText.grid(row=0, column=2, padx=10, pady=(10, 10), sticky="nw")

        self.controller.ParametersSett.FrontRHCount = ctk.StringVar(None, str(self.controller.ParametersSett.FrontRHCount))
        self.FrontRHEntry = ctk.CTkEntry(self ,textvariable=self.controller.ParametersSett.FrontRHCount,width= 100, placeholder_text= '4')
        self.FrontRHEntry.grid(row=0, column=3, padx=10, pady=(10, 0), sticky="w")
        self.FrontRHEntry.configure(state = 'disabled')
        self.FrontRHEntry.configure(fg_color = 'grey')

        self.RearRHText = ctk.CTkLabel(self, text='Rear RH (mm)')
        self.RearRHText.grid(row=0, column=4, padx=10, pady=(10, 10), sticky="nw")

        self.controller.ParametersSett.RearRHCount = ctk.StringVar(None, str(self.controller.ParametersSett.RearRHCount))
        self.RearRHEntry = ctk.CTkEntry(self ,textvariable=self.controller.ParametersSett.RearRHCount,width= 100, placeholder_text= '4')
        self.RearRHEntry.grid(row=0, column=5, padx=10, pady=(10, 0), sticky="w")
        self.RearRHEntry.configure(state = 'disabled')
        self.RearRHEntry.configure(fg_color = 'grey')


        self.RollText = ctk.CTkLabel(self, text='Roll')
        self.RollText.grid(row=1, column=0, padx=10, pady=(10, 10), sticky="nw")

        self.Roll_Var_Check = ctk.IntVar(value=0)
        self.Roll_Check_Box = ctk.CTkCheckBox(self, text="",variable=self.Roll_Var_Check,onvalue=1, offvalue=0, command=self.Roll_var_change)
        self.Roll_Check_Box.grid(row=1  , column=1, padx=10, pady=(10, 0), sticky="w")

        self.RollAngleText = ctk.CTkLabel(self, text='Angle (°)')
        self.RollAngleText.grid(row=1, column=2, padx=10, pady=(10, 10), sticky="nw")

        self.controller.ParametersSett.RollAngleCount = ctk.StringVar(None, str(self.controller.ParametersSett.RollAngleCount))
        self.RollAngleEntry = ctk.CTkEntry(self ,textvariable=self.controller.ParametersSett.RollAngleCount,width= 100, placeholder_text= '4')
        self.RollAngleEntry.grid(row=1, column=3, padx=10, pady=(10, 0), sticky="w")
        self.RollAngleEntry.configure(state = 'disabled')
        self.RollAngleEntry.configure(fg_color = 'grey')

        self.RollPivotText = ctk.CTkLabel(self, text='Pivot Z (mm)')
        self.RollPivotText.grid(row=1, column=4, padx=10, pady=(10, 10), sticky="nw")

        self.controller.ParametersSett.RollPivotCount = ctk.StringVar(None, str(self.controller.ParametersSett.RollPivotCount))
        self.RollPivotEntry = ctk.CTkEntry(self ,textvariable=self.controller.ParametersSett.RollPivotCount,width= 100, placeholder_text= '4')
        self.RollPivotEntry.grid(row=1, column=5, padx=10, pady=(10, 0), sticky="w")
        self.RollPivotEntry.configure(state = 'disabled')
        self.RollPivotEntry.configure(fg_color = 'grey')

        self.YawText = ctk.CTkLabel(self, text='Yaw')
        self.YawText.grid(row=2, column=0, padx=10, pady=(10, 10), sticky="nw")

        self.Yaw_Var_Check = ctk.IntVar(value=0)
        self.Yaw_Check_Box = ctk.CTkCheckBox(self, text="",variable=self.Yaw_Var_Check,onvalue=1, offvalue=0, command=self.Yaw_var_change)
        self.Yaw_Check_Box.grid(row=2  , column=1, padx=10, pady=(10, 0), sticky="w")

        self.YawAngleText = ctk.CTkLabel(self, text='Angle (°)')
        self.YawAngleText.grid(row=2, column=2, padx=10, pady=(10, 10), sticky="nw")
        
        self.controller.ParametersSett.YawAngleCount = ctk.StringVar(None, str(self.controller.ParametersSett.YawAngleCount))
        self.YawAngleEntry = ctk.CTkEntry(self ,textvariable=self.controller.ParametersSett.YawAngleCount,width= 100, placeholder_text= '4')
        self.YawAngleEntry.grid(row=2, column=3, padx=10, pady=(10, 0), sticky="w")
        self.YawAngleEntry.configure(state = 'disabled')
        self.YawAngleEntry.configure(fg_color = 'grey')

        self.YawPivotText = ctk.CTkLabel(self, text='Pivot X (mm)')
        self.YawPivotText.grid(row=2, column=4, padx=10, pady=(10, 10), sticky="nw")

        self.controller.ParametersSett.YawPivotCount = ctk.StringVar(None, str(self.controller.ParametersSett.YawPivotCount))
        self.YawPivotEntry = ctk.CTkEntry(self ,textvariable=self.controller.ParametersSett.YawPivotCount,width= 100, placeholder_text= '4')
        self.YawPivotEntry.grid(row=2, column=5, padx=10, pady=(10, 0), sticky="w")
        self.YawPivotEntry.configure(state = 'disabled')
        self.YawPivotEntry.configure(fg_color = 'grey')

        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, "Moment_X.png")
        image = Image.open(image_path)
        resized_image = image.resize((300, 210))
        ctk_image = ctk.CTkImage(light_image=resized_image, dark_image=resized_image, size=(300, 210))
        image_label = ctk.CTkLabel(self, image=ctk_image, text="")  # text="" hides label text
        image_label.image = ctk_image  # prevents garbage collection
        image_label.grid(row=3, column=0, columnspan=6, padx=10, pady=(20, 10), sticky="w")

        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, "Moment_Z.png")
        image = Image.open(image_path)
        resized_image = image.resize((350, 210))
        ctk_image = ctk.CTkImage(light_image=resized_image, dark_image=resized_image, size=(350, 210))
        image_label = ctk.CTkLabel(self, image=ctk_image, text="")  # text="" hides label text
        image_label.image = ctk_image  # prevents garbage collection
        image_label.grid(row=3, column=4, columnspan=6, padx=10, pady=(20, 10), sticky="w")
        





    def Pitch_var_change(self):
            '''
            Enable or disable pitch parametrization.
            '''
            print('Pitch Check State:') 
            print(self.Pitch_Var_Check.get())
            if self.Pitch_Var_Check.get() == 1:
                self.controller.ParametersSett.Pitch_check = True   
                print('Pitch Var State:')    
                print(self.controller.ParametersSett.Pitch_check)    
                
                self.FrontRHEntry.configure(state = 'normal')
                self.FrontRHEntry.configure(fg_color = 'gray24')
                self.RearRHEntry.configure(state = 'normal')
                self.RearRHEntry.configure(fg_color = 'gray24')
            else:
                self.controller.ParametersSett.Pitch_check = False
                print('Pitch Var State:')    
                print(self.controller.ParametersSett.Pitch_check)   
                self.FrontRHEntry.configure(state = 'disabled')
                self.FrontRHEntry.configure(fg_color = 'grey')
                self.RearRHEntry.configure(state = 'disabled')
                self.RearRHEntry.configure(fg_color = 'grey')

    def Roll_var_change(self):  
            '''
            Enable or disable roll parametrization.
            '''
            print('Roll Check State:') 
            print(self.Roll_Var_Check.get())
            if self.Roll_Var_Check.get() == 1:
                self.controller.ParametersSett.Roll_check = True   
                print('Roll Var State:')    
                print(self.controller.ParametersSett.Roll_check)    
                
                self.RollAngleEntry.configure(state = 'normal')
                self.RollAngleEntry.configure(fg_color = 'gray24')
                self.RollPivotEntry.configure(state = 'normal')
                self.RollPivotEntry.configure(fg_color = 'gray24')
            else:
                self.controller.ParametersSett.Roll_check = False
                print('Roll Var State:')    
                print(self.controller.ParametersSett.Roll_check)   
                self.RollAngleEntry.configure(state = 'disabled')
                self.RollAngleEntry.configure(fg_color = 'grey')
                self.RollPivotEntry.configure(state = 'disabled')
                self.RollPivotEntry.configure(fg_color = 'grey')

    def Yaw_var_change(self):
            '''
            Enable or disable Yaw parametrization.
            '''
            print('Yaw Check State:') 
            print(self.Yaw_Var_Check.get())
            if self.Yaw_Var_Check.get() == 1:
                self.controller.ParametersSett.Yaw_check = True   
                print('Yaw Var State:')    
                print(self.controller.ParametersSett.Yaw_check)    
                
                self.YawAngleEntry.configure(state = 'normal')
                self.YawAngleEntry.configure(fg_color = 'gray24')
                self.YawPivotEntry.configure(state = 'normal')
                self.YawPivotEntry.configure(fg_color = 'gray24')
            else:
                self.controller.ParametersSett.Yaw_check = False
                print('Yaw Var State:')    
                print(self.controller.ParametersSett.Yaw_check)   
                self.YawAngleEntry.configure(state = 'disabled')
                self.YawAngleEntry.configure(fg_color = 'grey')
                self.YawPivotEntry.configure(state = 'disabled')
                self.YawPivotEntry.configure(fg_color = 'grey')
     





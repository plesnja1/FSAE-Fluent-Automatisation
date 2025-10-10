
import customtkinter as ctk
from tkinter import filedialog
from tkinter import ttk
from GUI_SubClasses.GUI_General import Setting

class TunnelSett(Setting):
    '''
    Class containing settings regarding size, cell size of tunnel and wrap settings.
    '''
    def __init__(self):
        '''
        Default tunnel data initialisation.
        '''
        self.y_max = 5000   
        self.y_min = 0
        self.z_max = 5800
        self.z_min = -200
        self.x_max = 20500
        self.x_min = -4500
        self.Cell_size = 320
        self.Wrap_ratio = 0.5
        self.turn_check = False
        self.radius = 12
        self.angle = 90
        self.width = 10000

class Tunnel(ctk.CTkFrame):
    '''
    ctk.CTkFrame class servicing the Tunnel settings menu.
    '''
    def __init__(self, parent, controller):
        '''
        Frame initialisation and features placement.
        '''
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.Turn_Check_Var = ctk.CTkLabel(self, text='Simulate turn?')
        self.Turn_Check_Var.grid(row=0, column=4, padx=10, pady=(10, 10), sticky="nw")
        
        self.Turn_Check_Var = ctk.IntVar(value=0)
        self.Turn_Check_Box = ctk.CTkCheckBox(self, text="",variable=self.Turn_Check_Var,onvalue=1, offvalue=0, command=self.Turn_Switch)
        self.Turn_Check_Box.grid(row=0  , column=5, padx=10, pady=(10, 0), sticky="w")
        
        
        self.X_MaxText = ctk.CTkLabel(self, text='Max X Coordinate [mm]')
        self.X_MaxText.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="nw")
        
        controller.TunnelObject.x_max = ctk.StringVar(None, str(controller.TunnelObject.x_max))
        self.X_MaxEntry = ctk.CTkEntry(self ,textvariable=controller.TunnelObject.x_max,width= 60, placeholder_text= '4')
        self.X_MaxEntry.grid(row=0  , column=1, padx=10, pady=(10, 0), sticky="w")
        
        self.X_MinText = ctk.CTkLabel(self, text='Min X Coordinate [mm]')
        self.X_MinText.grid(row=0, column=2, padx=10, pady=(10, 10), sticky="nw")
        
        controller.TunnelObject.x_min = ctk.StringVar(None, str(controller.TunnelObject.x_min))
        self.X_MinEntry = ctk.CTkEntry(self ,textvariable=controller.TunnelObject.x_min,width= 60, placeholder_text= '4')
        self.X_MinEntry.grid(row=0, column=3, padx=10, pady=(10, 0), sticky="w")
        
        self.Y_MaxText = ctk.CTkLabel(self, text='Max Y Coordinate [mm]')
        self.Y_MaxText.grid(row=1, column=0, padx=10, pady=(10, 10), sticky="nw")
        
        controller.TunnelObject.y_max = ctk.StringVar(None, str(controller.TunnelObject.y_max))
        self.Y_MaxEntry = ctk.CTkEntry(self ,textvariable=controller.TunnelObject.y_max,width= 60, placeholder_text= '4')
        self.Y_MaxEntry.grid(row=1, column=1, padx=10, pady=(10, 0), sticky="w")
        
        self.Y_MinText = ctk.CTkLabel(self, text='Min Y Coordinate [mm]')
        self.Y_MinText.grid(row=1, column=2, padx=10, pady=(10, 10), sticky="nw")
        
        controller.TunnelObject.y_min = ctk.StringVar(None, str(controller.TunnelObject.y_min))
        self.Y_MinEntry = ctk.CTkEntry(self ,textvariable=controller.TunnelObject.y_min,width= 60, placeholder_text= '4')
        self.Y_MinEntry.grid(row=1, column=3, padx=10, pady=(10, 0), sticky="w")
        
        self.Z_MaxText = ctk.CTkLabel(self, text='Max Z Coordinate [mm]')
        self.Z_MaxText.grid(row=2, column=0, padx=10, pady=(10, 10), sticky="nw")
        
        controller.TunnelObject.z_max = ctk.StringVar(None, str(controller.TunnelObject.z_max))
        self.Z_MaxEntry = ctk.CTkEntry(self ,textvariable=controller.TunnelObject.z_max,width= 60, placeholder_text= '4')
        self.Z_MaxEntry.grid(row=2, column=1, padx=10, pady=(10, 0), sticky="w")
        
        self.Z_MinText = ctk.CTkLabel(self, text='Min Z Coordinate [mm]')
        self.Z_MinText.grid(row=2, column=2, padx=10, pady=(10, 10), sticky="nw")
        
        controller.TunnelObject.z_min = ctk.StringVar(None, str(controller.TunnelObject.z_min))
        self.Z_MinEntry = ctk.CTkEntry(self ,textvariable=controller.TunnelObject.z_min,width= 60, placeholder_text= '4')
        self.Z_MinEntry.grid(row=2, column=3, padx=10, pady=(10, 0), sticky="w")
        
        self.CellSizeText = ctk.CTkLabel(self, text='Tunnel Surface Cell Size [mm]')
        self.CellSizeText.grid(row=3, column=0, padx=10, pady=(10, 10), sticky="nw")
        
        controller.TunnelObject.Cell_size = ctk.StringVar(None, str(controller.TunnelObject.Cell_size))
        self.CellSizeEntry = ctk.CTkEntry(self ,textvariable=controller.TunnelObject.Cell_size,width= 60, placeholder_text= '4')
        self.CellSizeEntry.grid(row=3, column=1, padx=10, pady=(10, 0), sticky="w")
        
        self.WrapRatioText = ctk.CTkLabel(self, text='Resolution Factor [mm]')
        self.WrapRatioText.grid(row=3, column=2, padx=10, pady=(10, 10), sticky="nw")
        
        controller.TunnelObject.Wrap_ratio = ctk.StringVar(None, str(controller.TunnelObject.Wrap_ratio))
        self.WrapRatioEntry = ctk.CTkEntry(self ,textvariable=controller.TunnelObject.Wrap_ratio,width= 60, placeholder_text= '4')
        self.WrapRatioEntry.grid(row=3, column=3, padx=10, pady=(10, 0), sticky="w")
        
        
        
        
        
        self.Radius_Text = ctk.CTkLabel(self, text='Turn radius [m]')
        self.Radius_Text.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="nw")
        self.Radius_Text.grid_forget()
        
        controller.TunnelObject.radius = ctk.StringVar(None, str(controller.TunnelObject.radius))
        self.Radius_Entry = ctk.CTkEntry(self ,textvariable=controller.TunnelObject.radius,width= 60, placeholder_text= '12')
        self.Radius_Entry.grid(row=0  , column=1, padx=10, pady=(10, 0), sticky="w")
        self.Radius_Entry.grid_forget()
        
        self.AngleText = ctk.CTkLabel(self, text='Turn angle [deg]')
        self.AngleText.grid(row=0, column=2, padx=10, pady=(10, 10), sticky="nw")
        self.AngleText.grid_forget()
        
        controller.TunnelObject.angle = ctk.StringVar(None, str(controller.TunnelObject.angle))
        self.Angle_Entry = ctk.CTkEntry(self ,textvariable=controller.TunnelObject.angle,width= 60, placeholder_text= '90')
        self.Angle_Entry.grid(row=0, column=3, padx=10, pady=(10, 0), sticky="w")
        self.Angle_Entry.grid_forget()
        
        self.Width_Text = ctk.CTkLabel(self, text='Tunnel Width [mm]')
        self.Width_Text.grid(row=1, column=0, padx=10, pady=(10, 10), sticky="nw")
        self.Width_Text.grid_forget()
        
        controller.TunnelObject.width = ctk.StringVar(None, str(controller.TunnelObject.width))
        self.Width_Entry = ctk.CTkEntry(self ,textvariable=controller.TunnelObject.width,width= 60, placeholder_text= '10000')
        self.Width_Entry.grid(row=1, column=1, padx=10, pady=(10, 0), sticky="w")
        self.Width_Entry.grid_forget()
        
        
        
    def Turn_Switch(self):
        if self.Turn_Check_Var.get() == 1:
            self.controller.TunnelObject.turn_check = True
            
            self.X_MaxText.grid_forget()
            self.X_MaxEntry.grid_forget()
            self.X_MinEntry.grid_forget()
            self.X_MinText.grid_forget()
            self.Y_MaxText.grid_forget()
            self.Y_MaxEntry.grid_forget()
            self.Y_MinEntry.grid_forget()
            self.Y_MinText.grid_forget()
            
            self.Radius_Entry.grid(row=0  , column=1, padx=10, pady=(10, 0), sticky="w")
            self.Radius_Text.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="nw")
            self.Angle_Entry.grid(row=0, column=3, padx=10, pady=(10, 0), sticky="w")
            self.AngleText.grid(row=0, column=2, padx=10, pady=(10, 10), sticky="nw")
            self.Width_Text.grid(row=1, column=0, padx=10, pady=(10, 10), sticky="nw")
            self.Width_Entry.grid(row=1, column=1, padx=10, pady=(10, 0), sticky="w")
        
        else:
            self.controller.TunnelObject.turn_check = False
            
            self.Radius_Entry.grid_forget()
            self.Radius_Text.grid_forget()
            self.Angle_Entry.grid_forget()
            self.AngleText.grid_forget()
            self.Width_Text.grid_forget()
            self.Width_Entry.grid_forget()
            
            self.X_MaxText.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="nw")
            self.X_MaxEntry.grid(row=0  , column=1, padx=10, pady=(10, 0), sticky="w")
            self.X_MinEntry.grid(row=0, column=3, padx=10, pady=(10, 0), sticky="w")
            self.X_MinText.grid(row=0, column=2, padx=10, pady=(10, 10), sticky="nw")
            self.Y_MaxText.grid(row=1, column=0, padx=10, pady=(10, 10), sticky="nw")
            self.Y_MaxEntry.grid(row=1  , column=1, padx=10, pady=(10, 0), sticky="w")
            self.Y_MinEntry.grid(row=1, column=3, padx=10, pady=(10, 0), sticky="w")
            self.Y_MinText.grid(row=1, column=2, padx=10, pady=(10, 10), sticky="nw")
    
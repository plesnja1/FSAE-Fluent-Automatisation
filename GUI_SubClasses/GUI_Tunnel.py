
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

class Tunnel(ctk.CTkFrame):
    '''
    ctk.CTkFrame class servicing the Tunnel settings menu.
    '''
    def __init__(self, parent, controller):
        '''
        Frame initialisation and features placement.
        '''
        ctk.CTkFrame.__init__(self, parent)
        
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
    
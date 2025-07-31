import MeshObjects
import customtkinter as ctk
from tkinter import filedialog
from tkinter import ttk


class Prisms(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        
        self.treeview = ttk.Treeview(self, height= 20)
        self.treeview.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="w", rowspan= 9)
        self.treeview.bind("<Button-1>", self.OnClickTree)
        
        
                
        self.writeButt = ctk.CTkButton(self, height=30,width= 100, text= 'Write...', command=self.writeScopeSizeFile )
        self.writeButt.grid(row=8, column=1, padx=10, pady=(10, 10), sticky="nw")
    
    def LoadTree(self):
        self.treeview.delete(*self.treeview.get_children())
        for obj in self.controller.MeshObjList['vehicle']:
            if obj.Name == 'vehicle':
                self.treeview.insert(parent=obj.Parent, index=obj.MSH_ID,iid=str(obj.Name) , text= obj.Name, values=[obj.MSH_ID])
            else:
                self.treeview.insert(parent=obj.Parent, index=obj.MSH_ID,iid= (obj.Parent+ '-' + str(obj.Name)) , text= obj.Name, values=[obj.MSH_ID])
        
    def OnClickTree(self, event):
        print(event)
        
        self.item = self.treeview.identify('item',event.x,event.y)
        if int(self.treeview.item(self.item,"values")[0])-1 == -1:
            tree_id = 0
        else:
            tree_id = int(self.treeview.item(self.item,"values")[0])
        print(tree_id)
        self.obj = self.controller.MeshObjList['vehicle'][tree_id]
        print(self.obj.Name)
        
        self.ScopeToText = ctk.CTkLabel(self, text='Prism type...')
        self.ScopeToText.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="nw")

        self.ScopeToOption = ctk.CTkComboBox(self,height=32 ,width=130,  values=['uniform', 'aspect-ratio', 'last-ratio'],)# command= self.disableCurvProx)
        self.ScopeToOption['state'] = 'readonly'
        self.ScopeToOption.set(self.obj.Boundary_Type)
        self.ScopeToOption.grid(row=1, column=2, padx=10, pady=(0, 10), sticky="nw")
        
        
        self.GrowthText = ctk.CTkLabel(self, text='Growth rate')
        self.GrowthText.grid(row=1, column=3, padx=10, pady=(0, 10), sticky="nw")
        
        self.GrowthBox = ctk.CTkTextbox(self, width=50, height= 20, )
        self.GrowthBox.insert('0.0', str(self.obj.Pism_Growth_Rate))
        self.GrowthBox.grid(row=1, column=4, padx=10, pady=(0, 10), sticky="nw")

        self.UniformText = ctk.CTkLabel(self, text='First layer height')
        self.UniformText.grid(row=2, column=1, padx=10, pady=(0, 10), sticky="nw")
        
        self.UniformBox = ctk.CTkTextbox(self, width=50, height= 20, )
        self.UniformBox.insert('0.0', str(self.obj.First_Aspect_Ratio))
        self.UniformBox.grid(row=2, column=2, padx=10, pady=(0, 10), sticky="nw")
        
        self.AspectText = ctk.CTkLabel(self, text='First aspect ratio')
        self.AspectText.grid(row=2, column=3, padx=10, pady=(0, 10), sticky="nw")
        
        self.AspectBox = ctk.CTkTextbox(self, width=50, height= 20, )
        self.AspectBox.insert('0.0', str(self.obj.First_Aspect_Ratio))
        self.AspectBox.grid(row=2, column=4, padx=10, pady=(0, 10), sticky="nw")
        
        self.LayerNumText = ctk.CTkLabel(self, text='Number of layers')
        self.LayerNumText.grid(row=3, column=1, padx=10, pady=(0, 10), sticky="nw")
        
        self.LayerNumBox = ctk.CTkTextbox(self, width=50, height= 20, )
        self.LayerNumBox.insert('0.0', str(self.obj.Number_Of_Layers))
        self.LayerNumBox.grid(row=3, column=2, padx=10, pady=(0, 10), sticky="nw")
        
        self.updateScopeSize = ctk.CTkButton(self,height=30,width= 100, text= 'Update', command=self.updatePrisms )
        self.updateScopeSize.grid(row=8, column=3, padx=10, pady=(10, 10), sticky="nw")
        
        if self.ScopeToOption.get() == 'uniform':
            self.UniformBox.configure(state = 'normal')
            self.UniformBox.configure(fg_color = 'gray24')
            self.AspectBox.configure(state = 'disabled')
            self.AspectBox.configure(fg_color = 'grey')
        else:
            self.UniformBox.configure(state = 'disabled')
            self.UniformBox.configure(fg_color = 'grey')
            self.AspectBox.configure(state = 'normal')
            self.AspectBox.configure(fg_color = 'gray24')

            
    def writeScopeSizeFile(self):
            self.writeFilename = filedialog.asksaveasfilename(initialdir = self.controller.WorkDirText.get('1.0'),
                                          title = "Select a File",
                                          filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')],
                                          defaultextension='.txt'
            )
            print(self.controller.MeshObjList)
            MeshObjects.WriteObjToFile(self.controller.MeshObjList, self.writeFilename)
            print(self.writeFilename)
            
    def updatePrisms(self):
        self.controller.MeshObjList['vehicle'][self.obj.MSH_ID].Pism_Growth_Rate = float(self.GrowthBox.get('1.0', "end"))
        self.controller.MeshObjList['vehicle'][self.obj.MSH_ID].Boundary_Type = self.ScopeToOption.get()
        self.controller.MeshObjList['vehicle'][self.obj.MSH_ID].Number_Of_Layers = float(self.LayerNumBox.get('1.0', "end"))
        if self.ScopeToOption.get() == 'uniform':
            self.controller.MeshObjList['vehicle'][self.obj.MSH_ID].First_Aspect_Ratio = float(self.UniformBox.get('1.0', "end"))
        else:
            self.controller.MeshObjList['vehicle'][self.obj.MSH_ID].First_Aspect_Ratio = float(self.AspectBox.get('1.0', "end"))
        print(vars(self.controller.MeshObjList['vehicle'][self.obj.MSH_ID]))
  
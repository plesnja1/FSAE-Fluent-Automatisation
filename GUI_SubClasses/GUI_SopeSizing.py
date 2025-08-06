import Support_scripts.MeshObjects as MeshObjects
import customtkinter as ctk
from tkinter import filedialog
from tkinter import ttk



class ScopeSizing(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        
        self.treeview = ttk.Treeview(self, height= 20)
        self.treeview.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="w", rowspan= 9)
        self.treeview.bind("<Button-1>", self.OnClickTree)
        self.controller.MeshObjList = {'vehicle':[], 'BOI':[]} 
        self.vehObj  = MeshObjects.Vehicle('vehicle', 'vehicle')
        self.vehObj.MSH_ID = 0
        self.vehObj.Parent = ''
        self.controller.MeshObjList['vehicle'].append(self.vehObj)
        self.treeview.insert(parent=self.vehObj.Parent, index=self.vehObj.MSH_ID,iid=str(self.vehObj.Name) , text= self.vehObj.Name, values=[self.vehObj.MSH_ID])
        self.boiObj = MeshObjects.BOI('BOIs', 'BOI')
        self.boiObj.MSH_ID = 1000
        self.controller.MeshObjList['BOI'].append(self.boiObj)#
        self.treeview.insert(parent='', index=self.boiObj.MSH_ID,iid=str(self.boiObj.Name) , text= self.boiObj.Name, values=[self.boiObj.MSH_ID])

        
        self.scopeSizeFile =ctk.CTkTextbox(self, width= 370, height=15)
        self.scopeSizeFile.grid(row=0, column=1, padx=10, pady=(10, 10), sticky="nw", columnspan = 4)
        self.scopeSizeFile.insert('0.0', r'D:\work\scopefiles')
        
        self.scopeSizeFileButt = ctk.CTkButton(self,height=30,width= 100, text= 'Open...', command=self.browseFiles)
        self.scopeSizeFileButt.grid(row=0, column=5 , padx=10, pady=(10, 10), sticky="nw")

        self.writeButt = ctk.CTkButton(self, height=30,width= 100, text= 'Write...', command=self.writeScopeSizeFile )
        self.writeButt.grid(row=8, column=1, padx=10, pady=(10, 10), sticky="nw")
    
        
        
    def browseFiles(self):
        
        self.filename = filedialog.askopenfilename(initialdir = self.scopeSizeFile.get('1.0'),
                                          title = "Select a File",
                                          filetypes = (("JSON files",
                                                        "*.json*"),
                                                       ("Text files",
                                                        "*.txt*"),
                                                       ("all files",
                                                        "*.*")))     
        self.scopeSizeFile.delete('0.0', 'end')
        self.scopeSizeFile.insert('0.0', self.filename)
        self.controller.SFFile_Path = self.filename
        self.ReadScopeFile()
        
    def ReadScopeFile(self):
        self.treeview = ttk.Treeview(self, height= 20)
        self.treeview.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="w", rowspan= 9)
        self.treeview.bind("<Button-1>", self.OnClickTree)
        MeshObjects.MSH_Object._registry = []
        MeshObjects.BOI._BOIregistry = []
        MeshObjects.Vehicle._VEHregistry = []
        self.controller.MeshObjList = {'vehicle':[], 'BOI':[]} 
        #self.boiObj = MeshObjects.BOI('BOIs', 'BOI')
        #self.boiObj.MSH_ID = 1000
        #MSH_Obj_Dict = MeshObjects.ReadObjectList(self.filename)
        MSH_Obj_Dict = MeshObjects.ReadJsonObjList(self.filename)
        
        print(MSH_Obj_Dict)
        self.controller.MeshObjList['vehicle'].extend(MSH_Obj_Dict['vehicle'])
        #self.controller.MeshObjList['BOI'].append(self.boiObj)
        self.controller.MeshObjList['BOI'].extend(MSH_Obj_Dict['BOI'])
        
        print(self.controller.MeshObjList['BOI'][0].Name)
        
        for obj in self.controller.MeshObjList['vehicle']:
            if obj.Name == 'vehicle':
                self.treeview.insert(parent=obj.Parent, index=obj.MSH_ID,iid=str(obj.Name) , text= obj.Name, values=[obj.MSH_ID])
            else:
                self.treeview.insert(parent=obj.Parent, index=obj.MSH_ID,iid= (obj.Parent+ '-' + str(obj.Name)) , text= obj.Name, values=[obj.MSH_ID])
        
        for obj in self.controller.MeshObjList['BOI']:
            if obj.Name == 'BOIs':
                self.treeview.insert(parent='', index=obj.MSH_ID,iid=str(obj.Name) , text= obj.Name, values=[obj.MSH_ID])
            else:
                self.treeview.insert(parent='BOIs', index=obj.MSH_ID,iid= ('BOIs'+ '-' + str(obj.Name)) , text= obj.Name, values=[obj.MSH_ID])
        
                
    def OnClickTree(self, event):
        print(event)
        
        self.item = self.treeview.identify('item',event.x,event.y)
        if int(self.treeview.item(self.item,"values")[0])-1 == -1:
            tree_id = 0
        else:
            tree_id = int(self.treeview.item(self.item,"values")[0])
        
        print(tree_id)
        if tree_id < 1000:
            self.obj = self.controller.MeshObjList['vehicle'][tree_id]
        else:
            self.ProxBox.configure(state = 'disabled')
            self.CurvBox.configure(state = 'disabled')
            self.MinSizeBox.configure(state = 'disabled')
            self.obj = self.controller.MeshObjList['BOI'][tree_id-1000]
        print(self.obj.Name)
            
            
            
        self.scopeSizeFileButt.grid(row=0, column=4 , padx=10, pady=(10, 10), sticky="nw")

        self.NameText = ctk.CTkLabel(self, text='Name')
        self.NameText.grid(row=1, column=1, padx=10, pady=(10, 10), sticky="nw")

        self.NameBox = ctk.CTkTextbox(self, width=120, height= 20, )
        self.NameBox.insert('0.0', str(self.obj.Name))
        self.NameBox.grid(row=1, column=2, padx=10, pady=(10, 10), sticky="nw")

        self.IDText = ctk.CTkLabel(self, text='Obj ID')
        self.IDText.grid(row=1, column=3, padx=10, pady=(10, 10), sticky="nw")

        self.IdBox = ctk.CTkTextbox(self, width=50, height= 20, )
        self.IdBox.insert('0.0', str(tree_id))#self.obj.MSH_ID))
        self.IdBox.grid(row=1, column=4, padx=10, pady=(10, 10), sticky="nw")
        self.IdBox.configure(state = 'disabled')

        self.MaxSizeText = ctk.CTkLabel(self, text='Max. size')
        self.MaxSizeText.grid(row=2, column=1, padx=10, pady=(10, 10), sticky="nw")
        

        self.MaxSizeBox = ctk.CTkTextbox(self, width=50, height= 20, )
        self.MaxSizeBox.insert('0.0', str(self.obj.Max_Size))
        self.MaxSizeBox.grid(row=2, column=2, padx=10, pady=(10, 10), sticky="nw")
        
        self.GrowthText = ctk.CTkLabel(self, text='Growth rate')
        self.GrowthText.grid(row=3, column=1, padx=10, pady=(0, 10), sticky="nw")
        
        self.GrowthBox = ctk.CTkTextbox(self, width=50, height= 20, )
        self.GrowthBox.insert('0.0', str(self.obj.Growth_Rate))
        self.GrowthBox.grid(row=3, column=2, padx=10, pady=(0, 10), sticky="nw")
        
        

        
        if tree_id < 1000:
            self.MinSizeText = ctk.CTkLabel(self, text='Min. size')
            self.MinSizeText.grid(row=2, column=3, padx=10, pady=(10, 10), sticky="nw")
            
            self.MinSizeBox = ctk.CTkTextbox(self, width=50, height= 20, )
            self.MinSizeBox.insert('0.0', str(self.obj.Min_Size))
            self.MinSizeBox.grid(row=2, column=4, padx=10, pady=(10, 10), sticky="nw")
            
            

            
            self.SizeOpText = ctk.CTkLabel(self, text='Size control \n method')
            self.SizeOpText.grid(row=3, column=3, padx=10, pady=(0, 10), sticky="nw")

            self.SizeOption = ctk.CTkComboBox(self,height=32 ,width=100,  values=['Curvature and Proximity', 'Curvature', 'Proximity'], command= self.disableCurvProx)
            self.SizeOption.grid(row=3, column=4, padx=10, pady=(0, 10), sticky="nw")

            
            self.CurvText = ctk.CTkLabel(self, text='Curvature', )
            self.CurvText.grid(row=4, column=3, padx=10, pady=(0, 10), sticky="nw")
            
            self.CurvBox = ctk.CTkTextbox(self, width=50, height= 20,)
            self.CurvBox.insert('0.0', str(self.obj.Curvature))
            self.CurvBox.grid(row=4, column=4, padx=10, pady=(0, 10), sticky="nw")
            
            self.ProxText = ctk.CTkLabel(self, text='Cells per gap')
            self.ProxText.grid(row=4, column=1, padx=10, pady=(0, 10), sticky="nw")
        
            self.ProxBox = ctk.CTkTextbox(self, width=50, height= 20, )
            self.ProxBox.insert('0.0', str(self.obj.Cells_Per_Gap))
            self.ProxBox.grid(row=4, column=2, padx=10, pady=(0, 10), sticky="nw")
            
            self.ScopeToCurvText = ctk.CTkLabel(self, text='Curvature scope to...')
            self.ScopeToCurvText.grid(row=5, column=3, padx=10, pady=(0, 10), sticky="nw")

            self.ScopeToCurvOption = ctk.CTkComboBox(self,height=32 ,width=130,  values=['faces', 'edges', 'faces and edges'], command= self.disableCurvProx)
            self.ScopeToCurvOption.grid(row=5, column=4, padx=10, pady=(0, 10), sticky="nw")
            self.ScopeToCurvOption.set(self.obj.Scope_To_Curv)
        
            self.ScopeToProxText = ctk.CTkLabel(self, text='Proximity scope to...')
            self.ScopeToProxText.grid(row=5, column=1, padx=10, pady=(0, 10), sticky="nw")
            
            
            self.ScopeToProxOption = ctk.CTkComboBox(self,height=32 ,width=130,  values=['faces', 'edges', 'faces and edges'], command= self.disableCurvProx)
            self.ScopeToProxOption.grid(row=5, column=2, padx=10, pady=(0, 10), sticky="nw")
            self.ScopeToProxOption.set(self.obj.Scope_To_Prox)
            
        else:
            self.ScopeToText = ctk.CTkLabel(self, text='BOI scope to...')
            self.ScopeToText.grid(row=5, column=1, padx=10, pady=(0, 10), sticky="nw")

            self.ScopeToOption = ctk.CTkComboBox(self,height=32 ,width=130,  values=['faces', 'edges', 'faces and edges'], command= self.disableCurvProx)
            self.ScopeToOption.grid(row=5, column=2, padx=10, pady=(0, 10), sticky="nw")
        

        if tree_id < 1000:
            self.ProxBox.configure(state = 'normal')
            self.ProxBox.configure(fg_color = 'gray24')
            self.CurvBox.configure(state = 'normal')
            self.CurvBox.configure(fg_color = 'gray24')
            self.MinSizeBox.configure(state = 'normal')  
            self.MinSizeBox.configure(fg_color = 'gray24')
            self.SizeOption.configure(state = 'normal')      
            self.SizeOption.configure(fg_color = 'gray24')
            self.obj = self.controller.MeshObjList['vehicle'][tree_id]
        else:
            self.ProxBox.configure(state = 'disabled')
            self.ProxBox.configure(fg_color = 'grey')
            self.CurvBox.configure(state = 'disabled')
            self.CurvBox.configure(fg_color = 'grey')
            self.MinSizeBox.configure(state = 'disabled')
            self.MinSizeBox.configure(fg_color = 'grey')
            self.SizeOption.configure(state = 'disabled')      
            self.SizeOption.configure(fg_color = 'grey')
            self.obj = self.controller.MeshObjList['BOI'][tree_id-1000]
            
        self.updateScopeSize = ctk.CTkButton(self,height=30,width= 100, text= 'Update', command=self.updateValues )
        self.updateScopeSize.grid(row=8, column=3, padx=10, pady=(10, 10), sticky="nw")

        self.AddChildButt = ctk.CTkButton(self,height=30,width= 100, text= 'Add Child', command=self.addChildToTree )
        self.AddChildButt.grid(row=8, column=2, padx=10, pady=(10, 10), sticky="n")
        
    def updateValues(self):
        if self.obj.SF_class == 'vehicle':
            self.controller.MeshObjList['vehicle'][self.obj.MSH_ID].Name = self.NameBox.get('1.0', "end").replace('\n', '')
            self.controller.MeshObjList['vehicle'][self.obj.MSH_ID].Max_Size = int(float(self.MaxSizeBox.get('1.0', "end")))
            self.controller.MeshObjList['vehicle'][self.obj.MSH_ID].Min_Size = int(float(self.MinSizeBox.get('1.0', "end")))
            self.controller.MeshObjList['vehicle'][self.obj.MSH_ID].Growth_Rate = float(self.GrowthBox.get('1.0', "end"))
            self.controller.MeshObjList['vehicle'][self.obj.MSH_ID].Curvature = int(float(self.CurvBox.get('1.0', "end")))
            self.controller.MeshObjList['vehicle'][self.obj.MSH_ID].Cells_Per_Gap = int(float(self.CurvBox.get('1.0', "end")))
            self.controller.MeshObjList['vehicle'][self.obj.MSH_ID].Scope_To_Curv = self.ScopeToCurvOption.get()
            self.controller.MeshObjList['vehicle'][self.obj.MSH_ID].Scope_To_Prox = self.ScopeToProxOption.get()
            self.treeview.item(self.item, text=self.controller.MeshObjList['vehicle'][self.obj.MSH_ID].Name)
        
        elif self.obj.SF_class == 'BOI':
            self.controller.MeshObjList['BOI'][self.obj.MSH_ID-1000].Name = self.NameBox.get('1.0', "end").replace('\n', '')
            self.controller.MeshObjList['BOI'][self.obj.MSH_ID-1000].Max_Size = int(float(self.MaxSizeBox.get('1.0', "end")))
            self.controller.MeshObjList['BOI'][self.obj.MSH_ID-1000].Growth_Rate = float(self.GrowthBox.get('1.0', "end"))
            self.controller.MeshObjList['BOI'][self.obj.MSH_ID-1000].Scope_To = self.ScopeToOption.get()
            self.treeview.item(self.item, text=self.controller.MeshObjList['BOI'][self.obj.MSH_ID-1000].Name)
        
        print('values updated')
        
        
    def disableCurvProx(self,  select):
        print(select)
        print(self)

        if select == 'Curvature':
            self.ProxBox.configure(state = 'disabled')
            self.ProxBox.configure(fg_color = 'grey')
            self.CurvBox.configure(state = 'normal')
            self.CurvBox.configure(fg_color = 'gray24')
            self.ScopeToProxOption.configure(state = 'disabled')
            self.ScopeToProxOption.configure(fg_color = 'grey')
            self.ScopeToCurvOption.configure(state = 'normal')
            self.ScopeToCurvOption.configure(fg_color = 'gray24')
            print('Prox disabled')
        elif select == 'Proximity':
            self.CurvBox.configure(state = 'disabled')
            self.CurvBox.configure(fg_color = 'grey')
            self.ProxBox.configure(fg_color = 'gray24')
            self.ProxBox.configure(state = 'normal')
            self.ScopeToCurvOption.configure(state = 'disabled')
            self.ScopeToCurvOption.configure(fg_color = 'grey')
            self.ScopeToProxOption.configure(fg_color = 'gray24')
            self.ScopeToProxOption.configure(state = 'normal')
            print('Curv disabled')
        else:
            self.CurvBox.configure(state = 'normal')
            self.CurvBox.configure(fg_color = 'gray24')
            self.ProxBox.configure(state = 'normal')
            self.ProxBox.configure(fg_color = 'gray24')
            self.ScopeToCurvOption.configure(state = 'normal')
            self.ScopeToCurvOption.configure(fg_color = 'gray24')
            self.ScopeToProxOption.configure(state = 'normal')
            self.ScopeToProxOption.configure(fg_color = 'gray24')
            print('All enabled')
        
    def writeScopeSizeFile(self):
            self.writeFilename = filedialog.asksaveasfilename(initialdir = self.controller.WorkDirText.get('1.0'),
                                          title = "Select a File",
                                          filetypes=[('JSON Files', '*.json'),('Text Files', '*.txt'), ('All Files', '*.*')],
                                          defaultextension='.json'
            )
            print(self.controller.MeshObjList)
            #MeshObjects.WriteObjToFile(self.controller.MeshObjList, self.writeFilename)
            print('Muj debilni pokus \n')
            MeshObjects.WriteScopeToJson(self.controller.MeshObjList, self.writeFilename)
            #print(self.writeFilename)
    
    def addChildToTree(self):
        print(self.obj.SF_class)
        if self.obj.SF_class == 'vehicle':
            newObj = MeshObjects.Vehicle(self.NameBox.get('1.0', "end").replace('\n', ''), 'vehicle')
        elif self.obj.SF_class == 'BOI':
            if self.obj.MSH_ID != 1000:
                return None
            newObj = MeshObjects.BOI(self.NameBox.get('1.0', "end").replace('\n', ''), 'BOI')
            
        newObj.Max_Size = int(float(self.MaxSizeBox.get('1.0', "end")))
        newObj.Growth_Rate = float(self.GrowthBox.get('1.0', "end"))
        
        
        if self.obj.SF_class == 'vehicle':
            newObj.Parent = str(self.obj.Parent)+'-'+self.obj.Name
            newObj.Min_Size = int(float(self.MinSizeBox.get('1.0', "end")))
            newObj.Curvature = int(float(self.CurvBox.get('1.0', "end")))
            newObj.Cells_Per_Gap = int(float(self.CurvBox.get('1.0', "end")))
            newObj.Scope_To_Curv = self.ScopeToCurvOption.get()
            newObj.Scope_To_Prox = self.ScopeToProxOption.get()
        else:
            newObj.Scope_To = self.ScopeToOption.get()#

        
        print(vars(newObj))
        if self.obj.SF_class == 'vehicle':
            self.controller.MeshObjList['vehicle'].append(newObj)
            self.treeview.insert(parent=newObj.Parent, index=newObj.MSH_ID,iid= (newObj.Parent+ '-' + str(newObj.Name)) , text= newObj.Name, values=[newObj.MSH_ID])
        elif self.obj.SF_class == 'BOI':
            self.controller.MeshObjList['BOI'].append(newObj)
            self.treeview.insert(parent='BOIs', index=newObj.MSH_ID,iid= ('BOIs'+ '-' + str(newObj.Name)) , text= newObj.Name, values=[newObj.MSH_ID])
        print(self.controller.MeshObjList['BOI'])


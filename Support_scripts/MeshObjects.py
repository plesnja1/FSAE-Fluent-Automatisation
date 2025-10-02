import ansys.fluent.core as pyfluent
import json
'''
Library for reading, creating and manipulating objects containing information about scoped sizing and 
prism layer creation. 
date: 30.07.2024
version update: added BOIs writing, updating and child adding
v:0.06
author:Jan Plesnik
contact: plesnik.honza@seznam.cz 
'''

        

        
class MSH_Object:
    '''
    Main class for scope sizing objects.
    All objects used for meshing are MSH_Object
    MSH_Object contains functions for finding parents of objects
    and parts belonging to given object 
    '''
    _registry = [] #class registry for iterating through all objects in a class
    MSH_ID = 0
    def __init__(self, name, SF_class):
        self.SF_class = SF_class
        self.Name = name
        self._registry.append(self)
        self.MSH_ID = self._findID()
        
    #finction iterates through all active Meshing Objects and finds smallest avaiable ID
    def _findID(self):
        '''
        Function iterates through all active Meshing Objects and finds smallest avaiable ID
        
        :return: int
        '''
        curr_id = 0
        if self.SF_class == 'vehicle':
            print('vehicle true')
            print(Vehicle._registry)
            for i in Vehicle._VEHregistry: #iterating through objects in class
                if i.MSH_ID > curr_id:
                    curr_id = i.MSH_ID
                else: curr_id += 1
                
        elif self.SF_class == 'BOI':
            print('boi true')
            curr_id = 1000
            for i in BOI._BOIregistry: #iterating through objects in class
                if i.MSH_ID > curr_id:
                    curr_id = i.MSH_ID
                else: curr_id += 1
        print(curr_id)
        return curr_id
    
    def _findParents(self, Obj_list):
        '''
        Method for finding object parents based on their immediate parent
        !!!WARNING!!! - this method is obsolete as it was used for manually set Scope 
        Sizing file. This method can cope badly with same named Size Field objects as 
        is correct parrent
        '''
        Parent_tree = [self.Name, self.Parent]  #start branch of the parent tree
        check = 1
        b = self
        print('Finding parents')
        if self.Parent == 'vehicle': #check first parent is final parent
            return Parent_tree  #return list of all parents
        else:
            while check == 1:   #while loop until all parents are found
                print ('self object is ' + self.Name)
                for a in Obj_list:  #loop through all MSH_Objects
                    print('Current object ' + a.Name)
                    if a.Name == b.Parent:  #Check if current object is previus objects parent
                        Parent_tree.append(a.Parent)    #if so append to a list
                        print('Parent appended ' + a.Parent)
                        b = a    #start finding parent for current object              
                    if a.Parent == 'vehicle':
                        print('Parents found')
                        print('Returning parents')
                        return Parent_tree  #return list of all parents
            print('Returning parents')
            return Parent_tree
        
        
        
    def _findParentsNew(self):
        '''
        Newer method for finding parents where whole parent tree is already
        provided from Scope Sizing file as it is assumed that the file is automatically
        generated from user GUI and therefore can store more information without 
        being too anoying for user to manipulate with
        
        This function simply reads string af all object parents and creates
        a list of parents from that string.
        
        :returns: list[string]
        '''
        parent_list =[]
        start =0
        while True:
            next = self.Parent.find('-',start+1)    #find a dash from current position and assign position of a new dash
            if next == -1:       #check if there is any other dash in string
                parent_list.append(self.Parent[start::])    #append last parent from the list
                
                return parent_list  #return a list of all parents
            parent_list.append(self.Parent[start:next]) #append a parent located between previous and next dash
            start = next+1
        
            
    def _findParts(self, Obj_list, Part_list):
        '''
        Method for finding all parts containing the name
        
        :return: list[MSH_Object]
        '''    #
        '''
        if Obj_list[0].SF_class == 'vehicle':   
            parent_tree = self._findParentsNew()
        elif Obj_list[0].SF_class == 'BOI':
            parent_tree = ['bois', self.Name]
        print(parent_tree)
        parent_tree.append(self.Name)
        parent_tree.reverse()
        #parent_tree.pop(0)
        select_parts = []
        for parent in parent_tree:
            for part in Part_list:
                if part.find(parent+'-')!=-1 or part.find('-'+parent)!= -1:
                    select_parts.append(part)
            Part_list = select_parts
        '''
        select_parts = []
        if Obj_list[0].SF_class == 'vehicle' and self.Name != 'vehicle': 
            for part in Part_list:
                if part.find(self.Parent + '-' + self.Name) != -1:
                    select_parts.append(part)
        if Obj_list[0].SF_class == 'vehicle' and self.Name == 'vehicle': 
            for part in Part_list:
                if part.find(self.Name) != -1:
                    select_parts.append(part)
        elif Obj_list[0].SF_class == 'BOI':
            for part in Part_list:
                if part.find('bois-' + self.Name) != -1:
                    select_parts.append(part)
            
        print('Parts found')
        print(select_parts)
        return select_parts    
    
class BOI(MSH_Object):
    '''
    Mesh object subclass describing Body Of Influence objects. This class contains information abou scoped sizing for BOIs 
    '''
    _BOIregistry = []
    def __init__(self, name, SF_class):
        super().__init__(name, SF_class)
        self.Max_Size = 0
        self.Growth_Rate = 0
        self.Scope_To = 'objects'
        self._BOIregistry.append(self)
        
    def _ValueRead(self,LineList,  LinePointer):
        '''
        Iterates through all object attributes (except methods)
        and assigns values from the object text file to the empty
        values. Function takes as input whole list of object 
        properties (LineList) and pointer (int) to the line placement 
        of beggining of current object
        '''
        LineAttPointer = 1
        
        for x in vars(self).keys(): #iterating through all dictionary keys
            if ((x != 'Name') and (x!= 'SF_class') and (x!= 'MSH_ID')) : #excepting non zero values
                Line = LineList[LinePointer+LineAttPointer] 
                vars(self)[x] = Line[Line.find(':')+2:-1] #assigning object attributes from the list
                LineAttPointer+=1
        print(vars(self))
    
    def _ValueReadJson(self, Boi_dir):
        '''
        Reads values from a .json file
        '''
        for var in vars(self).keys():
            if ((var != 'Name') and (var!= 'SF_class') and (var!= 'MSH_ID')):
                vars(self)[var] = Boi_dir[var]
            
class Vehicle(MSH_Object):
    '''
    Class defining vehicle objects. Those are objects that are directly 
    parts of the vehicle (chassis, aero, suspension etc.).
    A such this class stores their atributes containing info 
    about these parts size fields and prisms as well as methods for their 
    initialisation.
    '''
    _VEHregistry = []
    
    def __init__(self, name, SF_class):
        super().__init__(name, SF_class)
        self.Parent = ''
        self.Min_Size = 1
        self.Max_Size = 100
        self.Growth_Rate = 1.2
        self.Curvature = 30
        self.Cells_Per_Gap = 1
        self.Scope_To_Curv = 'faces'
        self.Boundary_Type = 'aspect-ratio'
        self.Number_Of_Layers = 2
        self.First_Aspect_Ratio = 10
        self.Pism_Growth_Rate = 1.2
        self.Ignore_self = True
        self.Scope_To_Prox = 'faces'
        self._VEHregistry.append(self)
        
    def _ValueRead(self,LineList,  LinePointer):
        '''
        Iterates through all object attributes (except methods)
        and assigns values from the object text file to the empty
        values. Function takes as input whole list of object 
        properties (LineList) and pointer (int) to the line placement 
        of beggining of current object
        '''
        LineAttPointer = 1
        print(vars(self))
        for x in vars(self).keys(): #iterating through all dictionary keys
            if ((x != 'Name') and (x!= 'SF_class') and (x!= 'MSH_ID')) : #excepting non zero values
                Line = LineList[LinePointer+LineAttPointer] 
                vars(self)[x] = Line[Line.find(':')+2:-1] #assigning object attributes from the list
                LineAttPointer+=1
 
        self.ParentList = self._findParentsNew()
    
    def _ValueReadJson(self, Vehicle_dir):
        '''
        Reads values from a .json file
        '''
        for var in vars(self).keys():
            if ((var != 'Name') and (var!= 'SF_class') and (var!= 'MSH_ID')):
                vars(self)[var] = Vehicle_dir[var]
        
def ReadObjectList(SF_File_Path):
    '''
    Function responsible for reading a .txt file with size field data
    and writing these data into a responsible mesh objects
    Returns a list of all mesh objects
    '''
    MSH_Obj_List = {'vehicle':[], 'BOI':[]} #list of all mesh objects
    LineIterator = 0 #pointer to a current line in text file

    with open(SF_File_Path, 'r') as fr: #open text file in read mode
        lines = fr.readlines() 
        for line in lines:
            if line.find('*') != -1: #finding a object in a text file
                if line.find('vehicle') != -1: #finding a 'vehicle' type of object
                    #adding a new 'vehicle' object to the list
                    MSH_Obj_List['vehicle'].append(Vehicle(line[line.find('*')+1:line.find(' -')], line[line.find(' -')+3:-1]))
                    #reading a values from the text file into the creted object
                    MSH_Obj_List['vehicle'][len(MSH_Obj_List['vehicle'])-1]._ValueRead(lines, LineIterator)
                elif line.find('BOI') != -1:
                    print('Boi found')
                    MSH_Obj_List['BOI'].append(BOI(line[line.find('*')+1:line.find(' -')], line[line.find(' -')+3:-1]))
                    MSH_Obj_List['BOI'][len(MSH_Obj_List['BOI'])-1]._ValueRead(lines, LineIterator)
                    
                    
            LineIterator += 1
    return MSH_Obj_List

def ReadJsonObjList(SF_File_Path):
    '''
    Read data from .json list and initialise them as Mesh Objects
    
    :returns: dict[list[MSH_Objects]]
    '''
    MSH_Obj_List = {'vehicle':[], 'BOI':[]} #list of all mesh objects
    with open(SF_File_Path, mode = 'r', encoding= 'utf-8') as read_file:
        scope_data = json.load(read_file)
    for vehic in scope_data['vehicle']:
        MSH_Obj_List['vehicle'].append(Vehicle(vehic['Name'], vehic['SF_class']))
        MSH_Obj_List['vehicle'][-1]._ValueReadJson(vehic)
    for boi in scope_data['BOI']:
        MSH_Obj_List['BOI'].append(BOI(boi['Name'], boi['SF_class']))
        MSH_Obj_List['BOI'][-1]._ValueReadJson(boi)
    return MSH_Obj_List
    

def MakeBoundaryLayerDict(Obj_list, Part_list, Zone_list):
    '''
    Obsolete
    '''
    Bound_dict = {'rest':Part_list}
    
    for obj in Obj_list:
        Bound_dict[obj.Name] = obj._findParts(Obj_list, Part_list) 

    a=1
    print(Bound_dict)
    print('\n')


    Dict_keys = list(Bound_dict.keys())
    while a != 0:
        a=0
        for i in range(len(Bound_dict.keys())-1):
            if len(Bound_dict[Dict_keys[i]])>len(Bound_dict[Dict_keys[i+1]]):
                a+=1
                mid_key = Dict_keys[i]
                Dict_keys[i] = Dict_keys[i+1]
                Dict_keys[i+1] = mid_key
                
    Bound_dict['keys'] = Dict_keys

    for a in Bound_dict['keys']:
        for b in Bound_dict[a]:
            for c in Bound_dict['keys']:
                if c != a and b in Bound_dict[c]:
                    Bound_dict[c].remove(b)

    for MSH_Obj in Bound_dict['keys']:
        for i in range(len(Bound_dict[MSH_Obj])):
            part = str(Bound_dict[MSH_Obj][i])
            for zone in Zone_list:
                if zone.find(part) != -1:
                    Bound_dict[MSH_Obj][i] = zone

    ''' 
    for MSH_Obj in Bound_dict['keys']:
        for i in range(len(Bound_dict[MSH_Obj])):
            part = str(Bound_dict[MSH_Obj][i])
            end = part.rfind('-')
            start = part.rfind('-', 0, end)
            if Bound_dict[MSH_Obj][i][start+1:end] == 'geometry':
                start = part.rfind('-', 0, start)
            Bound_dict[MSH_Obj][i] = Bound_dict[MSH_Obj][i][start+1:end]+':'+Bound_dict[MSH_Obj][i]
    '''
    print(Bound_dict['keys'])
    for key in Bound_dict['keys']:
        print('\n key: \n' + key + '\n\n\n\n')
        print(Bound_dict[key])
        for Part in Bound_dict[key]:
            print(Part)
            if Part.find(':') < 0 and Part.find('tunnel') != -1:
                print('\n\n FOUND NO : !!!!! \n\n')
                Bound_dict[key].remove(Part)
    return Bound_dict

def MakeBoundaryLayerDict2(Obj_list, Part_list, Zone_list):
    '''
    Assigns correct prism settings to individual parts so no prism settings share the same part (due to the mesh setting inheritance)
    
    :return: dict
    '''
    Bound_dict = {'rest':Part_list}
    
    for MSH_obj in Obj_list:
        Bound_dict[MSH_obj.Name] = MSH_obj._findParts(Obj_list, Part_list)
        
    for key in Bound_dict.keys():
        for part in Bound_dict[key]:
            if part.find(':') ==-1:
                Bound_dict[key].remove(part)
                
    for MSH_obj in Obj_list:
        Parent_list = MSH_obj._findParentsNew()
        for Parent in Parent_list:
            for part in Bound_dict[MSH_obj.Name]:
                if Parent != '' and part in Bound_dict[Parent]:
                    Bound_dict[Parent].remove(part)
        for part in Bound_dict[MSH_obj.Name]:
            if part in Bound_dict['rest']:
                Bound_dict['rest'].remove(part)
            
    for key in Bound_dict.keys():
        for part_index in range(len(Bound_dict[key])):
            for zone in Zone_list:
                nameStart = zone.find(':')+1
                nameEnd = zone.find(':', nameStart+1)
                '''
                if part  == zone[nameStart:nameEnd] and part in Bound_dict[key]: 
                    Bound_dict[key] = list(map(lambda x: x.replace(part, zone), Bound_dict[key]))
                '''
                if Bound_dict[key][part_index]  == zone[nameStart:nameEnd] and Bound_dict[key][part_index] in Bound_dict[key]:
                    Bound_dict[key][part_index] = zone
                
    for key in Bound_dict.keys():
        for part in Bound_dict[key]:
            if part.find(':') == -1:
                Bound_dict[key].remove(part)
                
    return Bound_dict
        
def MakePrismWildcard(Self, Obj_list):
    included_obj_list = []
    for obj in Obj_list:
        if  (obj.Parent.find(Self.Parent) != -1 or obj.Parent == '') and obj.Parent.find(Self.Name) != -1:
            included_obj_list.append(obj)
    if Self.Name == 'vehicle':
        wildacard_string = '*'+Self.Name+'*'
    else:
        wildacard_string = '*'+Self.Parent+'-'+Self.Name+'*'
    
    for obj in included_obj_list:
        wildacard_string = wildacard_string +'&^*'+obj.Parent+'-' +obj.Name+'*'
    
    return wildacard_string
          
def WriteObjToFile(Obj_list, FilePath):
    'Only for legacy scope files. Surpassed by WriteScopeToJson() function'
    with open(FilePath, 'w') as fw:
        for obj in Obj_list['vehicle']:
            fw.write('*'+obj.Name+' - '+obj.SF_class+'\n')
            fw.write('    -Parent: '+obj.Parent+'\n')
            fw.write('    -Min_Size: '+str(obj.Min_Size)+'\n')
            fw.write('    -Max_Size: '+str(obj.Max_Size)+'\n')
            fw.write('    -Growth_Rate: '+str(obj.Growth_Rate)+'\n')
            fw.write('    -Curvature: '+str(obj.Curvature)+'\n')
            fw.write('    -Cells_Per_Gap: '+str(obj.Cells_Per_Gap)+'\n')
            fw.write('    -Scope_To_Curv: '+str(obj.Scope_To_Curv)+'\n')
            fw.write('    -Boudary_Type: '+str(obj.Boundary_Type)+'\n')
            fw.write('    -Number_Of_Layers: '+str(obj.Number_Of_Layers)+'\n')
            fw.write('    -First_Aspect_Ratio: '+str(obj.First_Aspect_Ratio)+'\n')
            fw.write('    -Prism_Growth_Rate: '+str(obj.Pism_Growth_Rate)+'\n')
            fw.write('    -Ignore_self: '+str(obj.Ignore_self)+'\n')
            fw.write('    -Scope_To_Prox: '+str(obj.Scope_To_Prox)+'\n')
            fw.write('\n')
        for obj in Obj_list['BOI'][1::]:
            fw.write('*'+obj.Name+' - '+obj.SF_class+'\n')
            fw.write('    -Max_Size: '+str(obj.Max_Size)+'\n')
            fw.write('    -Growth_Rate: '+str(obj.Growth_Rate)+'\n')
            fw.write('    -Scope_To: '+str(obj.Scope_To)+'\n')
            fw.write('\n')
            
def WriteScopeToJson(Obj_list, file_path):
    '''
    Writes given mesh object settings list into a provided .json file
    '''
    with open(file_path, mode = 'w', encoding= 'utf-8') as write_file:
        Obj_dict = {'vehicle':[], 'BOI':[]}
        for Obj in Obj_list['vehicle']:
            Obj_dict['vehicle'].append(vars(Obj))
        for Obj in Obj_list['BOI']:
            Obj_dict['BOI'].append(vars(Obj))
                
        json.dump(Obj_dict, write_file , indent=2)        

                

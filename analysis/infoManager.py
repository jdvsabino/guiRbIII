import sys
sys.path.append('../network')
import os
from analysis.picManager import PictureManager, AbsorptionPicture, Camera
import matplotlib.image as mpimg
import matplotlib.pyplot as plt # For teting purposes
import copy
import scipy as sio
import numpy as np
from network.data_collection import Data_Collection
from network.data_collection import data_collector as dc
from network.data_collection import PIC_SRC
from analysis.function_vars import *


class InfoManager():
    """
    Deals with the current information from adwin.
    This class is aimed to store and process all 
    the information needed to get the new pictures, 
    update variable values, store the new information 
    and make it available in the future.   

    Attributes
    ----------
    dc : DataCollector
        Local DataCollector
    abs_pic : AbsorptionPicture
        Absoprtion picture to be displayed to the user
    atom_pic : Picture
        Picture with atoms to be displayed to the user
    no_atom_pic : Picture
        Picture with no atoms to be displayed to the user
    background_pic : Picture
        Background picture to be displayed to the user
    cycle_num : 
    global_cycle_num : 
    scan_num :
    atom_num :
    variables : 
    var_computer : 
    status : 
    history : 

    
    Methods
    -------

    Notes
    -----

    """
    
    def __init__(self, data_collector=dc):

        # Buffer for data collector? -- seems to make sense - How/When to update it?
        # Waits for dc to get some data before coping it the first time.
        self.dc = Data_Collection()
        if dc.glob != -1:
            self.update_data_buffer()
        
            
        ### Pictures are to be set only when we get the
        ### paths to where they are from Adwin.
        
        self.atom_pic       = PictureManager(np.ones((256, 256)))
        self.no_atom_pic    = PictureManager(np.ones((256, 256)))
        self.abs_pic        = AbsorptionPicture(self.atom_pic, self.no_atom_pic)
        self.background_pic = None
        
        self.cycle_num = 0
        self.global_cycle_num = 0
        self.scan_num = 0
        
        self.atom_num  = 0

        
        self.variables = []
        self.var_computer =  dict()
        self.status = dict()   
        self.history = dict()  

        self.set_var_computer()
        self.set_vars()

    def update_data_buffer(self):
        """
        Copies the information from the global Data Collector if it is
        not being updated. The copy only happens if the information
        was changed (a new picture was received).

        Returns
        -------
        False
            If the information in the local Data Collector is the same.
        """
        if dc.glob == self.dc.glob:
            return False

        ###--- Make sure that dc is not being updated
        while(dc.receiving_flag == 1):
            continue
        
        dc.copy_flag = 1
        self.dc = copy.deepcopy(dc)
        dc.copy_flag = 0
    

    def update_info(self, win):
        """
        Receives information from Adwin through dc and 
        gets the pictures, calculates the absorption picture,
        updates the (global) cycle number as well as the other
        values to be calculated and stores them for future use.

        Parameters
        ----------
        win : Window object
            Window which shows the absorption picture

        Stuff to remove later...
        
        dc  - global 'Data_Collection' object
        win - main window where the info is displayed to the user 
        """
        if self.cycle_num +1 == self.dc.loop:
            self.cycle_num +=1
            
        else:
            self.cycle_num = self.dc.loop
            print("WARNING: Corrected loop number to " + str(self.cycle_num))

        
        if self.global_cycle_num +1 == self.dc.glob:
            self.global_cycle_num +=1
            temp_label = win.label_global + str(self.global_cycle_num)
            win.infoGlobalCounts.set_label(temp_label)
        else:
            self.global_cycle_num = self.dc.glob
            temp_label = win.label_global + str(self.global_cycle_num)            
            win.infoGlobalCounts.set_label(temp_label)
            print("WARNING: Corrected global loop number to " + str(self.cycle_num))        

        temp_label = win.label_scan + str(self.dc.scan)
        win.infoScanNum.set_label(temp_label)
        self.scan_num = self.dc.scan

        camera = self.gen_camera()

        if camera == -1 or camera == None:
            print("WARNING: Bad camera! Not updating.")
            return -1

        if self.dc.last_pic == -1:
            print(dc.last_pic)
            print("Dont know last pic...")
            return -1
       
        pic_atoms_name = camera.label + "_" + str(self.dc.last_pic[0]) + "atompic.tif"#"-withoutatoms.tif" ### name given by default
        pic_no_atoms_name = camera.label + "_" + str(self.dc.last_pic[0]) + "backpic.tif"#"-atomcloud.tif" ### 

        temp_str = self.dc.file.strip("\\")
        num = int(temp_str[-2]) - 4

        ###--- Paths from phantom
        path_atom_pic = PIC_SRC + self.dc.file[:-7] + str(num) + pic_atoms_name
        path_no_atom_pic = PIC_SRC + self.dc.file[:-7] + str(num) + pic_no_atoms_name
        print(pic_atoms_name)
        print(pic_no_atoms_name)

        ###--- Paths to network share
        print(pic_atoms_name)
        path_atom_pic = PIC_SRC + camera.label + "\\" + pic_atoms_name
        path_no_atom_pic = PIC_SRC + camera.label + "\\" + pic_no_atoms_name
        print("PATH my PATH: " + path_atom_pic)

        pic = mpimg.imread(path_atom_pic)
        self.atom_pic = PictureManager(pic, path=path_atom_pic, cam = camera)

        
        pic = mpimg.imread(path_no_atom_pic) 
        self.no_atom_pic = PictureManager(pic, path=path_no_atom_pic, cam = camera)
        self.background_pic = PictureManager(np.zeros(pic.shape)) # Creates a pic of zeros with same size as the other pics    
        
        
        try:
            self.abs_pic = AbsorptionPicture(self.atom_pic, self.no_atom_pic, cam = camera)
        except Exception as e:
            print("ERROR: " + str(e))
            print("No Abs pic set!!")

        win.update_pics()

        win.abs_pic = self.abs_pic
        win.update_pics_controll = 1

        try:
            self.atom_num = self.abs_pic.get_atom_number()
            print(self.atom_num)
        except Exception as e:
            print(e)
            print("Not possible to compute Atom number!")


        

        
        self.update_history()
        self.update_status()
        print("STILL UPDATING BITCH!")


    def set_vars(self):
        """
        Sets the variables shown in plot window.
        They are read from the variable 'self.vars'
        """
            
        for var in list(self.var_computer.keys()):
                self.history[var] = []
                self.status[var]  = ""
                

    def compute_vars(self, var):
        """
        Computes the variables shown in plot window.
        They are read from the variable 'self.variables'
        """
        
        if var in list(self.var_computer.keys()):
            return self.var_computer[var](self)
        else:
            print("WARNING: Variable not found!")
            print("Computation of '" + var + "' was not possible." )
            return -1


    def set_var_computer(self):
        """
        This function implements the dictionary that has
        the functions which compute the variables shown in the plot window.
        Each  key in 'self.var_computer' is a vaqriable to be computed
        and the correspondent key should be the function which computes the 
        variable described by the key (the function is already defined, of course).
        The key should be a string and start with capital letter.

        Example: To compute the mean, one should do

        var_computer["Mean"] = function_that_computes_the_mean
        
        """

        if self.variables == []:
            self.variables = list(var_list)
        
        self.var_computer= copy.deepcopy(func_dict)
        
            

        
   
    def update_history(self):
        """ 
        Stores the values of the variables 
        and adds the new ones
        """

        for var in self.var_computer:
            self.history[var].append(self.status[var])

        
        

    def update_status(self):
        """ 
        Stores the values of the variables of the last cycle
        The information is lost when information of another cycle 
        comes.
        """

        for var in self.var_computer:
            self.status[var] = self.compute_vars(var)
        
        

    def gen_camera(self):
        """
        Associates the correct camera to the last stored picture based
        on the information given by Adwin. 

        Returns
        -------
        Camera
            Camera object if successfull
        int
            -1 if not successfull
        """
        if self.dc.imsc == 0:
            return Camera(0)
        
        elif self.dc.imsc == 1 or self.dc.imsc == 2:
            return Camera(1)
        
        elif self.dc.imsc == 3:
            return Camera(3)
        
        else:
            print("Bad camera flag!")
            return -1

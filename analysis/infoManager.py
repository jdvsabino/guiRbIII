import sys
sys.path.append('../network')
import os
from picManager import PictureManager, AbsorptionPicture
import matplotlib.image as mpimg
import matplotlib.pyplot as plt # For teting purposes
import copy
import scipy as sio
import numpy as np
from network.data_collection import Data_Collection
from network.data_collection import data_collector as dc
from network.data_collection import PIC_SRC


class InfoManager():
    '''
    Deals with the current information from adwin.
    This class is aimed to store and process all 
    the information needed to get the new pictures, 
    update variable values, store the new information 
    and make it available in the future.   
    '''
    
    def __init__(self, data_collector=dc):
        
        # Buffer for data collector? -- seems to make sense - How/When to update it?
        # Waits for dc to get some data before coping it the first time.
        self.dc = Data_Collection()
        if dc.glob != -1:
            self.update_data_buffer()
        
        
        ### Pictures are to be set only when we get the
        ### paths to where they are from Adwin.
        self.abs_pic        = None
        self.atom_pic       = None
        self.no_atom_pic    = None
        self.background_pic = None
        
        self.cycle_num = 0
        self.global_cycle_num = 0
        self.scan_num = 0
        
        self.atom_num  = 0

        
        self.variables = []
        self.var_computer =  dict()
        self.status = dict()   ### TODO - Think how to implement
        self.history = dict()  ### TODO - Think how to implement

        self.set_var_computer()

    def update_data_buffer(self):
        print("GLOBAAAAAL: " + str(dc.glob))
        self.dc = copy.deepcopy(dc)
        

    def update_info(self, win):
        '''
        Receives information from Adwin through dc and 
        gets the pictures, calculates the absorption picture,
        updates the (global) cycle number as well as the other
        values to be calculated and stores them for future use.
        
        dc  - global 'Data_Collection' object
        win - main window where the info is displayed to the user 
        '''
        # update_data_buffer() ### INCLUDE THIS HERE???
        if self.cycle_num +1 == self.dc.loop:
            self.cycle_num +=1
        else:
            self.cycle_num = self.dc.loop
            print("WARNING: Corrected loop number to " + str(self.cycle_num))
        
        if self.global_cycle_num +1 == self.dc.glob:
            self.global_cycle_num +=1
        else:
            self.cycle_num = self.dc.loop
            print("WARNING: Corrected global loop number to " + str(self.cycle_num))        
        
        self.scan_num = self.dc.scan
        
        
        pic_atoms_name = "-withoutatoms.tif" ### name given by default
        pic_no_atoms_name = "-atomcloud.tif" ### 
        num = int(self.dc.file[-7:-1]) - 3
        path_atom_pic = PIC_SRC + self.dc.file[:-7] + str(num) + pic_atoms_name
        path_no_atom_pic = PIC_SRC + self.dc.file[:-7] + str(num) + pic_no_atoms_name

        #os.listdir(PIC_SRC + self.dc.file[:-7])
        #a = str(input("WAIT..."))


        # TESTING
        print("PATH my PATH: " + path_atom_pic)
        #path_atom_pic = "G:\\Codes\\MatLab\\Adwin_programs\\krb_acquisition_program_v10_Joao\\GUI_RbIII\\manos_na_neve.png"
        #path_no_atom_pic = "G:\\Codes\\MatLab\\Adwin_programs\\krb_acquisition_program_v10_Joao\\GUI_RbIII\\manos_na_neve.png"
        pic = mpimg.imread(path_atom_pic)
        self.atom_pic = PictureManager(pic, path=path_atom_pic)

        
        pic = mpimg.imread(path_no_atom_pic)
        self.no_atom_pic = PictureManager(pic, path=path_no_atom_pic)
        self.background_pic = None        
        
        
        self.abs_pic = AbsorptionPicture(self.atom_pic.pic, self.no_atom_pic.pic)
        #self.atom_num = self.abs_pic.get_atom_number()

        # TESTING BLOCK
        plt.imshow(self.abs_pic.pic)
        plt.savefig("G:\\Codes\\MatLab\\Adwin_programs\\krb_acquisition_program_v10_Joao\\GUI_RbIII\\Test_GUI_atompic", dpi=100)
        self.update_history()

        # Saves a matlab file with the data for this run
        file_name = PIC_SRC + self.dc.path + str(self.dc.loop) + "-data.mat"
        file_name = "datazinha.mat" # FOR TESTING
        #sio.savemat(file_name, self.status)
        
        ###--- TODO: Update hist and status
        # update_status() ### Really necessary?


    def set_vars(self):
        '''
        Sets the variables shown in plot window.
        They are read from the variable 'self.vars'
        '''
            
        for var in list(self.var_computer.keys()):
                self.history[var] = []
                self.status[var]  = []
                

    def compute_vars(self, var):
        '''
        Computes the variables shown in plot window.
        They are read from the variable 'self.variables'
        '''

        if var in list(self.var_computer.keys()):
            return self.var_computer[var]()
        else:
            print("WARNING: Variable not found!")
            print("Computation of '" + var + "' was not possible." )
            return -1
        


    def set_var_computer(self):
        '''
        This function implements the dictionary that has
        the functions which compute the variables shown in the plot window.
        Each  key in 'self.var_computer' is a vaqriable to be computed
        and the correspondent key should be the function which computes the 
        variable described by the key (the function is already defined, of course).
        The key should be a string and start with capital letter.

        Example: To compute the mean, one should do

        var_computer["Mean"] = function_that_computes_the_mean
        
        '''
   
    def update_history(self):
        ''' 
        Stores the values of the variables 
        and adds the new ones
        '''

        for var in self.var_computer:
            self.history[var].append(self.compute_vars(var))

        
        

    def update_status():
        ''' 
        Stores the values of the variables of the last cycle
        The information is lost when information of another cycle 
        comes.
        '''

        for var in self.var_computer:
            self.status[var].append(self.compute_vars(var))
        
        

        

        

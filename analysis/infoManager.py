from picManager import PictureManager
import matplotlib.image as mpimg

class InfoManager():
    '''
    Deals with the current information from adwin.
    This class is aimed to store and process all 
    the information needed to get the new pictures, 
    update variable values, store the new information 
    and make it available in the future.   
    '''

    def __init__(self):

        # 
        self.dc = dc
        
        
        ### Pictures are to be set only when we get the
        ### paths to where they are from Adwin.
        self.abs_pic        = None
        self.atom_pic       = None
        self.no_atom_pic    = None
        self.background_pic = None

        self.cycle_num = 0
        self.global_cycle_num = 0
        self.scan_num
        
        self.atom_num  = 0

        self.status = dict()   ### TODO - Think how to implement
        self.history = dict()  ### TODO - Think how to implement

        
    def update_info(self, dc, win):
        '''
        Receives information from Adwin through dc and 
        gets the pictures, calculates the absorption picture,
        updates the (global) cycle number as well as the other
        values to be calculated and stores them for future use.

        dc  - global 'Data_Collection' object
        win - main window where the info is displayed to the user 
        '''

        if self.cycle_num +1 == dc.loop:
            self.cycle_num +=1
        else:
            self.cycle_num = dc.loop
            print("WARNING: Corrected loop number to " + str(self.cycle_num))

        if self.global_cycle_num +1 == dc.glob:
            self.global_cycle_num +=1
        else:
            self.cycle_num = dc.loop
            print("WARNING: Corrected global loop number to " + str(self.cycle_num))        

        self.scan_num = dc.scan
            
        ### Implement how to get the Pics
        # 
        # path_atom_pic = ""
        # path_no_abs_pic = ""
        # 
        # pic = mpimg.imread(path_atom_pic)
        # self.atom_pic = PictureManager(pic, path=path_atom_pic)
        #
        # pic = mpimg.imread(path_no_atom_pic, path=path_no_atom_pic)
        # self.no_atom_pic = PictureManager(pic)
        # self.background_pic = NONE ????
        #
        ### Talk to Thomas

        self.abs_pic = AbsorptionPicture(self.atom_pic, self.no_atom_pic)
        #self.abs_pic.get_absorption_picture(self.atom_pic, self.no_atom_pic) # I

        self.atom_num = self.abs_pic.get_atom_number()
        

        ###--- TODO: Update hist and status

        def update_history():
           ''' TODO '''

           return NotImplemented

        def update_status():
           ''' TODO '''

           return NotImplemented

        

        

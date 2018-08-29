import numpy as np

class PictureManager():

    def __init__(pic, cam = None):

        self.pic = pic
        self.cam = cam

        self.int_x = None
        self.int_y = None


    ''' Setters and getters are  defined '''
    def set_pic(pic):
        ''' Only needed if user wants to update teh picture. '''
        self.pic = pic

    def get_pic():
        return self.pic
        
    def set_cam(cam):
        self.cam = cam
        
    def get_cam():
        return self.cam


    
    ''' Useful functions are defined '''
    def get_atoms():
        '''
        Returns number of atoms in the picture
        '''

        return NotImplemented

    def integrate_x():
        '''
        Returns an array with the pixels summed over y
        '''
        return np.sum(self.pic, axis=0) # Currently only works with tiff images or other format that is a 2D array

    def integrate_y():
        '''
        Returns an array with the pixels summed over x
        '''
        return np.sum(self.pic, axis=1) # Currently only works with tiff images or other format that is a 2D array
    

    def fit_integrated_x(plot=0):
        ''' 
        Fits a gaussian function to the picture summed over y
        and returns the data of the fit. It alsor returns the plot if 
        plot == 1
        '''

        return NotImplemented

    def fit_integrated_y(plot=0):
        ''' 
        Fits a gaussian function to the picture summed over x
        and returns the data of the fit. It alsor returns the plot if 
        plot == 1
        '''

        return NotImplemented
    
class Camera():

    def __init__(cam_type):

        self.cam_type = int(cam_type)

        self.label = ""
        self.pixel_size = 0. # Pixel size in um (micrometers)
        self.magnification = 0.
        self.correction = 0.

        if cam_type == 0:
            self.label = "TANDOR"
            self.pixel_size = 6.
            self.magnification = 0.
            self.correction = 0.

            return 0
        
        elif cam_type == 1:
            self.label = "LANDOR"
            self.pixel_size = 6.
            self.magnification = 0.
            self.correction = 0.

            return 0
        
        elif cam_type == 2 or cam_type == 3:
            self.label = "VANDOR"
            self.pixel_size = 6.
            self.magnification = 0.
            self.correction = 0.

            return 0

        else:
            print("Camera was not initialized. Problem with 'cam_type'. \n Check it is a number!\n")
            print("You can also defined the values manually.")
            


    

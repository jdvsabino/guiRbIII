import numpy as np
import pylab as plb
import sys
sys.path.append("..")
from classes.drawRectangle import roiRectangle, rbcRectangle


class PictureManager():

    def __init__(pic, cam = None):

        self.path = ""
        self.ID = -1
        
        self.pic = pic
        self.cam = cam

        self.TOF = -1
        self.gain = -1
        self.ROI = roiRectangle(1,1,1,1)
        self.RBC = rbcRectangle(1,1,1,1)


    ''' Getters are  defined '''

    def get_pic(self):
        return self.pic
        
    def get_cam(self):
        return self.cam


    
    ''' Useful functions are defined '''
    def get_atoms(self):
        '''
        Returns number of atoms in the picture
        '''

        return NotImplemented

    def integrate_x(self):
        '''
        Returns an array with the pixels summed over y
        '''
        return np.sum(self.pic, axis=0) # Currently only works with tiff images or other format that is a 2D array

    def integrate_y(self):
        '''
        Returns an array with the pixels summed over x
        '''
        return np.sum(self.pic, axis=1) # Currently only works with tiff images or other format that is a 2D array
    

    def fit_integrated_x(self, plot=0):
        ''' 
        Fits a gaussian function to the picture summed over y
        and returns the data of the fit. It alsor returns the plot if 
        plot == 1
        '''
        
        data = self.integrate_x()
        length = len(data)
        x_data = np.linspace(1,length, length)
        mean = np.sum(data)/length
        sigma = np.sqrt((data - mean)**2)
        popt, pcov = curve_fit(gaussian_func, x_data, data, p0=[1, mean, sigma])

        return popt, pcov
        

        

    def fit_integrated_y(plot=0):
        ''' 
        Fits a gaussian function to the picture summed over x
        and returns the data of the fit. It alsor returns the plot if 
        plot == 1
        '''
        data = self.integrate_x()
        length = len(data)
        x_data = np.linspace(1,length, length)
        mean = np.sum(data)/length
        sigma = np.sqrt((data - mean)**2)
        popt, pcov = curve_fit(gaussian_func, x_data, data, p0=[1, mean, sigma])

        return popt, pcov


    
class Camera():

    def __init__(cam_type):

        self.cam_type = int(cam_type)

        self.label = ""
        self.pixel_size = 0. # Pixel size in um (micrometers)
        self.magnification = 0.
        self.correction = 0.

        if cam_type == 0:
            self.label = "TANDOR"
            self.pixel_size = 13.*1e-4 # cm
            self.magnification = 12.39
            self.pixel2um = 1.05
            self.correction = 0.

            return 0
        
        elif cam_type == 1 or cam_type == 2:
            self.label = "LANDOR"
            self.pixel_size = 13.*1e-4 # cm
            self.magnification = 5.3
            self.pixel2um = 2.45
            self.correction = 0.

            return 0
        
        elif cam_type == 3:
            self.label = "VANDOR"
            self.pixel_size = 13.*1e-4 # cm
            self.magnification = 1.68
            self.pixel2um = 3.84
            self.correction = 0.

            return 0

        else:
            print("Camera was not initialized. Problem with 'cam_type'. \n Check it is a number!\n")
            print("You can also defined the values manually.")
            


    

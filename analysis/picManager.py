import numpy as np
# import pylab as plb
import sys


class PictureManager():
    '''
    Stores a picture with all the information 
    related to it, namely:
    - Path
    - Camera
    - ID: specifies the type of picture // OR PIC NUMBER???
          1 - Absorption Picture
          2 - Picture with atoms 
          3 - Picture without atoms
          4 - Background picture
    '''
    def __init__(self,pic, cam = None, path=""):
        
        self.path = ""
        self.ID = -1
        self.num = -1
        
        self.pic = pic
        self.cam = cam

        self.TOF = -1
        self.gain = -1
        self.ROI = [1, 1, 1, 1]#roiRectangle(1,1,1,1)
        self.RBC = [1, 1, 1, 1]#rbcRectangle(1,1,1,1)



class AbsorptionPicture(PictureManager):

    def __init__(self, atom_pic, no_atom_pic, cam = None, correction=True):

        PictureManager.__init__(self, pic)
        self.path = ""
        self.ID = 1 ### DECIDE ABOUT THIS _ CAREFUL!!! 
        
        self.pic = get_absorption_picture(atom_pic, no_atom_pic)
        self.cam = cam

        self.TOF = -1
        self.gain = -1
        self.ROI = [1, 1, 1, 1]#roiRectangle(1,1,1,1)
        self.RBC = [1, 1, 1, 1]#rbcRectangle(1,1,1,1)
        self.bkg_correction = correction


        '''
        Add a self.pic_roi?
        back_pics?
        '''

    
    ### Useful functions are defined 
    def get_atom_number(self):
        '''
        Returns number of atoms in the picture.
        Check if it is the complete formula!
        '''
        px_size = self.cam.pixel2um
        mag = self.cam.magnification
        abs_cross = self.cam.abs_cross
        final_pic = self.pic[self.ROI[0]:self.ROI[1], self.ROI[2]:self.ROI[4]]
        atom_number = px_size*pix_size/(mag*mag)/abs_cross*np.sum(np.sum(final_pic))

        return atom_number

    def get_absorption_picture(self, atom, no_atom):
        '''
        Computes the absorption picture.
        - Check formula - use gain?
                        - what the hell is eps? (in fringe analysis file)
        - We shouls set all negative elements to zero
        '''
        
        abs_pic = -np.log(atom/no_atom)
        
        return abs_pic
    
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
        

        

    def fit_integrated_y(self, plot=0):
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

    def background_correction(self):
        return NotImplementedError
        
    
class Camera():

    def __init__(self, cam_type):

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
            self.abs_cross = 1.938*1e-9
            self.correction = 0.

            return 0
        
        elif cam_type == 1 or cam_type == 2:
            self.label = "LANDOR"
            self.pixel_size = 13.*1e-4 # cm
            self.magnification = 5.3
            self.pixel2um = 2.45
            self.abs_cross = 2.9*1e-9
            self.correction = 0.

            return 0
        
        elif cam_type == 3:
            self.label = "VANDOR"
            self.pixel_size = 13.*1e-4 # cm
            self.magnification = 1.68
            self.pixel2um = 3.84
            self.abs_cross = 1.938*1e-9                    
            self.correction = 0.

            return 0

        else:
            print("Camera was not initialized. Problem with 'cam_type'. \n Check it is a number!\n")
            print("You can also defined the values manually.")

import numpy as np
# import pylab as plb
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import sys

###---- Minimum value to avoid zeros while computing abs_pic
MIN = sys.float_info.min


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

        PictureManager.__init__(self, atom_pic) # Doesnt make much sense, think about this...
        self.path = ""
        self.ID = 1 ### DECIDE ABOUT THIS _ CAREFUL!!! 

        self.atom_pic = atom_pic
        self.no_atom_pic = no_atom_pic
        self.bkg_pic = None # TODO
        self.pic = self.get_absorption_picture(atom_pic.pic, no_atom_pic.pic)
        self.cam = cam

        self.TOF = -1
        self.gain = -1
        self.ROI = [1, 1, 1, 1]#roiRectangle(1,1,1,1)
        self.RBC = [1, 1, 1, 1]#rbcRectangle(1,1,1,1)
        self.bkg_correction = correction

        self.fit_x    = 0
        self.fit_y    = 0
        self.fit_pars = {"x":[], "y":[]}


        '''
        Add a self.pic_roi?
        back_pics?
        '''

    
    ### Useful functions are defined

    def set_ROI(self, rectangle = None, up = None, down = None, left = None, right = None):

        
        if rectangle == None and up == None:
            print("Please use either a rectangle or coordinates as arguments.")
            return -1
        
        elif rectangle == None:
            print("Used coordinates!")
            self.ROI[0] = int(up)
            self.ROI[1] = int(down)
            self.ROI[2] = int(left)
            self.ROI[3] = int(up)
            return 1

        else:
            self.ROI[0] = int(rectangle.y_start)
            self.ROI[1] = int(rectangle.y_end)
            self.ROI[2] = int(rectangle.x_start)
            self.ROI[3] = int(rectangle.x_end)
            print("Used rectangle!")
            return 1

    def set_RBC(self, rectangle = None, up = None, down = None, left = None, right = None):

        
        if rectangle == None and up == None:
            print("Please use either a rectangle or coordinates as arguments.")
            return -1
        
        elif rectangle == None:
            self.RBC[0] = int(up)
            self.RBC[1] = int(down)
            self.RBC[2] = int(left)
            self.RBC[3] = int(up)
            return 1

        else:
            self.RBC[0] = int(rectangle.y_start)
            self.RBC[1] = int(rectangle.y_end)
            self.RBC[2] = int(rectangle.x_start)
            self.RBC[3] = int(rectangle.x_end)
            return 1

    
    def get_atom_number(self):
        '''
        Returns number of atoms in the picture.
        Check if it is the complete formula!
        '''
        px_size = self.cam.pixel2um
        mag = self.cam.magnification
        abs_cross = self.cam.abs_cross

        try:
            print("ROIZINHO: " + str(self.ROI[0]))
            print("ROIZINHO: " + str(self.ROI[1]))
            print("ROIZINHO: " + str(self.ROI[2]))
            print("ROIZINHO: " + str(self.ROI[3]))
            print("SHAPEZINHA: " + str(self.pic.shape))
            #final_pic = self.pic[self.ROI[0]:self.ROI[1], self.ROI[2]:self.ROI[4]]
            final_pic = self.pic[self.ROI[0]:self.ROI[1], self.ROI[2]:self.ROI[3]]

        except Exception as e:
            print(e)
            print("Couldnt compute atomnumber with ROI. Using whole picture!")
            final_pic = self.pic
        atom_number = self.cam.pixel_size*self.cam.pixel_size/(self.cam.magnification*self.cam.magnification)/self.cam.abs_cross*np.sum(np.sum(final_pic))

        return atom_number

    def get_absorption_picture(self, atom, no_atom, full=False):
        '''
        Computes the absorption picture.
        - Check formula - use gain?
                        - what the hell is eps? (in fringe analysis file)
        - We shouls set all negative elements to zero
        '''
        # abs_pic = np.divide(atom, no_atom, out=np.ones_like(atom), where=no_atom!=0) # test these arguments
        abs_pic = np.divide(atom, no_atom + MIN) # test if this works
        if full:
            '''
            For details on these values check Thomas Schweigler thesis, chapter 3.
            Discuss these formulas, is sig0 really necessary? Apparently not.
            '''
            # More versatile way of writing  I_sat
            # hbar = 1.0546*1e-34 # m^2.Kg/s
            # alpha = 1.83
            # lamb = 111
            # w = 0
            # tau = 1
            # sig0 = 3*lamb*lamb/(2*np.pi)
            # sig = sig0/alpha
            # I_sat = hbar*w/(2*sig0*tau)
            # I_sat = I_sat*alpha

            # Value for I_sat from KRbTools
            I_sat = 16.6933
            abs_pic = -np.log(abs_pic) + (no_atom - atom)/I_sat

            return abs_pic
        
        abs_pic = -np.log(abs_pic)
        return abs_pic
    
    def integrate_x(self):
        '''
        Returns an array with the pixels summed over y
        '''
        print("INT XXX - shape: " +str(self.pic[self.ROI[0]:self.ROI[1], self.ROI[2]:self.ROI[3]].shape))        
        return np.sum(self.pic[self.ROI[0]:self.ROI[1], self.ROI[2]:self.ROI[3]], axis=0) # Currently only works with tiff images or other format that is a 2D array

    def integrate_y(self):
        '''
        Returns an array with the pixels summed over x
        '''
        print("INT YYY - shape: " +str(self.pic[self.ROI[0]:self.ROI[1], self.ROI[2]:self.ROI[3]].shape))
        return np.sum(self.pic[self.ROI[0]:self.ROI[1], self.ROI[2]:self.ROI[3]], axis=1) # Currently only works with tiff images or other format that is a 2D array

    def integrate_abs_pic(axis):
        '''
        Integrates the absorpption picture in the desired direction.
        
        axis = 0 - integrates over xx (cloud along y)
        axis = 1 - integrates over yy (cloud along x)

        TODO
        '''
        return NotImplemented
        

    def fit_integrated_x(self, axis, x_min=0, x_max=0, tol=0.2, plot=0):
        ''' 
        Fits a gaussian function to the picture summed over y (or x?)
        and returns the data of the fit. It also returns the plot if 
        plot == 1.
        '''
        if  axis == "x":
            axis = 0;
            
        elif axis == "y":
            axis = 1;

        elif type(axis) == str:
            print("Check the axis you want to fit!")
        
        if axis == 0:
            data = self.integrate_x()
        elif axis ==1:
            data = self.integrate_y()
        else:
            print("Please choos the axis correctly!")
            return -1
            
        
        length     = len(data)
        x_data     = np.linspace(1,length, length, endpoint=True)


        ### Parameter estimation to help the fit
        sigma = 0
        mean  = 0
        
        mean_temp  = np.sum(data)/length
        temp       = np.array(data)
        
        temp[temp<mean_temp] = 0


        for i in range(1, len(data)): # starts in 1 to be sure we have one index before
            if temp[i] > 0 and temp[i-1] == 0:
                sigma = x_data[i]

            if  temp[i] > 0 and temp[i+1] == 0:
                mean  = (sigma + x_data[i])/2
                sigma = x_data[i] - sigma
            
        print("MEAN: " + str(mean))
        print("SIGMA: " + str(sigma))
        print("MAXIMUM:" + str(np.max(data)))
        print(self.ROI)
        
        popt, pcov = curve_fit(self.gaussian_func, x_data, data, p0=[np.max(data), mean, sigma])

        if axis == 0:
            self.fit_x         = popt[0]*np.exp(-0.5*(x_data-popt[1])*(x_data-popt[1])/popt[2])
            self.fit_pars["x"] = popt
        else:
            self.fit_y         = popt[0]*np.exp(-0.5*(x_data-popt[1])*(x_data-popt[1])/popt[2])
            self.fit_pars["y"] = popt

        if plot:
            print(popt)
            plt.plot(x_data, self.gaussian_func(x_data, popt[0],popt[1],popt[2]),"r")
            plt.plot(x_data, data, "b")
            plt.show()
            plt.close()
        
        return popt, pcov
        

        

    def fit_integrated_y(self, plot=0):
        ''' 
        Fits a gaussian function to the picture summed over x
        and returns the data of the fit. It alsor returns the plot if 
        plot == 1
        '''
        
        data       = self.integrate_y()
        length     = len(data)
        print("X DATA LENGTH: " + str(length))
        x_data     = np.linspace(1,length, length, endpoint=True)
        mean       = np.sum(data)/length
        sigma      = np.sum(np.sqrt((data - mean)**2))
        popt, pcov = curve_fit(self.gaussian_func, x_data, data, p0=[np.max(data), mean, sigma])

        self.fit_y         = popt[0]*np.exp((x_data-mean)*(x_data-mean)/(2*sigma))
        self.fit_pars["y"] = popt

        if plot:
            plt.plot(x_data, self.gaussian_func(x_data, popt[0],popt[1],popt[2]),"r")
            plt.plot(x_data, data, "b")
            plt.show()
            plt.close()
        
        return popt, pcov

    def background_correction(self):
        return NotImplementedError

    def gaussian_func(self, x, a, b, c):
        
        gauss = a*np.exp(-0.5*(x-b)*(x-b)/c) 
        return gauss
        
    
class Camera():

    def __init__(self, cam_type):

        self.cam_type = int(cam_type)

        self.label = ""
        self.pixel_size = 0. # Pixel size in um (micrometers)
        self.magnification = 0.
        self.correction = 0.

        if cam_type == 0:
            self.label = "TAndor"
            self.pixel_size = 13.*1e-4 # cm
            self.magnification = 12.39
            self.pixel2um = 1.05
            self.abs_cross = 1.938*1e-9
            self.correction = 0.

            #return 0
        
        elif cam_type == 1 or cam_type == 2:
            self.label = "LAndor"
            self.pixel_size = 13.*1e-4 # cm
            self.magnification = 5.3
            self.pixel2um = 2.45
            self.abs_cross = 2.9*1e-9
            self.correction = 0.

            #return 0
        
        elif cam_type == 3:
            self.label = "VAndor"
            self.pixel_size = 13.*1e-4 # cm
            self.magnification = 1.68
            self.pixel2um = 3.84
            self.abs_cross = 1.938*1e-9                    
            self.correction = 0.

            #return 0

        else:
            print("Camera was not initialized. Problem with 'cam_type'. \n Check it is a number!\n")
            print("You can also defined the values manually.")

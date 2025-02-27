import sys
import os

curr_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(curr_path + './network/')
sys.path.append(curr_path + './analysis/')
sys.path.append(curr_path + './gui/')
sys.path.append(curr_path + './gui/classes/')

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
from gui.mainWindow import mainWindow
import threading, select
from analysis.picManager import PictureManager, AbsorptionPicture



from network.get_data import get_data
from network.data_collection import data_collector as  dc
from analysis.infoManager import InfoManager
import time # TESTING PURPOSES
import matplotlib.image as mpimg # TESTING PURPOSES
import numpy as np
###---- MAIN VARIABLES
REC_PORT_AD = "49298" # Receiving port
REC_PORT_C1 = "8103"
REC_PORT_C2 = "8102"
REC_PORT_C3 = "8107"

LOCAL_IP = "127.0.0.1"
#LOCAL_IP = "192.0.0.100"




###---- OBJECT TO MANAGE INFO
info_man = InfoManager()


###---- GRAPHIC OBJECTS - uncommented for testing purposes
win = mainWindow(info_man)
win.connect("destroy", Gtk.main_quit)

dummy_img = np.zeros((256, 256))
im1 = dummy_img # mpimg.imread("./atoms.tif")
im2 = dummy_img # mpimg.imread("./noatoms.tif")
im3 = dummy_img # mpimg.imread("./bicla.jpg")

win.im.atom_pic = PictureManager(im1)
win.im.no_atom_pic = PictureManager(im2)
win.im.abs_pic = AbsorptionPicture(win.im.atom_pic, win.im.no_atom_pic)

win.set_picAtoms(im1)
win.set_picNoAtoms(im2)
win.set_picBkg(im2)
# win.set_picOriginal(im2)
# win.set_picZoomed(im1)

win.show_all()
# Gtk.main()


###---- Thread to receive data
print("Trying to communicate with Adwin...")
t = threading.Thread(target=get_data,args=((LOCAL_IP, REC_PORT_AD, REC_PORT_C1, REC_PORT_C2, REC_PORT_C3, dc)))
t.daemon = True
t.start()


print("Done!")

dc.glob = 1
dc.receiving_flag = 0

#print(t.is_alive())


def cycle():

    temp_glob = -1
    while(1):

    
    # Holds the program while dc
    # does not receive data from  Adwin.

        time.sleep(1)
        
        #read_data = dc.receiving_flag != 1 and dc.glob != info_man.dc.glob and dc.status == 1 ## OLD
        read_data = (dc.status == 0 and dc.glob == temp_glob) and temp_glob != -1
        temp_glob = dc.glob
        #print("READ DATA: " + str(read_data))
        if 1: #read_data:
            
            print("#####+++++#####")
            
            update = info_man.update_data_buffer()
            if update:
                info_man.update_info(win) # Argument is none for testing purposes

            print("STATUS: " + str(info_man.status))
            print("HIST: " + str(info_man.history))
            print("#####+++++#####")

###---- Thread to start Gtk loop
t_cycle = threading.Thread(target=cycle)
t_cycle.daemon = True
t_cycle.start()

Gtk.main()





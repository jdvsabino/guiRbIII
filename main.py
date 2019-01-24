import sys
sys.path.append('.\network')
sys.path.append('.\analysis')
sys.path.append('.\gui')

import threading, select
#from gui.mainWindow import mainWindow
#from analysis.picManager import PictureManager

from network.data_collection import data_collector as  dc

from network.get_data import get_data
from analysis.infoManager import InfoManager


###---- MAIN VARIABLES
REC_PORT_AD = "8101" # Receiving port
REC_PORT_C1 = "8103"
REC_PORT_C2 = "8104"
REC_PORT_C3 = "8107"

LOCAL_IP = "127.0.0.1"



###---- OBJECT TO MANAGE INFO
info_man = InfoManager()


###---- GRAPHIC OBJECTS - uncommented for testing purposes
# win = mainWindow()


###---- Thread to receive data
print("Trying to communicate with Adwin...")
t = threading.Thread(target=get_data,args=((LOCAL_IP, REC_PORT_AD, REC_PORT_C1, REC_PORT_C2, REC_PORT_C3, dc)))
t.start()
print("Done!")


print(t.is_alive())
while(1):

    
    # Holds the program while dc
    # does not receive data from  Adwin.
    while(dc.glob == -1):
        continue

    read_data = dc.receiving != 1 and dc.glob != info_man.dc.glob
    if read_data:
        print("#####+++++#####")
        info_man.update_data_buffer()
        info_man.update_info(None) # Argument is none for testing purposes
        print("#####+++++#####")
        
    



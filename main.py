import sys
sys.path.append('.\network')
sys.path.append('.\analysis')
sys.path.append('.\gui')

import threading, select
#from gui.mainWindow import mainWindow
#from analysis.picManager import PictureManager

from network.data_collection import data_collector as  dc

from network.get_data import get_data


###---- MAIN VARIABLES
REC_PORT_AD = "8101" # Receiving port
REC_PORT_C1 = "8103"
REC_PORT_C2 = "8102"
REC_PORT_C3 = "8107"

LOCAL_IP = "192.0.0.100"




dcbuffer =  "" # Just for testing


###---- Thread to receive data
print("Trying to communicate with Adwin...")
t = threading.Thread(target=get_data,args=((LOCAL_IP, REC_PORT_AD, REC_PORT_C1, REC_PORT_C2, REC_PORT_C3, dc)))
t.start()
print("Done!")


print(t.is_alive())
while(1):

    if dc.glob != dcbuffer:
        print("#####+++++#####")
        print(str(dc.glob))
        print("#####+++++#####")
        dcbuffer = dc.glob
    

a=input("Press any key to exit...")
print("BBBB: " + dc.path)









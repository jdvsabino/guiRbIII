import sys
sys.path.append('~/Dropbox/GUI_RbIII/network')
sys.path.append('~/Dropbox/GUI_RbIII/analysis')

import threading, select
from mainWindow import mainWindow
from analysis.picManager import PictureManager
import network.data_collection as dc
from network.get_data import get_data


###---- MAIN VARIABLES
REC_PORT_AD = "5005" # Receiving port
REC_PORT_C1 = "1234"
REC_PORT_C2 = "1235"
REC_PORT_C3 = "1236"

LOCAL_IP = "127.0.0.1"

###---- This is a global variable - BE CAREFUL
###---- If you change its name, make sure it is updated on function 'get_data'!
input_info = dc.data_collector



###---- Thread to receive data
t = threading.Thread(get_data(LOCAL_IP, REC_PORT_AD, REC_PORT_C1, REC_PORT_C2, REC_PORT_C3, input_info))

print("BBBB: " + input_info.path)









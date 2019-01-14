import sys
sys.path.append('./network')
sys.path.append('./analysis')
sys.path.append('./gui')

import threading, select
from mainWindow import mainWindow
from analysis.picManager import PictureManager
from network.data_collection import data_collector as  dc
from network.get_data import get_data


###---- MAIN VARIABLES
REC_PORT_AD = "5005" # Receiving port
REC_PORT_C1 = "1234"
REC_PORT_C2 = "1235"
REC_PORT_C3 = "1236"

LOCAL_IP = "127.0.0.1"





###---- Thread to receive data
t = threading.Thread(get_data(LOCAL_IP, REC_PORT_AD, REC_PORT_C1, REC_PORT_C2, REC_PORT_C3, dc))

print("BBBB: " + dc.path)









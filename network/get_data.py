from open_port import start_comm
from data_collection import Data_Collection

# Maybe define these as global??
REC_PORT = "8101" 
LOCAL_IP = "192.0.0.123"



def get_data():

    adwin_soccket = start_comm(LOCAL_IP, REC_PORT)
    global input_info = Data_Collection()
    
    while True:

        readable, writable, exceptional = select.select(inputs,[],[]) #check if any port received something
        for message in readable:
            data, addr = s.recvfrom(1024)
            input_info.set_data(data)

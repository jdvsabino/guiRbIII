from open_port import start_comm
from data_collection import Data_Collection
import select

# Maybe define these as global??
REC_PORT = "17600"#"8101" 
LOCAL_IP = "127.0.0.1"#"128.131.60.27"



def get_data(local_ip, rec_port):

    adwin_socket = start_comm(local_ip, rec_port)
    inputs = [adwin_socket]
    input_info = Data_Collection()
    
    while True:
        print("Inside while loop!")
        readable, writable, exceptional = select.select(inputs,[],[]) #check if any port received something
        print("Read something...")
        print(readable)
        for message in readable:
            data, addr = message.recvfrom(1024)
            print("DATA: " + data)
            input_info.set_data(data)


print("Started listening to port " + REC_PORT + ", on local machine.")
get_data(LOCAL_IP, REC_PORT)


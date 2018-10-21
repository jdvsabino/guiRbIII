from open_port import start_comm
from data_collection import Data_Collection
import select
import threading

# Maybe define these as global??
REC_PORT = "5005"#"8101" 
LOCAL_IP = "127.0.0.1"#"128.131.60.27"

input_info = Data_Collection() # This is going to be a global variable -  CAREFUL!!

def get_data(local_ip, rec_port_adwin, rec_port_c1, rec_port_c2, rec_port_c3):
    '''
    Gets all the data necessary
    for the program to work. It should be run in a new thread
    to make synching easier.
    '''
    ###---- Defined in the main program
    global input_info 

    ###---- Opening sockets for communication
    adwin_socket = start_comm(local_ip, rec_port_adwin)

    #---- Celcius computers
    c1_socket = start_comm(local_ip, rec_port_c1)
    c2_socket = start_comm(local_ip, rec_port_c2)
    c3_socket = start_comm(local_ip, rec_port_c3)    

    inputs = [adwin_socket, c1_socket, c2_socket, c3_socket]
    
    while True:
        print("Inside while loop!")
        readable, writable, exceptional = select.select(inputs,[],[]) #check if any port received something
        print("Read something...")
        print(readable)
        print(writable)
        print(exceptional)
        for socket in readable:
            data, addr = socket.recvfrom(1024)
            print("DATA: " + data)

            if socket is adwin_socket:
                input_info.set_data_adwin(data)

            elif socket is c1_socket:
                input_info.set_data_c1(data)

            elif socket is c2_socket:
                input_info.set_data_c2(data)

            elif socket is c3_socket:
                input_info.set_data_c3(data)

            else:
                print("Error: wierd socket detected!")


            

print("Started listening to port " + REC_PORT + ", on local machine.")
t = threading.Thread(get_data(LOCAL_IP, REC_PORT,5,6,7))




from open_port import start_comm
# from data_collection import data_collector as dc
import select
import threading


def get_data(local_ip, rec_port_adwin, rec_port_c1, rec_port_c2, rec_port_c3, input_info):
    '''
    Gets all the data necessary
    for the program to work. It should be run in a new thread
    to make synching easier.

    Parameters
    ----------
    local_ip : str
        The ip of the local computer.
    rec_port_adwin : str
        The port which recieves info from adwin.
    rec_port_c1 : str
        The port which recieves info from computer 'Celcius I'
    rec_port_c2 : str
        The port which recieves info from computer 'Celcius II'
    rec_port_c3 : str
        The port which recieves info from computer 'Celcius III'
    input_info : str
        Doesn't seem to be needed.
    '''
    
    ###---- Opening sockets for communication
    adwin_socket = start_comm(local_ip, rec_port_adwin)
    # adwin_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    #---- Celcius computers
    # c1_socket = start_comm(local_ip, rec_port_c1)
    # c2_socket = start_comm(local_ip, rec_port_c2)
    # c3_socket = start_comm(local_ip, rec_port_c3)    

    inputs = [adwin_socket]#, c1_socket, c2_socket, c3_socket]
    #input_info = dc.data_collector
    
    while 1:
        #print("Inside while loop!")
        readable, writable, exceptional = select.select(inputs,[],[]) #check if any port received something
        #print("Read something...")
        #print("READABLE:" + str(readable))
        #print(writable)
        #print(exceptional)
        for socket in readable:
            data, addr = socket.recvfrom(1024)

            # Code was written before python3 and data is expected to be as tring.
            # This line takes care of it.

            data = data.decode("utf-8") 
            print("DATA: " + data)

            if socket is adwin_socket:
                input_info.set_data_adwin(data)

            # elif socket is c1_socket:
            #     input_info.set_data_c1(data)
            #     print("Socket C1!")

            # elif socket is c2_socket:
            #     input_info.set_data_c2(data)
            #     print("Socket C2!")
                
            # elif socket is c3_socket:
            #     input_info.set_data_c3(data)
            #     print("Socket C3!")
                
            else:
                print("Error: wierd socket detected!")
                if i%2==0:
                    input_info.path="PAR!"
                else:
                    input_info.path="IMPAR!"



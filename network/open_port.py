import os
import socket
import select
import threading

#REC_PORT = "8101"
#LOCAL_IP = "192.0.0.123"

def start_comm(local_ip, rec_port_adwin):
    ''' Opens connection to port rec_port_adwin,
        the port through which admin info is sent.

        Parameters
        ----------
        local_ip : str
            The ip of the local computer.
        rec_port_adwin : str
            The port which recieves info from adwin.
        
        Returns
        -------
        sock : socket
        
    '''
    print("Local IP set to: " + local_ip + ".")
    print("Trying to open and bind socket in port: " + str(rec_port_adwin) + ".")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    #sock.setblocking(0)
    
    sock.bind((local_ip, int(rec_port_adwin)))
    #sock.connect((local_ip, int(rec_port_adwin)))
    #
    sock.listen()

    conn, addr = sock.accept()

    

    print(sock)
    print("sucess!")
    return conn


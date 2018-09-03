import os
import socket
import select
import thread

REC_PORT = "8101"
LOCAL_IP = "192.0.0.123"

def start_comm(local_ip, rec_port_adwin):
    ''' Opens connection to port rec_port_adwin'''
    print("Local IP set to: " + local_ip + ".")
    print("Trying to open and bind socket in port: " + rec_port + ".")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    sock.setblocking(0)
    sock.bind((LOCAL_IP, REC_PORT_ADWIN))
    print(sock)
    print("sucess!")
    return sock


import socket
import struct
import sys
import time
import select
import random

class Client:
    def __init__(self, host, port):
        self.smaller = "<"
        self.equal = "="
        self.lowBound = 1
        self.highBound = 101
        self.number = self.highBound // 2
        self.inputs = (self.smaller.encode(), self.number)
        self.pack = struct.Struct('1s I')
        self.packed_data = self.pack.pack(*self.inputs)

        self.m_server_address = (host, port)
        
        # Create a TCP/IP socket
        self.m_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        # Connect the socket to the port where the server is listening
        self.m_socket.connect(self.m_server_address)

    def game(self):
        self.m_socket.sendall(self.packed_data)
        self.m_socket.settimeout(2.0)
        while 1:
                socket_list = [self.m_socket]
                # Get the list sockets which are readable
                read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [], 1)
                for sock in read_sockets:
                    #incoming message from remote server
                    if sock == self.m_socket:
                        data = sock.recv(256).strip()
                        if data:
                            unpacked_data = self.pack.unpack(data)
                            server_response = unpacked_data[0].decode()
                            print(server_response)
                            if server_response == "N":
                                self.lowBound = self.number
                                # implements binary search
                                if self.highBound - self.lowBound == 1:
                                    self.inputs = (self.equal.encode(), self.highBound - 1)
                                    self.packed_data = self.pack.pack(*self.inputs)
                                    self.m_socket.sendall(self.packed_data)
                                    self.m_socket.settimeout(2.0)
                                else:
                                    self.number = (self.number + self.highBound) // 2 
                                    self.inputs = (self.smaller.encode(), self.number)
                                    self.packed_data = self.pack.pack(*self.inputs)
                                    self.m_socket.sendall(self.packed_data)
                                    self.m_socket.settimeout(2.0)
                            if server_response == "I":
                                self.highBound = self.number
                                self.number = (self.number + self.lowBound) // 2 
                                self.inputs = (self.smaller.encode(), self.number)
                                self.packed_data = self.pack.pack(*self.inputs)
                                self.m_socket.sendall(self.packed_data)
                                self.m_socket.settimeout(2.0)
                if server_response == "Y":
                    self.m_socket.close()
                    break
                if server_response == "K":
                    self.m_socket.close()
                    break
                if server_response == "V":
                    self.m_socket.close()
                    break

host = sys.argv[1]
port = int(sys.argv[2])

client = Client(host, port)
client.connect()
client.game()
import socket
import struct
import operator
import select

class Server:
    def __init__(self, host, port):
        self.m_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.m_server_socket.bind((host, port))

    def sendToClient(self, fname, offset, timeout):
        # read data
        f = open(fname, "r")
        f_data = f.read()
        file_lenght = int(len(f_data) / offset) + 1
        f.close()
        
        # get start message
        data, client_address = self.m_server_socket.recvfrom(4096)        
        intial_byte_offset = 0

        for i in range(0, file_lenght):
            tmp =  f_data[i * offset :  (i + 1) * offset]
            str_length_of_data = str(len(tmp)) + "s"
            intial_byte_offset += len(tmp)
            string = ""    
            if i == file_lenght - 1:
                string = "last"
            else:
                string = "nope"

            header = struct.pack("4si", string.encode('utf-8'), intial_byte_offset)
            data = struct.pack(str_length_of_data, tmp.encode('utf-8'))

            self.m_server_socket.sendto(header, 0, client_address)
            self.m_server_socket.sendto(data, 0, client_address)
            self.m_server_socket.setblocking(0)

            while True:
                ready = select.select([self.m_server_socket], [], [], timeout)
                if ready[0]:
                    data = self.m_server_socket.recv(4096)
                    print("Client", data.decode('utf-8'))
                    break
                else:
                    print("Client missed package")
                    # send again
                    self.m_server_socket.sendto(header, 0, client_address)
                    self.m_server_socket.sendto(data, 0, client_address)

    def close(self):
        self.m_server_socket.close()


server =  Server('localhost', 8080)
server.sendToClient( 'lorem.txt', 1000, 0.2)
server.close()
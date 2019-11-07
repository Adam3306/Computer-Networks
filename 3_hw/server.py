import sys
import socket
import struct
import select
import random

class Server:
    def __init__(self, host, port):
        # server_addr = (host, port)
        self.m_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.m_server.settimeout(1.0)
        self.m_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.m_server.bind((host, port))
        self.m_server.listen(5)
        self.num = random.randint(1, 101)
        print("self num", self.num)
        self.m_unpacker = struct.Struct('1s I')

    def game(self):
        yes = "I"
        no = "N"
        lost = "K"
        win = "Y"
        over = "V"
        end = False
        inputs = [self.m_server]
        while inputs:
            timeout = 1
            readable, writeable, excpectable = select.select(inputs, inputs, inputs, timeout)
            if not (readable or writeable or excpectable):
                continue

            for s in readable:
                try:
                    if s is self.m_server:
                        client, client_addr = s.accept()
                        client.setblocking(1)
                        inputs.append(client)
                    else:
                        data = s.recv(256).strip()
                        if data:
                            self.m_unpackered_data = self.m_unpacker.unpack(data)
                            client_operator = self.m_unpackered_data[0].decode()
                            client_num = self.m_unpackered_data[1]
                            print(self.m_unpackered_data, self.num)
                            if not end:
                                if client_operator == ">":
                                    if self.num == client_num:
                                        msg = self.m_unpacker.pack(no.encode(), 1)
                                        s.send(msg)
                                    if self.num > client_num:
                                        msg = self.m_unpacker.pack(yes.encode(), 1)
                                        s.send(msg)
                                    if self.num < client_num:
                                        msg = self.m_unpacker.pack(no.encode(), 1)
                                        s.send(msg)
                                if client_operator == "<":
                                    if self.num == client_num:
                                        msg = self.m_unpacker.pack(no.encode(), 1)
                                        s.send(msg)
                                    if self.num < client_num:
                                        msg = self.m_unpacker.pack(yes.encode(), 1)
                                        s.send(msg)
                                    if self.num > client_num:
                                        msg = self.m_unpacker.pack(no.encode(), 1)
                                        s.send(msg)
                                if client_operator == "=":
                                    if self.num != client_num:
                                        msg = self.m_unpacker.pack(lost.encode(), 1)
                                        s.send(msg)
                                    if self.num == client_num:
                                        end = True
                                        msg = self.m_unpacker.pack(win.encode(), 1)
                                        s.send(msg)
                                        break
                            else:
                                msg = self.m_unpacker.pack(over.encode(), 1)
                                s.sendall(msg)
                        else:
                            if [s] is inputs:
                                end = False
                                self.num = random.randint(1, 101)
                                print("Client disconnected", self.num)
                            inputs.remove(s)
                            if s in writeable:
                                writeable.remove(s)
                            s.close()
                except socket.error as n:
                    print("Error", n)
                    if s in writeable:
                        writeable.remove(s)
                    s.close()

host = sys.argv[1]
port = sys.argv[2]

server = Server(host, int(port))
server.game()

import socket
import struct
from time import sleep


class Client:
	def __init__(self, host, port):
		self.m_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.m_server_addr = (host, port)
		self.m_last_offset = 0
		
	def saveDataFromServer(self, fname):
		file = open(fname, "a")
		self.m_client_socket.sendto("START".encode(), 0, self.m_server_addr)
		while True:
			header, addr = self.m_client_socket.recvfrom(4096)
			data, addr = self.m_client_socket.recvfrom(4096)
			header = struct.unpack("4si", header)
			if (self.m_last_offset == header[1]):
				print("Server missed receipt")
				self.m_client_socket.sendto("got data".encode(), 0, self.m_server_addr)
			else:
				str_length_of_data = str(header[1] - self.m_last_offset) + "s"
				self.m_last_offset = header[1]
				data = struct.unpack(str_length_of_data, data)
				self.m_client_socket.sendto("got data".encode(), 0, self.m_server_addr)
				file.write(data[0].decode('utf-8'))
			# TODO
			if (header[0].decode('utf-8') == 'last'): 
				file.close()
				break

	def close(self):
		self.m_client_socket.close()

client = Client('localhost', 8080)
client.saveDataFromServer("copy.txt")
client.close()
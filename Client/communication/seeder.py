from _thread import start_new_thread
import socket
import json
import random
# request: { file_name: , piece_seq_no: , piece_size: , file_size:  }

class Seeder:
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind(('localhost', 0))
		self.sock.listen()
		# t = threading.Thread(target=main_thread)
		# t.start()
		print(self.sock)
		while True:
			s, addr = self.sock.accept()
			print("New connection accepted: ", s, addr)
			start_new_thread(self.handle_new_conn, (s,)) # Create new thread with process and connection object

	def get_piece(self, file_name, seq_num, piece_size, file_size):
		start = seq_num * piece_size
		end = (seq_num + 1) * piece_size
		end = end if end <= file_size else file_size
		end = end - start
		print(start, end)
		
		with open(file_name, 'rb') as f:
			f.seek(start)
			ret = f.read(end)

		return ret
			
	def handle_new_conn(self, s):
		r = s.recv(1024).decode("utf-8").rstrip("\x00")
		request = json.loads(r)
		print(request)
		if request['file_name']:
			piece_bytes = self.get_piece(request['file_name'], request['piece_seq_no'], request['piece_size'], request['file_size'])
			print(piece_bytes)
			s.send(piece_bytes)
		print('Sent')


if __name__=='__main__':
	up = Seeder()


# from functools import reduce
# from dateutil import parser
# import threading
# import datetime
# import socket
# import time
# from timeit import default_timer as timer


# clients = list()

# def main_thread():
# 	while True:
# 		if not clients:
# 			print('No clients connected')
# 			time.sleep(5)
# 			continue

# 		deltas = list()
# 		for client in clients:
# 			try:
# 				client.send('ping'.encode())

# 				client_time = parser.parse(client.recv(1024).decode())
# 				server_time = datetime.datetime.now()

# 				deltas.append(server_time - client_time)
# 				print('Time', client_time, 'received from client with delta', deltas[-1])
# 			except:
# 				pass

# 		try:
# 			avg_delta = sum(deltas, datetime.timedelta(0, 0)) / len(deltas)
# 			print('Average delta:', avg_delta)
# 			sending_time = datetime.datetime.now() + avg_delta
# 			print('Synced time for clients:', sending_time,'\n')
# 		except:
# 			pass

# 		for client in clients:
# 			try:
# 				client.send(str(sending_time).encode())
# 			except:
# 				pass

# 		time.sleep(5)

# if __name__=='__main__':
# 	sock.bind(('localhost', 20000))

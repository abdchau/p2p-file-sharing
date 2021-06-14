from _thread import start_new_thread
import socket
import json
import time

from config import server, idh

class Seeder:
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind(('localhost', 0))
		self.sock.listen()
		print(self.sock)
	
	def loop(self):
		while True:
			try:
				server.broadcast_seeder_port(idh.id, self.sock)
				print(self.sock)
				print('Seeder port broadcasted')
				break
			except:
				print('Server not found for seeder, trying again in 3s...')
				time.sleep(3)

		while True:
			s, addr = self.sock.accept()
			print("New connection accepted: ", s, addr)
			start_new_thread(self.handle_new_conn, (s,))

	def get_piece(self, file_id, seq_num, piece_size, file_size):
		start = seq_num * piece_size
		end = (seq_num + 1) * piece_size
		end = end if end <= file_size else file_size
		end = end - start
		print(start, end)

		with open(idh.seeding[file_id], 'rb') as f:
			f.seek(start)
			ret = f.read(end)

		return ret
			
	def handle_new_conn(self, s):
		r = s.recv(1024).decode("utf-8").rstrip("\x00")
		request = json.loads(r)
		print(request)
		if request['file_id']:
			piece_bytes = self.get_piece(request['file_id'], request['piece_seq_no'], request['piece_size'], request['file_size'])
			s.send(piece_bytes)
		print('Sent')

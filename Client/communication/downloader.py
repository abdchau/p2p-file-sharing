from _thread import start_new_thread
import socket
import json
import os
import random
# request: { file_id: , piece_seq_no: }

peers = { 0: ['localhost', 56775] }

			# file_id: 
torrents = [ {'name': 'main.py', 'size': 414, 'piece_size': 128, 'pieces_info':
						[
							{'piece_seq_no': 0, 'peers': [0]},
							{'piece_seq_no': 1, 'peers': [0]},
							{'piece_seq_no': 2, 'peers': [0]}
						]
			} ]

class Downloader:
	def __init__(self, file_id):
		self.file_id = file_id
		self.downloaded = None

	def get_piece(self, seq_num, piece_size, file_size, peer):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((peer[0], peer[1]))
		request = json.dumps({ 'file_id': self.file_id, 'piece_seq_no': seq_num, 'piece_size': piece_size, 'file_size': file_size })
		sock.send(request.encode())
		print('Sent')
		response = sock.recv(1024)
		print('Received')
		sock.close()
		print(response)
		return response

	def write_piece(self, seq_num, piece_size, file_size, peer):
		start = seq_num * piece_size

		if not os.path.isfile('new'+self.file_id):
			open('new'+self.file_id, 'w').close()

		with open('new'+self.file_id, 'r+b') as f:
			f.seek(start)
			f.write(self.get_piece(seq_num, piece_size, file_size, peer))

	def download(self):
		file_info = next((item for item in torrents if item["name"] == self.file_id), None)
		if file_info is not None:
			for piece in file_info['pieces_info']:
				print(piece['piece_seq_no'], file_info['piece_size'], 0, peers[piece['peers'][0]])
				self.write_piece(piece['piece_seq_no'], file_info['piece_size'], 414, peers[piece['peers'][0]])

			


if __name__=='__main__':
	dn = Downloader('main.py')
	dn.download()

from _thread import start_new_thread
import socket
import json
import os
import random

from config import PIECE_SIZE, server

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
	def __init__(self, torrent_info):
		self.torrent_info = torrent_info
		self.downloaded = None
		self.peers = dict()

	def get_piece(self, seq_num, piece_size, file_size, peer):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((peer[0], peer[1]))
		request = json.dumps({ 'file_id': self.torrent_info['file_id'], 'piece_seq_no': seq_num,
					'piece_size': piece_size, 'file_size': self.torrent_info['size'] })
		sock.send(request.encode())
		print('Sent')
		response = sock.recv(1024)
		print('Received')
		sock.close()
		print(response)
		return response

	def write_piece(self, seq_num, piece_size, file_size, peer):
		start = seq_num * piece_size

		if not os.path.isfile('new'+self.torrent_info['file_id']):
			open('new'+self.torrent_info['file_id'], 'w').close()

		with open('new'+self.torrent_info['file_id'], 'r+b') as f:
			f.seek(start)
			f.write(self.get_piece(seq_num, piece_size, file_size, peer))

	def download(self):
		# self.torrent_info = next((item for item in torrents if item['id'] == self.torrent_info['file_id']), None)
		if self.torrent_info is not None:
			for piece in self.torrent_info['pieces_info']:
				if piece['peers'][0] not in self.peers:
					self.peers[piece['peers'][0]] = server.get_peer(piece['peers'][0])
				print(piece['piece_seq_no'], PIECE_SIZE, self.peers[piece['peers'][0]])
				self.write_piece(piece['piece_seq_no'], PIECE_SIZE, 414, self.peers[piece['peers'][0]])

			


if __name__=='__main__':
	dn = Downloader('main.py')
	dn.download()

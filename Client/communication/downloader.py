from _thread import start_new_thread
from threading import Lock
import socket
import json
import os
import time
import random

from config import server, idh

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
		# idh.peers = dict()

	def get_piece(self, seq_num, piece_size, peer):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((peer[0], peer[1]))
		request = json.dumps({ 'file_id': self.torrent_info['file_id'], 'piece_seq_no': seq_num,
					'piece_size': piece_size, 'file_size': self.torrent_info['size'] })
		sock.send(request.encode())
		print('Request for piece sent')
		response = sock.recv(1024)
		print('Piece received')
		sock.close()
		# print(response)
		return response

	def write_piece(self, file_name, seq_num, piece_size, peer):
		start = seq_num * piece_size

		if not os.path.isfile(file_name):
			open(file_name, 'w').close()

		data = self.get_piece(seq_num, piece_size, peer)
		while True:
			try:
				with open(file_name, 'r+b') as f:
					f.seek(start)
					f.write(data)
					f.flush()
				break
			except PermissionError as e:
				print(e.__str__())
				time.sleep(0.2)
		server.update_piece_peer(self.torrent_info['file_id'], seq_num, idh.id)

	def download(self):
		file_name = os.path.join('downloads', self.torrent_info['file_name'])
		os.makedirs('downloads', exist_ok=True)

		idh.downloading[self.torrent_info['file_id']] = self.torrent_info
		idh.dump_ids()

		if self.torrent_info['file_id'] not in idh.seeding:
			idh.seeding[self.torrent_info['file_id']] = os.path.abspath(file_name)
			idh.dump_ids()

		if self.torrent_info is not None:
			# random.shuffle(self.torrent_info['pieces_info'])
			for piece in random.sample(self.torrent_info['pieces_info'], len(self.torrent_info['pieces_info'])):
				idx = random.randint(0, len(piece['peers'])-1)
				print(idx, 'PEER NO. CHOSEN')
				# time.sleep(15)
				count = 0
				while True:
					if piece['peers'][idx] not in idh.peers:
						idh.peers[piece['peers'][idx]] = server.get_peer(piece['peers'][idx])
						idh.dump_ids()
					try:
						count+=1
						print(piece['piece_seq_no'], self.torrent_info['piece_size'], idh.peers[piece['peers'][idx]])
						self.write_piece(file_name, piece['piece_seq_no'], self.torrent_info['piece_size'], idh.peers[piece['peers'][idx]])
						break
					except ConnectionRefusedError:
						time.sleep(1)
						if count < 3:
							idh.peers[piece['peers'][idx]] = server.get_peer(piece['peers'][idx])
							idh.dump_ids()
						else:
							print('Peer appears offline. Selecting new peer...')
							idx = random.randint(0, len(piece['peers'])-1)
							print(idx, 'PEER NO. CHOSEN')

		print('Download complete! File:', self.torrent_info['file_name'])
		idh.downloading.pop(self.torrent_info['file_id'], None)
		idh.dump_ids()
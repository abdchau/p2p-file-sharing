from threading import Lock, Thread
from _thread import start_new_thread
import socket
import json
import os
import time
import random

from config import server, idh

class Downloader:
	def __init__(self, torrent_info):
		self.torrent_info = torrent_info
		self.downloaded = None
		self.info_lock = Lock()
		self.complete = False

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

		return response

	def update_peer_thread(self, seq_num):
		while True:
			try:
				server.update_piece_peer(self.torrent_info['file_id'], seq_num, idh.id)
				break
			except:
				print('Unable to update peer info (server down). Trying again in 3s...')
				time.sleep(3)

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
		try:
			server.update_piece_peer(self.torrent_info['file_id'], seq_num, idh.id)
		except:
			start_new_thread(self.update_peer_thread, (seq_num))

	def update_torrent_info(self):
		while not self.complete:
			time.sleep(5)
			try:
				self.info_lock.acquire()
				self.torrent_info = server.get_seeding_info([self.torrent_info['file_id']])[0]
			except:
				print('Server unavailable for backgroud peer updation.')
			self.info_lock.release()
		

	def download(self):
		updater_thread = Thread(target=self.update_torrent_info, daemon=True)
		updater_thread.start()

		file_name = os.path.join('downloads', self.torrent_info['file_name'])
		os.makedirs('downloads', exist_ok=True)

		idh.downloading[self.torrent_info['file_id']] = self.torrent_info
		idh.dump_ids()

		if self.torrent_info['file_id'] not in idh.seeding:
			idh.seeding[self.torrent_info['file_id']] = os.path.abspath(file_name)
			idh.dump_ids()

		if self.torrent_info is not None:
			lst = list(range(len(self.torrent_info['pieces_info'])))
			for i in lst:
				self.info_lock.acquire()
				idx = random.randint(0, len(self.torrent_info['pieces_info'][i]['peers'])-1)
				print(idx, 'PEER NO. CHOSEN')
				self.info_lock.release()
				# time.sleep(15)
				count = 0
				while True:
					self.info_lock.acquire()
					if self.torrent_info['pieces_info'][i]['peers'][idx] not in idh.peers:
						idh.peers[self.torrent_info['pieces_info'][i]['peers'][idx]] = server.get_peer(self.torrent_info['pieces_info'][i]['peers'][idx])
						idh.dump_ids()
					try:
						count+=1
						print(self.torrent_info['pieces_info'][i]['piece_seq_no'], self.torrent_info['piece_size'], idh.peers[self.torrent_info['pieces_info'][i]['peers'][idx]])
						self.write_piece(file_name, self.torrent_info['pieces_info'][i]['piece_seq_no'], self.torrent_info['piece_size'], idh.peers[self.torrent_info['pieces_info'][i]['peers'][idx]])
						count = 0
						self.info_lock.release()
						break
					except Exception:
						self.info_lock.release()
						time.sleep(1)
						if count < 3:
							try:
								idh.peers[self.torrent_info['pieces_info'][i]['peers'][idx]] = server.get_peer(self.torrent_info['pieces_info'][i]['peers'][idx])
								idh.dump_ids()
							except:
								print('Server down! Will keep trying until success')
						else:
							print('Peer appears offline. Selecting new peer...')
							idx = random.randint(0, len(self.torrent_info['pieces_info'][i]['peers'])-1)
							print(idx, 'PEER NO. CHOSEN')
							count = 0
		self.complete = True
		print('Download complete! File:', self.torrent_info['file_name'])
		idh.downloading.pop(self.torrent_info['file_id'], None)
		idh.dump_ids()
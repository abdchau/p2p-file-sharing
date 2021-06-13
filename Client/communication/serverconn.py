import requests

class ServerConn:
	def __init__(self):
		self.api_address = 'http://127.0.0.1:5000'

	def get_all_torrents(self):
		torrents = requests.get(self.api_address, json={})
		return torrents.json()

	def get_seeding_info(self, seeding):
		torrents = requests.get(self.api_address+'/seeding', json=seeding)
		return torrents.json()


	def get_torrents(self, query):
		torrents = requests.get(self.api_address, json={'torrent_name' : query})
		# print(torrents.json())
		return torrents.json()

	def upload_torrent(self,torrent_name, torrent_desc, file_id, file_name, size, pieces_info, piece_size):
		response = requests.post(self.api_address, json={"torrent_name":torrent_name, "torrent_description": torrent_desc,
									 "file_id" : file_id, 'file_name': file_name,
									 "size" : size, "pieces_info" : pieces_info, 'piece_size': piece_size})
		return response

	def broadcast_seeder_port(self, id, sock):
		print(id, sock.getsockname())
		response = requests.post(self.api_address+'/id', json={"id" : id, 'sock': sock.getsockname()})
		return response.text

	def get_peer(self, id):
		response = requests.get(self.api_address+'/peer', json={"id" : id})
		print(response.json(), 'PEER REQUESTED')
		return response.json()

	def update_piece_peer(self, file_id, piece_seq_no, new_peer):
		response = requests.post(self.api_address+'/piece', json={"file_id": file_id, 
												'piece_seq_no': piece_seq_no, 'new_peer': new_peer})
		return response.text
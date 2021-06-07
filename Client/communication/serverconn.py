import requests

class ServerConn:
	def __init__(self):
		self.api_address = 'http://127.0.0.1:5000'

	def get_torrents(self, query):
		torrents = requests.get(self.api_address, json={'file_name' : query})
		# print(torrents.json())
		return torrents.json()

	def upload_torrent(self, file_id, file_name, size, pieces_info):
		response = requests.post(self.api_address, json={"file_id" : file_id, 'file_name': file_name,
									 "size" : size, "pieces_info" : pieces_info})
		return response

	def broadcast_seeder_port(self, id, sock):
		print(id, sock.getsockname())
		response = requests.post(self.api_address+'/id', json={"id" : id, 'sock': sock.getsockname()})
		return response

	def get_peer(self, id):
		response = requests.get(self.api_address+'/peer', json={"id" : id})
		print(response.json())
		return response.json()
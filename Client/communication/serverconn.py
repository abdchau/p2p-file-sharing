import requests

class ServerConn:
	def __init__(self):
		self.api_address = 'http://127.0.0.1:5000'

	def get_torrents(self, query):
		torrents = requests.get(self.api_address, json={'file_id' : query})
		print(torrents.json())
		return torrents.json()

	def upload_torrent(self, file_id, file_name, size, pieces_info):
		response = requests.post(self.api_address, json={"file_id" : file_id, 'file_name': file_name,
									 "size" : size, "pieces_info" : pieces_info})
		return response

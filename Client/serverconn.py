import requests

class ServerConn:
	def __init__(self):
		self.api_address = 'http://127.0.0.1:5000'
		pass

	def get_torrents(self, query):
		torrents = requests.get(self.api_address, {'query' : query})
		return torrents

	def upload_torrent(self, name, owner_ip, size, pieces_info, peers_info):
		response = requests.post(self.api_address, json={"name" : name, "owner_ip" : owner_ip, "size" : size,
											"pieces_info" : pieces_info, "peers_info" : peers_info})
		return response

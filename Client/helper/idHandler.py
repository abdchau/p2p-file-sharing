import json
import requests

# ids_data = { 'id': , 'seeding': [ {'file_id': file_name} , ]}

class IDHandler:
	def __init__(self):
		self.__api_address = 'http://127.0.0.1:5000/id'
		self.ids_file = 'helper/ids_data.json'
		self.browse_file = 'helper/browse_data.json'
		self.seed_file = 'helper/seed_data.json'

		try:
			with open(self.ids_file, 'r') as f:
				data = json.load(f)
				self.id = data['id']
				self.seeding = data['seeding']
				self.downloading = data['downloading']
				self.peers = data['peers']
		except:
			self.id = self.get_id_from_server()
			self.seeding = dict()
			self.downloading = dict()
			self.peers = dict()
			self.dump_ids()
		
		try:
			with open(self.browse_file, 'r') as f:
				self.browse_data = json.load(f)
		except:
			self.browse_data = dict()
		try:
			with open(self.seed_file, 'r') as f:
				self.seed_data = json.load(f)
		except:
			self.seed_data = dict()
		print(self.id)

	def get_id_from_server(self):
		response = requests.get(self.__api_address).json()
		return response['id']

	def assign_id_to_file(self, file_name):
		file_id = self.get_id_from_server()
		self.seeding[file_id] = file_name
		self.dump_ids()
		return file_id

	def dump_ids(self):
		with open(self.ids_file, 'w') as f:
			json.dump({'id': self.id, 'seeding': self.seeding, 
			'downloading': self.downloading, 'peers': self.peers}, f)
	
	def dump_browse(self):
		with open(self.browse_file, 'w') as f:
			json.dump(self.browse_data, f)
	
	def dump_seed(self):
		with open(self.seed_file, 'w') as f:
			json.dump(self.seed_data, f)
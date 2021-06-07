import json
import requests

# ids_data = { 'id': , 'seeding': [ {'file_id': file_name} , ]}

class IDHandler:
	def __init__(self):
		self.__api_address = 'http://127.0.0.1:5000/id'
		self.ids_file = 'helper/ids_data.json'

		try:
			with open(self.ids_file, 'r') as f:
				data = json.load(f)
				self.id = data['id']
				self.seeding = data['seeding']
		except:
			with open(self.ids_file, 'w') as f:
				self.id = self.get_id_from_server()
				self.seeding = []
				json.dump({'id': self.id, 'seeding': self.seeding}, f)
		print(self.id)


	def get_id_from_server(self):
		response = requests.get(self.__api_address).json()
		return response['id']
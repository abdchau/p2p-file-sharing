from functools import partial
import time

from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


from config import server, seeder

class TorrentSummary(BoxLayout):
	pass


class HomeScreen(Screen):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# server = ServerConn()
		self.results = []
		self.downloadsArea.data = [{'torrent_name': result['name'], 'on_press': partial(self.torrent_info, content=result)} for result in [{'name':'test'}]]*5

	def on_enter(self, *args):
		self.manager.transition.direction = 'left'
		return super().on_enter(*args)

	def upload_torrent(self):
		self.manager.current = 'create_torrent'

	def search(self, query):
		print(query)

		try:
			start = time.process_time()
			self.results = server.get_torrents(query)
			if not self.results:
				content = Button(text='Dismiss')
				self.clear()
				popup = Popup(title="No results found!", content=content, size_hint=(0.4, 0.2), auto_dismiss=False)
				content.bind(on_press=popup.dismiss)
				popup.open()
			else:
				print(self.results)
				self.searchResultsArea.data = [{'torrentName': result['torrent_name'],
						'numPeers': 'Peers: '+ str(max([len(piece['peers']) for piece in result['pieces_info']])),
						'numPieces': 'Pieces: '+ str(len(result['pieces_info'])), 'torrentSize': 'Size: '+str(result['size'])+' bytes',
						'resultNum': i} for i, result in enumerate(self.results)]
				self.searchResultsArea.refresh_from_data()
			print("Elapsed Time: " + str(time.process_time() - start))
		except Exception as e:
			content = Button(text='Dismiss')
			popup = Popup(title="Server not found!", content=content, size_hint=(0.4, 0.2), auto_dismiss=False)

			content.bind(on_press=popup.dismiss)
			popup.open()
	
	def torrent_info(self, i):
		print('here')
		self.manager.current_torrent_info = self.results[i]
		self.manager.current = 'torrent_info'

	
	def clear(self):
		self.searchResultsArea.data = []
		self.searchBox.text = ""
		self.results = []
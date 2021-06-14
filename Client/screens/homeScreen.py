from functools import partial
import time
from _thread import start_new_thread

from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


from config import server, idh

class TorrentSummary(BoxLayout):
	pass


class HomeScreen(Screen):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.search_results = []
		self.update_browse()

	def update_browse(self):
		try:
			idh.browse_data = server.get_all_torrents()
			idh.dump_browse()
		except:
			print('Server not available. Cached browse data displayed.')
		self.browseArea.data = [{'torrentName': 'Name: '+result['torrent_name'],
						'numPeers': 'Peers: '+ str(max([len(piece['peers']) for piece in result['pieces_info']])),
						'numPieces': 'Pieces: '+ str(len(result['pieces_info'])), 'torrentSize': 'Size: '+str(result['size'])+' bytes',
						'resultNum': i, 'type': 'browse'} for i, result in enumerate(idh.browse_data)]
		self.browseArea.refresh_from_data()

	def update_download(self):
		# idh.browse_data = server.get_all_torrents()
		self.downloadsArea.data = [{'torrentName': 'Name: '+idh.downloading[key]['torrent_name'],
						'numPeers': 'Peers: '+ str(max([len(piece['peers']) for piece in idh.downloading[key]['pieces_info']])),
						'numPieces': 'Pieces: '+ str(len(idh.downloading[key]['pieces_info'])), 'torrentSize': 'Size: '+str(idh.downloading[key]['size'])+' bytes',
						'resultNum': i, 'type': 'down'} for i, key in enumerate(idh.downloading)]
		self.downloadsArea.refresh_from_data()

	def update_seed(self):
		try:
			idh.seed_data = server.get_seeding_info(list(idh.seeding.keys()))
			idh.dump_seed()
		except:
			print('Server not available. Cached seed data displayed.')
		
		self.seedsArea.data = [{'torrentName': 'Name: '+result['torrent_name'],
						'numPeers': 'Peers: '+ str(max([len(piece['peers']) for piece in result['pieces_info']])),
						'numPieces': 'Pieces: '+ str(len(result['pieces_info'])), 'torrentSize': 'Size: '+str(result['size'])+' bytes',
						'resultNum': i, 'type': 'browse'} for i, result in enumerate(idh.seed_data)]
		self.seedsArea.refresh_from_data()

	def on_enter(self, *args):
		self.manager.transition.direction = 'left'
		return super().on_enter(*args)

	def upload_torrent(self):
		self.manager.current = 'create_torrent'

	def search(self, query):
		print(query)

		try:
			start = time.process_time()
			self.search_results = server.get_torrents(query)
			if not self.search_results:
				content = Button(text='Dismiss')
				self.clear()
				popup = Popup(title="No results found!", content=content, size_hint=(0.4, 0.2), auto_dismiss=False)
				content.bind(on_press=popup.dismiss)
				popup.open()
			else:
				print(self.search_results)
				self.searchResultsArea.data = [{'torrentName': 'Name: '+'Name: '+result['torrent_name'],
						'numPeers': 'Peers: '+ str(max([len(piece['peers']) for piece in result['pieces_info']])),
						'numPieces': 'Pieces: '+ str(len(result['pieces_info'])), 'torrentSize': 'Size: '+str(result['size'])+' bytes',
						'resultNum': i, 'type': 'search'} for i, result in enumerate(self.search_results)]
				self.searchResultsArea.refresh_from_data()
			print("Elapsed Time: " + str(time.process_time() - start))
		except Exception as e:
			content = Button(text='Dismiss')
			popup = Popup(title="Server not found!", content=content, size_hint=(0.4, 0.2), auto_dismiss=False)

			content.bind(on_press=popup.dismiss)
			popup.open()
	
	def torrent_info(self, i, type):
		print('here')
		if type == 'search':
			self.manager.current_torrent_info = self.search_results[i]
		elif type == 'browse':
			self.manager.current_torrent_info = idh.browse_data[i]
		elif type == 'down':
			try: 
				self.manager.current_torrent_info = idh.downloading[list(idh.downloading.keys())[i]]
			except:
				content = Button(text='Dismiss')
				popup = Popup(title="Downloads information has changed. Reopen this tab to view up to date information.", 
					content=content, size_hint=(0.4, 0.2), auto_dismiss=False)

				content.bind(on_press=popup.dismiss)
				popup.open()
				return
		self.manager.current = 'torrent_info'

	
	def clear(self):
		self.searchResultsArea.data = []
		self.searchBox.text = ""
		self.search_results = []
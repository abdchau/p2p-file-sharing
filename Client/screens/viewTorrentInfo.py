from kivy.uix.screenmanager import Screen
from communication.downloader import Downloader

class ViewTorrentInfo(Screen):
	def __init__(self, **kw):
		super().__init__(**kw)
		self.torrent_info = None
		# self.title

	def on_enter(self, *args):
		super().on_enter(*args)
		self.tname.text = self.manager.current_torrent_info['name']
		self.tsize.text = self.manager.current_torrent_info['size']

	def download(self):
		dn = Downloader(self.manager.current_torrent_info['name'])
		# dn.download()
		print('Downloading...')
		pass
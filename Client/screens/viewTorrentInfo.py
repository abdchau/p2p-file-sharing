from _thread import start_new_thread

from kivy.uix.screenmanager import Screen
from communication.downloader import Downloader

class ViewTorrentInfo(Screen):
	def __init__(self, **kw):
		super().__init__(**kw)
		self.torrent_info = None
		# self.title

	def on_enter(self, *args):
		super().on_enter(*args)
		# print(self.manager.current_torrent_info)
		self.tname.text = self.manager.current_torrent_info['file_name']
		self.tsize.text = str(self.manager.current_torrent_info['size']) + ' bytes'

	def download(self):
		dn = Downloader(self.manager.current_torrent_info)
		start_new_thread(dn.download, ())
		print('Downloading...')
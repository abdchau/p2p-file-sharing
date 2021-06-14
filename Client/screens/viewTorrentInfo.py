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
		self.fname.text = self.manager.current_torrent_info['file_name']
		self.tsize.text = str(self.manager.current_torrent_info['size']) + ' bytes'
		
		self.tname.text = str(self.manager.current_torrent_info['torrent_name'])
		self.fid.text = str(self.manager.current_torrent_info['file_id'])
		self.tdesc.text = str(self.manager.current_torrent_info['torrent_description'])

		num_pieces = (self.manager.current_torrent_info['size'] - 1) // self.manager.current_torrent_info['piece_size'] + 1
		self.tpieces.text = str(num_pieces)
		self.psize.text = str(self.manager.current_torrent_info['piece_size'])
		npeers = str(max([len(piece['peers']) for piece in self.manager.current_torrent_info['pieces_info']]))
		self.npeers.text = str(npeers)

	def download(self):
		dn = Downloader(self.manager.current_torrent_info)
		start_new_thread(dn.download, ())
		print('Downloading...')
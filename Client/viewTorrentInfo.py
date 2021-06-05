from kivy.uix.screenmanager import Screen

class ViewTorrentInfo(Screen):
	def __init__(self, **kw):
		super().__init__(**kw)
		self.torrent_info = None
		# self.title

	def on_enter(self, *args):
		super().on_enter(*args)
		self.tname.text = self.manager.current_torrent_info['name']
		return
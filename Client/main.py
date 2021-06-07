from random import sample
import os
from string import ascii_lowercase
from flask.wrappers import Response

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from screens.homeScreen import HomeScreen
from screens.viewTorrentInfo import ViewTorrentInfo
from screens.createTorrent import CreateTorrent

for layout in os.listdir('layouts'):
	Builder.load_file(os.path.join('layouts', layout))


class MyManager(ScreenManager):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.add_widget(HomeScreen())
		self.add_widget(ViewTorrentInfo())
		self.add_widget(CreateTorrent())
		self.current_torrent_info = None
		# self.ti

class TorrentApp(App):
	def build(self):	
		return MyManager()


if __name__ == '__main__':
	TorrentApp().run()
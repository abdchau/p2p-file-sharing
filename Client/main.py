from random import sample
import os
from string import ascii_lowercase
from flask.wrappers import Response

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from homeScreen import HomeScreen
from viewTorrentInfo import ViewTorrentInfo

for layout in os.listdir('layouts'):
	Builder.load_file(os.path.join('layouts', layout))


class MyManager(ScreenManager):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.add_widget(HomeScreen())
		self.add_widget(ViewTorrentInfo())
		self.current_torrent_info = None
		# self.ti

class TorrentApp(App):
	def build(self):	
		return MyManager()


if __name__ == '__main__':
	TorrentApp().run()
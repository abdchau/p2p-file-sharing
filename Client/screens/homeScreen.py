from functools import partial
import time

from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.button import Button

from config import server, seeder

class HomeScreen(Screen):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# server = ServerConn()
		self.downloadsArea.data = [{'text': result['name'], 'on_press': partial(self.torrent_info, content=result)} for result in [{'name':'test'}]]*5

	def upload_torrent(self):
		self.manager.current = 'create_torrent'

	def search(self, query):
		print(query)

		try:
			start = time.process_time()
			results = server.get_torrents(query)
			if not results:
				content = Button(text='Dismiss')
				self.clear()
				popup = Popup(title="No results found!", content=content, size_hint=(0.4, 0.2), auto_dismiss=False)
				content.bind(on_press=popup.dismiss)
				popup.open()
			else:
				self.resultArea.data = [{'text': result['name'], 'on_press': partial(self.torrent_info, content=result)} for result in results]
				self.resultArea.refresh_from_data()
			print("Elapsed Time: " + str(time.process_time() - start))
		except Exception as e:
			content = Button(text='Dismiss')
			popup = Popup(title=e.__str__(), content=content, size_hint=(0.4, 0.2), auto_dismiss=False)

			content.bind(on_press=popup.dismiss)
			popup.open()
	
	def torrent_info(self, content):
		self.manager.current_torrent_info = content
		self.manager.current = 'torrent_info'

	def clear(self):
		self.resultArea.data = []
		self.search_box.text = ""
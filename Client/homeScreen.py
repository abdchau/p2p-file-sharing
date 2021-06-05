from functools import partial
import time

from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout

from serverconn import ServerConn


class WrappedLabel(Label):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.bind(
			width=lambda *x:
			self.setter('text_size')(self, (self.width, None)),
			texture_size=lambda *x: self.setter('height')(self, self.texture_size[1]))

class TorrentView(Popup):
	def __init__(self, content):
		super().__init__(title=content['name'], size_hint=(1., 1.))
		self.title_size = 20
		box = BoxLayout(orientation='vertical', spacing=10, padding=10)
		box.add_widget(WrappedLabel(text=content['owner_ip'], size_hint=(1.0, 0.2), font_size="14sp"))
		scroll = ScrollView()
		scroll.add_widget(WrappedLabel(text=content['size'], size_hint=(1.0, None), font_size="20sp"))
		box.add_widget(scroll)

		box.add_widget(Button(text="Download", on_press=self.dismiss, size_hint=(1., 0.15)))
		box.add_widget(Button(text="Back", on_press=self.dismiss, size_hint=(1., 0.15)))
		self.content = box
		self.open()

class HomeScreen(Screen):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.server = ServerConn()
		self.downloadsArea.data = [{'text': result['name'], 'on_press': partial(self.torrent_info, content=result)} for result in [{'name':'test'}]]*5

	def upload_torrent(self):
		response = self.server.upload_torrent('name', 'owner_ip', 'size', 'pieces_info', 'peers_info')
		content = Button(text='Dismiss')
		popup = Popup(title=response.text, content=content, size_hint=(0.5, 0.2), auto_dismiss=False)

		content.bind(on_press=popup.dismiss)
		popup.open()
		# self.searcher.lexicon = load_lexicon(update=True)

	def search(self, query):
		print(query)

		try:
			start = time.process_time()
			results = self.server.get_torrents(query)
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

	def open_torrent(self, content=None):
		return TorrentView(content)
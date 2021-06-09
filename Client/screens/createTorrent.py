from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import os

from config import server, idh

class Chooser(FileChooserListView):
	def __init__(self, ct, **kwargs):
		super().__init__(**kwargs)
		self.ct = ct
		print('Chooser initialized')

	def on_submit(self, selected, touch):
		self.ct.file_selected(selected[0])
		# return super().on_submit(selected, touch=touch)

class FileChooserPopup(Popup):
	def __init__(self, ct):
		super().__init__(title='Choose File', size_hint=(1., 1.))
		self.title_size = 20
		box = BoxLayout(orientation='vertical', spacing=10, padding=10)
		# box.add_widget(WrappedLabel(text=content['owner_ip'], size_hint=(1.0, 0.2), font_size="14sp"))
		# scroll = ScrollView()
		# scroll.add_widget(WrappedLabel(text=content['size'], size_hint=(1.0, None), font_size="20sp"))
		# box.add_widget(scroll)
		fc = Chooser(ct)
		box.add_widget(fc)
		box.add_widget(Button(text="Okay", on_press=self.dismiss, size_hint=(1., 0.15)))
		self.content = box
		# self.parent = parent
		self.open()


class CreateTorrent(Screen):

	def __init__(self, **kw):
		super().__init__(**kw)
		self.torrent_info = None
		# server = ServerConn()
		self.piece_size = 256
		self.piece_size_dict = {'256B': 256, '1KB': 1024, '1MB': 2**20, '4MB': 2**22, '512KB': 2**19}
		self.file_name = None
		self.torrent_name = None
		self.torrent_desc = None

	def on_enter(self, *args):
		super().on_enter(*args)
		self.file_name = None
		# self.tname.text = self.manager.current_torrent_info['name']

	def choose_file(self):
		print('choosing file')
		FileChooserPopup(self)
		print(self.file_name)
		# fc.open()

	def file_selected(self, file_name):
		self.file_name = file_name
		self.name_label.text = self.file_name if len(self.file_name) < 50 else '...'+self.file_name[-47:]
		print(self.file_name)

	def set_piece_size(self, piece_size):
		self.piece_size = self.piece_size_dict[piece_size]
		print(self.piece_size)

	def create_torrent(self):
		
		if self.torrent_name is None or self.torrent_name == "":
			content = Button(text='Dismiss')
			popup = Popup(title="No name entered!", content=content, size_hint=(0.4, 0.2), auto_dismiss=False)
			content.bind(on_press=popup.dismiss)
			popup.open()
			return
		
		if self.torrent_desc is None or self.torrent_desc == "":
			content = Button(text='Dismiss')
			popup = Popup(title="No description entered!", content=content, size_hint=(0.4, 0.2), auto_dismiss=False)
			content.bind(on_press=popup.dismiss)
			popup.open()
			return

		if self.file_name is None:
			content = Button(text='Dismiss')
			popup = Popup(title="No file selected!", content=content, size_hint=(0.4, 0.2), auto_dismiss=False)
			content.bind(on_press=popup.dismiss)
			popup.open()
			return

		self.upload_torrent()

	def set_torrent_name(self, name):
		self.torrent_name = name

	def set_torrent_description(self, desc):
		self.torrent_desc = desc

	def upload_torrent(self):
		size = os.stat(self.file_name).st_size
		num_pieces = (size - 1) // self.piece_size + 1
		print(size)
		
		file_id = idh.assign_id_to_file(self.file_name)
		pieces_info = [{'piece_seq_no': i, 'peers': [idh.id]} for i in range(num_pieces)]
		file_name = os.path.basename(self.file_name)
		response = server.upload_torrent(self.torrent_name, self.torrent_desc, file_id, file_name, size, pieces_info, self.piece_size)
		content = Button(text='Dismiss')
		popup = Popup(title=response.text, content=content, size_hint=(0.5, 0.2), auto_dismiss=False)

		content.bind(on_press=popup.dismiss)
		popup.open()
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button

class Chooser(FileChooserListView):
	def __init__(self, ct, **kwargs):
		super().__init__(**kwargs)
		self.ct = ct
		print('Chooser initialized')

	def on_submit(self, selected, touch):
		self.ct.file_selected(selected[0])
		return super().on_submit(selected, touch=touch)

class FileChooserPopup(Popup):
	def __init__(self, ct):
		super().__init__(title='Choose File', size_hint=(1., 1.))
		self.title_size = 20
		box = BoxLayout(orientation='vertical', spacing=10, padding=10)
		
		fc = Chooser(ct)
		box.add_widget(fc)
		box.add_widget(Button(text="Okay", on_press=self.dismiss, size_hint=(1., 0.15)))
		self.content = box
		
		self.open()
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.label import Label


class SongRow(BoxLayout):
    title = StringProperty("")
    artist = StringProperty("")
    song_id = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(orientation="horizontal", **kwargs)
        self.add_widget(Label(text=self.title))

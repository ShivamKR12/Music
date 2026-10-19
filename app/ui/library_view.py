from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import ButtonBehavior

from ui.widgets import SongRow

class ClickableSongRow(ButtonBehavior, SongRow):
    def on_press(self):
        rv = self.parent.parent
        song = rv.db.get_song_by_id(self.song_id)
        rv.on_song_selected(song)


class LibraryView(RecycleView):
    def __init__(self, db, source_filter=None, on_song_selected=None, **kwargs):
        super().__init__(**kwargs)
        self.db = db
        self.source_filter = source_filter
        self.on_song_selected = on_song_selected

        self.viewclass = 'ClickableSongRow'

        layout = RecycleBoxLayout(
            default_size=(None, 48),
            default_size_hint=(1, None),
            size_hint_y=None,
            orientation='vertical'
        )
        layout.bind(minimum_height=layout.setter('height'))

        self.layout_manager = layout
        self.add_widget(layout)

        self.refresh()
    
    def refresh(self):
        if self.source_filter:
            songs = self.db.get_songs_by_source(self.source_filter)
        else:
            songs = self.db.get_all_songs()

        self.data = [{
            'title': row['title'],
            'artist': row['artist'],
            'song_id': row['id']
        } for row in songs]

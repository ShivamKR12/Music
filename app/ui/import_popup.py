from pathlib import Path
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.button import Button
from kivy.uix.popup import Popup

from library.local_scanner import scan_folder


class ImportPopup:
    def __init__(self, db, on_done):
        self.db = db
        self.on_done = on_done

    def open(self):
        music_dir = Path.home() / "Music"

        chooser = FileChooserIconView(
            path=str(music_dir),
            dirselect=True
        )

        select_btn = Button(text="Select This Folder", size_hint_y=None, height=40)

        layout = BoxLayout(orientation="vertical")
        layout.add_widget(chooser)
        layout.add_widget(select_btn)

        popup = Popup(
            title="Select Music Folder",
            content=layout,
            size_hint=(0.9, 0.9)
        )

        def on_select(*_):
            folder = chooser.path
            popup.dismiss()

            songs = scan_folder(folder)
            for song in songs:
                self.db.add_song(song)

            self.on_done(len(songs))

        select_btn.bind(on_press=on_select)
        popup.open()

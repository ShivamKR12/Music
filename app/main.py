# main.py

from kivy.app import App
from ui.screens import PlayerUI


class MusicApp(App):
    def build(self):
        return PlayerUI()


if __name__ == '__main__':
    MusicApp().run()

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock


class MiniPlayer(BoxLayout):
    def __init__(self, engine, **kwargs):
        super().__init__(
            orientation="horizontal",
            size_hint_y=None,
            height=50,
            **kwargs
        )

        self.engine = engine

        self.title = Label(text="No song playing")
        self.play_pause = Button(text="▶")

        self.play_pause.bind(on_press=self.toggle)

        self.add_widget(self.title)
        self.add_widget(self.play_pause)

        # Update UI periodically
        Clock.schedule_interval(self.update, 0.5)

    def toggle(self, *_):
        self.engine.toggle_pause()

    def update(self, dt):
        if not self.engine.player:
            self.title.text = "No song playing"
            self.play_pause.text = "▶"
            return

        self.title.text = "Playing audio"
        self.play_pause.text = "⏸" if not self.engine.paused else "▶"

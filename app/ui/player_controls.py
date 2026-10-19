from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock


class PlayerControls(BoxLayout):
    def __init__(self, engine, on_play_pressed, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        self.engine = engine
        self.on_play_pressed = on_play_pressed

        # --- Buttons ---
        buttons = BoxLayout(size_hint_y=None, height=40)
        self.play_btn = Button(text="Play")
        self.pause_btn = Button(text="Pause")

        self.play_btn.bind(on_press=lambda *_: self.on_play_pressed())
        self.pause_btn.bind(on_press=lambda *_: self.engine.toggle_pause())

        buttons.add_widget(self.play_btn)
        buttons.add_widget(self.pause_btn)

        # --- Status ---
        self.status = Label(text="Idle")

        # --- Progress ---
        self.progress = ProgressBar(max=1, value=0)
        self.time_label = Label(text="00:00 / 00:00")

        self.add_widget(buttons)
        self.add_widget(self.status)
        self.add_widget(self.progress)
        self.add_widget(self.time_label)

        Clock.schedule_interval(self.update, 0.1)

    def set_status(self, text):
        self.status.text = text

    def update(self, dt):
        if not self.engine.player:
            return

        self.progress.max = self.engine.duration or 1
        self.progress.value = min(self.engine.elapsed, self.engine.duration)
        self._update_time()

    def _update_time(self):
        def fmt(s):
            return f"{int(s//60):02}:{int(s%60):02}"

        self.time_label.text = (
            f"{fmt(self.engine.elapsed)} / {fmt(self.engine.duration)}"
        )

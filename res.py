from kivy.config import Config
Config.set('graphics', 'fullscreen', 'auto')
Config.write()  # Saves the configuration   

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout


class ResolutionApp(App):
    def build(self):
        width, height = Window.size

        # Calculate aspect ratio
        def simplify_ratio(w, h):
            from math import gcd
            g = gcd(int(w), int(h))
            return int(w / g), int(h / g)

        ar_w, ar_h = simplify_ratio(width, height)

        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        resolution_label = Label(
            text=f"Screen Resolution:\n{int(width)} x {int(height)}",
            font_size="20sp"
        )

        aspect_ratio_label = Label(
            text=f"Aspect Ratio:\n{ar_w}:{ar_h}",
            font_size="20sp"
        )

        layout.add_widget(resolution_label)
        layout.add_widget(aspect_ratio_label)

        return layout


if __name__ == "__main__":
    ResolutionApp().run()

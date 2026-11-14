import os
import sys
import time

os.environ["KIVY_HEADLESS"] = "1"
os.chdir(os.path.abspath('KivyMusicApp'))
sys.path.insert(0, os.path.abspath('.'))

from kivy.clock import Clock
from views.components import MarqueeLabel

from kivymd.app import MDApp

class TestApp(MDApp):
    def build(self):
        return None

def test_marquee():
    app = TestApp()
    app.theme_cls.theme_style = "Light"
    
    # Long text: exceeds 200dp width
    long_label = MarqueeLabel(
        text="Dil Lutiya | Jazzy B | Ft. Apache Indian | Sukshinder | Romeo | Jihne Mera Dil Luteya | Punjabi Hits",
        size_hint=(None, None),
        size=("200dp", "30dp")
    )
    from kivy.core.window import Window
    Window.add_widget(long_label)
    
    # Tick clock to process _check_overflow
    for _ in range(10):
        Clock.tick()
        time.sleep(0.02)
        
    print(f"Long label text width: {long_label._label.texture_size[0]} vs container width: {long_label.width}")
    assert long_label._label.texture_size[0] > long_label.width, "Text should exceed container width!"
    assert long_label._anim is not None, "Marquee animation should be active for overflowing text!"
    
    # Short text: fits within 200dp width
    short_label = MarqueeLabel(
        text="Short Song",
        size_hint=(None, None),
        size=("200dp", "30dp")
    )
    Window.add_widget(short_label)
    for _ in range(10):
        Clock.tick()
        time.sleep(0.02)
        
    print(f"Short label text width: {short_label._label.texture_size[0]} vs container width: {short_label.width}")
    assert short_label._label.texture_size[0] <= short_label.width, "Text should fit within container width!"
    assert short_label._anim is None, "Marquee animation should not be active for fitting text!"
    
    print("SUCCESS: MARQUEE LABEL VERIFICATION TEST PASSED!")

if __name__ == "__main__":
    test_marquee()

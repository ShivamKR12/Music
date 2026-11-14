import os
import sys

os.environ["KIVY_HEADLESS"] = "1"
APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "KivyMusicApp"))
os.chdir(APP_DIR)
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.card import MDCard
from kivymd.uix.list import MDListItem
from kivy.properties import StringProperty, ObjectProperty

# Define Python classes with properties FIRST
class TestHomeCardItem(MDCard):
    title = StringProperty("Unknown Title")
    artist = StringProperty("Unknown Artist")
    artwork = StringProperty("album_art.png")
    track_obj = ObjectProperty(None, allownone=True)

class TestTrackListItem(MDListItem):
    title = StringProperty("")
    artist = StringProperty("")
    artwork = StringProperty("album_art.png")
    track_obj = ObjectProperty(None, allownone=True)

test_kv = '''
<TestHomeCardItem>:
    style: "elevated"
    size_hint: None, None
    size: "140dp", "206dp"
    radius: [dp(16)]
    padding: ["8dp", "8dp", "8dp", "8dp"]
    md_bg_color: app.theme_cls.surfaceContainerColor
    
    MDBoxLayout:
        orientation: "vertical"
        spacing: "6dp"
        size_hint: 1, 1
        
        FitImage:
            source: root.artwork if root.artwork else "album_art.png"
            size_hint: 1, None
            height: "124dp"
            radius: [dp(12), dp(12), dp(12), dp(12)]
            
        MDBoxLayout:
            orientation: "vertical"
            spacing: "2dp"
            size_hint_y: None
            height: "56dp"
            
            MDLabel:
                text: root.title
                font_style: "Title"
                role: "small"
                bold: True
                adaptive_height: True
                max_lines: 1
                shorten: True
                shorten_from: "right"
                
            MDLabel:
                text: root.artist
                font_style: "Body"
                role: "small"
                adaptive_height: True
                max_lines: 1
                shorten: True
                shorten_from: "right"
                theme_text_color: "Custom"
                text_color: app.theme_cls.onSurfaceVariantColor

<TestTrackListItem>:
    radius: [16, 16, 16, 16]
    md_bg_color: app.theme_cls.surfaceContainerColor
    
    MDListItemLeadingAvatar:
        source: root.artwork if root.artwork else "album_art.png"
        radius: [dp(8), dp(8), dp(8), dp(8)]
        
    MDListItemHeadlineText:
        text: root.title
        
    MDListItemSupportingText:
        text: root.artist
'''

Builder.load_string(test_kv)

class ScratchTestApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        from kivymd.uix.boxlayout import MDBoxLayout
        box = MDBoxLayout(orientation="vertical")
        return box

app = ScratchTestApp()
app.root = app.build()

card = TestHomeCardItem()
card.title = "Test Song"
card.artist = "Test Artist"
card.artwork = "album_art.png"
app.root.add_widget(card)

item = TestTrackListItem()
item.title = "List Song"
item.artist = "List Artist"
item.artwork = "album_art.png"
app.root.add_widget(item)

for _ in range(5):
    Clock.tick()

print("Test components built successfully!")
print("Card size:", card.size)
print("Item size:", item.size)

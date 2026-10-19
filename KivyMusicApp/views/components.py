from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivymd.uix.list import MDListItem

Builder.load_string('''
<TrackListItem>:
    radius: [16, 16, 16, 16]
    md_bg_color: app.theme_cls.surfaceContainerColor
    
    MDListItemLeadingIcon:
        icon: "music-note"
        
    MDListItemHeadlineText:
        text: root.title
        
    MDListItemSupportingText:
        text: root.artist
''')

class TrackListItem(MDListItem):
    title = StringProperty("")
    artist = StringProperty("")
    track_obj = ObjectProperty(None)
    
    def on_release(self):
        from kivymd.app import MDApp
        if self.track_obj:
            MDApp.get_running_app().play_selected_track(self.track_obj)

Builder.load_string('''
<SearchHistoryItem>:
    MDListItemLeadingIcon:
        icon: "history"
    MDListItemHeadlineText:
        text: root.text
    MDListItemTrailingIcon:
        icon: "arrow-top-right"

<HomeCardItem>:
    style: "elevated"
    size_hint: None, None
    size: "140dp", "140dp"
    md_bg_color: app.theme_cls.surfaceContainerColor
    radius: [dp(16)]
    ripple_behavior: True
    MDRelativeLayout:
        MDBoxLayout:
            orientation: "vertical"
            padding: "8dp"
            spacing: "8dp"
            pos_hint: {"center_x": .5, "center_y": .5}
            adaptive_height: True
            MDIcon:
                icon: "album"
                pos_hint: {"center_x": .5}
                font_size: "64sp"
                adaptive_height: True
            MDLabel:
                text: root.text
                halign: "center"
                font_style: "Body"
                role: "medium"
                adaptive_height: True
''')

class SearchHistoryItem(MDListItem):
    text = StringProperty("")

from kivymd.uix.card import MDCard
class HomeCardItem(MDCard):
    text = StringProperty("")

from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivymd.uix.list import MDListItem
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.recycleview import RecycleView
from kivy.metrics import dp
from kivy.factory import Factory
import random

class DirectionalHorizontalScrollMixin:
    """
    Mixin for horizontal scroll containers (ScrollView, RecycleView) to enable
    bidirectional gesture arbitration in nested scrolling layouts:
    - Yields to parent vertical scroll container when user intent is vertical (|dy| > |dx|).
    - Smoothly absorbs and processes horizontal gestures when user intent is horizontal (|dx| > |dy|).
    - Delegates mouse wheel scrolling ('scrollup', 'scrolldown') to parent vertical scroll container.
    """
    def __init__(self, **kwargs):
        kwargs.setdefault('do_scroll_x', True)
        kwargs.setdefault('do_scroll_y', False)
        super().__init__(**kwargs)

    def on_scroll_start(self, touch, check_children=True):
        # 1. Forward desktop mouse wheel vertical scroll to parent vertical container
        if getattr(touch, "button", None) in ("scrollup", "scrolldown"):
            return False
        
        # 2. Track initial touch position for touch drag gesture arbitration
        touch.ud[f'{id(self)}_start_pos'] = (touch.x, touch.y)
        touch.ud[f'{id(self)}_locked'] = None
        
        # Initialize child's own effect
        super().on_scroll_start(touch, check_children=check_children)
        # Return False to allow parent vertical scroll container to also initialize its effect_y
        return False

    def on_scroll_move(self, touch):
        start_pos = touch.ud.get(f'{id(self)}_start_pos')
        locked = touch.ud.get(f'{id(self)}_locked')

        if start_pos and locked is None:
            dx = abs(touch.x - start_pos[0])
            dy = abs(touch.y - start_pos[1])
            slop = dp(8)
            if dx > slop or dy > slop:
                if dy > dx * 1.1:
                    touch.ud[f'{id(self)}_locked'] = 'v'
                else:
                    touch.ud[f'{id(self)}_locked'] = 'h'

        if touch.ud.get(f'{id(self)}_locked') == 'v':
            # Yield to parent vertical scrollview so it scrolls smoothly
            return False

        return super().on_scroll_move(touch)

class DirectionalHorizontalScrollView(DirectionalHorizontalScrollMixin, MDScrollView):
    """Horizontal MDScrollView with directional gesture arbitration."""
    pass

class DirectionalHorizontalRecycleView(DirectionalHorizontalScrollMixin, RecycleView):
    """Horizontal RecycleView with directional gesture arbitration."""
    pass

Factory.register('DirectionalHorizontalScrollView', cls=DirectionalHorizontalScrollView)
Factory.register('DirectionalHorizontalRecycleView', cls=DirectionalHorizontalRecycleView)


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
        app = MDApp.get_running_app()
        if self.track_obj:
            app.play_selected_track(self.track_obj)
        elif hasattr(app, "playlist_model") and app.playlist_model.tracks:
            # Fallback to playing first or random track
            track = random.choice(app.playlist_model.tracks)
            app.play_selected_track(track)

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

    def on_release(self):
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        if hasattr(app, "perform_search"):
            app.perform_search(self.text)
        elif hasattr(app, "root") and app.root and hasattr(app.root, "ids") and "screen_manager" in app.root.ids:
            try:
                search_screen = app.root.ids.screen_manager.get_screen("search")
                if "search_input" in search_screen.ids:
                    search_screen.ids.search_input.text = self.text
            except Exception:
                pass

class HomeCardItem(MDCard):
    text = StringProperty("")

    def on_release(self):
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        if hasattr(app, "playlist_model") and app.playlist_model.tracks:
            track = random.choice(app.playlist_model.tracks)
            app.play_selected_track(track)

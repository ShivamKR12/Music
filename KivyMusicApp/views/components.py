from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty, ColorProperty, NumericProperty
from kivymd.uix.list import MDListItem
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.scrollview import ScrollView
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.recycleview import RecycleView
from kivy.metrics import dp
from kivy.factory import Factory
import random

class MarqueeLabel(ScrollView):
    """
    A single-line auto-scrolling label for song titles, artist names, and metadata:
    - Strictly constrained to a single line (prevents layout and container overflow).
    - If text fits within the available width:
        - When halign == 'center': centers the text cleanly.
        - When halign == 'left': aligns to the left edge.
    - If text exceeds the available width:
        - Smooth ping-pong horizontal marquee animation (pauses at start/end).
        - User can freely drag or swipe horizontally to read any part manually.
        - Animation pauses during user touch and automatically resumes on release.
    """
    text = StringProperty("")
    font_style = StringProperty("Body")
    role = StringProperty("medium")
    bold = BooleanProperty(False)
    text_color = ColorProperty(None, allownone=True)
    halign = StringProperty("left")
    speed = NumericProperty(28.0)

    def __init__(self, **kwargs):
        kwargs.setdefault('do_scroll_y', False)
        kwargs.setdefault('do_scroll_x', True)
        kwargs.setdefault('bar_width', 0)
        kwargs.setdefault('size_hint_y', None)
        kwargs.setdefault('effect_cls', 'ScrollEffect')
        super().__init__(**kwargs)
        if not self.height or self.height == 100:
            self.height = "24dp"
        self._anim = None
        self._label = MDLabel(
            text=self.text,
            font_style=self.font_style,
            role=self.role,
            bold=self.bold,
            halign=self.halign,
            adaptive_size=True,
            height=self.height
        )
        self.bind(text=self._on_prop_change)
        self.bind(font_style=self._on_prop_change)
        self.bind(role=self._on_prop_change)
        self.bind(bold=self._on_prop_change)
        self.bind(halign=self._on_prop_change)
        self.bind(text_color=self._on_text_color)
        self.bind(width=self._schedule_marquee)
        self._label.bind(texture_size=self._schedule_marquee)
        self.add_widget(self._label)
        self._schedule_marquee()

    def _on_prop_change(self, *args):
        self._label.text = self.text
        self._label.font_style = self.font_style
        self._label.role = self.role
        self._label.bold = self.bold
        self._label.halign = self.halign
        self._schedule_marquee()

    def _on_text_color(self, *args):
        if self.text_color:
            self._label.theme_text_color = "Custom"
            self._label.text_color = self.text_color
        else:
            self._label.theme_text_color = "Primary"

    def _schedule_marquee(self, *args):
        Clock.unschedule(self._update_marquee)
        Clock.schedule_once(self._update_marquee, 0.05)

    def _update_marquee(self, dt):
        if self._anim:
            self._anim.cancel(self)
            self._anim = None

        container_w = self.width
        self._label.text_size = (None, None)
        self._label.texture_update()
        tex_w = self._label.texture_size[0]

        if container_w <= 0:
            return

        if tex_w <= container_w:
            # Fits within view: size label to container so halign aligns properly
            self._label.adaptive_size = False
            self._label.size_hint = (None, None)
            self._label.width = container_w
            self._label.height = self.height
            self.scroll_x = 0
        else:
            # Overflows view: size label to text width and start marquee animation with reading pauses
            self._label.adaptive_size = False
            self._label.size_hint = (None, None)
            self._label.width = tex_w
            self._label.height = self.height
            self.scroll_x = 0.0
            diff = tex_w - container_w
            dur = max(2.5, diff / float(self.speed))
            self._anim = (
                Animation(duration=2.5) +
                Animation(scroll_x=1.0, duration=dur, t='linear') +
                Animation(duration=2.0) +
                Animation(scroll_x=0.0, duration=dur, t='linear') +
                Animation(duration=2.5)
            )
            self._anim.repeat = True
            self._anim.start(self)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self._anim:
                self._anim.cancel(self)
                self._anim = None
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        res = super().on_touch_up(touch)
        if self.collide_point(*touch.pos):
            self._schedule_marquee()
        return res

Factory.register('MarqueeLabel', cls=MarqueeLabel)

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

from kivymd.uix.fitimage import FitImage

class TrackListItem(MDListItem):
    title = StringProperty("")
    artist = StringProperty("")
    artwork = StringProperty("album_art.png")
    track_obj = ObjectProperty(None, allownone=True)
    
    def on_release(self):
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        if self.track_obj:
            app.play_selected_track(self.track_obj)
        elif hasattr(app, "playlist_model") and app.playlist_model.tracks:
            track = random.choice(app.playlist_model.tracks)
            app.play_selected_track(track)

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
    title = StringProperty("Unknown Title")
    artist = StringProperty("Unknown Artist")
    artwork = StringProperty("album_art.png")
    text = StringProperty("")
    track_obj = ObjectProperty(None, allownone=True)

    def on_release(self):
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        if hasattr(self, "track_obj") and self.track_obj:
            app.play_selected_track(self.track_obj)
        elif hasattr(app, "playlist_model") and app.playlist_model.tracks:
            downloaded = [t for t in app.playlist_model.tracks if t.is_downloaded]
            track = downloaded[0] if downloaded else random.choice(app.playlist_model.tracks)
            app.play_selected_track(track)

Builder.load_string('''
<TrackListItem>:
    radius: [16, 16, 16, 16]
    md_bg_color: app.theme_cls.surfaceContainerColor
    
    MDListItemLeadingAvatar:
        source: root.artwork if root.artwork else "album_art.png"
        radius: [dp(8), dp(8), dp(8), dp(8)]
        
    MDListItemHeadlineText:
        text: root.title
        
    MDListItemSupportingText:
        text: root.artist

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
    size: "140dp", "210dp"
    md_bg_color: app.theme_cls.surfaceContainerColor
    radius: [dp(16)]
    ripple_behavior: True
    padding: ["8dp", "8dp", "8dp", "8dp"]
    
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
                text: root.title if root.title else root.text
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
''')

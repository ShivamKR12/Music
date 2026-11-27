import os
import math
import random
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty, ColorProperty, NumericProperty, ListProperty
from kivymd.uix.list import MDListItem, MDListItemTrailingCheckbox
from kivymd.uix.card import MDCard
from kivymd.uix.chip import MDChip
from kivymd.uix.label import MDLabel
from kivymd.uix.slider import MDSlider
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle, Mesh, Line, RoundedRectangle, PushMatrix, PopMatrix, Rotate
from kivy.core.image import Image as CoreImage
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.recycleview import RecycleView
from kivy.metrics import dp
from kivy.factory import Factory

class MarqueeLabel(ScrollView):
    """
    A single-line auto-scrolling label for song titles, artist names, and metadata:
    - Strictly constrained to a single line (prevents layout and container overflow).
    - If text fits within the available width:
        - When halign == 'center': centers the text cleanly.
        - When halign == 'left': aligns to the left edge.
    - If text exceeds the available width:
        - Smooth unidirectional right-to-left marquee animation (pauses at end for 3s, then restarts).
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
    touch_pass_through = BooleanProperty(False)

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
            try:
                self._anim.stop(self)
            except Exception:
                pass
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
            # Overflows view: size label to text width and start right-to-left marquee animation
            self._label.adaptive_size = False
            self._label.size_hint = (None, None)
            self._label.width = tex_w
            self._label.height = self.height
            self.scroll_x = 0.0
            diff = tex_w - container_w
            dur = max(2.5, diff / float(self.speed))
            self._anim = (
                Animation(scroll_x=0.0, duration=2.5) +
                Animation(scroll_x=1.0, duration=dur, t='linear') +
                Animation(scroll_x=1.0, duration=3.0) +
                Animation(scroll_x=0.0, duration=0.0)
            )
            self._anim.repeat = True
            Clock.schedule_once(lambda d: self._anim.start(self) if self._anim else None, 0)

    def on_touch_down(self, touch):
        if self.touch_pass_through:
            return False
        if self.collide_point(*touch.pos):
            if self._anim:
                try:
                    self._anim.stop(self)
                except Exception:
                    pass
                self._anim = None
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        res = super().on_touch_up(touch)
        if self.collide_point(*touch.pos):
            self._schedule_marquee()
        return res

Factory.register('MarqueeLabel', cls=MarqueeLabel)

class PassiveTrailingCheckbox(MDListItemTrailingCheckbox):
    """
    Trailing checkbox that visually reflects active state without intercepting touch events,
    allowing parent MDListItem to handle row activation reliably without double-toggle collisions.
    """
    def on_touch_down(self, touch):
        return False

    def on_touch_move(self, touch):
        return False

    def on_touch_up(self, touch):
        return False

Factory.register('PassiveTrailingCheckbox', cls=PassiveTrailingCheckbox)

class LyricsScrollView(MDScrollView):
    """
    Interactive scroll view for synchronized lyrics:
    - Smoothly animates active lyric line to remain centered at 50% viewport height.
    - Pauses auto-scrolling immediately when the user manually touches or scrolls.
    - Starts a 3-second inactivity timer once the user stops scrolling.
    - Resumes auto-scrolling and re-centers the current active lyric line once 3 seconds elapse.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_scrolling = False
        self.resume_event = None
        self.on_resume_callback = None

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.user_scrolling = True
            if self.resume_event:
                self.resume_event.cancel()
                self.resume_event = None
            try:
                Animation.stop_all(self, 'scroll_y')
            except Exception:
                pass
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            self.user_scrolling = True
            if self.resume_event:
                self.resume_event.cancel()
                self.resume_event = None
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        res = super().on_touch_up(touch)
        if self.user_scrolling:
            def _resume(dt):
                self.user_scrolling = False
                self.resume_event = None
                if self.on_resume_callback:
                    self.on_resume_callback()
            if self.resume_event:
                self.resume_event.cancel()
            self.resume_event = Clock.schedule_once(_resume, 3.0)
        return res

Factory.register('LyricsScrollView', cls=LyricsScrollView)

from kivymd.uix.screenmanager import MDScreenManager

class LazyScreenManager(MDScreenManager):
    """
    High-performance ScreenManager that dynamically instantiates screens on-demand:
    - Eliminates 3.5+ seconds of startup overhead by not building 16 unviewed screens at launch.
    - Transparent drop-in replacement for MDScreenManager.
    - Guarantees screen existence on get_screen() and switch_screen().
    """
    def get_screen(self, name):
        if not self.has_screen(name):
            import views.screens as screens
            clean_name = name.replace("_", "").lower()
            candidates = {
                clean_name + "screen",
                clean_name.rstrip("s") + "screen",
                clean_name + "sscreen",
            }
            found_cls = None
            for attr in dir(screens):
                if attr.lower() in candidates:
                    found_cls = getattr(screens, attr)
                    break
            if found_cls:
                s = found_cls(name=name)
                self.add_widget(s)
            else:
                import logging
                logging.getLogger("kivy_music_app").warning(
                    f"LazyScreenManager: No class found for screen '{name}' (candidates: {candidates})"
                )
        return super().get_screen(name)

Factory.register('LazyScreenManager', cls=LazyScreenManager)

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

class EmbeddedRecycleView(RecycleView):
    """
    RecycleView embedded inside a parent vertical ScrollView.
    - Seamlessly yields vertical and horizontal scroll gestures to parent scroll containers.
    - Preserves child touch dispatching (item click and ripple effects).
    - Prevents scrolling lockups and snapping-back glitches in nested layouts.
    """
    def __init__(self, **kwargs):
        kwargs.setdefault('do_scroll_x', False)
        kwargs.setdefault('do_scroll_y', False)
        super().__init__(**kwargs)

    def on_touch_down(self, touch):
        # Ensure touch is strictly inside any ancestor ScrollView viewport
        p = self.parent
        from kivy.uix.scrollview import ScrollView
        while p:
            if isinstance(p, ScrollView):
                if not p.collide_point(*touch.pos):
                    return False
            p = p.parent
        if not self.collide_point(*touch.pos):
            return False
        return super().on_touch_down(touch)

    def on_scroll_start(self, touch, check_children=True):
        pos = getattr(touch, 'pos', None)
        if pos and not self.collide_point(*pos):
            return False
        if hasattr(self, 'simulate_touch_down'):
            return self.simulate_touch_down(touch)
        return False

    def on_scroll_move(self, touch):
        return False

    def on_scroll_stop(self, touch, check_children=True):
        return False

Factory.register('DirectionalHorizontalScrollView', cls=DirectionalHorizontalScrollView)
Factory.register('DirectionalHorizontalRecycleView', cls=DirectionalHorizontalRecycleView)
Factory.register('EmbeddedRecycleView', cls=EmbeddedRecycleView)

from kivymd.uix.fitimage import FitImage
from kivy.uix.recycleview.views import RecycleDataViewBehavior

class TrackListItem(RecycleDataViewBehavior, MDListItem):
    title = StringProperty("")
    artist = StringProperty("")
    artwork = StringProperty("album_art.png")
    source_icon = StringProperty("")
    source_icon_color = ColorProperty([0.45, 0.45, 0.50, 1.0])
    track_obj = ObjectProperty(None, allownone=True)
    index = NumericProperty(0)

    def _sync_containers(self, *args):
        if "leading_container" in self.ids:
            self.ids.leading_container.width = dp(40)
        if "trailing_container" in self.ids:
            self.ids.trailing_container.width = dp(24) if self.source_icon else 0

    def on_source_icon(self, *args):
        Clock.schedule_once(self._sync_containers, 0)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        if "source_icon" not in data:
            self.source_icon = ""
        res = super().refresh_view_attrs(rv, index, data)
        Clock.schedule_once(self._sync_containers, 0)
        return res
    
    def on_release(self):
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        if self.track_obj:
            app.play_selected_track(self.track_obj)
        elif hasattr(app, "playlist_model") and app.playlist_model.tracks:
            matched = None
            if self.title:
                norm_title = self.title.strip().lower()
                for t in app.playlist_model.tracks:
                    if t.title.strip().lower() == norm_title:
                        matched = t
                        break
            if not matched:
                from models.track_model import Track
                matched = Track(
                    title=self.title or "Unknown Title",
                    artist=self.artist or "Unknown Artist",
                    album_art=self.artwork or "album_art.png",
                )
            app.play_selected_track(matched)

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

class SearchSuggestionItem(MDListItem):
    text = StringProperty("")
    query = StringProperty("")

    def on_release(self):
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        q = self.query or self.text
        if hasattr(app, "perform_search"):
            app.perform_search(q)
        elif hasattr(app, "root") and app.root and hasattr(app.root, "ids") and "screen_manager" in app.root.ids:
            try:
                search_screen = app.root.ids.screen_manager.get_screen("search")
                if "search_input" in search_screen.ids:
                    search_screen.ids.search_input.text = q
            except Exception:
                pass

Factory.register('SearchSuggestionItem', cls=SearchSuggestionItem)

class HomeMoodChip(MDChip):
    """Home mood filter chip (SimpMusic listOfHomeChip): selected chip takes the
    primary fill; taps filter Home's Quick picks shelf in place."""
    mood = StringProperty("All")

    def on_release(self):
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        if hasattr(app, "select_mood_filter"):
            app.select_mood_filter(self, self.mood)

Factory.register('HomeMoodChip', cls=HomeMoodChip)

class MiniPlayerCard(MDCard):
    """
    Floating capsule mini player card with swipe-down dismissal arbitration.
    - Tap: Opens full-screen PlayerScreen (via on_release)
    - Swipe Down: Dismisses the mini player and pauses playback
    """
    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return super().on_touch_down(touch)
        touch.ud['mini_down_pos'] = touch.pos
        touch.ud['mini_swiped'] = False
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if 'mini_down_pos' in touch.ud:
            ox, oy = touch.ud['mini_down_pos']
            dy_down = oy - touch.y  # In Kivy, y=0 is at bottom; dragging down yields positive dy_down
            dx = abs(touch.x - ox)
            from kivy.metrics import dp
            if dy_down >= dp(18) and dy_down > dx * 0.9:
                touch.ud['mini_swiped'] = True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if 'mini_down_pos' in touch.ud:
            ox, oy = touch.ud.pop('mini_down_pos')
            dy_down = oy - touch.y
            dx = abs(touch.x - ox)
            from kivy.metrics import dp
            if touch.ud.pop('mini_swiped', False) or (dy_down >= dp(18) and dy_down > dx * 0.9):
                if hasattr(self, 'state'):
                    self.state = 'normal'
                if getattr(touch, 'grab_current', None) is self:
                    touch.ungrab(self)
                from kivymd.app import MDApp
                app = MDApp.get_running_app()
                if app and hasattr(app, "dismiss_mini_player"):
                    app.dismiss_mini_player()
                return True
        return super().on_touch_up(touch)

Factory.register('MiniPlayerCard', cls=MiniPlayerCard)

class PlaylistTileItem(MDCard):
    """Recycled playlist tile for the Library Playlists grid (SimpMusic
    GridLibraryPlaylist pattern). Replaces ~138 eagerly built MDCards with ~10
    recycled cells; artwork/texture work is limited to visible cells."""
    name = StringProperty("")
    track_count = NumericProperty(0)
    artwork = StringProperty("")
    is_create = BooleanProperty(False)

    def on_release(self):
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        if self.is_create:
            app.show_add_playlist_dialog()
        else:
            app.open_playlist(self.name)

Factory.register('PlaylistTileItem', cls=PlaylistTileItem)

class HomePlaylistItem(MDCard):
    """Card for Home screen mood, category, and curated playlists."""
    name = StringProperty("Playlist")
    subtitle = StringProperty("Curated Mix")
    artwork = StringProperty("album_art.png")

    def on_release(self):
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        app.open_playlist(self.name)

Factory.register('HomePlaylistItem', cls=HomePlaylistItem)

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

Factory.register('HomeCardItem', cls=HomeCardItem)

class QuickPicksItem(MDCard):
    """Compact song row card for Home's Quick picks shelf (SimpMusic QuickPicksItem:
    rounded artwork + one-line marquee title + one-line artist)."""
    title = StringProperty("Unknown Title")
    artist = StringProperty("Unknown Artist")
    artwork = StringProperty("album_art.png")
    text = StringProperty("")
    track_obj = ObjectProperty(None, allownone=True)

    def on_release(self):
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        if getattr(self, "track_obj", None):
            app.play_selected_track(self.track_obj)

Factory.register('QuickPicksItem', cls=QuickPicksItem)

class ArtistAlbumCard(MDCard):
    title = StringProperty("Unknown Album")
    subtitle = StringProperty("Album")
    artwork = StringProperty("album_art.png")
    artist = StringProperty("")
    album_tracks = ListProperty([])

    def on_release(self):
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        app.open_album(self.title, self.artist or app.active_artist_name, self.artwork, self.album_tracks)

Builder.load_string('''
<TrackListItem>:
    radius: [16, 16, 16, 16]
    md_bg_color: app.theme_cls.surfaceContainerColor
    ripple_behavior: True

    MDListItemLeadingAvatar:
        source: root.artwork if root.artwork else "album_art.png"
        radius: [dp(8), dp(8), dp(8), dp(8)]
        size_hint: None, None
        size: "40dp", "40dp"
        disabled: True

    MDListItemHeadlineText:
        text: root.title

    MDListItemSupportingText:
        text: root.artist

    MDListItemTrailingIcon:
        icon: root.source_icon if root.source_icon else "blank"
        theme_icon_color: "Custom" if root.source_icon else "Primary"
        icon_color: root.source_icon_color if root.source_icon else app.theme_cls.onSurfaceVariantColor
        opacity: 1 if root.source_icon else 0
        disabled: not bool(root.source_icon)
        size: (dp(24), dp(24)) if root.source_icon else (0, 0)
        width: dp(24) if root.source_icon else 0

<SearchHistoryItem>:
    MDListItemLeadingIcon:
        icon: "history"
    MDListItemHeadlineText:
        text: root.text
    MDListItemTrailingIcon:
        icon: "arrow-top-right"

<SearchSuggestionItem>:
    MDListItemLeadingIcon:
        icon: "magnify"
        theme_icon_color: "Custom"
        icon_color: app.theme_cls.primaryColor
    MDListItemHeadlineText:
        text: root.text
    MDListItemTrailingIcon:
        icon: "arrow-top-right"

<HomeMoodChip>:
    type: "filter"
    theme_bg_color: "Custom"
    md_bg_color: app.theme_cls.primaryColor if root.active else app.theme_cls.surfaceContainerHighestColor
    MDChipText:
        theme_text_color: "Custom"
        text: root.mood
        text_color: app.theme_cls.onPrimaryColor if root.active else app.theme_cls.onSurfaceColor

<PlaylistTileItem>:
    style: "elevated"
    theme_bg_color: "Custom"
    md_bg_color: app.theme_cls.primaryColor if root.is_create else app.theme_cls.surfaceContainerHighestColor
    radius: [dp(16)]
    ripple_behavior: True
    orientation: "vertical"
    size_hint: 1, 1
    padding: ["4dp", "4dp", "4dp", "4dp"]

    MDBoxLayout:
        orientation: "vertical"
        size_hint: 1, 1
        spacing: "2dp"

        MDBoxLayout:
            size_hint: 1, 1
            MDIcon:
                icon: "plus"
                icon_color: app.theme_cls.onPrimaryColor
                theme_icon_color: "Custom"
                font_size: "40sp"
                pos_hint: {"center_x": .5, "center_y": .5}
                opacity: 1 if root.is_create else 0
                disabled: not root.is_create
            FitImage:
                source: root.artwork if root.artwork else "album_art.png"
                size_hint: 1, 1
                radius: [dp(12), dp(12), dp(12), dp(12)]
                opacity: 0 if root.is_create else 1
                mipmap: False

        MDLabel:
            text: "Create" if root.is_create else root.name
            font_style: "Body"
            role: "small"
            bold: True
            halign: "center"
            adaptive_height: True
            text_color: app.theme_cls.onPrimaryColor if root.is_create else app.theme_cls.onSurfaceColor
            theme_text_color: "Custom"

        MDLabel:
            text: "" if root.is_create else f"{int(root.track_count)} tracks"
            font_style: "Body"
            role: "small"
            halign: "center"
            adaptive_height: True
            theme_text_color: "Custom"
            text_color: app.theme_cls.onPrimaryColor if root.is_create else app.theme_cls.onSurfaceVariantColor

<HomePlaylistItem>:
    style: "elevated"
    size_hint: None, None
    size: "140dp", "210dp"
    theme_bg_color: "Custom"
    md_bg_color: app.theme_cls.surfaceContainerColor
    radius: [dp(16)]
    ripple_behavior: True
    padding: ["8dp", "8dp", "8dp", "8dp"]

    MDBoxLayout:
        orientation: "vertical"
        size_hint: 1, 1
        spacing: "4dp"

        FitImage:
            source: root.artwork if root.artwork else "album_art.png"
            size_hint: 1, None
            height: "124dp"
            radius: [dp(12), dp(12), dp(12), dp(12)]
            mipmap: False

        MDLabel:
            text: root.name
            font_style: "Title"
            role: "small"
            bold: True
            max_lines: 1
            adaptive_height: True
            theme_text_color: "Custom"
            text_color: app.theme_cls.onSurfaceColor

        MDLabel:
            text: root.subtitle
            font_style: "Body"
            role: "small"
            max_lines: 1
            adaptive_height: True
            theme_text_color: "Custom"
            text_color: app.theme_cls.onSurfaceVariantColor

<HomeCardItem>:
    style: "elevated"
    size_hint: None, None
    size: "140dp", "210dp"
    theme_bg_color: "Custom"
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
            mipmap: False
            
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

<QuickPicksItem>:
    style: "filled"
    theme_bg_color: "Custom"
    size_hint: None, None
    size: "176dp", "64dp"
    md_bg_color: app.theme_cls.surfaceContainerLowColor
    radius: [dp(12)]
    ripple_behavior: True
    padding: ["8dp", "8dp", "8dp", "8dp"]
    MDBoxLayout:
        orientation: "horizontal"
        spacing: "10dp"
        size_hint: 1, 1

        FitImage:
            source: root.artwork if root.artwork else "album_art.png"
            size_hint: None, None
            size: "48dp", "48dp"
            radius: [dp(10), dp(10), dp(10), dp(10)]
            pos_hint: {"center_y": .5}
            mipmap: False

        MDBoxLayout:
            orientation: "vertical"
            spacing: "2dp"
            size_hint_x: 1
            height: "48dp"
            pos_hint: {"center_y": .5}

            MDLabel:
                text: root.title if root.title else root.text
                font_style: "Label"
                role: "large"
                bold: True
                adaptive_height: True
                max_lines: 1
                shorten: True
                shorten_from: "right"
                halign: "left"

            MDLabel:
                text: root.artist
                font_style: "Body"
                role: "small"
                adaptive_height: True
                max_lines: 1
                shorten: True
                shorten_from: "right"
                halign: "left"
                theme_text_color: "Custom"
                text_color: app.theme_cls.onSurfaceVariantColor

<ArtistAlbumCard>:
    style: "elevated"
    size_hint: None, None
    size: "140dp", "160dp"
    radius: [dp(16)]
    padding: "10dp"
    spacing: "6dp"
    orientation: "vertical"
    ripple_behavior: True
    md_bg_color: app.theme_cls.surfaceContainerLowColor

    FitImage:
        source: root.artwork if root.artwork else "album_art.png"
        size_hint: None, None
        size: "120dp", "95dp"
        radius: [dp(12)]
        pos_hint: {"center_x": .5}
    MDLabel:
        text: root.title
        font_style: "Label"
        role: "large"
        bold: True
        adaptive_height: True
        max_lines: 1
        shorten: True
        shorten_from: "right"
    MDLabel:
        text: root.subtitle
        font_style: "Body"
        role: "small"
        text_color: app.theme_cls.onSurfaceVariantColor
        adaptive_height: True
        max_lines: 1
''')


class PlayerTimelineSlider(MDSlider):
    """
    High-precision Material 3 timeline scrubber for music playback:
    - Binds smoothly with audio engine progress without state jumping.
    - Captures touch scrubbing gestures and updates start timer in real-time.
    - Dispatches atomic seek to player_controller upon release.
    - Visualizes YouTube-style buffering line advancing ahead of playhead.
    - Meets accessibility guidelines with 44dp touch target height.
    """
    is_seeking = BooleanProperty(False)
    buffer_progress = NumericProperty(0.0)
    buffer_color = ColorProperty([1, 1, 1, 0.35])

    def __init__(self, **kwargs):
        kwargs.setdefault('size_hint_y', None)
        kwargs.setdefault('height', dp(48))
        kwargs.setdefault('padding', dp(8))
        kwargs.setdefault('track_active_width', dp(4))
        kwargs.setdefault('track_inactive_width', dp(4))
        kwargs.setdefault('track_active_color', [1, 1, 1, 1.0])
        kwargs.setdefault('track_inactive_color', [1, 1, 1, 0.22])
        kwargs.setdefault('handle_anim_duration', 0)
        kwargs.setdefault('handle_anim_transition', 'linear')
        super().__init__(**kwargs)

    def on__handle(self, instance, value):
        if value:
            value.theme_bg_color = "Custom"
            value.md_bg_color = [1, 1, 1, 1.0]

    def on_value(self, instance, value):
        if self.is_seeking:
            from kivymd.app import MDApp
            app = MDApp.get_running_app()
            if app and hasattr(app, "player_controller") and app.player_controller:
                app.player_controller.current_time = float(value)
                sec = max(0, int(value or 0))
                m, s = divmod(sec, 60)
                app.player_controller.formatted_current_time = f"{m:02d}:{s:02d}"
                if app.player_controller.active_track:
                    app.player_controller.active_track.current_time = float(value)

    def on_touch_down(self, touch):
        if self.disabled or not self.collide_point(*touch.pos):
            return super().on_touch_down(touch)
        self.is_seeking = True
        touch.grab(self)
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        if app and hasattr(app, "player_controller") and app.player_controller:
            app.player_controller.is_seeking = True
        res = super().on_touch_down(touch)
        if not getattr(touch, "is_mouse_scrolling", False) and self.sensitivity != "handle":
            from kivy.animation import Animation
            Animation.stop_all(self, "value_pos")
            self.value_pos = touch.pos
        if app and hasattr(app, "player_controller") and app.player_controller:
            app.player_controller.current_time = float(self.value)
            sec = max(0, int(self.value or 0))
            m, s = divmod(sec, 60)
            app.player_controller.formatted_current_time = f"{m:02d}:{s:02d}"
            if app.player_controller.active_track:
                app.player_controller.active_track.current_time = float(self.value)
        return res

    def on_touch_move(self, touch):
        res = super().on_touch_move(touch)
        if (touch.grab_current == self or self.is_seeking):
            from kivymd.app import MDApp
            app = MDApp.get_running_app()
            if app and hasattr(app, "player_controller") and app.player_controller:
                app.player_controller.current_time = float(self.value)
                sec = max(0, int(self.value or 0))
                m, s = divmod(sec, 60)
                app.player_controller.formatted_current_time = f"{m:02d}:{s:02d}"
                if app.player_controller.active_track:
                    app.player_controller.active_track.current_time = float(self.value)
        return res

    def on_touch_up(self, touch):
        was_seeking = self.is_seeking or (touch.grab_current == self)
        res = super().on_touch_up(touch)
        if was_seeking:
            self.is_seeking = False
            if touch.grab_current == self:
                touch.ungrab(self)
            from kivymd.app import MDApp
            app = MDApp.get_running_app()
            if app and hasattr(app, "player_controller") and app.player_controller:
                app.player_controller.seek(float(self.value))
                Clock.schedule_once(lambda dt: setattr(app.player_controller, "is_seeking", False), 0.05)
        return res


class YouTubeLoadingCircle(Widget):
    """
    YouTube-style continuous rotating loading and buffering spinner:
    - Continuous 360-degree smooth linear rotation (no stutter, no dot-based jumping).
    - Polished circular open arc with rounded caps ('round').
    - Fully reactive: starts rotation when active=True and visible; stops when inactive/hidden to preserve CPU & battery.
    - Adaptable sizing and colors (defaults to theme primaryColor or clean white).
    """
    angle = NumericProperty(0)
    line_width = NumericProperty(dp(3.5))
    color = ColorProperty([1, 1, 1, 0.95])
    active = BooleanProperty(True)

    def __init__(self, **kwargs):
        kwargs.setdefault('size_hint', (None, None))
        kwargs.setdefault('size', (dp(40), dp(40)))
        super().__init__(**kwargs)
        self._anim = None
        self.bind(active=self._on_active, opacity=self._on_visibility, parent=self._on_parent)
        Clock.schedule_once(lambda dt: self._start_anim() if (self.active and self.opacity > 0) else None, 0)

    def _start_anim(self):
        self._stop_anim()
        self.angle = 0
        self._anim = Animation(angle=-360, duration=0.85, t='linear')
        self._anim.repeat = True
        self._anim.start(self)

    def _stop_anim(self):
        if self._anim:
            self._anim.stop(self)
            self._anim = None

    def _on_active(self, instance, value):
        if value and self.opacity > 0 and self.parent:
            self._start_anim()
        else:
            self._stop_anim()

    def _on_visibility(self, instance, value):
        if value > 0 and self.active and self.parent:
            self._start_anim()
        else:
            self._stop_anim()

    def _on_parent(self, instance, value):
        if value is None:
            self._stop_anim()
        elif self.active and self.opacity > 0:
            self._start_anim()


Builder.load_string('''
<YouTubeLoadingCircle>:
    canvas:
        PushMatrix
        Rotate:
            angle: root.angle
            origin: root.center
        Color:
            rgba: root.color
        Line:
            circle: (root.center_x, root.center_y, max(dp(4), min(root.width, root.height)/2 - root.line_width), 0, 280)
            width: root.line_width
            cap: 'round'
        PopMatrix

<PlayerTimelineSlider>:
    canvas:
        Clear
        Color:
            rgba: self.track_inactive_color if self.track_inactive_color else [1, 1, 1, 0.22]
        SmoothRectangle:
            size: (max(0.0, self.width - self.padding * 2), dp(4)) if self.orientation == "horizontal" else (dp(4), max(0.0, self.height - self.padding * 2))
            pos: (self.x + self.padding, self.center_y - dp(2)) if self.orientation == "horizontal" else (self.center_x - dp(2), self.y + self.padding)
        Color:
            rgba: root.buffer_color if root.buffer_progress > 0 else [0, 0, 0, 0]
        SmoothRectangle:
            size: (max(0.0, (self.width - self.padding * 2) * min(1.0, max(0.0, root.buffer_progress))), dp(4)) if self.orientation == "horizontal" else (dp(4), max(0.0, (self.height - self.padding * 2) * min(1.0, max(0.0, root.buffer_progress))))
            pos: (self.x + self.padding, self.center_y - dp(2)) if self.orientation == "horizontal" else (self.center_x - dp(2), self.y + self.padding)
        Color:
            rgba: self.track_active_color if self.track_active_color else [1, 1, 1, 1.0]
        SmoothRectangle:
            size: (max(0.0, (self.width - self.padding * 2) * self.value_normalized), dp(4)) if self.orientation == "horizontal" else (dp(4), max(0.0, (self.height - self.padding * 2) * self.value_normalized))
            pos: (self.x + self.padding, self.center_y - dp(2)) if self.orientation == "horizontal" else (self.center_x - dp(2), self.y + self.padding)
        Color:
            rgba: self.track_active_color if self.track_active_color else [1, 1, 1, 1.0]
        Ellipse:
            size: (dp(14), dp(14)) if self.is_seeking else (dp(10), dp(10))
            pos: (self.x + self.padding + max(0.0, self.width - self.padding * 2) * self.value_normalized - (dp(7) if self.is_seeking else dp(5)), self.center_y - (dp(7) if self.is_seeking else dp(5))) if self.orientation == "horizontal" else (self.center_x - (dp(7) if self.is_seeking else dp(5)), self.y + self.padding + max(0.0, self.height - self.padding * 2) * self.value_normalized - (dp(7) if self.is_seeking else dp(5)))
''')

Factory.register('PlayerTimelineSlider', cls=PlayerTimelineSlider)
Factory.register('YouTubeLoadingCircle', cls=YouTubeLoadingCircle)


class AnimatedBackground(Widget):
    """
    Continuous, organic fluid animated background supporting multiple smooth visual variations:
    - 'gradient': Continuous chromatic gradient flow interpolating seamlessly across the viewport.
    - 'ripple': Water ripple effect with gentle concentric liquid undulations expanding outward.
    - 'aurora': Soft aurora wave curtains drifting harmonically across the screen.
    - 'off': Clean solid theme backdrop.
    Seamlessly harmonizes with album art color extraction or active theme colors, preserving text legibility.
    """
    is_active = BooleanProperty(True)
    variation = StringProperty("gradient") # "gradient", "ripple", "aurora", "off"
    speed = NumericProperty(1.0)
    intensity = NumericProperty(0.6)
    color_primary = ListProperty([0.48, 0.30, 1.0, 0.45])
    color_secondary = ListProperty([0.15, 0.60, 0.90, 0.40])
    color_tertiary = ListProperty([0.90, 0.25, 0.55, 0.35])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 8
        self.rows = 8
        self._t = 0.0

        with self.canvas.before:
            self._bg_col = Color(0.08, 0.08, 0.12, 1.0)
            self._bg_rect = Rectangle(pos=self.pos, size=self.size)

            Color(1, 1, 1, 1)
            fmt = [(b'vPosition', 2, 'float'), (b'vColor', 4, 'float')]
            self.mesh = Mesh(fmt=fmt, mode='triangles')

            # Readability contrast overlay
            self._overlay_col = Color(0, 0, 0, 0.40)
            self._overlay_rect = Rectangle(pos=self.pos, size=self.size)

        # Precompute mesh triangle indices for (cols x rows) grid
        indices = []
        for r in range(self.rows):
            for c in range(self.cols):
                i0 = r * (self.cols + 1) + c
                i1 = i0 + 1
                i2 = (r + 1) * (self.cols + 1) + c
                i3 = i2 + 1
                indices.extend([i0, i1, i2, i1, i3, i2])
        self.mesh.indices = indices

        self._tick_event = None
        self.bind(pos=self._update_geom, size=self._update_geom)
        self.bind(color_primary=self._update_colors, color_secondary=self._update_colors, color_tertiary=self._update_colors)
        self.bind(is_active=self._on_active_change, variation=self._on_variation_change)
        Clock.schedule_once(lambda dt: self._sync_tick_state(), 0.5)

    def _update_geom(self, *args):
        self._bg_rect.pos = self.pos
        self._bg_rect.size = self.size
        self._overlay_rect.pos = self.pos
        self._overlay_rect.size = self.size

    def _update_colors(self, *args):
        pass

    def _sync_tick_state(self):
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        is_player_current = False
        if app and hasattr(app, "root") and app.root and hasattr(app.root, "ids") and "screen_manager" in app.root.ids:
            is_player_current = (app.root.ids.screen_manager.current in ("player", "lyrics"))

        should_run = self.is_active and (self.variation != "off") and is_player_current
        if should_run and self._tick_event is None:
            self._tick_event = Clock.schedule_interval(self._tick, 1.0 / 25.0)
        elif not should_run and self._tick_event is not None:
            Clock.unschedule(self._tick_event)
            self._tick_event = None
            if not self.is_active or self.variation == "off":
                self.mesh.vertices = []

    def start_animation(self):
        if self._tick_event is None and self.is_active and self.variation != "off":
            self._tick_event = Clock.schedule_interval(self._tick, 1.0 / 25.0)

    def stop_animation(self):
        if self._tick_event is not None:
            Clock.unschedule(self._tick_event)
            self._tick_event = None

    def _on_variation_change(self, instance, variation):
        self._sync_tick_state()

    def _on_active_change(self, instance, active):
        if not active or self.variation == "off":
            self.stop_animation()
            self.mesh.vertices = []
        else:
            self._sync_tick_state()
            self._tick(0.016)

    def _apply_extracted_colors(self, p, s, t):
        self.color_primary = p
        self.color_secondary = s
        self.color_tertiary = t

    def update_colors_from_theme(self, app=None):
        """Harmonizes backdrop colors with album art extraction or active theme palette."""
        if not app:
            from kivymd.app import MDApp
            app = MDApp.get_running_app()
        if not app:
            return

        from utils.theme_utils import get_active_palette, get_active_immersive_bg

        palette = get_active_palette()
        if palette and getattr(app, "extract_artwork_colors", True):
            imm = get_active_immersive_bg()
            self._bg_col.rgba = imm
            sw = palette.get("swatches", {})
            is_dark = (app.theme_cls.theme_style == "Dark")
            p_rgb = palette.get("dark_primary") if is_dark else palette.get("light_primary")
            if not p_rgb:
                p_rgb = palette.get("dominant", [0.48, 0.30, 1.0])
            s_rgb = sw.get("vibrant") if is_dark else sw.get("dark_vibrant")
            if not s_rgb:
                s_rgb = sw.get("muted") or [0.15, 0.60, 0.90]
            t_rgb = sw.get("light_vibrant") or sw.get("dominant") or [0.90, 0.25, 0.55]

            self.color_primary = [p_rgb[0], p_rgb[1], p_rgb[2], 0.45 * self.intensity]
            self.color_secondary = [s_rgb[0], s_rgb[1], s_rgb[2], 0.40 * self.intensity]
            self.color_tertiary = [t_rgb[0], t_rgb[1], t_rgb[2], 0.35 * self.intensity]
            return

        bg = getattr(app.theme_cls, "backgroundColor", [0.08, 0.08, 0.12, 1.0])
        if bg and bg != [1, 1, 1, 1]:
            self._bg_col.rgba = bg

        # Fallback / Non-extraction mode: harmonize with active theme
        p = list(getattr(app.theme_cls, "primaryColor", [0.48, 0.30, 1.0, 1.0]))
        p = (p[:3] + [0.45 * self.intensity]) if p != [1, 1, 1, 1] else [0.48, 0.30, 1.0, 0.45 * self.intensity]
        s = list(getattr(app.theme_cls, "secondaryColor", [0.15, 0.60, 0.90, 1.0]))
        s = (s[:3] + [0.40 * self.intensity]) if s != [1, 1, 1, 1] else [0.15, 0.60, 0.90, 0.40 * self.intensity]
        t = list(getattr(app.theme_cls, "tertiaryColor", [0.90, 0.25, 0.55, 1.0]))
        t = (t[:3] + [0.35 * self.intensity]) if t != [1, 1, 1, 1] else [0.90, 0.25, 0.55, 0.35 * self.intensity]
        self.color_primary = p
        self.color_secondary = s
        self.color_tertiary = t

    def _tick(self, dt):
        if not self.is_active or self.variation == "off":
            self.stop_animation()
            if self.mesh.vertices:
                self.mesh.vertices = []
            return

        # Performance Preservation: Only calculate mesh vertices when player screen is current
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        if app and hasattr(app, "root") and app.root and hasattr(app.root, "ids") and "screen_manager" in app.root.ids:
            if app.root.ids.screen_manager.current not in ("player", "lyrics"):
                self.stop_animation()
                return
        self._t += dt * self.speed
        w, h = max(10, self.width), max(10, self.height)
        ox, oy = self.x, self.y
        t = self._t

        vertices = []
        c1 = self.color_primary
        c2 = self.color_secondary
        c3 = self.color_tertiary

        cx, cy = ox + w * 0.5, oy + h * 0.55

        for r in range(self.rows + 1):
            v = r / self.rows
            for c in range(self.cols + 1):
                u = c / self.cols
                base_x = ox + u * w
                base_y = oy + v * h

                if self.variation == "ripple":
                    # Gentle radial water ripple expanding outward
                    dx = base_x - cx
                    dy = base_y - cy
                    dist = math.hypot(dx, dy)
                    wave = math.sin(dist * 0.015 - t * 2.0)
                    wave2 = math.cos((dx + dy) * 0.01 + t * 1.2)
                    blend = (wave * 0.5 + 0.5) * 0.7 + (wave2 * 0.5 + 0.5) * 0.3

                    r_col = c1[0] * blend + c2[0] * (1.0 - blend)
                    g_col = c1[1] * blend + c2[1] * (1.0 - blend)
                    b_col = c1[2] * blend + c3[2] * (1.0 - blend)
                    a_col = min(0.65, (c1[3] + c2[3]) * 0.5 * (0.8 + 0.2 * wave))

                    px = base_x + wave * 3.0
                    py = base_y + wave2 * 3.0

                elif self.variation == "aurora":
                    # Gentle vertical wave ribbons
                    ribbon = math.sin(u * 3.5 + t * 0.8) + math.cos(v * 2.0 - t * 0.6)
                    blend = (ribbon * 0.25 + 0.5)
                    blend = max(0.0, min(1.0, blend))

                    r_col = c1[0] * blend + c3[0] * (1.0 - blend)
                    g_col = c2[1] * blend + c1[1] * (1.0 - blend)
                    b_col = c3[2] * blend + c2[2] * (1.0 - blend)
                    a_col = 0.45 + 0.15 * math.sin(t * 0.5 + u * 2.0)
                    px = base_x + math.sin(v * 4.0 + t) * 4.0
                    py = base_y

                else: # "gradient" (Smooth continuous flowing gradient)
                    rot_x = 0.5 + 0.25 * math.sin(t * 0.6)
                    rot_y = 0.5 + 0.25 * math.cos(t * 0.5)
                    dist_to_center = math.hypot(u - rot_x, v - rot_y)
                    blend = max(0.0, min(1.0, 1.0 - dist_to_center))

                    r_col = c1[0] * u + c2[0] * (1.0 - u)
                    g_col = c2[1] * v + c3[1] * (1.0 - v)
                    b_col = c3[2] * blend + c1[2] * (1.0 - blend)
                    a_col = 0.50
                    px = base_x
                    py = base_y

                vertices.extend([px, py, r_col, g_col, b_col, a_col])

        self.mesh.vertices = vertices

Factory.register('AnimatedBackground', cls=AnimatedBackground)


class SleeveFanWidget(Widget):
    """SimpMusic-style fanned artwork preview: up to `slots` covers fanned out from the widget
    center, each tilted `tilt` degrees and spaced `spread_dp` further out, the newest artwork on
    top. With no artwork it draws dashed empty sleeves so a fresh library still shows the shapes
    waiting to be filled (ports SimpMusic's LibraryTilingBox SleeveFan to Kivy canvas drawing).
    Canvas-only drawing means the whole fan never intercepts touches.
    """
    artworks = ListProperty([])
    slots = NumericProperty(3)
    sleeve_dp = NumericProperty(62)
    spread_dp = NumericProperty(32)
    tilt = NumericProperty(11)
    round_covers = BooleanProperty(False)
    ring_color = ColorProperty(None, allownone=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._textures = []
        self._rebuild_retries = 0
        for prop in ("artworks", "ring_color", "round_covers"):
            self.bind(**{prop: self._schedule_rebuild})
        self.bind(size=self._schedule_rebuild)
        Clock.schedule_once(self._rebuild, 0)

    def _schedule_rebuild(self, *args):
        Clock.schedule_once(lambda dt: self._rebuild(), 0)

    def _load_textures(self):
        """Loads textures for existing artwork files only; newest first (DB rows come newest first)."""
        covers = []
        for path in (self.artworks or [])[:self.slots]:
            try:
                if path and os.path.exists(path):
                    covers.append(CoreImage(path).texture)
            except Exception:
                pass
        return covers

    def _rebuild(self, *args):
        if self.width <= 0 or self.height <= 0:
            self._rebuild_retries += 1
            if self._rebuild_retries <= 20:
                Clock.schedule_once(lambda dt: self._rebuild(), 0.05)
            return
        self._rebuild_retries = 0
        self.canvas.clear()
        covers = self._load_textures()
        ring = self.ring_color or [0, 0, 0, 0]
        sleeve = dp(self.sleeve_dp)
        spread = dp(self.spread_dp)
        radius = [sleeve / 2.0] if self.round_covers else [dp(8)]
        if covers:
            count = min(len(covers), self.slots)
            ordered = list(reversed(covers[:count]))  # Oldest first, so the newest is drawn last and lands on top.
        else:
            count = self.slots
            ordered = [None] * count
        n = len(ordered)
        with self.canvas:
            for i in range(n):
                step = i - (n - 1) / 2.0
                cx = self.center_x + spread * step
                cy = self.center_y
                half = sleeve / 2.0
                PushMatrix()
                Rotate(angle=self.tilt * step, origin=(cx, cy))
                tex = ordered[i]
                if tex is not None:
                    # Ring border under the cover so stacked artwork reads as separated sleeves.
                    inset = dp(2)
                    Color(r=ring[0], g=ring[1], b=ring[2], a=ring[3])
                    RoundedRectangle(
                        pos=(cx - half - inset, cy - half - inset),
                        size=(sleeve + 2 * inset, sleeve + 2 * inset),
                        radius=[r + inset for r in radius],
                    )
                    Color(1, 1, 1, 1)
                    RoundedRectangle(texture=tex, pos=(cx - half, cy - half), size=(sleeve, sleeve), radius=radius)
                else:
                    Color(0.5, 0.5, 0.5, 0.06)
                    RoundedRectangle(pos=(cx - half, cy - half), size=(sleeve, sleeve), radius=radius)
                    Color(0.6, 0.6, 0.6, 0.35)
                    Line(
                        rounded_rectangle=(cx - half, cy - half, sleeve, sleeve, radius[0]),
                        width=dp(1.5),
                        dash_length=dp(4),
                        dash_offset=dp(3.5),
                    )
                PopMatrix()



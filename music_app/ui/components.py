import os
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.image import Image, AsyncImage
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle, Rectangle, PushMatrix, PopMatrix, Scale, Translate, StencilPush, StencilUse, StencilUnUse, StencilPop, Rotate
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.properties import NumericProperty
from kivy.app import App

from config import LIGHT_THEME

class ArtworkIcon(Widget):
    def __init__(self, **kwargs):
        kwargs.setdefault("size_hint", (None, None))
        kwargs.setdefault("size", (dp(220), dp(220)))
        super().__init__(**kwargs)
        with self.canvas.before:
            PushMatrix()
            self.scale_origin = Translate()
            self.scale_inst = Scale(1, 1, 1)
            self.scale_restore = Translate()
            Color(*LIGHT_THEME["accent_soft"])
            self.bg = RoundedRectangle(radius=[dp(28)])
            StencilPush()
            self.stencil_bg = RoundedRectangle(radius=[dp(28)])
            StencilUse()
        self.icon = Label(text="\ue405", font_name="MaterialIcons", font_size="96sp", color=LIGHT_THEME["icon"], center=self.center)
        self.image = AsyncImage(fit_mode="cover")
        self.add_widget(self.icon)
        self.add_widget(self.image)
        
        with self.canvas.after:
            StencilUnUse()
            self.stencil_bg_after = RoundedRectangle(radius=[dp(28)])
            StencilPop()
            PopMatrix()
        
        self.bind(pos=self._update, size=self._update)
        self._show_placeholder()

        self.breathing = False

    def _update(self, *args):
        self.scale_origin.xy = self.center_x, self.center_y
        self.scale_restore.xy = -self.center_x, -self.center_y
        
        self.bg.pos = self.pos
        self.bg.size = self.size
        
        self.stencil_bg.pos = self.pos
        self.stencil_bg.size = self.size
        self.stencil_bg.radius = self.bg.radius
        
        self.stencil_bg_after.pos = self.pos
        self.stencil_bg_after.size = self.size
        self.stencil_bg_after.radius = self.bg.radius
        
        self.icon.center = self.center
        self.image.pos = self.pos
        self.image.size = self.size
        
    def start_breathing(self):
        if self.breathing: return
        self.breathing = True
        self._breathe_step1()
        
    def _breathe_step1(self, *args):
        if not self.breathing: return
        anim = Animation(x=1.03, y=1.03, duration=3.0, t="in_out_sine")
        anim.bind(on_complete=self._breathe_step2)
        anim.start(self.scale_inst)

    def _breathe_step2(self, *args):
        if not self.breathing: return
        anim = Animation(x=1.0, y=1.0, duration=3.0, t="in_out_sine")
        anim.bind(on_complete=self._breathe_step1)
        anim.start(self.scale_inst)
        
    def stop_breathing(self):
        self.breathing = False
        Animation.cancel_all(self.scale_inst)
        Animation(x=1.0, y=1.0, duration=0.5, t="out_quad").start(self.scale_inst)
    
    def set_artwork(self, path):
        if path and (path.startswith("http") or os.path.exists(path)):
            if self.image.source != path:
                self._show_image(path)
        else:
            self._show_placeholder()
    
    def _show_placeholder(self):
        self.icon.opacity = 1
        self.image.opacity = 0
        self.image.source = ""

    def _show_image(self, path):
        self.image.source = path
        self.image.reload()
        self.image.opacity = 1
        self.icon.opacity = 0


class BottomNavBar(MDBoxLayout):
    def __init__(self, root_layout, **kwargs):
        super().__init__(orientation="horizontal", size_hint_y=None, height=dp(80), padding=[dp(16), dp(12)], spacing=dp(32), **kwargs)
        self.root_layout = root_layout
        with self.canvas.before:
            Color(*LIGHT_THEME["surface"])
            self.bg = Rectangle()
        self.bind(pos=self._update_bg, size=self._update_bg)
        self.add_navigation_btn("\ue88a", "library")
        self.add_navigation_btn("\ue8b6", "search")
        self.add_navigation_btn("\ue03b", "playlists")

    def _update_bg(self, *args):
        self.bg.pos, self.bg.size = self.pos, self.size

    def add_navigation_btn(self, icon, screen):
        self.add_widget(Button(
            text=icon, font_name="MaterialIcons", font_size="26sp",
            color=LIGHT_THEME["icon"], background_normal="", background_color=(0,0,0,0),
            on_press=lambda x: self.root_layout.go_to(screen)
        ))


class MiniPlayerBar(MDBoxLayout):
    def __init__(self, root_layout, **kwargs):
        super().__init__(orientation="horizontal", size_hint_y=None, height=dp(72), padding=dp(8), spacing=dp(12), **kwargs)
        self.root_layout = root_layout
        self.progress = 0.0

        with self.canvas.before:
            PushMatrix()
            self.scale_origin = Translate()
            self.scale_inst = Scale(1, 1, 1)
            self.scale_restore = Translate()
            
            self.bg_color = Color(*LIGHT_THEME["surface"])
            self.bg = RoundedRectangle(radius=[dp(32)])

            Color(*LIGHT_THEME["surface_alt"])
            self.progress_bg = RoundedRectangle(radius=[0, 0, dp(32), dp(32)])
            
            Color(*LIGHT_THEME["accent"])
            self.progress_fill = RoundedRectangle(radius=[0, 0, dp(32), dp(32)])
            
        with self.canvas.after:
            PopMatrix()
            
        self.bind(pos=self._update_bg, size=self._update_bg)
        self.artwork = ArtworkIcon()
        self.artwork.size = (dp(56), dp(56))
        self.artwork.bg.radius = [dp(28)]
        self.artwork.icon.font_size = "28sp"
        from kivymd.uix.label import MDLabel
        from kivymd.uix.button import MDIconButton
        
        text_box = MDBoxLayout(orientation="vertical", spacing=0, size_hint_x=1)
        self.title_label = MDLabel(text="Not Playing", theme_text_color="Custom", text_color=LIGHT_THEME["text_primary"], halign="left", valign="bottom", bold=True, size_hint_y=None, height=dp(24), shorten=True, shorten_from="right")
        self.title_label.bind(size=self.title_label.setter("text_size"))
        self.artist_label = MDLabel(text="Select a track to start", theme_text_color="Custom", text_color=LIGHT_THEME["text_secondary"], halign="left", valign="top", size_hint_y=None, height=dp(20), shorten=True, shorten_from="right")
        self.artist_label.bind(size=self.artist_label.setter("text_size"))
        text_box.add_widget(Widget())
        text_box.add_widget(self.title_label)
        text_box.add_widget(self.artist_label)
        text_box.add_widget(Widget())
        
        from kivymd.uix.anchorlayout import MDAnchorLayout
        from kivymd.uix.progressindicator import MDCircularProgressIndicator
        
        self.play_container = MDAnchorLayout(anchor_x="center", anchor_y="center", size_hint=(None, None), size=(dp(56), dp(56)))
        self.play_btn = MDIconButton(icon="play", theme_icon_color="Custom", icon_color=LIGHT_THEME["text_primary"], style="standard")
        self.play_spinner = MDCircularProgressIndicator(size_hint=(None, None), size=(dp(32), dp(32)), active=False, opacity=0, color=LIGHT_THEME["text_primary"])
        
        self.play_container.add_widget(self.play_btn)
        self.play_container.add_widget(self.play_spinner)
        
        self.fav_btn = MDIconButton(icon="heart-outline", theme_icon_color="Custom", icon_color=LIGHT_THEME["text_primary"], style="standard")
        self.play_btn.bind(on_release=lambda *_: self.root_layout.toggle_play())
        self.fav_btn.bind(on_release=self.toggle_favorite)
        self.add_widget(self.artwork)
        self.add_widget(text_box)
        self.add_widget(self.fav_btn)
        self.add_widget(self.play_container)

    def _update_bg(self, *args):
        self.scale_origin.xy = self.center_x, self.center_y
        self.scale_restore.xy = -self.center_x, -self.center_y
        self.bg.pos, self.bg.size = self.pos, self.size

        self.progress_bg.pos = self.pos
        self.progress_bg.size = (self.width, dp(4))
        self.progress_fill.pos = self.pos
        self.progress_fill.size = (self.width * self.progress, dp(4))
    
    def set_progress(self, progress):
        self.progress = progress
        self.progress_fill.size = (self.width * self.progress, dp(4))

    def _update_play(self, *args):
        self.play_bg.pos, self.play_bg.size = self.play_btn.pos, self.play_btn.size

    def update_play_state(self, is_playing):
        self.play_btn.icon = "pause" if is_playing else "play"
        self.animate_play()

    def animate_play(self, *args):
        (Animation(font_size=dp(36), duration=0.1, t="out_quad") + Animation(font_size=dp(32), duration=0.25, t="out_back")).start(self.play_btn)
    
    def update_loading_state(self, is_loading):
        if is_loading:
            self.play_btn.opacity = 0
            self.play_btn.disabled = True
            self.play_spinner.opacity = 1
            self.play_spinner.active = True
        else:
            self.play_btn.opacity = 1
            self.play_btn.disabled = False
            self.play_spinner.opacity = 0
            self.play_spinner.active = False
            self.update_play_state(self.root_layout.is_playing)

    def update_favorite_state(self, is_fav):
        if is_fav:
            self.fav_btn.icon = "heart"
            self.fav_btn.icon_color = (0.9, 0.2, 0.2, 1)  # Red
        else:
            self.fav_btn.icon = "heart-outline"
            self.fav_btn.icon_color = LIGHT_THEME["text_primary"]

    def toggle_favorite(self, *args):
        if not self.root_layout.songs or self.root_layout.current_song_index is None or self.root_layout.current_song_index < 0: return
        song = self.root_layout.songs[self.root_layout.current_song_index]
        from models.database import toggle_favorite
        is_fav = toggle_favorite(song[3])
        self.update_favorite_state(is_fav)
        # also update NowPlayingScreen
        now_screen = App.get_running_app().root.screen_manager.get_screen("now_playing")
        if hasattr(now_screen, 'update_favorite_state'):
            now_screen.update_favorite_state(is_fav)

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return super().on_touch_down(touch)
        if super().on_touch_down(touch):
            return True
        touch.ud['mp_swipe_start_x'] = touch.x
        touch.ud['mp_swipe_start_y'] = touch.y
        Animation(rgba=LIGHT_THEME["surface_alt"], duration=0.1).start(self.bg_color)
        Animation(x=0.97, y=0.97, duration=0.15, t="out_quad").start(self.scale_inst)
        self._touch_valid = True
        return True
    
    def on_touch_move(self, touch):
        if hasattr(self, '_touch_valid') and self._touch_valid:
            if not self.collide_point(*touch.pos):
                self._cancel_touch()
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if hasattr(self, '_touch_valid') and self._touch_valid:
            self._cancel_touch()
            if 'mp_swipe_start_x' in touch.ud:
                dx = touch.x - touch.ud['mp_swipe_start_x']
                dy = touch.y - touch.ud['mp_swipe_start_y']
                
                # Check for swipe right or left
                if abs(dx) > dp(50) and abs(dx) > abs(dy):
                    if not self.root_layout.is_playing:
                        self.root_layout.hide_mini_player()
                    return True
                # Check for swipe down
                if dy < -dp(50) and abs(dy) > abs(dx):
                    if not self.root_layout.is_playing:
                        self.root_layout.hide_mini_player()
                    return True
            self.root_layout.go_to("now_playing")
        return super().on_touch_up(touch)

    def _cancel_touch(self):
        self._touch_valid = False
        Animation(rgba=LIGHT_THEME["surface"], duration=0.2).start(self.bg_color)
        Animation(x=1.0, y=1.0, duration=0.25, t="out_back").start(self.scale_inst)

    def update_song(self, title, artist):
        self.title_label.text = title
        self.artist_label.text = artist

    def set_artwork(self, path):
        self.artwork.set_artwork(path)



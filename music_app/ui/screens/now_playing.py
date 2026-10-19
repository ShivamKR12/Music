from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.app import App

from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton, MDFabButton
from kivymd.uix.slider import MDSlider, MDSliderHandle
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout

from config import LIGHT_THEME
from ui.components import ArtworkIcon

class NowPlayingScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_container = MDBoxLayout(orientation="vertical", padding=[dp(24), dp(32), dp(24), dp(32)], spacing=dp(16))
        
        top_bar = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(56), padding=[dp(8), 0])
        back_btn = MDIconButton(
            icon="arrow-left", 
            theme_icon_color="Custom",
            icon_color=LIGHT_THEME["icon"], 
            pos_hint={"center_y": 0.5},
            on_release=self.go_back
        )
        top_bar.add_widget(back_btn)
        top_bar.add_widget(Widget())
        
        self.menu_btn = MDIconButton(
            icon="dots-vertical",
            theme_icon_color="Custom",
            icon_color=LIGHT_THEME["icon"],
            pos_hint={"center_y": 0.5},
            on_release=self.open_bottom_menu
        )
        top_bar.add_widget(self.menu_btn)
        self.main_container.add_widget(top_bar)
        
        self.hero = MDCard(
            style="filled",
            theme_bg_color="Custom",
            md_bg_color=(0.95, 0.95, 0.97, 1), # LIGHT_THEME surface_alt
            size_hint_y=1,
            radius=[dp(32)]
        )
        
        self.hero_content = MDBoxLayout(orientation="vertical", spacing=dp(16), padding=dp(24))
        
        art_container = MDAnchorLayout(anchor_x="center", anchor_y="center")
        self.artwork = ArtworkIcon(size_hint=(None, None))
        def _update_art_size(instance, size):
            side = min(instance.width, instance.height)
            self.artwork.size = (side, side)
        art_container.bind(size=_update_art_size)
        art_container.add_widget(self.artwork)
        self.artwork.bg.radius = [dp(32)]
        
        text_box = MDBoxLayout(orientation="vertical", size_hint_y=None, height=dp(52), spacing=dp(4))
        self.title_label = MDLabel(text="Not Playing", font_style="Headline", role="small", bold=True, halign="center", shorten=True, shorten_from="right")
        self.artist_label = MDLabel(text="Select a track", font_style="Title", role="medium", theme_text_color="Hint", halign="center", shorten=True, shorten_from="right")
        text_box.add_widget(self.title_label)
        text_box.add_widget(self.artist_label)
        
        self.hero_content.add_widget(art_container)
        self.hero_content.add_widget(text_box)
        self.hero.add_widget(self.hero_content)
        

        
        self.main_container.add_widget(self.hero)
        
        self.timeline_container = MDBoxLayout(size_hint_y=None, height=dp(48), padding=[dp(16), 0])
        self.current_time_label = MDLabel(text="0:00", font_style="Body", role="small", theme_text_color="Hint", size_hint_x=None, width=dp(48), halign="left")
        
        self.slider = MDSlider(
            MDSliderHandle(),
            value=0
        )
        self.slider.bind(on_touch_down=self.on_slider_touch_down, on_touch_up=self.on_slider_touch_up, on_touch_move=self.on_slider_touch_move)
        
        self.total_time_label = MDLabel(text="0:00", font_style="Body", role="small", theme_text_color="Hint", size_hint_x=None, width=dp(48), halign="right")
        
        self.fav_btn = MDIconButton(
            icon="heart-outline", 
            theme_icon_color="Custom", 
            icon_color=LIGHT_THEME["icon"],
            pos_hint={'center_y': 0.5},
            on_release=self.toggle_favorite
        )
        
        self.timeline_container.add_widget(self.current_time_label)
        self.timeline_container.add_widget(self.slider)
        self.timeline_container.add_widget(self.total_time_label)
        self.timeline_container.add_widget(self.fav_btn)
        self.main_container.add_widget(self.timeline_container)
        
        self.controls = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(96), spacing=dp(12), padding=[dp(16), 0])
        
        self.shuffle_btn = MDIconButton(icon="shuffle", theme_icon_color="Custom", icon_color=LIGHT_THEME["icon"], pos_hint={'center_y': 0.5})
        self.prev_btn = MDIconButton(icon="skip-previous", theme_icon_color="Custom", icon_color=LIGHT_THEME["icon"], pos_hint={'center_y': 0.5}, on_release=self.previous)
        
        from kivy.uix.behaviors import ButtonBehavior
        class PlayContainer(ButtonBehavior, MDAnchorLayout):
            pass
            
        self.play_container = PlayContainer(
            anchor_x="center", anchor_y="center", 
            size_hint=(None, None), size=(dp(64), dp(64)),
            pos_hint={'center_y': 0.5}
        )
        
        with self.play_container.canvas.before:
            from kivy.graphics import Color, RoundedRectangle
            self.play_bg_color = Color(0.2, 0.6, 1.0, 1)
            self.play_bg = RoundedRectangle(pos=self.play_container.pos, size=self.play_container.size, radius=[dp(20)])
            
        def _update_bg(instance, value):
            self.play_bg.pos = instance.pos
            self.play_bg.size = instance.size
        self.play_container.bind(pos=_update_bg, size=_update_bg)
        self.play_container.bind(on_release=lambda *_: App.get_running_app().root.toggle_play())
        
        from kivymd.uix.label import MDIcon
        self.play_btn = MDIcon(
            icon="play",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            halign="center",
            valign="center",
            font_size=dp(36)
        )
        
        from kivymd.uix.progressindicator import MDCircularProgressIndicator
        self.play_spinner = MDCircularProgressIndicator(
            size_hint=(None, None),
            size=(dp(48), dp(48)),
            active=False,
            opacity=0,
            color=(0.2, 0.6, 1.0, 1)
        )
        
        self.play_container.add_widget(self.play_btn)
        self.play_container.add_widget(self.play_spinner)
        
        self.next_btn = MDIconButton(icon="skip-next", theme_icon_color="Custom", icon_color=LIGHT_THEME["icon"], pos_hint={'center_y': 0.5}, on_release=self.next)
        self.repeat_btn = MDIconButton(icon="repeat-off", theme_icon_color="Custom", icon_color=LIGHT_THEME["icon"], pos_hint={'center_y': 0.5})

        self.shuffle_btn.bind(on_release=lambda *_: App.get_running_app().root.toggle_shuffle())
        self.repeat_btn.bind(on_release=lambda *_: App.get_running_app().root.toggle_repeat())
        
        self.controls.add_widget(Widget())
        self.controls.add_widget(self.shuffle_btn)
        self.controls.add_widget(self.prev_btn)
        self.controls.add_widget(self.play_container)
        self.controls.add_widget(self.next_btn)
        self.controls.add_widget(self.repeat_btn)
        self.controls.add_widget(Widget())
        self.main_container.add_widget(self.controls)
        self.add_widget(self.main_container)
        self.seeking = False
        self.playlist_dialog = None

    def open_bottom_menu(self, *args):
        from models.database import is_favorite
        root_layout = App.get_running_app().root
        current_video_id = None
        if root_layout.current_song_index is not None:
            current_video_id = root_layout.songs[root_layout.current_song_index][3]
            
        is_fav = False
        if current_video_id:
            is_fav = is_favorite(current_video_id)

        if hasattr(self, 'bottom_menu') and self.bottom_menu:
            self.like_icon.icon = "heart" if is_fav else "heart-outline"
            self.like_icon.theme_icon_color = "Custom"
            self.like_icon.icon_color = (1, 0, 0, 1) if is_fav else LIGHT_THEME["icon"]
            self.bottom_menu.set_state("open")
            return
            
        from kivymd.uix.bottomsheet import MDBottomSheet, MDBottomSheetDragHandle
        from kivymd.uix.list import MDList, MDListItem, MDListItemLeadingIcon, MDListItemHeadlineText
        from kivymd.uix.boxlayout import MDBoxLayout
        
        self.bottom_menu = MDBottomSheet(
            size_hint_y=None,
            height=dp(300),
            radius=[dp(24), dp(24), 0, 0]
        )
        
        # Completely bypass KivyMD's strict physics threshold by observing the movement progress directly
        def _on_open_progress(instance, value):
            if value < 0.90 and getattr(instance, 'status', '') in ["closing_with_swipe", "opened"]:
                instance.set_state("close")
        self.bottom_menu.bind(open_progress=_on_open_progress)
        
        layout = MDBoxLayout(orientation="vertical", spacing=dp(8))
        layout.add_widget(MDBottomSheetDragHandle())
        
        lst = MDList(spacing=dp(4))
        
        self.like_icon = MDListItemLeadingIcon(
            icon="heart" if is_fav else "heart-outline",
            theme_icon_color="Custom",
            icon_color=(1, 0, 0, 1) if is_fav else LIGHT_THEME["icon"]
        )
        
        # Helper to ignore clicks if it was actually a drag gesture
        def _is_drag(btn):
            touch = getattr(btn, 'last_touch', None)
            if touch:
                if abs(touch.y - touch.opos[1]) > dp(10) or abs(touch.x - touch.opos[0]) > dp(10):
                    return True
            return False

        # Like / Favorite
        def _like(x):
            if _is_drag(x): return
            self.toggle_favorite()
                
        lst.add_widget(MDListItem(
            self.like_icon,
            MDListItemHeadlineText(text="Like"),
            on_release=_like
        ))
        
        # Add to Playlist
        def _add_playlist(x):
            if _is_drag(x): return
            self.bottom_menu.set_state("close")
            self.show_playlist_dialog()
            
        lst.add_widget(MDListItem(
            MDListItemLeadingIcon(icon="playlist-plus"),
            MDListItemHeadlineText(text="Add to playlist"),
            on_release=_add_playlist
        ))
        
        # Play Next
        def _play_next(x):
            if _is_drag(x): return
            self.bottom_menu.set_state("close")
            self.show_message("Queue modified: Playing next")
            
        lst.add_widget(MDListItem(
            MDListItemLeadingIcon(icon="skip-next"),
            MDListItemHeadlineText(text="Play next"),
            on_release=_play_next
        ))
        
        # Add to Queue
        def _add_queue(x):
            if _is_drag(x): return
            self.bottom_menu.set_state("close")
            self.show_message("Added to queue")
            
        lst.add_widget(MDListItem(
            MDListItemLeadingIcon(icon="playlist-play"),
            MDListItemHeadlineText(text="Add to queue"),
            on_release=_add_queue
        ))
        
        # Download
        def _download(x):
            if _is_drag(x): return
            self.bottom_menu.set_state("close")
            self.show_message("Download started")
            
        lst.add_widget(MDListItem(
            MDListItemLeadingIcon(icon="download"),
            MDListItemHeadlineText(text="Download"),
            on_release=_download
        ))
        
        layout.add_widget(lst)
        self.bottom_menu.add_widget(layout)
        
        # Add directly to the Screen (RelativeLayout) so it floats over UI
        # rather than pushing the global Root BoxLayout up!
        self.add_widget(self.bottom_menu)
        self.bottom_menu.set_state("open")

    def show_message(self, text):
        from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogButtonContainer
        from kivymd.uix.button import MDButton, MDButtonText
        dialog = MDDialog(
            MDDialogHeadlineText(text=text, halign="center")
        )
        btn = MDButton(MDButtonText(text="OK"), style="text", on_release=lambda x: dialog.dismiss())
        container = MDDialogButtonContainer()
        container.add_widget(Widget())
        container.add_widget(btn)
        dialog.add_widget(container)
        dialog.open()

    def show_playlist_dialog(self, *args):
        from models.database import get_all_playlists, add_track_to_playlist
        from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogContentContainer
        from kivymd.uix.list import MDList, MDListItem, MDListItemHeadlineText
        from kivy.metrics import dp
        
        root_layout = App.get_running_app().root
        if not root_layout.songs or root_layout.current_song_index is None: return
        song = root_layout.songs[root_layout.current_song_index]
        video_id = song[3]

        playlists = get_all_playlists()
        if not playlists: return

        lst = MDList(spacing=dp(8))
        for p_name in playlists:
            def _add_and_dismiss(x, n=p_name):
                add_track_to_playlist(n, video_id)
                self.playlist_dialog.dismiss()
                
            item = MDListItem(
                MDListItemHeadlineText(text=p_name),
                radius=[dp(12)],
                theme_bg_color="Custom",
                md_bg_color=(0.95, 0.95, 0.97, 1),
                on_release=_add_and_dismiss
            )
            lst.add_widget(item)

        scroll = MDScrollView(size_hint_y=None, height=dp(200))
        scroll.add_widget(lst)

        self.playlist_dialog = MDDialog(
            MDDialogHeadlineText(text="Add to Playlist"),
            MDDialogContentContainer(scroll, orientation="vertical")
        )
        self.playlist_dialog.open()

    def update_play_state(self, is_playing):
        self.play_btn.icon = "pause" if is_playing else "play"

    def update_shuffle_state(self, enabled):
        self.shuffle_btn.opacity = 1 if enabled else 0.4
    
    def update_loading_state(self, is_loading):
        if is_loading:
            self.play_btn.opacity = 0
            self.play_container.disabled = True
            self.play_spinner.opacity = 1
            self.play_spinner.active = True
        else:
            self.play_btn.opacity = 1
            self.play_container.disabled = False
            self.play_spinner.opacity = 0
            self.play_spinner.active = False
            self.update_play_state(App.get_running_app().root.is_playing)

    def update_repeat_state(self, mode):
        if mode == "off":
            self.repeat_btn.icon = "repeat-off"
            self.repeat_btn.opacity = 0.4
        elif mode == "all":
            self.repeat_btn.icon = "repeat"
            self.repeat_btn.opacity = 1
        else:
            self.repeat_btn.icon = "repeat-once"
            self.repeat_btn.opacity = 1

    def on_slider_touch_down(self, instance, touch):
        if self.slider.collide_point(*touch.pos):
            root_layout = App.get_running_app().root
            if root_layout.audio.loading or not root_layout.audio.player: return True
            self.seeking = True
            self._was_playing_before_seek = root_layout.is_playing
            try:
                if hasattr(root_layout.audio.player, 'set_pause'):
                    root_layout.audio.player.set_pause(True)
                else:
                    root_layout.audio.player.stop()
            except: pass
            return False
        return False

    def update_favorite_state(self, is_fav):
        if is_fav:
            self.fav_btn.icon = "heart"
            self.fav_btn.icon_color = (1, 0, 0, 1)  # Red
            if hasattr(self, 'like_icon') and self.like_icon:
                self.like_icon.icon = "heart"
                self.like_icon.icon_color = (1, 0, 0, 1)
        else:
            self.fav_btn.icon = "heart-outline"
            self.fav_btn.icon_color = LIGHT_THEME["icon"]
            if hasattr(self, 'like_icon') and self.like_icon:
                self.like_icon.icon = "heart-outline"
                self.like_icon.icon_color = LIGHT_THEME["icon"]

    def toggle_favorite(self, *args):
        root_layout = App.get_running_app().root
        if not root_layout.songs or root_layout.current_song_index is None or root_layout.current_song_index < 0: return
        song = root_layout.songs[root_layout.current_song_index]
        from models.database import toggle_favorite
        is_fav = toggle_favorite(song[3])
        self.update_favorite_state(is_fav)
        root_layout.mini_player.update_favorite_state(is_fav)

    def on_slider_touch_move(self, instance, touch):
        if self.seeking:
            return False
        return False

    def on_slider_touch_up(self, instance, touch):
        if self.seeking:
            self.seeking = False
            root_layout = App.get_running_app().root
            if root_layout.audio.loading or not root_layout.audio.player or root_layout.audio.duration <= 0: return False
            
            seek_time = (self.slider.value / 100.0) * root_layout.audio.duration
            try:
                if hasattr(root_layout.audio.player, 'seek'):
                    try:
                        root_layout.audio.player.seek(seek_time, relative=False)
                    except TypeError:
                        root_layout.audio.player.seek(seek_time)
                root_layout.audio.elapsed = seek_time
            except Exception as e:
                print("Seek exception:", e)
                
            if self._was_playing_before_seek:
                try:
                    if hasattr(root_layout.audio.player, 'set_pause'):
                        root_layout.audio.player.set_pause(False)
                    else:
                        root_layout.audio.player.play()
                        if hasattr(root_layout.audio.player, 'seek'):
                            try: root_layout.audio.player.seek(seek_time, relative=False)
                            except TypeError: root_layout.audio.player.seek(seek_time)
                except: pass
            return False
        return False

    def animate_song_change(self, new_title, new_artist):
        Animation.cancel_all(self.title_label)
        Animation.cancel_all(self.artist_label)
        Animation.cancel_all(self.artwork.scale_inst)
        
        out_anim = Animation(opacity=0, duration=0.15, t="in_quad")
        def update_text(*args):
            self.title_label.text = new_title
            self.artist_label.text = new_artist
            Animation(opacity=1, duration=0.3, t="out_back").start(self.title_label)
            Animation(opacity=0.8, duration=0.35, t="out_back").start(self.artist_label)
            
            self.artwork.scale_inst.xyz = (0.9, 0.9, 1)
            Animation(x=1.0, y=1.0, duration=0.4, t="out_back").start(self.artwork.scale_inst)
        out_anim.bind(on_complete=update_text)
        out_anim.start(self.title_label)
        out_anim.start(self.artist_label)


    def next(self, *args, **kwargs): App.get_running_app().root.next_song()
    def previous(self, *args, **kwargs): App.get_running_app().root.previous_song()
    def go_back(self, *args): App.get_running_app().root.go_back()
    
    def reset_timeline(self):
        self.update_timeline_state(0, 0, 0)

    def update_timeline_state(self, progress, elapsed, duration):
        if not self.seeking:
            self.slider.value = progress * 100 if progress else 0
        self.current_time_label.text = f"{int(elapsed)//60}:{int(elapsed)%60:02d}"
        self.total_time_label.text = f"{int(duration)//60}:{int(duration)%60:02d}"

    def on_touch_down(self, touch):
        if hasattr(self, 'bottom_menu') and self.bottom_menu and self.bottom_menu.collide_point(*touch.pos):
            touch.ud['started_on_bottom_menu'] = True
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        dy = touch.y - touch.opos[1]
        dx = touch.x - touch.opos[0]
        
        # Main Screen swipe down
        if self.collide_point(*touch.opos):
            if dy < -dp(50) and abs(dy) > abs(dx):
                # Completely ignore the swipe if it originated on the bottom sheet, regardless of its current state
                if touch.ud.get('started_on_bottom_menu'):
                    return super().on_touch_up(touch)
                self.go_back()
                return True
                
        return super().on_touch_up(touch)
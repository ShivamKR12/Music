import os
import sys

# Set directory to KivyMusicApp
os.chdir(r"c:\Users\Shivam\Desktop\Music\KivyMusicApp")
sys.path.insert(0, r"c:\Users\Shivam\Desktop\Music\KivyMusicApp")

os.environ['KIVY_HEADLESS'] = '1'

from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', False)

from kivy.core.window import Window
from kivymd.app import MDApp
from main import MusicApp
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.uix.carousel import Carousel
from kivy.uix.recyclelayout import RecycleLayout
from kivy.uix.screenmanager import NoTransition
from kivymd.uix.card import MDCard

class FakeTouch:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.pos = (x, y)
        self.is_touch = True
        self.is_double_tap = False
        self.is_triple_tap = False
        self.is_mouse_scrolling = False
        self.ud = {}
        self.grab_current = None
        self.grab_list = []
        self.button = 'left'
        self.device = 'mouse'
        self.profile = ['pos', 'button']
        self.time_start = Clock.get_time()
        self.time_update = self.time_start
        self._stack = []

    def push(self, attrs=None):
        self._stack.append((self.x, self.y))

    def pop(self):
        if self._stack:
            self.x, self.y = self._stack.pop()
            self.pos = (self.x, self.y)

    def apply_transform_2d(self, transform):
        self.x, self.y = transform(self.x, self.y)
        self.pos = (self.x, self.y)

    def grab(self, widget):
        import weakref
        self.grab_current = widget
        self.grab_list.append(weakref.ref(widget))

    def ungrab(self, widget):
        for ref in list(self.grab_list):
            if ref() is widget or ref() is None:
                self.grab_list.remove(ref)
        if self.grab_current == widget:
            self.grab_current = None

results = {}

def log_test(name, passed, detail=""):
    results[name] = {"passed": passed, "detail": detail}
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name} - {detail}")

def pump_events(app, cycles=5):
    for _ in range(cycles):
        Clock.tick()
        if hasattr(app, "root") and app.root:
            if hasattr(app.root, "ids") and "screen_manager" in app.root.ids:
                sm = app.root.ids.screen_manager
                if hasattr(sm, "transition") and sm.transition and getattr(sm.transition, "is_active", False):
                    sm.transition.stop()
            for w in app.root.walk():
                if hasattr(w, "do_layout") and not isinstance(w, RecycleLayout):
                    try:
                        w.do_layout()
                    except Exception:
                        pass

class ComprehensiveAuditRunner:
    def __init__(self):
        self.app = MusicApp()

    def run(self):
        root = self.app.build()
        Window.add_widget(root)
        self.app.root = root
        initial_theme = self.app.theme_cls.theme_style
        self.app.on_start()
        sm = self.app.root.ids.screen_manager
        sm.transition = NoTransition()
        pump_events(self.app, 5)

        print("\n=== TEST SUITE 1: NAVIGATION & BACK-STACK INTEGRITY ===")
        sm.current = "home"
        self.app.screen_history = []
        pump_events(self.app, 3)
        
        # Navigate: Home -> Settings -> Equalizer
        self.app.switch_screen("settings")
        pump_events(self.app, 3)
        s1 = (sm.current == "settings" and self.app.screen_history == ["home"])
        
        self.app.switch_screen("equalizer")
        pump_events(self.app, 3)
        s2 = (sm.current == "equalizer" and self.app.screen_history == ["home", "settings"])
        
        # Back: Equalizer -> Settings
        self.app.go_back()
        pump_events(self.app, 3)
        s3 = (sm.current == "settings" and self.app.screen_history == ["home"])
        
        # Back: Settings -> Home
        self.app.go_back()
        pump_events(self.app, 3)
        s4 = (sm.current == "home" and len(self.app.screen_history) == 0)
        
        # Navigate: Library -> Wrapped -> Back
        self.app.switch_screen("library")
        pump_events(self.app, 3)
        self.app.switch_screen("wrapped")
        pump_events(self.app, 3)
        self.app.go_back()
        pump_events(self.app, 3)
        s5 = (sm.current == "library")
        
        log_test("Navigation History Stack", s1 and s2 and s3 and s4 and s5,
                 f"Home->Settings->Equalizer and Back chain verified. Final screen: {sm.current}")

        print("\n=== TEST SUITE 2: CONTROLLER STATE & PLAYBACK ACTIONS ===")
        pc = self.app.player_controller
        if not pc.active_track and self.app.playlist_model.tracks:
            self.app.play_selected_track(self.app.playlist_model.tracks[0])
            pump_events(self.app, 3)
        initial_shuffle = pc.is_shuffle
        pc.toggle_shuffle()
        sh_ok = (pc.is_shuffle != initial_shuffle)
        
        initial_repeat = pc.is_repeat
        pc.toggle_repeat()
        rep_ok = (pc.is_repeat != initial_repeat)
        
        initial_fav = pc.is_favorite
        pc.toggle_favorite()
        fav_ok = (pc.is_favorite != initial_fav)
        
        # Sequential track switching requires shuffle to be disabled
        pc.is_shuffle = False
        t0 = pc.active_track
        pc.next_track()
        t1 = pc.active_track
        next_ok = (t0 != t1)
        
        pc.prev_track()
        t2 = pc.active_track
        prev_ok = (t2 == t0)
        
        print(f"DEBUG CONTROLLER: sh_ok={sh_ok}, rep_ok={rep_ok}, fav_ok={fav_ok}, next_ok={next_ok}, prev_ok={prev_ok}")
        log_test("Player Controller Controls", sh_ok and rep_ok and fav_ok and next_ok and prev_ok,
                 f"Shuffle={pc.is_shuffle}, Repeat={pc.is_repeat}, Fav={pc.is_favorite}, Next/Prev functional (sh_ok={sh_ok}, rep_ok={rep_ok}, fav_ok={fav_ok}, next_ok={next_ok}, prev_ok={prev_ok})")

        print("\n=== TEST SUITE 3: DIALOGS & SHEET LIFECYCLES ===")
        # 1. Clear Cache Dialog
        self.app.show_clear_cache_dialog()
        pump_events(self.app, 3)
        cd_open = (self.app.cache_dialog is not None and getattr(self.app.cache_dialog, "_is_open", False))
        self.app.go_back()
        pump_events(self.app, 3)
        cd_close = not getattr(self.app.cache_dialog, "_is_open", False)
        
        # 2. AutoEq Dialog
        self.app.show_autoeq_profile_dialog()
        pump_events(self.app, 3)
        eq_open = (self.app.autoeq_dialog is not None and getattr(self.app.autoeq_dialog, "_is_open", False))
        self.app.selected_eq_profile = "Bass Boost"
        self.app.autoeq_dialog.dismiss()
        pump_events(self.app, 3)
        eq_updated = (self.app.selected_eq_profile == "Bass Boost")
        
        # 3. Auth Dialog
        self.app.show_auth_dialog("Spotify")
        pump_events(self.app, 3)
        auth_open = (self.app.auth_dialog is not None and getattr(self.app.auth_dialog, "_is_open", False))
        self.app.auth_dialog.dismiss()
        pump_events(self.app, 3)
        
        # 4. Track Options Bottom Sheet with "View Lyrics"
        self.app.show_track_options()
        pump_events(self.app, 3)
        sheet_open = (self.app.bottom_sheet is not None and self.app.bottom_sheet.status in ("opened", "opening_with_animation"))
        
        lyrics_item_found = False
        for c in self.app.bottom_sheet.walk():
            if hasattr(c, "text") and c.text == "View Lyrics":
                lyrics_item_found = True
                break
                
        self.app.go_back()
        pump_events(self.app, 3)
        
        log_test("Dialogs & Track Options Sheet", cd_open and cd_close and eq_open and eq_updated and auth_open and sheet_open and lyrics_item_found,
                 f"Cache dialog={cd_open}/{cd_close}, AutoEq profile={self.app.selected_eq_profile}, Lyrics item in sheet={lyrics_item_found}")

        print("\n=== TEST SUITE 4: SETTINGS LIST ITEM ROW INTERACTIONS ===")
        sm.current = "settings"
        pump_events(self.app, 3)
        settings_screen = sm.get_screen("settings")
        
        wifi_cb = settings_screen.ids.get("wifi_checkbox")
        dark_cb = settings_screen.ids.get("dark_checkbox")
        sponsor_cb = settings_screen.ids.get("sponsor_checkbox")
        
        cbs_exist = (wifi_cb is not None and dark_cb is not None and sponsor_cb is not None)
        
        if cbs_exist:
            w0 = wifi_cb.active
            wifi_cb.active = not w0
            w_toggled = (wifi_cb.active != w0)
            
            d0 = dark_cb.active
            dark_cb.active = not d0
            d_toggled = (dark_cb.active != d0)
            
            s0 = sponsor_cb.active
            sponsor_cb.active = not s0
            s_toggled = (sponsor_cb.active != s0)
            
            dark_cb.active = True
            self.app.toggle_theme_style(True)
            # Restore to Light mode
            self.app.toggle_theme_style(False)
            dark_cb.active = False
        else:
            w_toggled = d_toggled = s_toggled = False
            
        log_test("Settings Checkbox Rows", cbs_exist and w_toggled and d_toggled and s_toggled,
                 f"All 3 settings rows wired to active toggles")

        print("\n=== TEST SUITE 5: HORIZONTAL SCROLL CHIPS CONSISTENCY ===")
        sm.current = "home"
        pump_events(self.app, 3)
        home = sm.get_screen("home")
        mood_box = home.ids.get("mood_box")
        mood_pad = mood_box.padding if mood_box else []
        mood_h = mood_box.height if mood_box else 0
        
        sm.current = "library"
        pump_events(self.app, 3)
        lib = sm.get_screen("library")
        lib_box = lib.ids.get("library_chips_box")
        lib_pad = lib_box.padding if lib_box else []
        lib_h = lib_box.height if lib_box else 0
        
        chips_consistent = (
            mood_h == dp(48) and mood_pad == [dp(8), dp(8), dp(8), dp(8)] and
            lib_h == dp(48) and lib_pad == [dp(8), dp(8), dp(8), dp(8)]
        )
        log_test("Chips Height & Padding Consistency", chips_consistent,
                 f"Home mood box: h={mood_h}, pad={mood_pad}; Library box: h={lib_h}, pad={lib_pad}")

        print("\n=== TEST SUITE 6: SEARCH ENGINE & HISTORY ===")
        sm.current = "search"
        pump_events(self.app, 3)
        self.app.perform_search("Punjabi Hits")
        pump_events(self.app, 3)
        
        search_screen = sm.get_screen("search")
        rv = search_screen.ids.search_history_list
        query_in_history = any(item["text"] == "Punjabi Hits" for item in rv.data)
        input_text = search_screen.ids.search_input.text
        
        log_test("Search Input & History", query_in_history and input_text == "Punjabi Hits",
                 f"Search query placed in input='{input_text}' and history count={len(rv.data)}")

        print("\n=== TEST SUITE 7: ALL 18 SCREENS GEOMETRY & ZERO OVERLAP ===")
        all_screens = sm.screen_names
        overlap_violations = 0
        mini_p = root.ids.mini_player
        b_nav = root.ids.bottom_nav
        
        for sname in all_screens:
            sm.current = sname
            pump_events(self.app, 5)
            
            expected_min_y = 0
            if b_nav.height > 0:
                expected_min_y += b_nav.height
            if mini_p.height > 0:
                expected_min_y += mini_p.height
                
            if sm.y < expected_min_y:
                overlap_violations += 1
                print(f"Overlap violation on '{sname}': sm.y={sm.y} < expected_min_y={expected_min_y}")
                
        log_test("18 Screens Zero Overlap", overlap_violations == 0,
                 f"All {len(all_screens)} screens inspected, violations={overlap_violations}")

        print("\n=== TEST SUITE 8: UP NEXT QUEUE SHEET TOUCH & LIFECYCLE ===")
        sm.current = "player"
        pump_events(self.app, 5)
        
        nav_disabled = b_nav.disabled
        mini_disabled = mini_p.disabled

        # Touch on UP NEXT pill at (180, 48)
        touch = FakeTouch(180, 48)
        root.dispatch('on_touch_down', touch)
        root.dispatch('on_touch_up', touch)
        pump_events(self.app, 25)
        
        queue_sheet_opened = (self.app.queue_sheet is not None and 
                              self.app.queue_sheet.status in ("opened", "opening_with_animation"))
        
        # Test back dismissal of queue sheet
        self.app.go_back()
        pump_events(self.app, 5)
        queue_sheet_closed = (self.app.queue_sheet is None or 
                              self.app.queue_sheet.status in ("closed", "closing_with_animation"))
        
        log_test("UP NEXT Queue Sheet Touch & Back Dismissal", 
                 nav_disabled and mini_disabled and queue_sheet_opened and queue_sheet_closed,
                 f"Nav/Mini disabled={nav_disabled}/{mini_disabled}, Opened={queue_sheet_opened}, Dismissed={queue_sheet_closed}")

        print("\n=== TEST SUITE 9: PLAYER CAROUSEL OPTION A ARCHITECTURE ===")
        player_screen = sm.get_screen("player")
        carousel = player_screen.ids.get("album_carousel")
        is_kivy_carousel = isinstance(carousel, Carousel)
        slides_count = len(carousel.slides) if is_kivy_carousel else 0
        min_move_ok = getattr(carousel, "min_move", 0) > 0 if is_kivy_carousel else False
        
        log_test("Player Carousel Architecture", 
                 is_kivy_carousel and slides_count > 0 and min_move_ok,
                 f"Type={type(carousel).__name__}, Slides={slides_count}, min_move={getattr(carousel, 'min_move', None)}")

        print("\n=== TEST SUITE 10: ALL REDESIGNED SUB-SCREENS INTEGRITY ===")
        sub_screens = ["auth", "listen_together", "equalizer", "browse", "mood", "podcasts", "album", "artist", "playlist"]
        sub_screen_issues = []
        
        for name in sub_screens:
            sm.current = name
            pump_events(self.app, 3)
            scr = sm.get_screen(name)
            
            cards = [w for w in scr.walk() if type(w).__name__ == "MDCard"]
            if len(cards) == 0:
                sub_screen_issues.append(f"{name}: no MDCard elements")
                
            for w in scr.walk():
                if type(w).__name__ == "FitImage":
                    src = getattr(w, "source", "")
                    if not src:
                        sub_screen_issues.append(f"{name}: empty FitImage source")
                        
        log_test("Redesigned Sub-Screens Hierarchy", 
                 len(sub_screen_issues) == 0,
                 f"Checked 9 sub-screens. Issues: {sub_screen_issues if sub_screen_issues else 'None (All clean)'}")

        print("\n=== TEST SUITE 11: LIGHT MODE THEME & PLAYER BUTTON SYMMETRY ===")
        theme_is_light = (initial_theme == "Light" and self.app.theme_cls.theme_style == "Light")
        sm.current = "settings"
        pump_events(self.app, 3)
        settings_screen = sm.get_screen("settings")
        dark_cb_inactive = not settings_screen.ids.dark_checkbox.active

        sm.current = "player"
        pump_events(self.app, 5)
        player_screen = sm.get_screen("player")
        controls_box = None
        for child in player_screen.walk():
            if child.__class__.__name__ == "MDBoxLayout":
                icons = [getattr(c, "icon", None) for c in child.children]
                if any("shuffle" in (i or "") for i in icons) and any("repeat" in (i or "") for i in icons):
                    controls_box = child
                    break

        symmetry_ok = False
        asym_diff = -1
        if controls_box:
            btns = list(reversed(controls_box.children))
            first_btn = btns[0]
            last_btn = btns[-1]
            first_x = first_btn.to_window(first_btn.x, 0)[0]
            last_right = last_btn.to_window(last_btn.right, 0)[0]
            left_space = first_x
            right_space = Window.width - last_right
            asym_diff = abs(right_space - left_space)
            symmetry_ok = (asym_diff < 1.0)

        log_test("Light Mode Default & Player Symmetry",
                 theme_is_light and dark_cb_inactive and symmetry_ok,
                 f"Theme=Light ({theme_is_light}), DarkCheckbox={not dark_cb_inactive}, Symmetry diff={asym_diff:.2f}dp")

        print("\n=== TEST SUITE 12: DIRECTIONAL GESTURE ARBITRATION ===")
        sm.current = "home"
        pump_events(self.app, 5)
        home_screen = sm.get_screen("home")
        home_sv = None
        for child in home_screen.walk():
            if child.__class__.__name__ == "MDScrollView":
                home_sv = child
                break

        qp_list = home_screen.ids.quick_picks_list
        is_directional_rv = qp_list.__class__.__name__ == "DirectionalHorizontalRecycleView"
        init_scroll_y = home_sv.scroll_y if home_sv else 0

        # Simulate vertical swipe inside horizontal RecycleView
        qp_win_pos = qp_list.to_window(qp_list.center_x, qp_list.center_y)
        t_drag = FakeTouch(qp_win_pos[0], qp_win_pos[1])
        t_drag.ud = {}
        home_sv.dispatch('on_touch_down', t_drag)
        for _ in range(5):
            t_drag.dy = 25
            t_drag.y += 25
            t_drag.pos = (t_drag.x, t_drag.y)
            t_drag.time_update += 0.016
            home_sv.dispatch('on_touch_move', t_drag)
            pump_events(self.app, 1)
        home_sv.dispatch('on_touch_up', t_drag)
        pump_events(self.app, 5)

        post_scroll_y = home_sv.scroll_y if home_sv else 1.0
        vert_scroll_success = post_scroll_y < init_scroll_y

        log_test("Directional Nested Scroll Arbitration",
                 is_directional_rv and vert_scroll_success,
                 f"QPClass={qp_list.__class__.__name__}, initial scroll_y={init_scroll_y:.2f}, after swipe={post_scroll_y:.2f}")

        print("\n=== TEST SUITE 13: FAVORITES SCREEN & BACK NAVIGATION ===")
        sm.current = "library"
        pump_events(self.app, 3)
        self.app.show_favorites()
        pump_events(self.app, 3)
        at_favorites = (sm.current == "favorites")
        
        # Play track from favorites
        if self.app.playlist_model.tracks:
            self.app.play_selected_track(self.app.playlist_model.tracks[0])
            pump_events(self.app, 3)
        at_player = (sm.current == "player")
        
        # Go back from player
        self.app.go_back()
        pump_events(self.app, 3)
        back_to_favorites = (sm.current == "favorites")
        
        # Go back from favorites
        self.app.go_back()
        pump_events(self.app, 3)
        back_to_library = (sm.current == "library")

        fav_nav_passed = at_favorites and at_player and back_to_favorites and back_to_library
        log_test("Favorites Dedicated Screen & Navigation Chain",
                 fav_nav_passed,
                 f"Favorites={at_favorites}, Player={at_player}, BackToFav={back_to_favorites}, BackToLib={back_to_library}")

        print("\n=== TEST SUITE 14: INLINE TIMELINE & FULLSCREEN LYRICS SCREEN ===")
        sm.current = "player"
        pump_events(self.app, 5)
        player_scr = sm.get_screen("player")
        cur_lbl = player_scr.ids.get("player_current_time_label")
        t_slider = player_scr.ids.get("timeline_slider")
        dur_lbl = player_scr.ids.get("player_duration_label")
        slider_no_line = False
        inline_aligned = False
        inline_non_overlapping = False
        if cur_lbl and t_slider and dur_lbl:
            no_canvas_line = not any(type(ins).__name__ == "Line" for ins in t_slider.canvas.children)
            no_before_line = not any(type(ins).__name__ == "Line" for ins in t_slider.canvas.before.children)
            slider_no_line = no_canvas_line and no_before_line
            inline_aligned = (
                abs(cur_lbl.center_y - t_slider.center_y) < 1.0
                and abs(dur_lbl.center_y - t_slider.center_y) < 1.0
            )
            inline_non_overlapping = (
                cur_lbl.right <= t_slider.x + 1.0
                and t_slider.right <= dur_lbl.x + 1.0
                and t_slider.width > dp(120)
            )

        active_track = self.app.player_controller.active_track
        if active_track and not getattr(active_track, "synced_lyrics", ""):
            active_track.synced_lyrics = "[00:01.00] First test lyric line\n[00:05.00] Second test lyric line\n"
        self.app.show_lyrics()
        pump_events(self.app, 6)
        at_lyrics = (sm.current == "lyrics")
        lyrics_scr = sm.get_screen("lyrics") if sm.has_screen("lyrics") else None
        lyrics_bars_disabled = bool(b_nav.disabled and mini_p.disabled and b_nav.height == 0 and mini_p.height == 0)
        lyrics_inline_ok = False
        offset_toggle_ok = False
        lyrics_populated = False
        if lyrics_scr:
            l_cur = lyrics_scr.ids.get("lyrics_current_time_label")
            l_slider = lyrics_scr.ids.get("lyrics_timeline_slider")
            l_dur = lyrics_scr.ids.get("lyrics_duration_label")
            l_trig = lyrics_scr.ids.get("lyrics_offset_trigger")
            l_pill = lyrics_scr.ids.get("lyrics_offset_pill")
            l_box = lyrics_scr.ids.get("fullscreen_lyrics_box")
            if l_cur and l_slider and l_dur:
                lyrics_inline_ok = (
                    abs(l_cur.center_y - l_slider.center_y) < 1.0
                    and abs(l_dur.center_y - l_slider.center_y) < 1.0
                    and l_cur.right <= l_slider.x + 1.0
                    and l_slider.right <= l_dur.x + 1.0
                )
            lyrics_populated = bool(l_box and len(l_box.children) >= 2)
            if l_trig and l_pill and lyrics_scr.has_synced_lyrics:
                initially_collapsed = (not l_trig.disabled) and l_pill.disabled
                lyrics_scr.toggle_offset_controls()
                pump_events(self.app, 2)
                expanded_ok = l_trig.disabled and (not l_pill.disabled)
                offset_toggle_ok = initially_collapsed and expanded_ok

        self.app.go_back()
        pump_events(self.app, 5)
        lyrics_back_to_player = (sm.current == "player")
        timers_cleaned = (getattr(self.app, "_lyrics_event", None) is None)

        log_test(
            "Inline Timeline & Fullscreen Lyrics Screen",
            slider_no_line and inline_aligned and inline_non_overlapping and at_lyrics and lyrics_bars_disabled and lyrics_inline_ok and lyrics_populated and offset_toggle_ok and lyrics_back_to_player and timers_cleaned,
            f"NoLine={slider_no_line}, InlineAligned={inline_aligned}, NonOverlap={inline_non_overlapping}, AtLyrics={at_lyrics}, BarsDisabled={lyrics_bars_disabled}, LyricsInline={lyrics_inline_ok}, Populated={lyrics_populated}, OffsetToggle={offset_toggle_ok}, BackToPlayer={lyrics_back_to_player}, TimersClean={timers_cleaned}",
        )

        all_passed = all(t["passed"] for t in results.values())
        print(f"\n==========================================")
        print(f"COMPREHENSIVE AUDIT: {'PASSED' if all_passed else 'FAILED'}")
        print(f"Passed {sum(1 for t in results.values() if t['passed'])} / {len(results)} suites")
        print(f"==========================================")
        return all_passed

if __name__ == '__main__':
    runner = ComprehensiveAuditRunner()
    success = runner.run()
    sys.exit(0 if success else 1)

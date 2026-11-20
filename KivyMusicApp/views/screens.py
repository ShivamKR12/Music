from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty, NumericProperty
from kivy.clock import Clock

class SplashScreen(MDScreen):
    pass

class HomeScreen(MDScreen):
    pass

class SearchScreen(MDScreen):
    pass

class LibraryScreen(MDScreen):
    pass

class SettingsScreen(MDScreen):
    pass

class PlayerScreen(MDScreen):
    pass

class AnalyticsScreen(MDScreen):
    total_tracks_text = StringProperty("0 Tracks")
    total_artists_text = StringProperty("0 Artists")
    total_playtime_text = StringProperty("0h 0m")
    most_played_text = StringProperty("None")

    bar_mon_h = NumericProperty(0.2)
    bar_tue_h = NumericProperty(0.2)
    bar_wed_h = NumericProperty(0.2)
    bar_thu_h = NumericProperty(0.2)
    bar_fri_h = NumericProperty(0.2)
    bar_sat_h = NumericProperty(0.2)
    bar_sun_h = NumericProperty(0.2)

    segment_1_name = StringProperty("Top Artist 1")
    segment_1_pct = StringProperty("40%")
    segment_1_end = NumericProperty(144)

    segment_2_name = StringProperty("Top Artist 2")
    segment_2_pct = StringProperty("35%")
    segment_2_end = NumericProperty(270)

    segment_3_name = StringProperty("Top Artist 3")
    segment_3_pct = StringProperty("25%")
    segment_3_end = NumericProperty(360)

    # Data loading is handled by MusicApp.switch_screen(); a former on_enter
    # duplicate ran 6 SQL queries a second time on every visit.

class NotificationScreen(MDScreen):
    pass

NotificationsScreen = NotificationScreen
    
class RecentlyPlayedScreen(MDScreen):
    # Data loading is handled by MusicApp.switch_screen() (see note above).
    pass

class WrappedScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.carousel_event = None

    def on_enter(self, *args):
        # Reset carousel to first slide
        self.ids.wrapped_carousel.index = 0
        # Start auto-advance every 3 seconds
        self.carousel_event = Clock.schedule_interval(self.advance_slide, 3)

    def on_leave(self, *args):
        # Stop auto-advance
        if self.carousel_event:
            self.carousel_event.cancel()
            self.carousel_event = None

    def advance_slide(self, dt):
        carousel = self.ids.wrapped_carousel
        # Advance slide using native Carousel load_next
        max_slides = 3 # Hardcoding to 3 since we have exactly 3 slides
        if carousel.index < max_slides - 1:
            carousel.load_next()
        else:
            # End of wrapped, return to library
            from kivymd.app import MDApp
            app = MDApp.get_running_app()
            if app:
                app.go_back()
            elif self.manager:
                self.manager.current = "library"

class AlbumScreen(MDScreen): pass
class ArtistScreen(MDScreen): pass
class PlaylistScreen(MDScreen): pass
class BrowseScreen(MDScreen): pass
class PodcastsScreen(MDScreen): pass
class MoodScreen(MDScreen): pass
class EqualizerScreen(MDScreen): pass
class ListenTogetherScreen(MDScreen): pass
class AuthScreen(MDScreen): pass
class FavoritesScreen(MDScreen): pass

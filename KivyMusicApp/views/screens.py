from kivymd.uix.screen import MDScreen

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

from kivy.clock import Clock

class AnalyticsScreen(MDScreen):
    pass

class NotificationScreen(MDScreen):
    pass
    
class RecentlyPlayedScreen(MDScreen):
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

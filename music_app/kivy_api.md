# Kivy API Reference

> Automatically generated from the Kivy documentation.
> Source: https://kivy.org/doc/stable/

---

## API - [`kivy._metrics`](https://kivy.org/doc/stable/api-kivy._metrics.html)

**kivy._metrics.dispatch_pixel_scale**

Dispatches all properties that and watch pixel_scale_observers.
This should be called by Metrics when it changes any of the scaling
properties.

**kivy._metrics.dpi2px**

Converts the value according to the ext.

**kivy._metrics.sync_pixel_scale**

Internal method to manually updated the scaling factors when metrics
changes, before anything has been dispatched.
Do not call in user code!

---

## API - [`kivy.animation`](https://kivy.org/doc/stable/api-kivy.animation.html)

**kivy.animation.Animation**

Bases: [`kivy.event.EventDispatcher`](https://kivy.org/doc/stable/api-kivy.event.html#kivy.event.EventDispatcher)
Create an animation definition that can be used to animate a Widget.

Changed in version 1.4.0:Added s/step parameter.
Changed in version 1.10.0:The default value of the step parameter was changed from 1/60. to 0.

**kivy.animation.Animation.animated_properties**

Return the properties used to animate.

**kivy.animation.Animation.cancel**

Cancel the animation previously applied to a widget. Same
effect as [`stop`](https://kivy.org/doc/stable/#kivy.animation.Animation.stop), except the on_complete event will
*not* be triggered!
New in version 1.4.0.

**kivy.animation.Animation.cancel_all**

Cancel all animations that concern a specific widget / list of
properties. See [`cancel`](https://kivy.org/doc/stable/#kivy.animation.Animation.cancel).
Example:

New in version 1.4.0.
Changed in version 2.1.0:If the parameter `widget` is None, all animated widgets will be
the target and cancelled. If `largs` is also given, animation of
these properties will be canceled for all animated widgets.

**kivy.animation.Animation.cancel_property**

Even if an animation is running, remove a property. It will not be
animated further. If it was the only/last property being animated,
the animation will be canceled (see [`cancel`](https://kivy.org/doc/stable/#kivy.animation.Animation.cancel))
New in version 1.4.0.

**kivy.animation.Animation.duration**

Return the duration of the animation.

**kivy.animation.Animation.have_properties_to_animate**

Return True if a widget still has properties to animate.
New in version 1.8.0.

**kivy.animation.Animation.start**

Start the animation on a widget.

**kivy.animation.Animation.stop**

Stop the animation previously applied to a widget, triggering the
on_complete event.

**kivy.animation.Animation.stop_all**

Stop all animations that concern a specific widget / list of
properties.
Example:

**kivy.animation.Animation.stop_property**

Even if an animation is running, remove a property. It will not be
animated further. If it was the only/last property being animated,
the animation will be stopped (see [`stop`](https://kivy.org/doc/stable/#kivy.animation.Animation.stop)).

**kivy.animation.Animation.transition**

Return the transition of the animation.

**kivy.animation.AnimationTransition**

Bases: `builtins.object`
Collection of animation functions to be used with the Animation object.
Easing Functions ported to Kivy from the Clutter Project
[https://developer.gnome.org/clutter/stable/ClutterAlpha.html](https://developer.gnome.org/clutter/stable/ClutterAlpha.html)
The progress parameter in each animation function is in the range 0-1.

**kivy.animation.AnimationTransition.in_back**

**kivy.animation.AnimationTransition.in_bounce**

**kivy.animation.AnimationTransition.in_circ**

**kivy.animation.AnimationTransition.in_cubic**

**kivy.animation.AnimationTransition.in_elastic**

**kivy.animation.AnimationTransition.in_expo**

**kivy.animation.AnimationTransition.in_out_back**

**kivy.animation.AnimationTransition.in_out_bounce**

**kivy.animation.AnimationTransition.in_out_circ**

**kivy.animation.AnimationTransition.in_out_cubic**

**kivy.animation.AnimationTransition.in_out_elastic**

**kivy.animation.AnimationTransition.in_out_expo**

**kivy.animation.AnimationTransition.in_out_quad**

**kivy.animation.AnimationTransition.in_out_quart**

**kivy.animation.AnimationTransition.in_out_quint**

**kivy.animation.AnimationTransition.in_out_sine**

**kivy.animation.AnimationTransition.in_quad**

**kivy.animation.AnimationTransition.in_quart**

**kivy.animation.AnimationTransition.in_quint**

**kivy.animation.AnimationTransition.in_sine**

**kivy.animation.AnimationTransition.linear**

**kivy.animation.AnimationTransition.out_back**

**kivy.animation.AnimationTransition.out_bounce**

**kivy.animation.AnimationTransition.out_circ**

**kivy.animation.AnimationTransition.out_cubic**

**kivy.animation.AnimationTransition.out_elastic**

**kivy.animation.AnimationTransition.out_expo**

**kivy.animation.AnimationTransition.out_quad**

**kivy.animation.AnimationTransition.out_quart**

**kivy.animation.AnimationTransition.out_quint**

**kivy.animation.AnimationTransition.out_sine**

---

## API - [`kivy.app`](https://kivy.org/doc/stable/api-kivy.app.html)

**kivy.app.App**

Bases: [`kivy.event.EventDispatcher`](https://kivy.org/doc/stable/api-kivy.event.html#kivy.event.EventDispatcher)
Application class, see module documentation for more information.

Changed in version 1.7.0:Parameter kv_file added.
Changed in version 1.8.0:Parameters kv_file and kv_directory are now properties of App.

**kivy.app.App.async_run**

Identical to [`run()`](https://kivy.org/doc/stable/#kivy.app.App.run), but is a coroutine and can be
scheduled in a running async event loop.
See [`kivy.app`](https://kivy.org/doc/stable/#module-kivy.app) for example usage.
New in version 2.0.0.

**kivy.app.App.build**

Initializes the application; it will be called only once.
If this method returns a widget (tree), it will be used as the root
widget and added to the window.

**kivy.app.App.build_config**

New in version 1.0.7.
This method is called before the application is initialized to
construct your [`ConfigParser`](https://kivy.org/doc/stable/api-kivy.config.html#kivy.config.ConfigParser) object. This
is where you can put any default section / key / value for your
config. If anything is set, the configuration will be
automatically saved in the file returned by
[`get_application_config()`](https://kivy.org/doc/stable/#kivy.app.App.get_application_config).

**kivy.app.App.build_settings**

New in version 1.0.7.
This method is called when the user (or you) want to show the
application settings. It is called once when the settings panel
is first opened, after which the panel is cached. It may be
called again if the cached settings panel is removed by
[`destroy_settings()`](https://kivy.org/doc/stable/#kivy.app.App.destroy_settings).
You can use this method to add settings panels and to
customise the settings widget e.g. by changing the sidebar
width. See the module documentation for full details.

**kivy.app.App.close_settings**

Close the previously opened settings panel.

**kivy.app.App.config**

Returns an instance of the [`ConfigParser`](https://kivy.org/doc/stable/api-kivy.config.html#kivy.config.ConfigParser) for
the application configuration. You can use this to query some config
tokens in the [`build()`](https://kivy.org/doc/stable/#kivy.app.App.build) method.

**kivy.app.App.create_settings**

Create the settings panel. This method will normally
be called only one time per
application life-time and the result is cached internally,
but it may be called again if the cached panel is removed
by [`destroy_settings()`](https://kivy.org/doc/stable/#kivy.app.App.destroy_settings).
By default, it will build a settings panel according to
[`settings_cls`](https://kivy.org/doc/stable/#kivy.app.App.settings_cls), call [`build_settings()`](https://kivy.org/doc/stable/#kivy.app.App.build_settings), add a Kivy panel if
[`use_kivy_settings`](https://kivy.org/doc/stable/#kivy.app.App.use_kivy_settings) is True, and bind to
on_close/on_config_change.
If you want to plug your own way of doing settings, without the Kivy
panel or close/config change events, this is the method you want to
overload.
New in version 1.8.0.

**kivy.app.App.destroy_settings**

New in version 1.8.0.
Dereferences the current settings panel if one
exists. This means that when [`App.open_settings()`](https://kivy.org/doc/stable/#kivy.app.App.open_settings) is next
run, a new panel will be created and displayed. It doesn’t
affect any of the contents of the panel, but lets you (for
instance) refresh the settings panel layout if you have
changed the settings widget in response to a screen size
change.
If you have modified [`open_settings()`](https://kivy.org/doc/stable/#kivy.app.App.open_settings) or
[`display_settings()`](https://kivy.org/doc/stable/#kivy.app.App.display_settings), you should be careful to
correctly detect if the previous settings widget has been
destroyed.

**kivy.app.App.directory**

New in version 1.0.7.
Return the directory where the application lives.

**kivy.app.App.display_settings**

New in version 1.8.0.
Display the settings panel. By default, the panel is drawn directly
on top of the window. You can define other behavior by overriding
this method, such as adding it to a ScreenManager or Popup.
You should return True if the display is successful, otherwise False.

**kivy.app.App.get_application_config**

Return the filename of your application configuration. Depending
on the platform, the application file will be stored in
different locations:
on iOS: <appdir>/Documents/.<appname>.ini
on Android: <user_data_dir>/.<appname>.ini
otherwise: <appdir>/<appname>.ini
When you are distributing your application on Desktops, please
note that if the application is meant to be installed
system-wide, the user might not have write-access to the
application directory. If you want to store user settings, you
should overload this method and change the default behavior to
save the configuration file in the user directory.

Some notes:
The tilda ‘~’ will be expanded to the user directory.
%(appdir)s will be replaced with the application [`directory`](https://kivy.org/doc/stable/#kivy.app.App.directory)
%(appname)s will be replaced with the application [`name`](https://kivy.org/doc/stable/#kivy.app.App.name)
New in version 1.0.7.
Changed in version 1.4.0:Customized the defaultpath for iOS and Android platforms. Added a
defaultpath parameter for desktop OS’s (not applicable to iOS
and Android.)
Changed in version 1.11.0:Changed the Android version to make use of the
[`user_data_dir`](https://kivy.org/doc/stable/#kivy.app.App.user_data_dir) and added a missing dot to the iOS
config file name.

**kivy.app.App.get_application_icon**

Return the icon of the application.

**kivy.app.App.get_application_name**

Return the name of the application.

**kivy.app.App.get_running_app**

Return the currently running application instance.
New in version 1.1.0.

**kivy.app.App.icon**

Icon of your application.
The icon can be located in the same directory as your main file. You can
set this as follows:

New in version 1.0.5.
Changed in version 1.8.0:icon is now a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty). Don’t set the
icon in the class as previously stated in the documentation.

**kivy.app.App.kv_directory**

Path of the directory where application kv is stored, defaults to None
New in version 1.8.0.
If a kv_directory is set, it will be used to get the initial kv file. By
default, the file is assumed to be in the same directory as the current App
definition file.

**kivy.app.App.kv_file**

Filename of the Kv file to load, defaults to None.
New in version 1.8.0.
If a kv_file is set, it will be loaded when the application starts. The
loading of the “default” kv file will be prevented.

**kivy.app.App.load_config**

(internal) This function is used for returning a ConfigParser with
the application configuration. It’s doing 3 things:
Creating an instance of a ConfigParser
Loading the default configuration by calling
[`build_config()`](https://kivy.org/doc/stable/#kivy.app.App.build_config), then
If it exists, it loads the application configuration file,
otherwise it creates one.

**kivy.app.App.load_kv**

This method is invoked the first time the app is being run if no
widget tree has been constructed before for this app.
This method then looks for a matching kv file in the same directory as
the file that contains the application class.
For example, say you have a file named main.py that contains:

This method will search for a file named showcase.kv in
the directory that contains main.py. The name of the kv file has to be
the lowercase name of the class, without the ‘App’ postfix at the end
if it exists.
You can define rules and a root widget in your kv file:

There must be only one root widget. See the [Kivy Language](https://kivy.org/doc/stable/api-kivy.lang.html)
documentation for more information on how to create kv files. If your
kv file contains a root widget, it will be used as self.root, the root
widget for the application.

**kivy.app.App.name**

New in version 1.0.7.
Return the name of the application based on the class name.

**kivy.app.App.on_config_change**

Event handler fired when a configuration token has been changed by
the settings page.
Changed in version 1.10.1:Added corresponding `on_config_change` event.

**kivy.app.App.on_pause**

Event handler called when Pause mode is requested. You should
return True if your app can go into Pause mode, otherwise
return False and your application will be stopped.
You cannot control when the application is going to go into this mode.
It’s determined by the Operating System and mostly used for mobile
devices (android/ios) and for resizing.
The default return value is True.
New in version 1.1.0.
Changed in version 1.10.0:The default return value is now True.

**kivy.app.App.on_resume**

Event handler called when your application is resuming from
the Pause mode.
New in version 1.1.0.

**kivy.app.App.on_start**

Event handler for the on_start event which is fired after
initialization (after build() has been called) but before the
application has started running.

**kivy.app.App.on_stop**

Event handler for the on_stop event which is fired when the
application has finished running (i.e. the window is about to be
closed).

**kivy.app.App.open_settings**

Open the application settings panel. It will be created the very
first time, or recreated if the previously cached panel has been
removed by [`destroy_settings()`](https://kivy.org/doc/stable/#kivy.app.App.destroy_settings). The settings panel will be
displayed with the
[`display_settings()`](https://kivy.org/doc/stable/#kivy.app.App.display_settings) method, which by default adds the
settings panel to the Window attached to your application. You
should override that method if you want to display the
settings panel differently.

**kivy.app.App.options**

Options passed to the __init__ of the App

**kivy.app.App.pause**

Pause the application.
On Android set OS state to pause, Kivy app state follows.
No functionality on other OS.
.. versionadded:: 2.2.0

**kivy.app.App.root**

The *root* widget returned by the [`build()`](https://kivy.org/doc/stable/#kivy.app.App.build) method or by the
[`load_kv()`](https://kivy.org/doc/stable/#kivy.app.App.load_kv) method if the kv file contains a root widget.

**kivy.app.App.root_window**

New in version 1.9.0.
Returns the root window instance used by [`run()`](https://kivy.org/doc/stable/#kivy.app.App.run).

**kivy.app.App.run**

Launches the app in standalone mode.

**kivy.app.App.settings_cls**

New in version 1.8.0.
The class used to construct the settings panel and
the instance passed to [`build_config()`](https://kivy.org/doc/stable/#kivy.app.App.build_config). You should
use either [`Settings`](https://kivy.org/doc/stable/api-kivy.uix.settings.html#kivy.uix.settings.Settings) or one of the provided
subclasses with different layouts
([`SettingsWithSidebar`](https://kivy.org/doc/stable/api-kivy.uix.settings.html#kivy.uix.settings.SettingsWithSidebar),
[`SettingsWithSpinner`](https://kivy.org/doc/stable/api-kivy.uix.settings.html#kivy.uix.settings.SettingsWithSpinner),
[`SettingsWithTabbedPanel`](https://kivy.org/doc/stable/api-kivy.uix.settings.html#kivy.uix.settings.SettingsWithTabbedPanel),
[`SettingsWithNoMenu`](https://kivy.org/doc/stable/api-kivy.uix.settings.html#kivy.uix.settings.SettingsWithNoMenu)). You can also create your
own Settings subclass. See the documentation
of [`Settings`](https://kivy.org/doc/stable/api-kivy.uix.settings.html#kivy.uix.settings.Settings) for more information.
[`settings_cls`](https://kivy.org/doc/stable/#kivy.app.App.settings_cls) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty)
and defaults to [`SettingsWithSpinner`](https://kivy.org/doc/stable/api-kivy.uix.settings.html#kivy.uix.settings.SettingsWithSpinner) which
displays settings panels with a spinner to switch between them. If you set
a string, the [`Factory`](https://kivy.org/doc/stable/api-kivy.factory.html#kivy.factory.Factory) will be used to resolve the
class.

**kivy.app.App.stop**

Stop the application.
If you use this method, the whole application will stop by issuing
a call to [`stopTouchApp()`](https://kivy.org/doc/stable/api-kivy.base.html#kivy.base.stopTouchApp).
Except on Android, set Android state to stop, Kivy state then follows.

**kivy.app.App.title**

Title of your application. You can set this as follows:

New in version 1.0.5.
Changed in version 1.8.0:title is now a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty). Don’t
set the title in the class as previously stated in the documentation.

**kivy.app.App.use_kivy_settings**

New in version 1.0.7.
If True, the application settings will also include the Kivy settings. If
you don’t want the user to change any kivy settings from your settings UI,
change this to False.

**kivy.app.App.user_data_dir**

New in version 1.7.0.
Returns the path to the directory in the users file system which the
application can use to store additional data.
Different platforms have different conventions with regards to where
the user can store data such as preferences, saved games and settings.
This function implements these conventions. The <app_name> directory
is created when the property is called, unless it already exists.
On iOS, ~/Documents/<app_name> is returned (which is inside the
app’s sandbox).
On Windows, %APPDATA%/<app_name> is returned.
On OS X, ~/Library/Application Support/<app_name> is returned.
On Linux, $XDG_CONFIG_HOME/<app_name> is returned.
On Android, [Context.GetFilesDir](https://developer.android.com/reference/android/content/Context.html#getFilesDir()) is returned.
Changed in version 1.11.0:On Android, this function previously returned
/sdcard/<app_name>. This folder became read-only by default
in Android API 26 and the user_data_dir has therefore been moved
to a writeable location.

**kivy.app.async_runTouchApp**

Identical to [`runTouchApp()`](https://kivy.org/doc/stable/#kivy.app.runTouchApp) but instead it is a coroutine
that can be run in an existing async event loop.
`async_lib` is the async library to use. See [`kivy.app`](https://kivy.org/doc/stable/#module-kivy.app) for details
and example usage.
New in version 2.0.0.

**kivy.app.runTouchApp**

Static main function that starts the application loop.
You can access some magic via the following arguments:
See [`kivy.app`](https://kivy.org/doc/stable/#module-kivy.app) for example usage.

**kivy.app.stopTouchApp**

Stop the current application by leaving the main loop.
See [`kivy.app`](https://kivy.org/doc/stable/#module-kivy.app) for example usage.

---

## API - [`kivy.atlas`](https://kivy.org/doc/stable/api-kivy.atlas.html)

**kivy.atlas.Atlas**

Bases: [`kivy.event.EventDispatcher`](https://kivy.org/doc/stable/api-kivy.event.html#kivy.event.EventDispatcher)
Manage texture atlas. See module documentation for more information.

**kivy.atlas.Atlas.create**

This method can be used to create an atlas manually from a set of
images.

**kivy.atlas.Atlas.filename**

Filename of the current Atlas.
[`filename`](https://kivy.org/doc/stable/#kivy.atlas.Atlas.filename) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) and defaults
to None.

**kivy.atlas.Atlas.original_textures**

List of original atlas textures (which contain the [`textures`](https://kivy.org/doc/stable/#kivy.atlas.Atlas.textures)).
[`original_textures`](https://kivy.org/doc/stable/#kivy.atlas.Atlas.original_textures) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) and
defaults to [].
New in version 1.9.1.

**kivy.atlas.Atlas.textures**

List of available textures within the atlas.
[`textures`](https://kivy.org/doc/stable/#kivy.atlas.Atlas.textures) is a [`DictProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.DictProperty) and defaults
to {}.

---

## API - [`kivy.base`](https://kivy.org/doc/stable/api-kivy.base.html)

**kivy.base.EventLoop**

EventLoop instance

**kivy.base.EventLoopBase**

Bases: [`kivy.event.EventDispatcher`](https://kivy.org/doc/stable/api-kivy.event.html#kivy.event.EventDispatcher)
Main event loop. This loop handles the updating of input and
dispatching events.

**kivy.base.EventLoopBase.add_event_listener**

Add a new event listener for getting touch events.

**kivy.base.EventLoopBase.add_input_provider**

Add a new input provider to listen for touch events.

**kivy.base.EventLoopBase.add_postproc_module**

Add a postproc input module (DoubleTap, TripleTap, DeJitter
RetainTouch are defaults).

**kivy.base.EventLoopBase.async_idle**

Identical to [`idle()`](https://kivy.org/doc/stable/#kivy.base.EventLoopBase.idle), but instead used when running
within an async event loop.

**kivy.base.EventLoopBase.close**

Exit from the main loop and stop all configured
input providers.

**kivy.base.EventLoopBase.dispatch_input**

Called by [`EventLoopBase.idle()`](https://kivy.org/doc/stable/#kivy.base.EventLoopBase.idle) to read events from input
providers, pass events to postproc, and dispatch final events.

**kivy.base.EventLoopBase.ensure_window**

Ensure that we have a window.

**kivy.base.EventLoopBase.exit**

Close the main loop and close the window.

**kivy.base.EventLoopBase.idle**

This function is called after every frame. By default:
it “ticks” the clock to the next frame.
it reads all input and dispatches events.
it dispatches on_update, on_draw and on_flip events to the
window.

**kivy.base.EventLoopBase.on_pause**

Event handler for on_pause which will be fired when
the event loop is paused.

**kivy.base.EventLoopBase.on_start**

Event handler for on_start which will be fired right
after all input providers have been started.

**kivy.base.EventLoopBase.on_stop**

Event handler for on_stop events which will be fired right
after all input providers have been stopped.

**kivy.base.EventLoopBase.post_dispatch_input**

This function is called by [`EventLoopBase.dispatch_input()`](https://kivy.org/doc/stable/#kivy.base.EventLoopBase.dispatch_input)
when we want to dispatch an input event. The event is dispatched to
all listeners and if grabbed, it’s dispatched to grabbed widgets.

**kivy.base.EventLoopBase.remove_android_splash**

Remove android presplash in SDL2 bootstrap.

**kivy.base.EventLoopBase.remove_event_listener**

Remove an event listener from the list.

**kivy.base.EventLoopBase.remove_input_provider**

Remove an input provider.
Changed in version 2.1.0:Provider will be also removed if it exist in auto-remove list.

**kivy.base.EventLoopBase.remove_postproc_module**

Remove a postproc module.

**kivy.base.EventLoopBase.run**

Main loop

**kivy.base.EventLoopBase.set_window**

Set the window used for the event loop.

**kivy.base.EventLoopBase.start**

Must be called before [`EventLoopBase.run()`](https://kivy.org/doc/stable/#kivy.base.EventLoopBase.run). This starts all
configured input providers.
Changed in version 2.1.0:Method can be called multiple times, but event loop will start only
once.

**kivy.base.EventLoopBase.stop**

Stop all input providers and call callbacks registered using
EventLoop.add_stop_callback().
Changed in version 2.1.0:Method can be called multiple times, but event loop will stop only
once.

**kivy.base.EventLoopBase.touches**

Return the list of all touches currently in down or move states.

**kivy.base.ExceptionHandler**

Bases: `builtins.object`
Base handler that catches exceptions in [`runTouchApp()`](https://kivy.org/doc/stable/#kivy.base.runTouchApp).
You can subclass and extend it as follows:

Then, all exceptions will be set to PASS, and logged to the console!

**kivy.base.ExceptionHandler.handle_exception**

Called by [`ExceptionManagerBase`](https://kivy.org/doc/stable/#kivy.base.ExceptionManagerBase) to handle a exception.
Defaults to returning `ExceptionManager.RAISE` that re-raises the
exception. Return `ExceptionManager.PASS` to indicate that the
exception was handled and should be ignored.
This may be called multiple times with the same exception, if
`ExceptionManager.RAISE` is returned as the exception bubbles
through multiple kivy exception handling levels.

**kivy.base.ExceptionManager**

The [`ExceptionManagerBase`](https://kivy.org/doc/stable/#kivy.base.ExceptionManagerBase) instance that handles kivy exceptions.

**kivy.base.ExceptionManagerBase**

Bases: `builtins.object`
ExceptionManager manages exceptions handlers.

**kivy.base.ExceptionManagerBase.PASS**

The exception should be ignored as it was handled by the handler.

**kivy.base.ExceptionManagerBase.RAISE**

The exception should be re-raised.

**kivy.base.ExceptionManagerBase.add_handler**

Add a new exception handler to the stack.

**kivy.base.ExceptionManagerBase.handle_exception**

Called when an exception occurred in the [`runTouchApp()`](https://kivy.org/doc/stable/#kivy.base.runTouchApp)
main loop.

**kivy.base.ExceptionManagerBase.remove_handler**

Remove the exception handler from the stack.

**kivy.base.async_runTouchApp**

Identical to [`runTouchApp()`](https://kivy.org/doc/stable/#kivy.base.runTouchApp) but instead it is a coroutine
that can be run in an existing async event loop.
`async_lib` is the async library to use. See [`kivy.app`](https://kivy.org/doc/stable/api-kivy.app.html#module-kivy.app) for details
and example usage.
New in version 2.0.0.

**kivy.base.runTouchApp**

Static main function that starts the application loop.
You can access some magic via the following arguments:
See [`kivy.app`](https://kivy.org/doc/stable/api-kivy.app.html#module-kivy.app) for example usage.

**kivy.base.stopTouchApp**

Stop the current application by leaving the main loop.
See [`kivy.app`](https://kivy.org/doc/stable/api-kivy.app.html#module-kivy.app) for example usage.

---

## API - [`kivy.cache`](https://kivy.org/doc/stable/api-kivy.cache.html)

**kivy.cache.Cache**

Bases: `builtins.object`
See module documentation for more information.

**kivy.cache.Cache.append**

Add a new object to the cache.

Changed in version 2.0.0:Raises ValueError if None is used as key.

**kivy.cache.Cache.get**

Get a object from the cache.

**kivy.cache.Cache.get_lastaccess**

Get the objects last access time in the cache.

**kivy.cache.Cache.get_timestamp**

Get the object timestamp in the cache.

**kivy.cache.Cache.print_usage**

Print the cache usage to the console.

**kivy.cache.Cache.register**

Register a new category in the cache with the specified limit.

**kivy.cache.Cache.remove**

Purge the cache.

---

## API - [`kivy.clock`](https://kivy.org/doc/stable/api-kivy.clock.html)

**kivy.clock.Clock**

The kivy Clock instance. See module documentation for details.

**kivy.clock.ClockBase**

Bases: [`kivy.clock.ClockBaseBehavior`](https://kivy.org/doc/stable/#kivy.clock.ClockBaseBehavior), `kivy._clock.CyClockBase`
The `default` kivy clock. See module for details.

**kivy.clock.ClockBase.usleep**

Sleeps for the number of microseconds.

**kivy.clock.ClockBaseBehavior**

Bases: `builtins.object`
The base of the kivy clock.

**kivy.clock.ClockBaseBehavior.MIN_SLEEP**

The minimum time to sleep. If the remaining time is less than this,
the event loop will continue.

**kivy.clock.ClockBaseBehavior.async_idle**

(internal) async version of [`idle()`](https://kivy.org/doc/stable/#kivy.clock.ClockBaseBehavior.idle).

**kivy.clock.ClockBaseBehavior.async_tick**

async version of [`tick()`](https://kivy.org/doc/stable/#kivy.clock.ClockBaseBehavior.tick).

**kivy.clock.ClockBaseBehavior.frames**

Number of internal frames (not necessarily drawn) from the start of
the clock.
New in version 1.8.0.

**kivy.clock.ClockBaseBehavior.frames_displayed**

Number of displayed frames from the start of the clock.

**kivy.clock.ClockBaseBehavior.frametime**

Time spent between the last frame and the current frame
(in seconds).
New in version 1.8.0.

**kivy.clock.ClockBaseBehavior.get_boottime**

Get the time in seconds from the application start.

**kivy.clock.ClockBaseBehavior.get_fps**

Get the current average FPS calculated by the clock.

**kivy.clock.ClockBaseBehavior.get_rfps**

Get the current “real” FPS calculated by the clock.
This counter reflects the real framerate displayed on the screen.
In contrast to get_fps(), this function returns a counter of the
number of frames, not the average of frames per second.

**kivy.clock.ClockBaseBehavior.get_time**

Get the last tick made by the clock.

**kivy.clock.ClockBaseBehavior.idle**

(internal) waits here until the next frame.

**kivy.clock.ClockBaseBehavior.init_async_lib**

Manually sets the async library to use internally, when running in
a asynchronous manner.
This can be called anytime before the kivy event loop has started,
but not once the kivy App is running.

**kivy.clock.ClockBaseBehavior.post_idle**

Called after [`idle()`](https://kivy.org/doc/stable/#kivy.clock.ClockBaseBehavior.idle) by [`tick()`](https://kivy.org/doc/stable/#kivy.clock.ClockBaseBehavior.tick).

**kivy.clock.ClockBaseBehavior.pre_idle**

Called before [`idle()`](https://kivy.org/doc/stable/#kivy.clock.ClockBaseBehavior.idle) by [`tick()`](https://kivy.org/doc/stable/#kivy.clock.ClockBaseBehavior.tick).

**kivy.clock.ClockBaseBehavior.tick**

Advance the clock to the next step. Must be called every frame.
The default clock has a tick() function called by the core Kivy
framework.

**kivy.clock.ClockBaseBehavior.tick_draw**

Tick the drawing counter.

**kivy.clock.ClockBaseBehavior.time**

Proxy method for [`clock()`](https://kivy.org/doc/stable/api-kivy.compat.html#kivy.compat.clock).

**kivy.clock.ClockBaseBehavior.usleep**

Sleeps for the number of microseconds.

**kivy.clock.ClockBaseFreeInterruptAll**

Bases: [`kivy.clock.ClockBaseInterruptFreeBehavior`](https://kivy.org/doc/stable/#kivy.clock.ClockBaseInterruptFreeBehavior), `kivy._clock.CyClockBaseFree`
The `free_all` kivy clock. See module for details.

**kivy.clock.ClockBaseFreeInterruptOnly**

Bases: [`kivy.clock.ClockBaseInterruptFreeBehavior`](https://kivy.org/doc/stable/#kivy.clock.ClockBaseInterruptFreeBehavior), `kivy._clock.CyClockBaseFree`
The `free_only` kivy clock. See module for details.

**kivy.clock.ClockBaseFreeInterruptOnly.async_idle**

(internal) async version of [`idle()`](https://kivy.org/doc/stable/#kivy.clock.ClockBaseFreeInterruptOnly.idle).

**kivy.clock.ClockBaseFreeInterruptOnly.idle**

(internal) waits here until the next frame.

**kivy.clock.ClockBaseInterrupt**

Bases: [`kivy.clock.ClockBaseInterruptBehavior`](https://kivy.org/doc/stable/#kivy.clock.ClockBaseInterruptBehavior), `kivy._clock.CyClockBase`
The `interrupt` kivy clock. See module for details.

**kivy.clock.ClockBaseInterruptBehavior**

Bases: [`kivy.clock.ClockBaseBehavior`](https://kivy.org/doc/stable/#kivy.clock.ClockBaseBehavior)
A kivy clock which can be interrupted during a frame to execute events.

**kivy.clock.ClockBaseInterruptBehavior.async_idle**

(internal) async version of [`idle()`](https://kivy.org/doc/stable/#kivy.clock.ClockBaseInterruptBehavior.idle).

**kivy.clock.ClockBaseInterruptBehavior.idle**

(internal) waits here until the next frame.

**kivy.clock.ClockBaseInterruptBehavior.init_async_lib**

Manually sets the async library to use internally, when running in
a asynchronous manner.
This can be called anytime before the kivy event loop has started,
but not once the kivy App is running.

**kivy.clock.ClockBaseInterruptBehavior.usleep**

Sleeps for the number of microseconds.

**kivy.clock.ClockBaseInterruptFreeBehavior**

Bases: [`kivy.clock.ClockBaseInterruptBehavior`](https://kivy.org/doc/stable/#kivy.clock.ClockBaseInterruptBehavior)
A base class for the clock that interrupts the sleep interval for
free events.

**kivy.clock.ClockEvent**

Bases: `builtins.object`
This class is never created by the user; instead, kivy creates and returns
an instance of this class when scheduling a callback.
An event can be triggered (scheduled) by calling it. If it’s already
scheduled, nothing will happen, otherwise it’ll be scheduled. E.g.:

**kivy.clock.ClockEvent.callback**

callback: object

**kivy.clock.ClockEvent.cancel**

Cancels the callback if it was scheduled to be called. If not
scheduled, nothing happens.

**kivy.clock.ClockEvent.cid**

cid: object

**kivy.clock.ClockEvent.clock**

clock: kivy._clock.CyClockBase
The [`CyClockBase`](https://kivy.org/doc/stable/#kivy.clock.CyClockBase) instance associated with the event.

**kivy.clock.ClockEvent.clock_ended_callback**

clock_ended_callback: object
A Optional callback for this event, which if provided is called by the clock
when the clock is stopped and the event was not ticked.

**kivy.clock.ClockEvent.get_callback**

Returns the callback associated with the event. Callbacks get stored
with a indirect ref so that it doesn’t keep objects alive. If the callback
is dead, None is returned.

**kivy.clock.ClockEvent.get_clock_ended_callback**

Returns the clock_ended_callback associated with the event.
Callbacks get stored with a indirect ref so that it doesn’t keep
objects alive. If the callback is dead or wasn’t provided,
None is returned.

**kivy.clock.ClockEvent.is_triggered**

Returns whether the event is scheduled to have its callback executed by
the kivy thread.

**kivy.clock.ClockEvent.loop**

loop: ‘int’
Whether this event repeats at intervals of [`timeout`](https://kivy.org/doc/stable/#kivy.clock.ClockEvent.timeout).

**kivy.clock.ClockEvent.next**

next: kivy._clock.ClockEvent
The next [`ClockEvent`](https://kivy.org/doc/stable/#kivy.clock.ClockEvent) in order they were scheduled.

**kivy.clock.ClockEvent.prev**

prev: kivy._clock.ClockEvent
The previous [`ClockEvent`](https://kivy.org/doc/stable/#kivy.clock.ClockEvent) in order they were scheduled.

**kivy.clock.ClockEvent.release**

(internal method) Converts the callback into a indirect ref.

**kivy.clock.ClockEvent.release_ref**

release_ref: ‘int’
If True, the event should never release the reference to the callbacks.
If False, a weakref may be created instead.

**kivy.clock.ClockEvent.tick**

(internal method) Processes the event for the kivy thread.

**kivy.clock.ClockEvent.timeout**

timeout: ‘double’
The duration after scheduling when the callback should be executed.

**kivy.clock.ClockEvent.weak_callback**

weak_callback: object

**kivy.clock.ClockEvent.weak_clock_ended_callback**

weak_clock_ended_callback: object

**kivy.clock.ClockNotRunningError**

Bases: `RuntimeError`
Raised by the kivy Clock when scheduling an event if the
Kivy Clock has already finished ([`stop_clock`](https://kivy.org/doc/stable/#kivy.clock.CyClockBase.stop_clock) was
called).

**kivy.clock.CyClockBase**

Bases: `builtins.object`

**kivy.clock.CyClockBase.clock_resolution**

clock_resolution: ‘double’
If the remaining time until the event timeout is less than [`clock_resolution`](https://kivy.org/doc/stable/#kivy.clock.CyClockBase.clock_resolution),
the clock will execute the callback even if it hasn’t exactly timed out.
If -1, the default, the resolution will be computed from config’s `maxfps`.
Otherwise, the provided value is used. Defaults to -1.

**kivy.clock.CyClockBase.create_lifecycle_aware_trigger**

Create a Trigger event similarly to [`create_trigger()`](https://kivy.org/doc/stable/#kivy.clock.CyClockBase.create_trigger), but the event
is sensitive to the clock’s state.
If this event is triggered after the clock has stopped ([`stop_clock()`](https://kivy.org/doc/stable/#kivy.clock.CyClockBase.stop_clock)), then a
[`ClockNotRunningError`](https://kivy.org/doc/stable/#kivy.clock.ClockNotRunningError) will be raised. If the error is not raised,
then either `callback` or `clock_ended_callback` will be
called. `callback` will be called when the event
is normally executed. If the clock is stopped before it can be executed,
provided the app exited normally without crashing and the event wasn’t manually
canceled, and the callbacks are not garbage collected then
`clock_ended_callback` will be called instead when the clock is stopped.

New in version 2.0.0.

**kivy.clock.CyClockBase.create_trigger**

Create a Trigger event. It is thread safe but not `__del__` or
`__dealloc__` safe (see [`schedule_del_safe()`](https://kivy.org/doc/stable/#kivy.clock.CyClockBase.schedule_del_safe)).
Check module documentation for more information.
To cancel the event before it is executed, call [`ClockEvent.cancel()`](https://kivy.org/doc/stable/#kivy.clock.ClockEvent.cancel)
on the returned event.
To schedule it again, simply call the event (`event()`) and it’ll be safely
rescheduled if it isn’t already scheduled.

New in version 1.0.5.
Changed in version 1.10.0:`interval` has been added.
Changed in version 2.0.0:`release_ref` has been added.

**kivy.clock.CyClockBase.get_before_frame_events**

Returns the list of [`ClockEvent`](https://kivy.org/doc/stable/#kivy.clock.ClockEvent) instances that are scheduled
to be called before the next frame (`-1` timeout).
New in version 2.1.0.

**kivy.clock.CyClockBase.get_events**

Returns the list of [`ClockEvent`](https://kivy.org/doc/stable/#kivy.clock.ClockEvent) instances currently scheduled.

**kivy.clock.CyClockBase.get_min_timeout**

Returns the remaining time since the start of the current frame
for the event with the smallest timeout.

**kivy.clock.CyClockBase.get_resolution**

Returns the minimum resolution the clock has. It’s a function of
[`clock_resolution`](https://kivy.org/doc/stable/#kivy.clock.CyClockBase.clock_resolution) and `maxfps` provided at the config.

**kivy.clock.CyClockBase.handle_exception**

Provides an opportunity to handle an event’s exception.
If desired, the exception is handled, otherwise it should be raised
again. By default it is raised again.

New in version 2.0.0.

**kivy.clock.CyClockBase.has_ended**

has_ended: ‘int’

**kivy.clock.CyClockBase.has_started**

has_started: ‘int’

**kivy.clock.CyClockBase.max_iteration**

max_iteration: ‘int’
The maximum number of callback iterations at the end of the frame, before the next
frame. If more iterations occur, a warning is issued.

**kivy.clock.CyClockBase.on_schedule**

Function that is called internally every time an event is triggered
for this clock. It takes the event as a parameter.
The order of `on_schedule` calls are not guaranteed to be in the same
order that the events are scheduled. Similarly, it is possible that the
event being scheduled was canceled before this is called on the event.
That’s because [`on_schedule()`](https://kivy.org/doc/stable/#kivy.clock.CyClockBase.on_schedule) may be called from different threads.

**kivy.clock.CyClockBase.schedule_del_safe**

Schedule a callback that is thread safe and `__del__` or
`__dealloc__` safe.
It’s unsafe to call various kinds of code from `__del__` or
`__dealloc__` methods because they can be executed at any time. Most
Kivy’s Clock methods are unsafe to call the Clock from these methods. Instead,
use this method, which is thread safe and `__del__` or `__dealloc__`
safe, to schedule the callback in the kivy thread. It’ll be executed
in order after the normal events are processed.

New in version 1.11.0.

**kivy.clock.CyClockBase.schedule_interval**

Schedule an event to be called every <timeout> seconds.
See [`create_trigger()`](https://kivy.org/doc/stable/#kivy.clock.CyClockBase.create_trigger) for advanced scheduling and more details.
To cancel the event before it is executed, call [`ClockEvent.cancel()`](https://kivy.org/doc/stable/#kivy.clock.ClockEvent.cancel)
on the returned event.
If the callback is a class method, a weakref to the object is created and it
may be garbage collected if there’s no other reference to the object.

**kivy.clock.CyClockBase.schedule_lifecycle_aware_del_safe**

Schedule a callback that is thread safe and `__del__` or
`__dealloc__` safe similarly to [`schedule_del_safe()`](https://kivy.org/doc/stable/#kivy.clock.CyClockBase.schedule_del_safe), but the callback
is sensitive to the clock’s state.
If this event is triggered after the clock has stopped ([`stop_clock()`](https://kivy.org/doc/stable/#kivy.clock.CyClockBase.stop_clock)), then a
[`ClockNotRunningError`](https://kivy.org/doc/stable/#kivy.clock.ClockNotRunningError) will be raised. If the error is not raised,
then either `callback` or `clock_ended_callback` will be
called. `callback` will be called when the callback
is normally executed. If the clock is stopped before it can be executed,
provided the app exited normally without crashing then
`clock_ended_callback` will be called instead when the clock is stopped.

New in version 2.0.0.

**kivy.clock.CyClockBase.schedule_once**

Schedule an event in <timeout> seconds. If <timeout> is unspecified
or 0, the callback will be called after the next frame is rendered.
See [`create_trigger()`](https://kivy.org/doc/stable/#kivy.clock.CyClockBase.create_trigger) for advanced scheduling and more details.
To cancel the event before it is executed, call [`ClockEvent.cancel()`](https://kivy.org/doc/stable/#kivy.clock.ClockEvent.cancel)
on the returned event.
If the callback is a class method, a weakref to the object is created and it
may be garbage collected if there’s no other reference to the object.

Changed in version 1.0.5:If the timeout is -1, the callback will be called before the next
frame (at `tick_draw()`).

**kivy.clock.CyClockBase.start_clock**

Must be called to start the clock.
Once [`stop_clock()`](https://kivy.org/doc/stable/#kivy.clock.CyClockBase.stop_clock) is called, it cannot be started again.

**kivy.clock.CyClockBase.stop_clock**

Stops the clock and cleans up.
This must be called to process the lifecycle_aware callbacks etc.

**kivy.clock.CyClockBase.unschedule**

Remove a previously scheduled event.
An [`ClockEvent`](https://kivy.org/doc/stable/#kivy.clock.ClockEvent) can also be canceled directly by calling
[`ClockEvent.cancel()`](https://kivy.org/doc/stable/#kivy.clock.ClockEvent.cancel).

Changed in version 1.9.0:The all parameter was added. Before, it behaved as if all was
True.

**kivy.clock.CyClockBaseFree**

Bases: `kivy._clock.CyClockBase`
A clock class that supports scheduling free events in addition to normal
events.
Each of the [`create_trigger()`](https://kivy.org/doc/stable/#kivy.clock.CyClockBase.create_trigger),
[`schedule_once()`](https://kivy.org/doc/stable/#kivy.clock.CyClockBase.schedule_once), and [`schedule_interval()`](https://kivy.org/doc/stable/#kivy.clock.CyClockBase.schedule_interval)
methods, which create a normal event, have a corresponding method
for creating a free event.

**kivy.clock.CyClockBaseFree.create_lifecycle_aware_trigger**

**kivy.clock.CyClockBaseFree.create_lifecycle_aware_trigger_free**

Similar to [`create_lifecycle_aware_trigger()`](https://kivy.org/doc/stable/#kivy.clock.CyClockBase.create_lifecycle_aware_trigger), but instead creates
a free event.

**kivy.clock.CyClockBaseFree.create_trigger**

**kivy.clock.CyClockBaseFree.create_trigger_free**

Similar to [`create_trigger()`](https://kivy.org/doc/stable/#kivy.clock.CyClockBase.create_trigger), but instead creates
a free event.

**kivy.clock.CyClockBaseFree.get_min_free_timeout**

Returns the remaining time since the start of the current frame
for the *free* event with the smallest timeout.

**kivy.clock.CyClockBaseFree.schedule_interval**

**kivy.clock.CyClockBaseFree.schedule_interval_free**

Similar to [`schedule_interval()`](https://kivy.org/doc/stable/#kivy.clock.CyClockBase.schedule_interval), but instead creates
a free event.

**kivy.clock.CyClockBaseFree.schedule_once**

**kivy.clock.CyClockBaseFree.schedule_once_free**

Similar to [`schedule_once()`](https://kivy.org/doc/stable/#kivy.clock.CyClockBase.schedule_once), but instead creates
a free event.

**kivy.clock.FreeClockEvent**

Bases: `kivy._clock.ClockEvent`
[`CyClockBaseFree`](https://kivy.org/doc/stable/#kivy.clock.CyClockBaseFree). It stores whether the event was scheduled as a
free event.

**kivy.clock.FreeClockEvent.free**

free: ‘int’
Whether this event was scheduled as a free event.

**kivy.clock.mainthread**

Decorator that will schedule the call of the function for the next
available frame in the mainthread. It can be useful when you use
[`UrlRequest`](https://kivy.org/doc/stable/api-kivy.network.urlrequest.html#kivy.network.urlrequest.UrlRequest) or when you do Thread
programming: you cannot do any OpenGL-related work in a thread.
Please note that this method will return directly and no result can be
returned:

New in version 1.8.0.

**kivy.clock.triggered**

Decorator that will trigger the call of the function at the specified
timeout, through the method [`CyClockBase.create_trigger()`](https://kivy.org/doc/stable/#kivy.clock.CyClockBase.create_trigger). Subsequent
calls to the decorated function (while the timeout is active) are ignored.
It can be helpful when an expensive function (i.e. call to a server) can be
triggered by different methods. Setting a proper timeout will delay the
calling and only one of them will be triggered.
@triggered(timeout, interval=False)
def callback(id):
print(‘The callback has been called with id=%d’ % id)
>> callback(id=1)
>> callback(id=2)
The callback has been called with id=2
The decorated callback can also be unscheduled using:
>> callback.cancel()
New in version 1.10.1.

---

## API - [`kivy.compat`](https://kivy.org/doc/stable/api-kivy.compat.html)

**kivy.compat.PY2**

False, because we don’t support Python 2 anymore.

**kivy.compat.clock**

A clock with the highest available resolution on your current Operating
System.

**kivy.compat.isclose**

Determine whether two floating-point numbers are close in value.

Return True if a is close in value to b, and False otherwise.
For the values to be considered close, the difference between them
must be smaller than at least one of the tolerances.
-inf, inf and NaN behave similarly to the IEEE 754 Standard. That
is, NaN is not close to anything, even itself. inf and -inf are
only close to themselves.

**kivy.compat.string_types**

A utility type for detecting string in a Python 2/3 friendly way. For
example:

---

## API - [`kivy.config`](https://kivy.org/doc/stable/api-kivy.config.html)

**kivy.config.Config**

The default Kivy configuration object. This is a [`ConfigParser`](https://kivy.org/doc/stable/#kivy.config.ConfigParser)
instance with the [`name`](https://kivy.org/doc/stable/#kivy.config.ConfigParser.name) set to ‘kivy’.

**kivy.config.ConfigParser**

Bases: `configparser.RawConfigParser`, `builtins.object`
Enhanced ConfigParser class that supports the addition of default
sections and default values.
By default, the kivy ConfigParser instance, [`Config`](https://kivy.org/doc/stable/#kivy.config.Config),
is named ‘kivy’ and the ConfigParser instance used by the
`App.build_settings` method is named
‘app’.

Changed in version 1.9.0:Each ConfigParser can now be [`named`](https://kivy.org/doc/stable/#kivy.config.ConfigParser.name). You can get the
ConfigParser associated with a name using [`get_configparser()`](https://kivy.org/doc/stable/#kivy.config.ConfigParser.get_configparser).
In addition, you can now control the config values with
[`ConfigParserProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ConfigParserProperty).
New in version 1.0.7.

**kivy.config.ConfigParser.add_callback**

Add a callback to be called when a specific section or key has
changed. If you don’t specify a section or key, it will call the
callback for all section/key changes.
Callbacks will receive 3 arguments: the section, key and value.
New in version 1.4.1.

**kivy.config.ConfigParser.adddefaultsection**

Add a section if the section is missing.

**kivy.config.ConfigParser.get**

Get an option value for a given section.
If vars is provided, it must be a dictionary. The option is looked up
in vars (if provided), section, and in DEFAULTSECT in that order.
If the key is not found and fallback is provided, it is used as
a fallback value. None can be provided as a fallback value.
If interpolation is enabled and the optional argument raw is False,
all interpolations are expanded in the return values.
Arguments raw, vars, and fallback are keyword only.
The section DEFAULT is special.

**kivy.config.ConfigParser.get_configparser**

Returns the [`ConfigParser`](https://kivy.org/doc/stable/#kivy.config.ConfigParser) instance whose name is name, or
None if not found.

**kivy.config.ConfigParser.getdefault**

Get the value of an option in the specified section. If not found,
it will return the default value.

**kivy.config.ConfigParser.getdefaultint**

Get the value of an option in the specified section. If not found,
it will return the default value. The value will always be
returned as an integer.
New in version 1.6.0.

**kivy.config.ConfigParser.name**

The name associated with this ConfigParser instance, if not ‘’.
Defaults to ‘’. It can be safely changed dynamically or set to ‘’.
When a ConfigParser is given a name, that config object can be
retrieved using [`get_configparser()`](https://kivy.org/doc/stable/#kivy.config.ConfigParser.get_configparser). In addition, that config
instance can also be used with a
[`ConfigParserProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ConfigParserProperty) instance that set its
config value to this name.
Setting more than one ConfigParser with the same name will raise a
ValueError.

**kivy.config.ConfigParser.read**

Read only one filename. In contrast to the original ConfigParser of
Python, this one is able to read only one file at a time. The last
read file will be used for the [`write()`](https://kivy.org/doc/stable/#kivy.config.ConfigParser.write) method.
Changed in version 1.9.0:[`read()`](https://kivy.org/doc/stable/#kivy.config.ConfigParser.read) now calls the callbacks if read changed any values.

**kivy.config.ConfigParser.remove_callback**

Removes a callback added with [`add_callback()`](https://kivy.org/doc/stable/#kivy.config.ConfigParser.add_callback).
[`remove_callback()`](https://kivy.org/doc/stable/#kivy.config.ConfigParser.remove_callback) must be called with the same parameters as
[`add_callback()`](https://kivy.org/doc/stable/#kivy.config.ConfigParser.add_callback).
Raises a ValueError if not found.
New in version 1.9.0.

**kivy.config.ConfigParser.set**

Functions similarly to PythonConfigParser’s set method, except that
the value is implicitly converted to a string.

**kivy.config.ConfigParser.setall**

Sets multiple key-value pairs in a section. keyvalues should be a
dictionary containing the key-value pairs to be set.

**kivy.config.ConfigParser.setdefault**

Set the default value for an option in the specified section.

**kivy.config.ConfigParser.setdefaults**

Set multiple key-value defaults in a section. keyvalues should be
a dictionary containing the new key-value defaults.

**kivy.config.ConfigParser.update_config**

Upgrade the configuration based on a new default config file.
Overwrite any existing values if overwrite is True.

**kivy.config.ConfigParser.write**

Write the configuration to the last file opened using the
[`read()`](https://kivy.org/doc/stable/#kivy.config.ConfigParser.read) method.
Return True if the write finished successfully, False otherwise.

---

## API - [`kivy.context`](https://kivy.org/doc/stable/api-kivy.context.html)

**kivy.context.Context**

Bases: `builtins.dict`

**kivy.context.Context.pop**

If the key is not found, return the default if given; otherwise,
raise a KeyError.

**kivy.context.get_current_context**

Return the current context.

**kivy.context.register_context**

Register a new context.

---

## API - [`kivy.core`](https://kivy.org/doc/stable/api-kivy.core.html)

**kivy.core.CoreCriticalException**

Bases: `Exception`

---

## API - [`kivy.core.audio`](https://kivy.org/doc/stable/api-kivy.core.audio.html)

**kivy.core.audio.Sound**

Bases: [`kivy.event.EventDispatcher`](https://kivy.org/doc/stable/api-kivy.event.html#kivy.event.EventDispatcher)
Represents a sound to play. This class is abstract, and cannot be used
directly.
Use SoundLoader to load a sound.

**kivy.core.audio.Sound.get_pos**

Returns the current position of the audio file.
Returns 0 if not playing.
New in version 1.4.1.

**kivy.core.audio.Sound.length**

Get length of the sound (in seconds).

**kivy.core.audio.Sound.load**

Load the file into memory.

**kivy.core.audio.Sound.loop**

Set to True if the sound should automatically loop when it finishes.
New in version 1.8.0.
[`loop`](https://kivy.org/doc/stable/#kivy.core.audio.Sound.loop) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and defaults to
False.

**kivy.core.audio.Sound.pitch**

Pitch of a sound. 2 is an octave higher, .5 one below. This is only
implemented for SDL2 audio provider yet.
New in version 1.10.0.
[`pitch`](https://kivy.org/doc/stable/#kivy.core.audio.Sound.pitch) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and defaults
to 1.

**kivy.core.audio.Sound.play**

Play the file.

**kivy.core.audio.Sound.seek**

Go to the <position> (in seconds).

**kivy.core.audio.Sound.source**

Filename / source of your audio file.
New in version 1.3.0.
[`source`](https://kivy.org/doc/stable/#kivy.core.audio.Sound.source) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) that defaults
to None and is read-only. Use the [`SoundLoader.load()`](https://kivy.org/doc/stable/#kivy.core.audio.SoundLoader.load) for loading
audio.

**kivy.core.audio.Sound.state**

State of the sound, one of ‘stop’ or ‘play’.
New in version 1.3.0.
[`state`](https://kivy.org/doc/stable/#kivy.core.audio.Sound.state) is a read-only [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty).

**kivy.core.audio.Sound.stop**

Stop playback.

**kivy.core.audio.Sound.unload**

Unload the file from memory.

**kivy.core.audio.Sound.volume**

Volume, in the range 0-1. 1 means full volume, 0 means mute.
New in version 1.3.0.
[`volume`](https://kivy.org/doc/stable/#kivy.core.audio.Sound.volume) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and defaults
to 1.

**kivy.core.audio.SoundLoader**

Bases: `builtins.object`
Load a sound, using the best loader for the given file type.

**kivy.core.audio.SoundLoader.load**

Load a sound, and return a Sound() instance.

**kivy.core.audio.SoundLoader.register**

Register a new class to load the sound.

---

## API - [`kivy.core.camera`](https://kivy.org/doc/stable/api-kivy.core.camera.html)

**kivy.core.camera.CameraBase**

Bases: [`kivy.event.EventDispatcher`](https://kivy.org/doc/stable/api-kivy.event.html#kivy.event.EventDispatcher)
Abstract Camera Widget class.
Concrete camera classes must implement initialization and
frame capturing to a buffer that can be uploaded to the gpu.

**kivy.core.camera.CameraBase.index**

Source index of the camera

**kivy.core.camera.CameraBase.init_camera**

Initialize the camera (internal)

**kivy.core.camera.CameraBase.resolution**

Resolution of camera capture (width, height)

**kivy.core.camera.CameraBase.start**

Start the camera acquire

**kivy.core.camera.CameraBase.stop**

Release the camera

**kivy.core.camera.CameraBase.texture**

Return the camera texture with the latest capture

---

## API - [`kivy.core.image`](https://kivy.org/doc/stable/api-kivy.core.image.html)

**kivy.core.image.Image**

Bases: [`kivy.event.EventDispatcher`](https://kivy.org/doc/stable/api-kivy.event.html#kivy.event.EventDispatcher)
Load an image and store the size and texture.
Changed in version 1.0.7:mipmap attribute has been added. The texture_mipmap and
texture_rectangle have been deleted.
Changed in version 1.0.8:An Image widget can change its texture. A new event ‘on_texture’ has
been introduced. New methods for handling sequenced animation have been
added.

**kivy.core.image.Image.anim_available**

Return True if this Image instance has animation available.
New in version 1.0.8.

**kivy.core.image.Image.anim_delay**

Delay between each animation frame. A lower value means faster
animation.
New in version 1.0.8.

**kivy.core.image.Image.anim_index**

Return the index number of the image currently in the texture.
New in version 1.0.8.

**kivy.core.image.Image.anim_reset**

Reset an animation if available.
New in version 1.0.8.

Usage:

You can change the animation speed whilst it is playing:

**kivy.core.image.Image.filename**

Get/set the filename of image

**kivy.core.image.Image.height**

Image height

**kivy.core.image.Image.image**

Get/set the data image object

**kivy.core.image.Image.load**

Load an image

**kivy.core.image.Image.load_memory**

(internal) Method to load an image from raw data.

**kivy.core.image.Image.nocache**

Indicate whether the texture will not be stored in the cache or not.
New in version 1.6.0.

**kivy.core.image.Image.on_texture**

New in version 1.0.8.

**kivy.core.image.Image.read_pixel**

For a given local x/y position, return the pixel color at that
position.

**kivy.core.image.Image.remove_from_cache**

Remove the Image from cache. This facilitates re-loading of
images from disk in case the image content has changed.
New in version 1.3.0.
Usage:

**kivy.core.image.Image.save**

Save image texture to file.
The filename should have the ‘.png’ extension because the texture data
read from the GPU is in the RGBA format. ‘.jpg’ might work but has not
been heavily tested so some providers might break when using it.
Any other extensions are not officially supported.
The flipped parameter flips the saved image vertically, and
defaults to False.
Example:

New in version 1.7.0.
Changed in version 1.8.0:Parameter flipped added to flip the image before saving, default
to False.
Changed in version 1.11.0:Parameter fmt added to force the output format of the file
Filename can now be a BytesIO object.

**kivy.core.image.Image.size**

Image size (width, height)

**kivy.core.image.Image.texture**

Texture of the image

**kivy.core.image.Image.width**

Image width

**kivy.core.image.ImageData**

Bases: `builtins.object`
Container for images and mipmap images.
The container will always have at least the mipmap level 0.

**kivy.core.image.ImageData.add_mipmap**

Add a image for a specific mipmap level.
New in version 1.0.7.

**kivy.core.image.ImageData.data**

Image data.
(If the image is mipmapped, it will use the level 0)

**kivy.core.image.ImageData.flip_vertical**

Indicate if the texture will need to be vertically flipped

**kivy.core.image.ImageData.fmt**

Decoded image format, one of a available texture format

**kivy.core.image.ImageData.get_mipmap**

Get the mipmap image at a specific level if it exists
New in version 1.0.7.

**kivy.core.image.ImageData.height**

Image height in pixels.
(If the image is mipmapped, it will use the level 0)

**kivy.core.image.ImageData.iterate_mipmaps**

Iterate over all mipmap images available.
New in version 1.0.7.

**kivy.core.image.ImageData.mipmaps**

Data for each mipmap.

**kivy.core.image.ImageData.rowlength**

Image rowlength.
(If the image is mipmapped, it will use the level 0)
New in version 1.9.0.

**kivy.core.image.ImageData.size**

Image (width, height) in pixels.
(If the image is mipmapped, it will use the level 0)

**kivy.core.image.ImageData.source**

Image source, if available

**kivy.core.image.ImageData.width**

Image width in pixels.
(If the image is mipmapped, it will use the level 0)

---

## API - [`kivy.core.spelling`](https://kivy.org/doc/stable/api-kivy.core.spelling.html)

**kivy.core.spelling.NoLanguageSelectedError**

Bases: `Exception`
Exception to be raised when a language-using method is called but no
language was selected prior to the call.

**kivy.core.spelling.NoSuchLangError**

Bases: `Exception`
Exception to be raised when a specific language could not be found.

**kivy.core.spelling.SpellingBase**

Bases: `builtins.object`
Base class for all spelling providers.
Supports some abstract methods for checking words and getting suggestions.

**kivy.core.spelling.SpellingBase.check**

If word is a valid word in self._language (the currently active
language), returns True. If the word shouldn’t be checked, returns
None (e.g. for ‘’). If it is not a valid word in self._language,
return False.

**kivy.core.spelling.SpellingBase.list_languages**

Return a list of all supported languages.
E.g. [‘en’, ‘en_GB’, ‘en_US’, ‘de’, …]

**kivy.core.spelling.SpellingBase.select_language**

From the set of registered languages, select the first language
for language.

**kivy.core.spelling.SpellingBase.suggest**

For a given fragment (i.e. part of a word or a word by itself),
provide corrections (fragment may be misspelled) or completions
as a list of strings.

---

## API - [`kivy.core.text`](https://kivy.org/doc/stable/api-kivy.core.text.html)

**kivy.core.text.LabelBase**

Bases: `builtins.object`
Core text label.
This is the abstract class used by different backends to render text.

New in version 2.3.0:limit_render_to_text_bbox was added to allow to limit text rendering
to the text bounding box (PIL only).
Deprecated since version 2.2.0:padding_x and padding_y have been deprecated. Please use padding
instead.
Changed in version 2.2.0:padding is now a list and defaults to [0, 0, 0, 0]. padding accepts
int|float or a list|tuple with 1, 2 or 4 elements.
Changed in version 1.10.1:font_context, font_family, font_features, base_direction
and text_language were added.
Changed in version 1.10.0:outline_width and outline_color were added.
Changed in version 1.9.0:strip, strip_reflow, shorten_from, split_str, and
unicode_errors were added.
Changed in version 1.9.0:padding_x and padding_y has been fixed to work as expected.
In the past, the text was padded by the negative of their values.
Changed in version 1.8.0:max_lines parameters has been added.
Changed in version 1.0.8:size have been deprecated and replaced with text_size.
Changed in version 1.0.7:The valign is now respected. This wasn’t the case previously
so you might have an issue in your application if you have not
considered this.

**kivy.core.text.LabelBase.content_height**

Return the content height; i.e. the height of the text without
any padding.

**kivy.core.text.LabelBase.content_size**

Return the content size (width, height)

**kivy.core.text.LabelBase.content_width**

Return the content width; i.e. the width of the text without
any padding.

**kivy.core.text.LabelBase.find_base_direction**

Searches a string the first character that has a strong direction,
according to the Unicode bidirectional algorithm. Returns None if
the base direction cannot be determined, or one of ‘ltr’ or ‘rtl’.

**kivy.core.text.LabelBase.fontid**

Return a unique id for all font parameters

**kivy.core.text.LabelBase.get_cached_extents**

Returns a cached version of the [`get_extents()`](https://kivy.org/doc/stable/#kivy.core.text.LabelBase.get_extents) function.

New in version 1.9.0.

**kivy.core.text.LabelBase.get_extents**

Return a tuple (width, height) indicating the size of the specified
text

**kivy.core.text.LabelBase.get_system_fonts_dir**

Return the directories used by the system for fonts.

**kivy.core.text.LabelBase.label**

Get/Set the text

**kivy.core.text.LabelBase.refresh**

Force re-rendering of the text

**kivy.core.text.LabelBase.register**

Register an alias for a Font.
New in version 1.1.0.
If you’re using a ttf directly, you might not be able to use the
bold/italic properties of
the ttf version. If the font is delivered in multiple files
(one regular, one italic and one bold), then you need to register these
files and use the alias instead.
All the fn_regular/fn_italic/fn_bold parameters are resolved with
[`kivy.resources.resource_find()`](https://kivy.org/doc/stable/api-kivy.resources.html#kivy.resources.resource_find). If fn_italic/fn_bold are None,
fn_regular will be used instead.

**kivy.core.text.LabelBase.render**

Return a tuple (width, height) to create the image
with the user constraints. (width, height) includes the padding.

**kivy.core.text.LabelBase.shorten**

Shortens the text to fit into a single line by the width specified
by [`text_size`](https://kivy.org/doc/stable/#kivy.core.text.LabelBase.text_size) [0]. If [`text_size`](https://kivy.org/doc/stable/#kivy.core.text.LabelBase.text_size) [0] is None, it returns
text unchanged.
`split_str` and `shorten_from` determines how the text is
shortened.

**kivy.core.text.LabelBase.text**

Get/Set the text

**kivy.core.text.LabelBase.text_size**

Get/set the (width, height) of the ‘
‘contrained rendering box

**kivy.core.text.LabelBase.usersize**

(deprecated) Use text_size instead.

---

## API - [`kivy.core.text.markup`](https://kivy.org/doc/stable/api-kivy.core.text.markup.html)

**kivy.core.text.markup.MarkupLabel**

Bases: [`kivy.core.text.LabelBase`](https://kivy.org/doc/stable/api-kivy.core.text.html#kivy.core.text.LabelBase)
Markup text label.
See module documentation for more information.

**kivy.core.text.markup.MarkupLabel.anchors**

Get the position of all the `[anchor=...]`:

**kivy.core.text.markup.MarkupLabel.markup**

Return the text with all the markup split:

**kivy.core.text.markup.MarkupLabel.refs**

Get the bounding box of all the `[ref=...]`:

**kivy.core.text.markup.MarkupLabel.render**

Return a tuple (width, height) to create the image
with the user constraints. (width, height) includes the padding.

**kivy.core.text.markup.MarkupLabel.shorten_post**

Shortens the text to a single line according to the label options.
This function operates on a text that has already been laid out because
for markup, parts of text can have different size and options.
If `text_size` [0] is None, the lines are returned unchanged.
Otherwise, the lines are converted to a single line fitting within the
constrained width, `text_size` [0].

---

## API - [`kivy.core.text.text_layout`](https://kivy.org/doc/stable/api-kivy.core.text.text_layout.html)

**kivy.core.text.text_layout.LayoutLine**

Bases: `builtins.object`
Formally describes a line of text. A line of text is composed of many
[`LayoutWord`](https://kivy.org/doc/stable/#kivy.core.text.text_layout.LayoutWord) instances, each with it’s own text, size and options.
A [`LayoutLine`](https://kivy.org/doc/stable/#kivy.core.text.text_layout.LayoutLine) instance does not always imply that the words
contained in the line ended with a newline. That is only the case if
[`is_last_line`](https://kivy.org/doc/stable/#kivy.core.text.text_layout.LayoutLine.is_last_line) is True. For example a single real line of text can
be split across multiple [`LayoutLine`](https://kivy.org/doc/stable/#kivy.core.text.text_layout.LayoutLine) instances if the whole line
doesn’t fit in the constrained width.

**kivy.core.text.text_layout.LayoutLine.h**

h: ‘int’

**kivy.core.text.text_layout.LayoutLine.is_last_line**

is_last_line: ‘int’

**kivy.core.text.text_layout.LayoutLine.line_wrap**

line_wrap: ‘int’

**kivy.core.text.text_layout.LayoutLine.w**

w: ‘int’

**kivy.core.text.text_layout.LayoutLine.words**

words: list

**kivy.core.text.text_layout.LayoutLine.x**

x: ‘int’

**kivy.core.text.text_layout.LayoutLine.y**

y: ‘int’

**kivy.core.text.text_layout.LayoutWord**

Bases: `builtins.object`
Formally describes a word contained in a line. The name word simply
means a chunk of text and can be used to describe any text.
A word has some width, height and is rendered according to options saved
in [`options`](https://kivy.org/doc/stable/#kivy.core.text.text_layout.LayoutWord.options). See [`LayoutLine`](https://kivy.org/doc/stable/#kivy.core.text.text_layout.LayoutLine) for its usage.

**kivy.core.text.text_layout.LayoutWord.lh**

lh: ‘int’

**kivy.core.text.text_layout.LayoutWord.lw**

lw: ‘int’

**kivy.core.text.text_layout.LayoutWord.options**

options: dict

**kivy.core.text.text_layout.LayoutWord.text**

text: object

**kivy.core.text.text_layout.layout_text**

Lays out text into a series of [`LayoutWord`](https://kivy.org/doc/stable/#kivy.core.text.text_layout.LayoutWord) and
[`LayoutLine`](https://kivy.org/doc/stable/#kivy.core.text.text_layout.LayoutLine) instances according to the options specified.
The function is designed to be called many times, each time new text is
appended to the last line (or first line if appending upwards), unless a
newline is present in the text. Each text appended is described by its own
options which can change between successive calls. If the text is
constrained, we stop as soon as the constraint is reached.

Following is a simple example with no padding and no stripping:

---

## API - [`kivy.core.video`](https://kivy.org/doc/stable/api-kivy.core.video.html)

**kivy.core.video.VideoBase**

Bases: [`kivy.event.EventDispatcher`](https://kivy.org/doc/stable/api-kivy.event.html#kivy.event.EventDispatcher)
VideoBase, a class used to implement a video reader.

**kivy.core.video.VideoBase.duration**

Get the video duration (in seconds)

**kivy.core.video.VideoBase.filename**

Get/set the filename/uri of the current video

**kivy.core.video.VideoBase.load**

Load the video from the current filename

**kivy.core.video.VideoBase.pause**

Pause the video
New in version 1.4.0.

**kivy.core.video.VideoBase.play**

Play the video

**kivy.core.video.VideoBase.position**

Get/set the position in the video (in seconds)

**kivy.core.video.VideoBase.seek**

Move to position as percentage (strictly, a proportion from
0 - 1) of the duration

**kivy.core.video.VideoBase.state**

Get the video playing status

**kivy.core.video.VideoBase.stop**

Stop the video playing

**kivy.core.video.VideoBase.texture**

Get the video texture

**kivy.core.video.VideoBase.unload**

Unload the actual video

**kivy.core.video.VideoBase.volume**

Get/set the volume in the video (1.0 = 100%)

---

## API - [`kivy.core.window`](https://kivy.org/doc/stable/api-kivy.core.window.html)

**kivy.core.window.Keyboard**

Bases: [`kivy.event.EventDispatcher`](https://kivy.org/doc/stable/api-kivy.event.html#kivy.event.EventDispatcher)
Keyboard interface that is returned by
[`WindowBase.request_keyboard()`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.request_keyboard). When you request a keyboard,
you’ll get an instance of this class. Whatever the keyboard input is
(system or virtual keyboard), you’ll receive events through this
instance.

Here is an example of how to request a Keyboard in accordance with the
current configuration:

**kivy.core.window.Keyboard.callback**

Callback that will be called when the keyboard is released

**kivy.core.window.Keyboard.keycode_to_string**

Convert a keycode number to a string according to the
`Keyboard.keycodes`. If the value is not found in the
keycodes, it will return ‘’.

**kivy.core.window.Keyboard.release**

Call this method to release the current keyboard.
This will ensure that the keyboard is no longer attached to your
callback.

**kivy.core.window.Keyboard.string_to_keycode**

Convert a string to a keycode number according to the
`Keyboard.keycodes`. If the value is not found in the
keycodes, it will return -1.

**kivy.core.window.Keyboard.target**

Target that have requested the keyboard

**kivy.core.window.Keyboard.widget**

VKeyboard widget, if allowed by the configuration

**kivy.core.window.Keyboard.window**

Window which the keyboard is attached too

**kivy.core.window.WindowBase**

Bases: [`kivy.event.EventDispatcher`](https://kivy.org/doc/stable/api-kivy.event.html#kivy.event.EventDispatcher)
WindowBase is an abstract window widget for any window implementation.

**kivy.core.window.WindowBase.add_widget**

Add a widget to a window

**kivy.core.window.WindowBase.allow_screensaver**

Whether the screen saver is enabled, or on mobile devices whether the
device is allowed to go to sleep while the app is open.
New in version 1.10.0.
[`allow_screensaver`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.allow_screensaver) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to True.

**kivy.core.window.WindowBase.always_on_top**

When enabled, the window will be brought to the front and will keep
the window above the rest. If disabled, it will restore the default
behavior.
This option can be toggled freely during the window’s lifecycle.
Only works for the sdl2 window provider. Check the [`config`](https://kivy.org/doc/stable/api-kivy.config.html#module-kivy.config)
documentation for a more detailed explanation on the values.
New in version 2.2.0.
[`always_on_top`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.always_on_top) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to False.

**kivy.core.window.WindowBase.borderless**

When set to True, this property removes the window border/decoration.
Check the [`config`](https://kivy.org/doc/stable/api-kivy.config.html#module-kivy.config) documentation for a more detailed
explanation on the values.
New in version 1.9.0.
[`borderless`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.borderless) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to False.

**kivy.core.window.WindowBase.center**

Center of the rotated window.
New in version 1.0.9.
[`center`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.center) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty).

**kivy.core.window.WindowBase.children**

List of the children of this window.
[`children`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.children) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) instance and
defaults to an empty list.
Use [`add_widget()`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.add_widget) and [`remove_widget()`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.remove_widget) to manipulate the list of
children. Don’t manipulate the list directly unless you know what you are
doing.

**kivy.core.window.WindowBase.clear**

Clear the window with the background color

**kivy.core.window.WindowBase.clearcolor**

Color used to clear the window.

Changed in version 1.7.2:The clearcolor default value is now: (0, 0, 0, 1).
New in version 1.0.9.
[`clearcolor`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.clearcolor) is an [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty) and
defaults to (0, 0, 0, 1).
Changed in version 2.1.0:Changed from [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) to
[`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty).

**kivy.core.window.WindowBase.close**

Close the window

**kivy.core.window.WindowBase.create_window**

Will create the main window and configure it.

**kivy.core.window.WindowBase.custom_titlebar**

When set to True, allows the user to set a widget as a titlebar.
Check the [`config`](https://kivy.org/doc/stable/api-kivy.config.html#module-kivy.config) documentation for a more detailed
explanation on the values.
New in version 2.1.0.
see [`set_custom_titlebar()`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.set_custom_titlebar)
for detailed usage
[`custom_titlebar`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.custom_titlebar) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to False.

**kivy.core.window.WindowBase.dpi**

Return the DPI of the screen as computed by the window. If the
implementation doesn’t support DPI lookup, it’s 96.

**kivy.core.window.WindowBase.event_managers**

Holds a list of registered event managers.
Don’t change the property directly but use
[`register_event_manager()`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.register_event_manager) and [`unregister_event_manager()`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.unregister_event_manager) to
register and unregister an event manager.
Event manager is an instance of
[`EventManagerBase`](https://kivy.org/doc/stable/api-kivy.eventmanager.html#kivy.eventmanager.EventManagerBase).
New in version 2.1.0.

**kivy.core.window.WindowBase.event_managers_dict**

Holds a dict of type_id to list of event managers.
Don’t change the property directly but use
[`register_event_manager()`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.register_event_manager) and [`unregister_event_manager()`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.unregister_event_manager) to
register and unregister an event manager.
Event manager is an instance of
[`EventManagerBase`](https://kivy.org/doc/stable/api-kivy.eventmanager.html#kivy.eventmanager.EventManagerBase).
New in version 2.1.0.

**kivy.core.window.WindowBase.flip**

Flip between buffers

**kivy.core.window.WindowBase.focus**

Check whether or not the window currently has focus.
New in version 1.9.1.
[`focus`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.focus) is a read-only [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) and
defaults to True.

**kivy.core.window.WindowBase.fullscreen**

This property sets the fullscreen mode of the window. Available options
are: True, False, ‘auto’ and ‘fake’. Check the [`config`](https://kivy.org/doc/stable/api-kivy.config.html#module-kivy.config)
documentation for more detailed explanations on these values.
fullscreen is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty) and defaults to
False.
New in version 1.2.0.

**kivy.core.window.WindowBase.get_gl_backend_name**

Returns the gl backend that will or is used with this window.

**kivy.core.window.WindowBase.gl_backends_allowed**

A list of Kivy gl backend names, which if not empty, will be the
exclusive list of gl backends that can be used with this window.

**kivy.core.window.WindowBase.gl_backends_ignored**

A list of Kivy gl backend names that may not be used with this window.

**kivy.core.window.WindowBase.grab_mouse**

Grab mouse - so won’t leave window
New in version 1.10.0.

**kivy.core.window.WindowBase.height**

Rotated window height.
[`height`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.height) is a read-only [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty).

**kivy.core.window.WindowBase.hide**

Hides the window. This method should be used on desktop
platforms only.
New in version 1.9.0.

**kivy.core.window.WindowBase.icon**

A path to the window icon.
New in version 1.1.2.
[`icon`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.icon) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty).

**kivy.core.window.WindowBase.keyboard_anim_args**

The attributes for animating softkeyboard/IME.
t = transition, d = duration. This value will have no effect on
desktops.
New in version 1.10.0.
[`keyboard_anim_args`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.keyboard_anim_args) is a dict and defaults to
{‘t’: ‘in_out_quart’, ‘d’: .5}.

**kivy.core.window.WindowBase.keyboard_height**

Returns the height of the softkeyboard/IME on mobile platforms.
Will return 0 if not on mobile platform or if IME is not active.

New in version 1.9.0.
[`keyboard_height`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.keyboard_height) is a read-only
[`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) and defaults to 0.

**kivy.core.window.WindowBase.keyboard_padding**

The padding to have between the softkeyboard/IME & target
or bottom of window. Will have no effect on desktops.
New in version 1.10.0.
[`keyboard_padding`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.keyboard_padding) is a
[`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and defaults to 0.

**kivy.core.window.WindowBase.left**

Left position of the window.

Changed in version 1.10.0:[`left`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.left) is now an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty)
New in version 1.9.1.
[`left`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.left) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) and defaults to
the position set in [`Config`](https://kivy.org/doc/stable/api-kivy.config.html#kivy.config.Config).

**kivy.core.window.WindowBase.mainloop**

Called by the EventLoop every frame after it idles.

**kivy.core.window.WindowBase.managed_textinput**

True if this Window class uses on_textinput to insert text, internal.

**kivy.core.window.WindowBase.maximize**

Maximizes the window. This method should be used on desktop
platforms only.
New in version 1.9.0.

**kivy.core.window.WindowBase.minimize**

Minimizes the window. This method should be used on desktop
platforms only.
New in version 1.9.0.

**kivy.core.window.WindowBase.minimum_height**

The minimum height to restrict the window to.
New in version 1.9.1.
[`minimum_height`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.minimum_height) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0.

**kivy.core.window.WindowBase.minimum_width**

The minimum width to restrict the window to.
New in version 1.9.1.
[`minimum_width`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.minimum_width) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0.

**kivy.core.window.WindowBase.modifiers**

List of keyboard modifiers currently active.
New in version 1.0.9.
[`modifiers`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.modifiers) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty).

**kivy.core.window.WindowBase.mouse_pos**

2d position of the mouse cursor within the window.
Position is relative to the left/bottom point of the window.

New in version 1.2.0.
[`mouse_pos`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.mouse_pos) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to (0, 0).

**kivy.core.window.WindowBase.on_close**

Event called when the window is closed.

**kivy.core.window.WindowBase.on_cursor_enter**

Event called when the cursor enters the window.
New in version 1.9.1.

**kivy.core.window.WindowBase.on_cursor_leave**

Event called when the cursor leaves the window.
New in version 1.9.1.

**kivy.core.window.WindowBase.on_drop_begin**

Event called when a text or a file drop on the application is about
to begin. It will be followed-up by a single or a multiple
on_drop_text or on_drop_file events ending with an on_drop_end
event.
Arguments x and y are the mouse cursor position at the time of the
drop and you should only rely on them if the drop originated from the
mouse.

New in version 2.1.0.

**kivy.core.window.WindowBase.on_drop_end**

Event called when a text or a file drop on the application has
ended.
Arguments x and y are the mouse cursor position at the time of the
drop and you should only rely on them if the drop originated from the
mouse.

New in version 2.1.0.

**kivy.core.window.WindowBase.on_drop_file**

Event called when a file is dropped on the application.
Arguments x and y are the mouse cursor position at the time of the
drop and you should only rely on them if the drop originated from the
mouse.

New in version 1.2.0.
Changed in version 2.1.0:Renamed from on_dropfile to on_drop_file.

**kivy.core.window.WindowBase.on_drop_text**

Event called when a text is dropped on the application.
Arguments x and y are the mouse cursor position at the time of the
drop and you should only rely on them if the drop originated from the
mouse.

New in version 2.1.0.

**kivy.core.window.WindowBase.on_flip**

Flip between buffers (event)

**kivy.core.window.WindowBase.on_hide**

Event called when the window is hidden.
New in version 1.10.0.

**kivy.core.window.WindowBase.on_joy_axis**

Event called when a joystick has a stick or other axis moved.
New in version 1.9.0.

**kivy.core.window.WindowBase.on_joy_ball**

Event called when a joystick has a ball moved.
New in version 1.9.0.

**kivy.core.window.WindowBase.on_joy_button_down**

Event called when a joystick has a button pressed.
New in version 1.9.0.

**kivy.core.window.WindowBase.on_joy_button_up**

Event called when a joystick has a button released.
New in version 1.9.0.

**kivy.core.window.WindowBase.on_joy_hat**

Event called when a joystick has a hat/dpad moved.
New in version 1.9.0.

**kivy.core.window.WindowBase.on_key_down**

Event called when a key is down (same arguments as on_keyboard)

**kivy.core.window.WindowBase.on_key_up**

Event called when a key is released (same arguments as on_keyboard).

**kivy.core.window.WindowBase.on_keyboard**

Event called when keyboard is used.

**kivy.core.window.WindowBase.on_maximize**

Event called when the window is maximized.
New in version 1.10.0.

**kivy.core.window.WindowBase.on_memorywarning**

Event called when the platform have memory issue.
Your goal is to clear the cache in your app as much as you can,
release unused widgets, do garbage collection etc.
Currently, this event is fired only from the SDL2 provider, for
iOS and Android.
New in version 1.9.0.

**kivy.core.window.WindowBase.on_minimize**

Event called when the window is minimized.
New in version 1.10.0.

**kivy.core.window.WindowBase.on_motion**

Event called when a motion event is received.

Changed in version 2.1.0:Event managers get to handle the touch event first and if none of
them accepts the event (by returning True) then window will
dispatch me through “on_touch_down”, “on_touch_move”,
“on_touch_up” events depending on the etype. All non-touch events
will go only through managers.

**kivy.core.window.WindowBase.on_mouse_down**

Event called when the mouse is used (pressed/released).

**kivy.core.window.WindowBase.on_mouse_move**

Event called when the mouse is moved with buttons pressed.

**kivy.core.window.WindowBase.on_mouse_up**

Event called when the mouse is moved with buttons pressed.

**kivy.core.window.WindowBase.on_request_close**

Event called before we close the window. If a bound function returns
True, the window will not be closed. If the event is triggered
because of the keyboard escape key, the keyword argument source is
dispatched along with a value of keyboard to the bound functions.

**kivy.core.window.WindowBase.on_resize**

Event called when the window is resized.

**kivy.core.window.WindowBase.on_restore**

Event called when the window is restored.
New in version 1.10.0.

**kivy.core.window.WindowBase.on_rotate**

Event called when the screen has been rotated.

**kivy.core.window.WindowBase.on_show**

Event called when the window is shown.
New in version 1.10.0.

**kivy.core.window.WindowBase.on_textedit**

Event called when inputting with IME.
The string inputting with IME is set as the parameter of
this event.
New in version 1.10.1.

**kivy.core.window.WindowBase.on_textinput**

Event called when text: i.e. alpha numeric non control keys or set
of keys is entered. As it is not guaranteed whether we get one
character or multiple ones, this event supports handling multiple
characters.
New in version 1.9.0.

**kivy.core.window.WindowBase.on_touch_down**

Event called when a touch down event is initiated.
Changed in version 1.9.0:The touch pos is now transformed to window coordinates before
this method is called. Before, the touch pos coordinate would be
(0, 0) when this method was called.

**kivy.core.window.WindowBase.on_touch_move**

Event called when a touch event moves (changes location).
Changed in version 1.9.0:The touch pos is now transformed to window coordinates before
this method is called. Before, the touch pos coordinate would be
(0, 0) when this method was called.

**kivy.core.window.WindowBase.on_touch_up**

Event called when a touch event is released (terminated).
Changed in version 1.9.0:The touch pos is now transformed to window coordinates before
this method is called. Before, the touch pos coordinate would be
(0, 0) when this method was called.

**kivy.core.window.WindowBase.opacity**

Opacity of the window. Accepts a value between 0.0 (transparent) and
1.0 (opaque).

New in version 2.3.0.
[`opacity`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.opacity) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) and defaults
to 1.0.

**kivy.core.window.WindowBase.parent**

Parent of this window.
[`parent`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.parent) is a [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) instance and
defaults to None. When created, the parent is set to the window itself.
You must take care of it if you are doing a recursive check.

**kivy.core.window.WindowBase.raise_window**

Raise the window. This method should be used on desktop
platforms only.
New in version 1.9.1.

**kivy.core.window.WindowBase.register_event_manager**

Register and start an event manager to handle events declared in
[`type_ids`](https://kivy.org/doc/stable/api-kivy.eventmanager.html#kivy.eventmanager.EventManagerBase.type_ids) attribute.
New in version 2.1.0.

**kivy.core.window.WindowBase.release_all_keyboards**

New in version 1.0.8.
This will ensure that no virtual keyboard / system keyboard is
requested. All instances will be closed.

**kivy.core.window.WindowBase.release_keyboard**

New in version 1.0.4.
Internal method for the widget to release the real-keyboard. Check
[`request_keyboard()`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.request_keyboard) to understand how it works.

**kivy.core.window.WindowBase.remove_widget**

Remove a widget from a window

**kivy.core.window.WindowBase.request_keyboard**

New in version 1.0.4.
Internal widget method to request the keyboard. This method is rarely
required by the end-user as it is handled automatically by the
[`TextInput`](https://kivy.org/doc/stable/api-kivy.uix.textinput.html#kivy.uix.textinput.TextInput). We expose it in case you want
to handle the keyboard manually for unique input scenarios.
A widget can request the keyboard, indicating a callback to call
when the keyboard is released (or taken by another widget).

**kivy.core.window.WindowBase.restore**

Restores the size and position of a maximized or minimized window.
This method should be used on desktop platforms only.
New in version 1.9.0.

**kivy.core.window.WindowBase.rotation**

Get/set the window content rotation. Can be one of 0, 90, 180, 270
degrees.
New in version 1.0.9.
[`rotation`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.rotation) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty).

**kivy.core.window.WindowBase.screenshot**

Save the actual displayed image to a file.

**kivy.core.window.WindowBase.set_custom_titlebar**

Sets a Widget as a titlebar

New in version 2.1.0.
This function returns True on successfully setting the custom titlebar,
else false
How to use this feature

If you want a child of the widget to receive touch events, in
that child define a property draggable and set it to False
If you set the property draggable on a layout,
all the child in the layout will receive touch events
If you want to override default behavior, add function in_drag_area(x,y)
to the widget
The function is call with two args x,y which are mouse.x, and mouse.y
the function should return
True if that point should be used to drag the window
False if you want to receive the touch event at the point

**kivy.core.window.WindowBase.set_icon**

Set the icon of the window.
New in version 1.0.5.

**kivy.core.window.WindowBase.set_system_cursor**

Set type of a mouse cursor in the Window.
It can be one of ‘arrow’, ‘ibeam’, ‘wait’, ‘crosshair’, ‘wait_arrow’,
‘size_nwse’, ‘size_nesw’, ‘size_we’, ‘size_ns’, ‘size_all’, ‘no’, or
‘hand’.
On some platforms there might not be a specific cursor supported and
such an option falls back to one of the substitutable alternatives:
Windows
MacOS
Linux X11
Linux Wayland
arrow
arrow
arrow
arrow
arrow
ibeam
ibeam
ibeam
ibeam
ibeam
wait
wait
arrow
wait
wait
crosshair
crosshair
crosshair
crosshair
hand
wait_arrow
arrow
arrow
wait
wait
size_nwse
size_nwse
size_all
size_all
hand
size_nesw
size_nesw
size_all
size_all
hand
size_we
size_we
size_we
size_we
hand
size_ns
size_ns
size_ns
size_ns
hand
size_all
size_all
size_all
size_all
hand
no
no
no
no
ibeam
hand
hand
hand
hand
hand
New in version 1.10.1.

**kivy.core.window.WindowBase.set_title**

Set the window title.
New in version 1.0.5.

**kivy.core.window.WindowBase.set_vkeyboard_class**

New in version 1.0.8.
Set the VKeyboard class to use. If set to None, it will use the
[`kivy.uix.vkeyboard.VKeyboard`](https://kivy.org/doc/stable/api-kivy.uix.vkeyboard.html#kivy.uix.vkeyboard.VKeyboard).

**kivy.core.window.WindowBase.shape_color_key**

Color key of the shaped window - sets which color will be hidden from
the window [`shape_image`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.shape_image) (only works for sdl2 window provider).
New in version 1.10.1.
[`shape_color_key`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.shape_color_key) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
instance and defaults to [1, 1, 1, 1].
Changed in version 2.0.0:Changed from [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) to
[`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty).

**kivy.core.window.WindowBase.shape_cutoff**

The window [`shape_image`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.shape_image) cutoff property (only works for sdl2
window provider).
New in version 1.10.1.
[`shape_cutoff`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.shape_cutoff) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to True.

**kivy.core.window.WindowBase.shape_image**

An image for the window shape (only works for sdl2 window provider).

New in version 1.10.1.
[`shape_image`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.shape_image) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to ‘data/images/defaultshape.png’. This value is taken from
[`Config`](https://kivy.org/doc/stable/api-kivy.config.html#kivy.config.Config).

**kivy.core.window.WindowBase.shape_mode**

Window mode for shaping (only works for sdl2 window provider).

New in version 1.10.1.
[`shape_mode`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.shape_mode) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty).

**kivy.core.window.WindowBase.shaped**

Read only property to check if the window is shapable or not (only works
for sdl2 window provider).
New in version 1.10.1.
[`shaped`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.shaped) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty).

**kivy.core.window.WindowBase.show**

Shows the window. This method should be used on desktop
platforms only.
New in version 1.9.0.

**kivy.core.window.WindowBase.show_cursor**

Set whether or not the cursor is shown on the window.
New in version 1.9.1.
[`show_cursor`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.show_cursor) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to True.

**kivy.core.window.WindowBase.size**

Get the rotated size of the window. If [`rotation`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.rotation) is set, then the
size will change to reflect the rotation.
New in version 1.0.9.
[`size`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.size) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty).

**kivy.core.window.WindowBase.softinput_mode**

This specifies the behavior of window contents on display of the soft
keyboard on mobile platforms. It can be one of ‘’, ‘pan’, ‘scale’,
‘resize’ or ‘below_target’. Their effects are listed below.
Value
Effect
‘’
The main window is left as is, allowing you to use
the [`keyboard_height`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.keyboard_height) to manage the window
contents manually.
‘pan’
The main window pans, moving the bottom part of the
window to be always on top of the keyboard.
‘resize’
The window is resized and the contents scaled to fit
the remaining space.
‘below_target’
The window pans so that the current target TextInput
widget requesting the keyboard is presented just above
the soft keyboard.
[`softinput_mode`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.softinput_mode) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty) and
defaults to ‘’.

New in version 1.9.0.
Changed in version 1.9.1:The ‘below_target’ option was added.

**kivy.core.window.WindowBase.system_size**

Real size of the window ignoring rotation. If the density is
not 1, the [`system_size`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.system_size) is the [`size`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.size) divided by
density.
New in version 1.0.9.
[`system_size`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.system_size) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty).

**kivy.core.window.WindowBase.to_normalized_pos**

Transforms absolute coordinates to normalized (0-1) coordinates
using [`system_size`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.system_size).
New in version 2.1.0.

**kivy.core.window.WindowBase.top**

Top position of the window.

Changed in version 1.10.0:[`top`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.top) is now an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty)
New in version 1.9.1.
[`top`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.top) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) and defaults to
the position set in [`Config`](https://kivy.org/doc/stable/api-kivy.config.html#kivy.config.Config).

**kivy.core.window.WindowBase.transform_motion_event_2d**

Transforms the motion event me to this window size and then if
widget is passed transforms me to widget’s local coordinates.

New in version 2.1.0.

**kivy.core.window.WindowBase.ungrab_mouse**

Ungrab mouse
New in version 1.10.0.

**kivy.core.window.WindowBase.unregister_event_manager**

Unregister and stop an event manager previously registered with
[`register_event_manager()`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.register_event_manager).
New in version 2.1.0.

**kivy.core.window.WindowBase.width**

Rotated window width.
[`width`](https://kivy.org/doc/stable/#kivy.core.window.WindowBase.width) is a read-only [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty).

---

## API - [`kivy.effects.dampedscroll`](https://kivy.org/doc/stable/api-kivy.effects.dampedscroll.html)

**kivy.effects.dampedscroll.DampedScrollEffect**

Bases: [`kivy.effects.scroll.ScrollEffect`](https://kivy.org/doc/stable/api-kivy.effects.scroll.html#kivy.effects.scroll.ScrollEffect)
DampedScrollEffect class. See the module documentation for more
information.

**kivy.effects.dampedscroll.DampedScrollEffect.edge_damping**

Edge damping.
[`edge_damping`](https://kivy.org/doc/stable/#kivy.effects.dampedscroll.DampedScrollEffect.edge_damping) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0.25

**kivy.effects.dampedscroll.DampedScrollEffect.min_overscroll**

An overscroll less than this amount will be normalized to 0.
New in version 1.8.0.
[`min_overscroll`](https://kivy.org/doc/stable/#kivy.effects.dampedscroll.DampedScrollEffect.min_overscroll) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to .5.

**kivy.effects.dampedscroll.DampedScrollEffect.round_value**

If True, when the motion stops, `value` is rounded to the nearest
integer.
New in version 1.8.0.
[`round_value`](https://kivy.org/doc/stable/#kivy.effects.dampedscroll.DampedScrollEffect.round_value) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to True.

**kivy.effects.dampedscroll.DampedScrollEffect.spring_constant**

Spring constant.
[`spring_constant`](https://kivy.org/doc/stable/#kivy.effects.dampedscroll.DampedScrollEffect.spring_constant) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 2.0

**kivy.effects.dampedscroll.DampedScrollEffect.update_velocity**

(internal) Update the velocity according to the frametime and
friction.

---

## API - [`kivy.effects.kinetic`](https://kivy.org/doc/stable/api-kivy.effects.kinetic.html)

**kivy.effects.kinetic.KineticEffect**

Bases: [`kivy.event.EventDispatcher`](https://kivy.org/doc/stable/api-kivy.event.html#kivy.event.EventDispatcher)
Kinetic effect class. See module documentation for more information.

**kivy.effects.kinetic.KineticEffect.cancel**

Cancel a movement. This can be used in case [`stop()`](https://kivy.org/doc/stable/#kivy.effects.kinetic.KineticEffect.stop) cannot be
called. It will reset [`is_manual`](https://kivy.org/doc/stable/#kivy.effects.kinetic.KineticEffect.is_manual) to False, and compute the
movement if the velocity is > 0.

**kivy.effects.kinetic.KineticEffect.friction**

Friction to apply on the velocity
[`friction`](https://kivy.org/doc/stable/#kivy.effects.kinetic.KineticEffect.friction) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0.05.

**kivy.effects.kinetic.KineticEffect.is_manual**

Indicate if a movement is in progress (True) or not (False).
[`is_manual`](https://kivy.org/doc/stable/#kivy.effects.kinetic.KineticEffect.is_manual) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to False.

**kivy.effects.kinetic.KineticEffect.max_history**

Save up to max_history movement value into the history. This is used
for correctly calculating the velocity according to the movement.
[`max_history`](https://kivy.org/doc/stable/#kivy.effects.kinetic.KineticEffect.max_history) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 5.

**kivy.effects.kinetic.KineticEffect.min_distance**

The minimal distance for a movement to have nonzero velocity.
New in version 1.8.0.
[`min_distance`](https://kivy.org/doc/stable/#kivy.effects.kinetic.KineticEffect.min_distance) is [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0.1.

**kivy.effects.kinetic.KineticEffect.min_velocity**

Velocity below this quantity is normalized to 0. In other words,
any motion whose velocity falls below this number is stopped.
New in version 1.8.0.
[`min_velocity`](https://kivy.org/doc/stable/#kivy.effects.kinetic.KineticEffect.min_velocity) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0.5.

**kivy.effects.kinetic.KineticEffect.start**

Start the movement.

**kivy.effects.kinetic.KineticEffect.std_dt**

New in version 2.0.0.
[`std_dt`](https://kivy.org/doc/stable/#kivy.effects.kinetic.KineticEffect.std_dt) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0.017.

**kivy.effects.kinetic.KineticEffect.stop**

Stop the movement.
See [`start()`](https://kivy.org/doc/stable/#kivy.effects.kinetic.KineticEffect.start) for the arguments.

**kivy.effects.kinetic.KineticEffect.update**

Update the movement.
See [`start()`](https://kivy.org/doc/stable/#kivy.effects.kinetic.KineticEffect.start) for the arguments.

**kivy.effects.kinetic.KineticEffect.update_velocity**

(internal) Update the velocity according to the frametime and
friction.

**kivy.effects.kinetic.KineticEffect.value**

Value (during the movement and computed) of the effect.
[`value`](https://kivy.org/doc/stable/#kivy.effects.kinetic.KineticEffect.value) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0.

**kivy.effects.kinetic.KineticEffect.velocity**

Velocity of the movement.
[`velocity`](https://kivy.org/doc/stable/#kivy.effects.kinetic.KineticEffect.velocity) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0.

---

## API - [`kivy.effects.opacityscroll`](https://kivy.org/doc/stable/api-kivy.effects.opacityscroll.html)

**kivy.effects.opacityscroll.OpacityScrollEffect**

Bases: [`kivy.effects.dampedscroll.DampedScrollEffect`](https://kivy.org/doc/stable/api-kivy.effects.dampedscroll.html#kivy.effects.dampedscroll.DampedScrollEffect)
OpacityScrollEffect class. Uses the overscroll
information to reduce the opacity of the scrollview widget. When the user
stops the drag, the opacity is set back to 1.

---

## API - [`kivy.effects.scroll`](https://kivy.org/doc/stable/api-kivy.effects.scroll.html)

**kivy.effects.scroll.ScrollEffect**

Bases: [`kivy.effects.kinetic.KineticEffect`](https://kivy.org/doc/stable/api-kivy.effects.kinetic.html#kivy.effects.kinetic.KineticEffect)
ScrollEffect class. See the module documentation for more information.

**kivy.effects.scroll.ScrollEffect.displacement**

Cumulative distance of the movement during the interaction. This is used
to determine if the movement is a drag (more than [`drag_threshold`](https://kivy.org/doc/stable/#kivy.effects.scroll.ScrollEffect.drag_threshold))
or not.
[`displacement`](https://kivy.org/doc/stable/#kivy.effects.scroll.ScrollEffect.displacement) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0.

**kivy.effects.scroll.ScrollEffect.drag_threshold**

Minimum distance to travel before the movement is considered as a drag.
[`drag_threshold`](https://kivy.org/doc/stable/#kivy.effects.scroll.ScrollEffect.drag_threshold) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 20sp.

**kivy.effects.scroll.ScrollEffect.max**

Maximum boundary to use for scrolling.
[`max`](https://kivy.org/doc/stable/#kivy.effects.scroll.ScrollEffect.max) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and defaults to
0.

**kivy.effects.scroll.ScrollEffect.min**

Minimum boundary to use for scrolling.
[`min`](https://kivy.org/doc/stable/#kivy.effects.scroll.ScrollEffect.min) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and defaults to
0.

**kivy.effects.scroll.ScrollEffect.overscroll**

Computed value when the user over-scrolls i.e. goes out of the bounds.
[`overscroll`](https://kivy.org/doc/stable/#kivy.effects.scroll.ScrollEffect.overscroll) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0.

**kivy.effects.scroll.ScrollEffect.reset**

(internal) Reset the value and the velocity to the pos.
Mostly used when the bounds are checked.

**kivy.effects.scroll.ScrollEffect.scroll**

Computed value for scrolling. This value is different from
[`kivy.effects.kinetic.KineticEffect.value`](https://kivy.org/doc/stable/api-kivy.effects.kinetic.html#kivy.effects.kinetic.KineticEffect.value)
in that it will return to one of the min/max bounds.
[`scroll`](https://kivy.org/doc/stable/#kivy.effects.scroll.ScrollEffect.scroll) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and defaults
to 0.

**kivy.effects.scroll.ScrollEffect.start**

Start the movement.

**kivy.effects.scroll.ScrollEffect.stop**

Stop the movement.
See [`start()`](https://kivy.org/doc/stable/#kivy.effects.scroll.ScrollEffect.start) for the arguments.

**kivy.effects.scroll.ScrollEffect.target_widget**

Widget to attach to this effect. Even if this class doesn’t make changes
to the target_widget by default, subclasses can use it to change the
graphics or apply custom transformations.
[`target_widget`](https://kivy.org/doc/stable/#kivy.effects.scroll.ScrollEffect.target_widget) is a [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to None.

**kivy.effects.scroll.ScrollEffect.update**

Update the movement.
See [`start()`](https://kivy.org/doc/stable/#kivy.effects.scroll.ScrollEffect.start) for the arguments.

---

## API - [`kivy.event`](https://kivy.org/doc/stable/api-kivy.event.html)

**kivy.event.EventDispatcher**

Bases: [`kivy.event.ObjectWithUid`](https://kivy.org/doc/stable/#kivy.event.ObjectWithUid)
See the module docstring for usage.

**kivy.event.EventDispatcher.apply_property**

Adds properties at runtime to the class. The function accepts
keyword arguments of the form prop_name=prop, where prop is a
`Property` instance and prop_name is the name of the attribute
of the property.
New in version 1.9.1.

For example:

**kivy.event.EventDispatcher.bind**

Bind an event type or a property to a callback.
Usage:

In general, property callbacks are called with 2 arguments (the
object and the property’s new value) and event callbacks with
one argument (the object). The example above illustrates this.
The following example demonstrates various ways of using the bind
function in a complete application:

If a callback has already been bound to a given event or property,
it won’t be added again.
When binding a method to an event or property, a
[`kivy.weakmethod.WeakMethod`](https://kivy.org/doc/stable/api-kivy.weakmethod.html#kivy.weakmethod.WeakMethod) of the callback is saved. That is,
rather than storing a regular reference, it stores both a weak
reference to the instance (see Python’s `weakref`).
This has two consequences.
The first is that the binding will not prevent garbage collection of
the method’s object. The client must maintain a reference to the instance for
the desired lifetime. The callback reference is silently removed if it
becomes invalid.
The second is that when using a decorated method e.g.:

the decorator (`my_decorator` here) must use [wraps](https://docs.python.org/3/library/functools.html#functools.wraps) internally.

**kivy.event.EventDispatcher.create_property**

Create a new property at runtime.
New in version 1.0.9.
Changed in version 1.8.0:value parameter added, can be used to set the default value of the
property. Also, the type of the value is used to specialize the
created property.
Changed in version 1.9.0:In the past, if value was of type bool, a NumericProperty
would be created, now a BooleanProperty is created.
Also, now and positional and keyword arguments are passed to the
property when created.
Changed in version 2.0.0:default_value has been added.

**kivy.event.EventDispatcher.dispatch**

Dispatch an event across all the handlers added in bind/fbind().
As soon as a handler returns True, the dispatching stops.
The function collects all the positional and keyword arguments and
passes them on to the handlers.

Changed in version 1.9.0:Keyword arguments collection and forwarding was added. Before, only
positional arguments would be collected and forwarded.

**kivy.event.EventDispatcher.dispatch_children**

**kivy.event.EventDispatcher.dispatch_generic**

**kivy.event.EventDispatcher.events**

Return all the events in the class. Can be used for introspection.
New in version 1.8.0.

**kivy.event.EventDispatcher.fbind**

A method for advanced, and typically faster binding. This method is
different than [`bind()`](https://kivy.org/doc/stable/#kivy.event.EventDispatcher.bind) and is meant for more advanced users and
internal usage. It can be used as long as the following points are heeded.
As opposed to [`bind()`](https://kivy.org/doc/stable/#kivy.event.EventDispatcher.bind), it does not check that this function and
largs/kwargs has not been bound before to this name. So binding
the same callback multiple times will just keep adding it.
Although [`bind()`](https://kivy.org/doc/stable/#kivy.event.EventDispatcher.bind) creates a `WeakMethod` of the callback when
binding to an event or property, this method stores the callback
directly, unless a keyword argument ref with value True is provided
and then a `WeakMethod` is saved.
This is useful when there’s no risk of a memory leak by storing the
callback directly.
This method returns a unique positive number if name was found and
bound, and 0, otherwise. It does not raise an exception, like
[`bind()`](https://kivy.org/doc/stable/#kivy.event.EventDispatcher.bind) if the property name is not found. If not zero,
the uid returned is unique to this name and callback and can be
used with [`unbind_uid()`](https://kivy.org/doc/stable/#kivy.event.EventDispatcher.unbind_uid) for unbinding.
When binding a callback with largs and/or kwargs, [`funbind()`](https://kivy.org/doc/stable/#kivy.event.EventDispatcher.funbind)
must be used for unbinding. If no largs and kwargs are provided,
[`unbind()`](https://kivy.org/doc/stable/#kivy.event.EventDispatcher.unbind) may be used as well. [`unbind_uid()`](https://kivy.org/doc/stable/#kivy.event.EventDispatcher.unbind_uid) can be used in
either case.
This method passes on any caught positional and/or keyword arguments to
the callback, removing the need to call partial. When calling the
callback the expended largs are passed on followed by instance/value
(just instance for kwargs) followed by expended kwargs.
Following is an example of usage similar to the example in
[`bind()`](https://kivy.org/doc/stable/#kivy.event.EventDispatcher.bind):

New in version 1.9.0.
Changed in version 1.9.1:The ref keyword argument has been added.

**kivy.event.EventDispatcher.funbind**

Similar to [`fbind()`](https://kivy.org/doc/stable/#kivy.event.EventDispatcher.fbind).
When unbinding, [`unbind()`](https://kivy.org/doc/stable/#kivy.event.EventDispatcher.unbind) will unbind all callbacks that match the
callback, while this method will only unbind the first.
To unbind, the same positional and keyword arguments passed to
[`fbind()`](https://kivy.org/doc/stable/#kivy.event.EventDispatcher.fbind) must be passed on to funbind.

New in version 1.9.0.

**kivy.event.EventDispatcher.get_property_observers**

Returns a list of methods that are bound to the property/event
passed as the *name* argument:

New in version 1.8.0.
Changed in version 1.9.0:args has been added.

**kivy.event.EventDispatcher.getter**

Return the getter of a property.
New in version 1.0.9.

**kivy.event.EventDispatcher.is_event_type**

Return True if the event_type is already registered.
New in version 1.0.4.

**kivy.event.EventDispatcher.properties**

Return all the properties in the class in a dictionary of
key/property class. Can be used for introspection.
New in version 1.0.9.

**kivy.event.EventDispatcher.property**

Get a property instance from the property name. If quiet is True,
None is returned instead of raising an exception when name is not a
property. Defaults to False.
New in version 1.0.9.

Changed in version 1.9.0:quiet was added.

**kivy.event.EventDispatcher.proxy_ref**

Returns a [`WeakProxy`](https://kivy.org/doc/stable/api-kivy.weakproxy.html#kivy.weakproxy.WeakProxy) reference to the
[`EventDispatcher`](https://kivy.org/doc/stable/#kivy.event.EventDispatcher).
New in version 1.9.0.
Changed in version 2.0.0:Previously it just returned itself, now it actually returns a
[`WeakProxy`](https://kivy.org/doc/stable/api-kivy.weakproxy.html#kivy.weakproxy.WeakProxy).

**kivy.event.EventDispatcher.register_event_type**

Register an event type with the dispatcher.
Registering event types allows the dispatcher to validate event handler
names as they are attached and to search attached objects for suitable
handlers. Each event type declaration must:
start with the prefix on_.
have a default handler in the class.
Example of creating a custom event:

**kivy.event.EventDispatcher.setter**

Return the setter of a property. Use: instance.setter(‘name’).
The setter is a convenient callback function useful if you want
to directly bind one property to another.
It returns a partial function that will accept
(obj, value) args and results in the property ‘name’ of instance
being set to value.
New in version 1.0.9.
For example, to bind number2 to number1 in python you would do:

This is equivalent to kv binding:

**kivy.event.EventDispatcher.unbind**

Unbind properties from callback functions with similar usage as
[`bind()`](https://kivy.org/doc/stable/#kivy.event.EventDispatcher.bind).
If a callback has been bound to a given event or property multiple
times, only the first occurrence will be unbound.

**kivy.event.EventDispatcher.unbind_uid**

Uses the uid returned by [`fbind()`](https://kivy.org/doc/stable/#kivy.event.EventDispatcher.fbind) to unbind the callback.
This method is much more efficient than [`funbind()`](https://kivy.org/doc/stable/#kivy.event.EventDispatcher.funbind). If uid
evaluates to False (e.g. 0) a ValueError is raised. Also, only
callbacks bound with [`fbind()`](https://kivy.org/doc/stable/#kivy.event.EventDispatcher.fbind) can be unbound with this method.
Since each call to [`fbind()`](https://kivy.org/doc/stable/#kivy.event.EventDispatcher.fbind) will generate a unique uid,
only one callback will be removed. If uid is not found among the
callbacks, no error is raised.
E.g.:

New in version 1.9.0.

**kivy.event.EventDispatcher.unregister_event_type**

Unregister an event type in the dispatcher.
Changed in version 2.1.0:Method renamed from unregister_event_types to
unregister_event_type.

**kivy.event.EventDispatcher.unregister_event_types**

**kivy.event.ObjectWithUid**

Bases: `builtins.object`
(internal) This class assists in providing unique identifiers for class
instances. It is not intended for direct usage.

**kivy.event.Observable**

Bases: [`kivy.event.ObjectWithUid`](https://kivy.org/doc/stable/#kivy.event.ObjectWithUid)
[`Observable`](https://kivy.org/doc/stable/#kivy.event.Observable) is a stub class defining the methods required
for binding. [`EventDispatcher`](https://kivy.org/doc/stable/#kivy.event.EventDispatcher) is (the) one example of a class that
implements the binding interface. See [`EventDispatcher`](https://kivy.org/doc/stable/#kivy.event.EventDispatcher) for details.
New in version 1.9.0.

**kivy.event.Observable.bind**

**kivy.event.Observable.fbind**

See [`EventDispatcher.fbind()`](https://kivy.org/doc/stable/#kivy.event.EventDispatcher.fbind).

**kivy.event.Observable.funbind**

See [`fbind()`](https://kivy.org/doc/stable/#kivy.event.Observable.fbind) and [`EventDispatcher.funbind()`](https://kivy.org/doc/stable/#kivy.event.EventDispatcher.funbind).

**kivy.event.Observable.unbind**

**kivy.event.Observable.unbind_uid**

See [`fbind()`](https://kivy.org/doc/stable/#kivy.event.Observable.fbind) and [`EventDispatcher.unbind_uid()`](https://kivy.org/doc/stable/#kivy.event.EventDispatcher.unbind_uid).

---

## API - [`kivy.eventmanager`](https://kivy.org/doc/stable/api-kivy.eventmanager.html)

**kivy.eventmanager.EventManagerBase**

Bases: `builtins.object`
Abstract class with methods [`start()`](https://kivy.org/doc/stable/#kivy.eventmanager.EventManagerBase.start), [`stop()`](https://kivy.org/doc/stable/#kivy.eventmanager.EventManagerBase.stop) and
[`dispatch()`](https://kivy.org/doc/stable/#kivy.eventmanager.EventManagerBase.dispatch) for specific class to implement.
Example of the manager receiving touch and hover events:

**kivy.eventmanager.EventManagerBase.dispatch**

Dispatch event me to the widgets in the [`window`](https://kivy.org/doc/stable/#kivy.eventmanager.EventManagerBase.window).

New in version 2.1.0.

**kivy.eventmanager.EventManagerBase.start**

Start the manager, bind callbacks to the objects and create
additional resources. Attribute [`window`](https://kivy.org/doc/stable/#kivy.eventmanager.EventManagerBase.window) is assigned when this
method is called.
New in version 2.1.0.

**kivy.eventmanager.EventManagerBase.stop**

Stop the manager, unbind from any objects and release any allocated
resources.
New in version 2.1.0.

**kivy.eventmanager.EventManagerBase.type_ids**

Override this attribute to declare the type ids of the events which
manager wants to receive. This attribute will be used by
[`WindowBase`](https://kivy.org/doc/stable/api-kivy.core.window.html#kivy.core.window.WindowBase) to know which events to pass to the
[`dispatch()`](https://kivy.org/doc/stable/#kivy.eventmanager.EventManagerBase.dispatch) method.
New in version 2.1.0.

**kivy.eventmanager.EventManagerBase.window**

Holds the instance of the [`WindowBase`](https://kivy.org/doc/stable/api-kivy.core.window.html#kivy.core.window.WindowBase).
New in version 2.1.0.

**kivy.eventmanager.MODE_DEFAULT_DISPATCH**

Assign this mode to make event dispatch through widget’s children list,
starting with the first widget in the list until event gets accepted or last
widget registered for that event is reached. Widgets after the last registered
widget are ignored.
New in version 2.1.0.

**kivy.eventmanager.MODE_DONT_DISPATCH**

Assign this mode to prevent event from dispatching to child widgets.
New in version 2.1.0.

**kivy.eventmanager.MODE_FILTERED_DISPATCH**

Assign this mode to make event dispatch only to child widgets which were
previously registered to receive events of the same
[`type_id`](https://kivy.org/doc/stable/api-kivy.input.motionevent.html#kivy.input.motionevent.MotionEvent.type_id) and not to all
child widgets.
New in version 2.1.0.

---

## API - [`kivy.factory`](https://kivy.org/doc/stable/api-kivy.factory.html)

**kivy.factory.Factory**

Factory instance to use for getting new classes

**kivy.factory.FactoryException**

Bases: `Exception`

---

## API - [`kivy.garden`](https://kivy.org/doc/stable/api-kivy.garden.html)

**kivy.garden.GardenImporter**

Bases: `importlib.abc.MetaPathFinder`

**kivy.garden.garden_system_dir**

system path where garden modules can be installed

---

## API - [`kivy.geometry`](https://kivy.org/doc/stable/api-kivy.geometry.html)

**kivy.geometry.circumcircle**

Computes the circumcircle of a triangle defined by a, b, c.
See: [http://en.wikipedia.org/wiki/Circumscribed_circle](http://en.wikipedia.org/wiki/Circumscribed_circle)

**kivy.geometry.minimum_bounding_circle**

Returns the minimum bounding circle for a set of points.
For a description of the problem being solved, see the [Smallest Circle
Problem](http://en.wikipedia.org/wiki/Smallest_circle_problem).
The function uses Applet’s Algorithm, the runtime is `O(h^3, *n)`,
where h is the number of points in the convex hull of the set of points.
**But** it runs in linear time in almost all real world cases.
See: [http://tinyurl.com/6e4n5yb](http://tinyurl.com/6e4n5yb)

---

## API - [`kivy.gesture`](https://kivy.org/doc/stable/api-kivy.gesture.html)

**kivy.gesture.Gesture**

Bases: `builtins.object`
A python implementation of a gesture recognition algorithm by
Oleg Dopertchouk: [http://www.gamedev.net/reference/articles/article2039.asp](http://www.gamedev.net/reference/articles/article2039.asp)
Implemented by Jeiel Aranal ([chemikhazi@gmail.com](mailto:chemikhazi%40gmail.com)),
released into the public domain.

**kivy.gesture.Gesture.add_stroke**

Adds a stroke to the gesture and returns the Stroke instance.
Optional point_list argument is a list of the mouse points for
the stroke.

**kivy.gesture.Gesture.dot_product**

Calculates the dot product of the gesture with another gesture.

**kivy.gesture.Gesture.get_rigid_rotation**

Extract the rotation to apply to a group of points to minimize the
distance to a second group of points. The two groups of points are
assumed to be centered. This is a simple version that just picks
an angle based on the first point of the gesture.

**kivy.gesture.Gesture.get_score**

Returns the matching score of the gesture against another gesture.

**kivy.gesture.Gesture.normalize**

Runs the gesture normalization algorithm and calculates the dot
product with self.

**kivy.gesture.GestureDatabase**

Bases: `builtins.object`
Class to handle a gesture database.

**kivy.gesture.GestureDatabase.add_gesture**

Add a new gesture to the database.

**kivy.gesture.GestureDatabase.find**

Find a matching gesture in the database.

**kivy.gesture.GestureDatabase.gesture_to_str**

Convert a gesture into a unique string.

**kivy.gesture.GestureDatabase.str_to_gesture**

Convert a unique string to a gesture.

**kivy.gesture.GestureStroke**

Bases: `builtins.object`
Gestures can be made up of multiple strokes.

**kivy.gesture.GestureStroke.add_point**

Adds a point to the stroke.

**kivy.gesture.GestureStroke.center_stroke**

Centers the stroke by offsetting the points.

**kivy.gesture.GestureStroke.normalize_stroke**

Normalizes strokes so that every stroke has a standard number of
points. Returns True if stroke is normalized, False if it can’t be
normalized. sample_points controls the resolution of the stroke.

**kivy.gesture.GestureStroke.points_distance**

Returns the distance between two GesturePoints.

**kivy.gesture.GestureStroke.scale_stroke**

Scales the stroke down by scale_factor.

**kivy.gesture.GestureStroke.stroke_length**

Finds the length of the stroke. If a point list is given,
finds the length of that list.

---

## API - [`kivy.graphics`](https://kivy.org/doc/stable/api-kivy.graphics.html)

**kivy.graphics.ApplyContextMatrix**

Bases: [`kivy.graphics.instructions.ContextInstruction`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.ContextInstruction)
target_stack by the matrix at the top of the ‘source_stack’
New in version 1.6.0.

**kivy.graphics.ApplyContextMatrix.source_stack**

Name of the matrix stack to use as a source.
Can be ‘modelview_mat’, ‘projection_mat’ or ‘frag_modelview_mat’.
New in version 1.6.0.

**kivy.graphics.ApplyContextMatrix.target_stack**

Name of the matrix stack to use as a target.
Can be ‘modelview_mat’, ‘projection_mat’ or ‘frag_modelview_mat’.
New in version 1.6.0.

**kivy.graphics.Bezier**

Bases: [`kivy.graphics.instructions.VertexInstruction`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.VertexInstruction)
New in version 1.0.8.

**kivy.graphics.Bezier.dash_length**

Property for getting/setting the length of the dashes in the curve.

**kivy.graphics.Bezier.dash_offset**

Property for getting/setting the offset between the dashes in the
curve.

**kivy.graphics.Bezier.points**

Property for getting/settings the points of the triangle.

**kivy.graphics.Bezier.segments**

Property for getting/setting the number of segments of the curve.

**kivy.graphics.BindTexture**

Bases: [`kivy.graphics.instructions.ContextInstruction`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.ContextInstruction)
The BindTexture Instruction will bind a texture and enable
GL_TEXTURE_2D for subsequent drawing.

**kivy.graphics.BindTexture.source**

Set/get the source (filename) to load for the texture.

**kivy.graphics.BorderImage**

Bases: [`kivy.graphics.vertex_instructions.Rectangle`](https://kivy.org/doc/stable/api-kivy.graphics.vertex_instructions.html#kivy.graphics.vertex_instructions.Rectangle)
concept of a CSS3 border-image.

**kivy.graphics.BorderImage.auto_scale**

Property for setting if the corners are automatically scaled
when the BorderImage is too small.

**kivy.graphics.BorderImage.border**

Property for getting/setting the border of the class.

**kivy.graphics.BorderImage.display_border**

Property for getting/setting the border display size.

**kivy.graphics.BoxShadow**

Bases: [`kivy.graphics.instructions.InstructionGroup`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.InstructionGroup)
New in version 2.2.0.
Changed in version 2.3.0:Fixed [`Canvas`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.Canvas) management using
[`add()`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.Canvas.add),
`insert()` and
[`remove()`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.Canvas.remove).
Previously, using them to manage the [`Canvas`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.Canvas) had no effect.
The base class also changed from [`Fbo`](https://kivy.org/doc/stable/api-kivy.graphics.fbo.html#kivy.graphics.fbo.Fbo)
to [`InstructionGroup`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.InstructionGroup).

**kivy.graphics.BoxShadow.blur_radius**

Define the shadow blur radius. Controls shadow expansion and softness.
Defaults to `15.0`.
In the images below, the start and end positions of the shadow blur
effect length are indicated.
The transition between color and transparency is seamless, and although
the shadow appears to end before before the dotted rectangle, its end
is made to be as smooth as possible.

**kivy.graphics.BoxShadow.border_radius**

Specifies the radii used for the rounded corners clockwise:
top-left, top-right, bottom-right, bottom-left.
Defaults to `(0.0, 0.0, 0.0, 0.0)`.

**kivy.graphics.BoxShadow.inset**

Defines whether the shadow is drawn from the inside out or from the outline to the inside of the `BoxShadow` instruction.
Defaults to `False`.

**Modes:**
`False` (default) - The shadow is drawn inside out the `BoxShadow` instruction, creating a raised effect.
`True` - The shadow is drawn from the outline to the inside of the `BoxShadow` instruction, creating a inset effect.

**kivy.graphics.BoxShadow.offset**

Specifies shadow offsets in [horizontal, vertical] format. 
Positive values for the offset indicate that the shadow should move to
the right and/or top.
The negative ones indicate that the shadow should move to the left
and/or down.
Defaults to `(0.0, 0.0)`.
For this property to work as expected, it is indicated that the value
of [`pos`](https://kivy.org/doc/stable/#kivy.graphics.BoxShadow.pos) coincides with the position of the target element of the
shadow, as in the example below:

**kivy.graphics.BoxShadow.pos**

Define the raw position of the shadow, that is, you should not take
into account changes in the value of the [`offset`](https://kivy.org/doc/stable/#kivy.graphics.BoxShadow.offset) property when
setting this property.

Defaults to `(0.0, 0.0)`.

**kivy.graphics.BoxShadow.size**

Define the raw size of the shadow, that is, you should not take into
account changes in the value of [`blur_radius`](https://kivy.org/doc/stable/#kivy.graphics.BoxShadow.blur_radius) and [`spread_radius`](https://kivy.org/doc/stable/#kivy.graphics.BoxShadow.spread_radius) properties.

Defaults to `(100.0, 100.0)`.

**kivy.graphics.BoxShadow.spread_radius**

Define the shrink/expansion of the shadow in [horizontal, vertical] format.
Defaults to `(0.0, 0.0)`.
This property is especially useful for cases where you want to achieve
a softer shadow around the element, by setting negative values for
[`spread_radius`](https://kivy.org/doc/stable/#kivy.graphics.BoxShadow.spread_radius) and a larger value for [`blur_radius`](https://kivy.org/doc/stable/#kivy.graphics.BoxShadow.blur_radius) as
in the [example](https://kivy.org/doc/stable/api-kivy.graphics.boxshadow.html#example).

**kivy.graphics.Callback**

Bases: [`kivy.graphics.instructions.Instruction`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.Instruction)
A Callback is an instruction that will be called when the drawing
operation is performed. When adding instructions to a canvas, you can do
this:

The definition of the callback must be:

The updating of your canvas does not occur until something new happens.
From your callback, you can ask for an update:

If you use the Callback class to call rendering methods of another
toolkit, you will have issues with the OpenGL context. The OpenGL state may
have been manipulated by the other toolkit, and as soon as program flow
returns to Kivy, it will just break. You can have glitches, crashes, black
holes might occur, etc.
To avoid that, you can activate the [`reset_context`](https://kivy.org/doc/stable/#kivy.graphics.Callback.reset_context) option. It will
reset the OpenGL context state to make Kivy’s rendering correct after the
call to your callback.

**kivy.graphics.Callback.ask_update**

Inform the parent canvas that we’d like it to update on the next
frame. This is useful when you need to trigger a redraw due to some
value having changed for example.
New in version 1.0.4.

**kivy.graphics.Callback.callback**

Property for getting/setting func.

**kivy.graphics.Callback.reset_context**

Set this to True if you want to reset the OpenGL context for Kivy
after the callback has been called.

**kivy.graphics.Canvas**

Bases: [`kivy.graphics.instructions.CanvasBase`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.CanvasBase)
instructions that you want to be used for drawing.

Usage of a canvas without the `with` statement:

Usage of a canvas with Python’s `with` statement:

**kivy.graphics.Canvas.add**

Append an [`Instruction`](https://kivy.org/doc/stable/#kivy.graphics.Instruction) to our list. If the canvas contains
an after group, then this instruction is inserted just before the
after group, which remains last. This is different from how
`insert()` works, which can insert anywhere.

**kivy.graphics.Canvas.after**

Property for getting the ‘after’ group.

**kivy.graphics.Canvas.ask_update**

Inform the canvas that we’d like it to update on the next frame.
This is useful when you need to trigger a redraw due to some value
having changed for example.

**kivy.graphics.Canvas.before**

Property for getting the ‘before’ group.

**kivy.graphics.Canvas.clear**

Clears every [`Instruction`](https://kivy.org/doc/stable/#kivy.graphics.Instruction) in the canvas, leaving it clean.

**kivy.graphics.Canvas.draw**

Apply the instruction to our window.

**kivy.graphics.Canvas.has_after**

Property to see if the [`after`](https://kivy.org/doc/stable/#kivy.graphics.Canvas.after) group has already been created.
New in version 1.7.0.

**kivy.graphics.Canvas.has_before**

Property to see if the [`before`](https://kivy.org/doc/stable/#kivy.graphics.Canvas.before) group has already been created.
New in version 1.7.0.

**kivy.graphics.Canvas.opacity**

Property to get/set the opacity value of the canvas.
New in version 1.4.1.
The opacity attribute controls the opacity of the canvas and its
children. Be careful, it’s a cumulative attribute: the value is
multiplied to the current global opacity and the result is applied to
the current context color.
For example: if your parent has an opacity of 0.5 and a child has an
opacity of 0.2, the real opacity of the child will be 0.5 * 0.2 = 0.1.
Then, the opacity is applied on the shader as:

**kivy.graphics.Canvas.remove**

**kivy.graphics.CanvasBase**

Bases: [`kivy.graphics.instructions.InstructionGroup`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.InstructionGroup)
CanvasBase provides the context manager methods for the
[`Canvas`](https://kivy.org/doc/stable/#kivy.graphics.Canvas).

**kivy.graphics.ChangeState**

Bases: [`kivy.graphics.instructions.ContextInstruction`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.ContextInstruction)
current render context.
New in version 1.6.0.

**kivy.graphics.ClearBuffers**

Bases: [`kivy.graphics.instructions.Instruction`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.Instruction)
New in version 1.3.0.
Clear the buffers specified by the instructions buffer mask property.
By default, only the coloc buffer is cleared.

**kivy.graphics.ClearBuffers.clear_color**

If True, the color buffer will be cleared.

**kivy.graphics.ClearBuffers.clear_depth**

If True, the depth buffer will be cleared.

**kivy.graphics.ClearBuffers.clear_stencil**

If True, the stencil buffer will be cleared.

**kivy.graphics.ClearColor**

Bases: [`kivy.graphics.instructions.Instruction`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.Instruction)
New in version 1.3.0.
Sets the clear color used to clear buffers with the glClear function or
[`ClearBuffers`](https://kivy.org/doc/stable/#kivy.graphics.ClearBuffers) graphics instructions.

**kivy.graphics.ClearColor.a**

Alpha component, between 0 and 1.

**kivy.graphics.ClearColor.b**

Blue component, between 0 and 1.

**kivy.graphics.ClearColor.g**

Green component, between 0 and 1.

**kivy.graphics.ClearColor.r**

Red component, between 0 and 1.

**kivy.graphics.ClearColor.rgb**

RGB color, a list of 3 values in 0-1 range where alpha will be 1.

**kivy.graphics.ClearColor.rgba**

RGBA color used for the clear color, a list of 4 values in the 0-1
range.

**kivy.graphics.Color**

Bases: [`kivy.graphics.instructions.ContextInstruction`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.ContextInstruction)
drawn after it.
This represents a color between 0 and 1, but is applied as a
*multiplier* to the texture of any vertex instructions following
it in a canvas. If no texture is set, the vertex instruction
takes the precise color of the Color instruction.
For instance, if a Rectangle has a texture with uniform color
`(0.5, 0.5, 0.5, 1.0)` and the preceding Color has
`rgba=(1, 0.5, 2, 1)`, the actual visible color will be
`(0.5, 0.25, 1.0, 1.0)` since the Color instruction is applied as
a multiplier to every rgba component. In this case, a Color
component outside the 0-1 range gives a visible result as the
intensity of the blue component is doubled.
To declare a Color in Python, you can do:

You can also set color components that are available as properties
by passing them as keyword arguments:

In kv lang you can set the color properties directly:

**kivy.graphics.Color.a**

Alpha component, between 0 and 1.

**kivy.graphics.Color.b**

Blue component, between 0 and 1.

**kivy.graphics.Color.g**

Green component, between 0 and 1.

**kivy.graphics.Color.h**

Hue component, between 0 and 1.

**kivy.graphics.Color.hsv**

HSV color, list of 3 values in 0-1 range, alpha will be 1.

**kivy.graphics.Color.r**

Red component, between 0 and 1.

**kivy.graphics.Color.rgb**

RGB color, list of 3 values in 0-1 range. The alpha will be 1.

**kivy.graphics.Color.rgba**

RGBA color, list of 4 values in 0-1 range.

**kivy.graphics.Color.s**

Saturation component, between 0 and 1.

**kivy.graphics.Color.v**

Value component, between 0 and 1.

**kivy.graphics.ContextInstruction**

Bases: [`kivy.graphics.instructions.Instruction`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.Instruction)
that don’t have a direct visual representation, but instead modify the
current Canvas’ state, e.g. texture binding, setting color parameters,
matrix manipulation and so on.

**kivy.graphics.Ellipse**

Bases: [`kivy.graphics.vertex_instructions.Rectangle`](https://kivy.org/doc/stable/api-kivy.graphics.vertex_instructions.html#kivy.graphics.vertex_instructions.Rectangle)

Changed in version 1.0.7:Added angle_start and angle_end.
Changed in version 2.2.0:The default number of segments is no longer 180, it is now calculated
according to the angle range, as this is a more efficient approach.

**kivy.graphics.Ellipse.angle_end**

End angle of the ellipse in degrees, defaults to 360.

**kivy.graphics.Ellipse.angle_start**

Start angle of the ellipse in degrees, defaults to 0.

**kivy.graphics.Ellipse.segments**

Property for getting/setting the number of segments of the ellipse.
The ellipse drawing will be smoother if you have many segments, however
you can also use this property to create polygons with 3 or more sides.
Values smaller than 3 will not be represented and the number of
segments will be automatically calculated.
Changed in version 2.2.0:The minimum number of segments allowed is 3. Smaller values will be
ignored and the number of segments will be automatically calculated.

**kivy.graphics.Fbo**

Bases: [`kivy.graphics.instructions.RenderContext`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.RenderContext)
“with” statement.

**kivy.graphics.Fbo.add_reload_observer**

Add a callback to be called after the whole graphics context has
been reloaded. This is where you can reupload your custom data in GPU.
New in version 1.2.0.

**kivy.graphics.Fbo.bind**

Bind the FBO to the current opengl context.
Bind mean that you enable the Framebuffer, and all the drawing
operations will act inside the Framebuffer, until [`release()`](https://kivy.org/doc/stable/#kivy.graphics.Fbo.release) is
called.
The bind/release operations are automatically called when you add
graphics objects into it. If you want to manipulate a Framebuffer
yourself, you can use it like this:

**kivy.graphics.Fbo.clear_buffer**

Clear the framebuffer with the [`clear_color`](https://kivy.org/doc/stable/#kivy.graphics.Fbo.clear_color).
You need to bind the framebuffer yourself before calling this
method:

**kivy.graphics.Fbo.clear_color**

Clear color in (red, green, blue, alpha) format.

**kivy.graphics.Fbo.get_pixel_color**

Get the color of the pixel with specified window
coordinates wx, wy. It returns result in RGBA format.
New in version 1.8.0.

**kivy.graphics.Fbo.pixels**

Get the pixels texture, in RGBA format only, unsigned byte. The
origin of the image is at bottom left.
New in version 1.7.0.

**kivy.graphics.Fbo.release**

Release the Framebuffer (unbind).

**kivy.graphics.Fbo.remove_reload_observer**

Remove a callback from the observer list, previously added by
[`add_reload_observer()`](https://kivy.org/doc/stable/#kivy.graphics.Fbo.add_reload_observer).
New in version 1.2.0.

**kivy.graphics.Fbo.size**

Size of the framebuffer, in (width, height) format.
If you change the size, the framebuffer content will be lost.

**kivy.graphics.Fbo.texture**

Return the framebuffer texture

**kivy.graphics.GraphicException**

Bases: `Exception`
Exception raised when a graphics error is fired.

**kivy.graphics.Instruction**

Bases: [`kivy.event.ObjectWithUid`](https://kivy.org/doc/stable/api-kivy.event.html#kivy.event.ObjectWithUid)
usage only, don’t use it directly.

**kivy.graphics.Instruction.flag_data_update**

**kivy.graphics.Instruction.flag_update**

**kivy.graphics.Instruction.group**

group: unicode

**kivy.graphics.Instruction.proxy_ref**

Return a proxy reference to the Instruction i.e. without creating a
reference of the widget. See [weakref.proxy](http://docs.python.org/2/library/weakref.html?highlight=proxy#weakref.proxy)
for more information.
New in version 1.7.2.

**kivy.graphics.InstructionGroup**

Bases: [`kivy.graphics.instructions.Instruction`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.Instruction)
of graphics instructions. It can be used directly as follows:
blue = InstructionGroup()
blue.add(Color(0, 0, 1, 0.2))
blue.add(Rectangle(pos=self.pos, size=(100, 100)))
green = InstructionGroup()
green.add(Color(0, 1, 0, 0.4))
green.add(Rectangle(pos=(100, 100), size=(100, 100)))
# Here, self should be a Widget or subclass
[self.canvas.add(group) for group in [blue, green]]

**kivy.graphics.InstructionGroup.add**

Add a new [`Instruction`](https://kivy.org/doc/stable/#kivy.graphics.Instruction) to our list.

**kivy.graphics.InstructionGroup.children**

children: list

**kivy.graphics.InstructionGroup.clear**

Remove all the [`Instructions`](https://kivy.org/doc/stable/#kivy.graphics.Instruction).

**kivy.graphics.InstructionGroup.get_group**

Return an iterable for all the [`Instructions`](https://kivy.org/doc/stable/#kivy.graphics.Instruction)
with a specific group name.

**kivy.graphics.InstructionGroup.indexof**

**kivy.graphics.InstructionGroup.insert**

Insert a new [`Instruction`](https://kivy.org/doc/stable/#kivy.graphics.Instruction) into our list at index.

**kivy.graphics.InstructionGroup.length**

**kivy.graphics.InstructionGroup.remove**

Remove an existing [`Instruction`](https://kivy.org/doc/stable/#kivy.graphics.Instruction) from our list.

**kivy.graphics.InstructionGroup.remove_group**

Remove all [`Instructions`](https://kivy.org/doc/stable/#kivy.graphics.Instruction) with a specific group
name.

**kivy.graphics.Line**

Bases: [`kivy.graphics.instructions.VertexInstruction`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.VertexInstruction)
Drawing a line can be done easily:

The line has 3 internal drawing modes that you should be aware of
for optimal results:
If the [`width`](https://kivy.org/doc/stable/#kivy.graphics.Line.width) is 1.0 and [`force_custom_drawing_method`](https://kivy.org/doc/stable/#kivy.graphics.Line.force_custom_drawing_method) is False, then the
standard GL_LINE drawing from OpenGL will be used. [`dash_length`](https://kivy.org/doc/stable/#kivy.graphics.Line.dash_length),
[`dash_offset`](https://kivy.org/doc/stable/#kivy.graphics.Line.dash_offset), and [`dashes`](https://kivy.org/doc/stable/#kivy.graphics.Line.dashes) will work, while properties for
cap and joint have no meaning here.
If the [`width`](https://kivy.org/doc/stable/#kivy.graphics.Line.width) is greater than 1.0 or [`force_custom_drawing_method`](https://kivy.org/doc/stable/#kivy.graphics.Line.force_custom_drawing_method)
is True, then a custom drawing method, based on triangulation,
will be used. [`dash_length`](https://kivy.org/doc/stable/#kivy.graphics.Line.dash_length), [`dash_offset`](https://kivy.org/doc/stable/#kivy.graphics.Line.dash_offset),
and [`dashes`](https://kivy.org/doc/stable/#kivy.graphics.Line.dashes) do not work in this mode.
Additionally, if the current color has an alpha less than 1.0, a
stencil will be used internally to draw the line.

Changed in version 1.0.8:dash_offset and dash_length have been added.
Changed in version 1.4.1:width, cap, joint, cap_precision, joint_precision, close,
ellipse, rectangle have been added.
Changed in version 1.4.1:bezier, bezier_precision have been added.
Changed in version 1.11.0:dashes have been added
Changed in version 2.3.0:force_custom_drawing_method has been added

**kivy.graphics.Line.bezier**

Use this property to build a bezier line, without calculating the
[`points`](https://kivy.org/doc/stable/#kivy.graphics.Line.points). You can only set this property, not get it.
The argument must be a tuple of 2n elements, n being the number of points.
Usage:

New in version 1.4.2.

**kivy.graphics.Line.bezier_precision**

Number of iteration for drawing the bezier between 2 segments,
defaults to 180. The bezier_precision must be at least 1.
New in version 1.4.2.

**kivy.graphics.Line.cap**

Determine the cap of the line, defaults to ‘round’. Can be one of
‘none’, ‘square’ or ‘round’
New in version 1.4.1.

**kivy.graphics.Line.cap_precision**

Number of iteration for drawing the “round” cap, defaults to 10.
The cap_precision must be at least 1.
New in version 1.4.1.

**kivy.graphics.Line.circle**

Use this property to build a circle, without calculating the
[`points`](https://kivy.org/doc/stable/#kivy.graphics.Line.points).
The argument must be a tuple of (center_x, center_y, radius, angle_start,
angle_end, segments):
center_x and center_y represent the center of the circle
radius represent the radius of the circle
(optional) angle_start and angle_end are in degree. The default
value is 0 and 360.
(optional) segments is the precision of the ellipse. The default
value is calculated from the range between angle.
Note that it’s up to you to [`close`](https://kivy.org/doc/stable/#kivy.graphics.Line.close) the circle or not.
For example, for building a simple ellipse, in python:

New in version 1.4.1.
Changed in version 2.2.0:Now you can get the circle generated through the property.

**kivy.graphics.Line.close**

If True, the line will be closed by joining the two ends, according to [`close_mode`](https://kivy.org/doc/stable/#kivy.graphics.Line.close_mode).
New in version 1.4.1.

**kivy.graphics.Line.close_mode**

Defines how the ends of the line will be connected.
Defaults to `"straight-line"`.

Available modes:
`"straight-line"` (all drawing shapes): the ends will be closed by a straight line.
`"center-connected"` ([`ellipse`](https://kivy.org/doc/stable/#kivy.graphics.Line.ellipse) specific): the ends will be closed by a line passing through the center of the ellipse.
New in version 2.2.0.

**kivy.graphics.Line.dash_length**

Property for getting/setting the length of the dashes in the curve
New in version 1.0.8.

**kivy.graphics.Line.dash_offset**

Property for getting/setting the offset between the dashes in the curve
New in version 1.0.8.

**kivy.graphics.Line.dashes**

Property for getting/setting `dashes`.
List of [ON length, offset, ON length, offset, …]. E.g. `[2,4,1,6,8,2]`
would create a line with the first dash length 2 then an offset of 4 then
a dash length of 1 then an offset of 6 and so on.
New in version 1.11.0.

**kivy.graphics.Line.ellipse**

Use this property to build an ellipse, without calculating the
[`points`](https://kivy.org/doc/stable/#kivy.graphics.Line.points).
The argument must be a tuple of (x, y, width, height, angle_start,
angle_end, segments):
x and y represent the bottom left of the ellipse
width and height represent the size of the ellipse
(optional) angle_start and angle_end are in degree. The default
value is 0 and 360.
(optional) segments is the precision of the ellipse. The default
value is calculated from the range between angle. You can use this
property to create polygons with 3 or more sides. Values smaller than
3 will not be represented and the number of segments will be
automatically calculated.
Note that it’s up to you to [`close`](https://kivy.org/doc/stable/#kivy.graphics.Line.close) or not.
If you choose to close, use [`close_mode`](https://kivy.org/doc/stable/#kivy.graphics.Line.close_mode) to define how the figure
will be closed. Whether it will be by closed by a `"straight-line"`
or by `"center-connected"`.
For example, for building a simple ellipse, in python:

New in version 1.4.1.
Changed in version 2.2.0:Now you can get the ellipse generated through the property.
The minimum number of segments allowed is 3. Smaller values will be
ignored and the number of segments will be automatically calculated.

**kivy.graphics.Line.force_custom_drawing_method**

If True, the line will be drawn using the custom drawing method, no matter what the width is.
New in version 2.3.0.

**kivy.graphics.Line.joint**

Determine the join of the line, defaults to ‘round’. Can be one of
‘none’, ‘round’, ‘bevel’, ‘miter’.
New in version 1.4.1.

**kivy.graphics.Line.joint_precision**

Number of iteration for drawing the “round” joint, defaults to 10.
The joint_precision must be at least 1.
New in version 1.4.1.

**kivy.graphics.Line.points**

Property for getting/settings points of the line

**kivy.graphics.Line.rectangle**

Use this property to build a rectangle, without calculating the
[`points`](https://kivy.org/doc/stable/#kivy.graphics.Line.points).
The argument must be a tuple of (x, y, width, height):
x and y represent the bottom-left position of the rectangle
width and height represent the size
The line is automatically closed.
Usage:

New in version 1.4.1.
Changed in version 2.2.0:Now you can get the rectangle generated through the property.

**kivy.graphics.Line.rounded_rectangle**

Use this property to build a rectangle, without calculating the
[`points`](https://kivy.org/doc/stable/#kivy.graphics.Line.points).
The argument must be a tuple of one of the following forms:
(x, y, width, height, corner_radius)
(x, y, width, height, corner_radius, resolution)
(x, y, width, height, corner_radius1, corner_radius2, corner_radius3, corner_radius4)
(x, y, width, height, corner_radius1, corner_radius2, corner_radius3, corner_radius4, resolution)
x and y represent the bottom-left position of the rectangle.
width and height represent the size.
corner_radius specifies the radius used for the rounded corners clockwise: top-left, top-right, bottom-right, bottom-left.
resolution is the number of line segment that will be used to draw the circle arc at each corner (defaults to 45).
The line is automatically closed.
Usage:

New in version 1.9.0.
Changed in version 2.2.0:Default value of resolution changed from 30 to 45.
Now you can get the rounded rectangle generated through the property.
The order of corner_radius has been changed to match the RoundedRectangle radius property (clockwise).
It was bottom-left, bottom-right, top-right, top-left in previous versions.
Now both are clockwise: top-left, top-right, bottom-right, bottom-left.
To keep the corner radius order without changing the order manually, you can use python’s built-in method reversed or [::-1],
to reverse the order of the corner radius.

**kivy.graphics.Line.width**

Determine the width of the line, defaults to 1.0.
New in version 1.4.1.

**kivy.graphics.LoadIdentity**

Bases: [`kivy.graphics.instructions.ContextInstruction`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.ContextInstruction)
the instructions stack property (default=’modelview_mat’)
New in version 1.6.0.

**kivy.graphics.LoadIdentity.stack**

Name of the matrix stack to use. Can be ‘modelview_mat’,
‘projection_mat’ or ‘frag_modelview_mat’.

**kivy.graphics.MatrixInstruction**

Bases: [`kivy.graphics.instructions.ContextInstruction`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.ContextInstruction)

**kivy.graphics.MatrixInstruction.matrix**

Matrix property. Matrix from the transformation module.
Setting the matrix using this property when a change is made
is important because it will notify the context about the update.

**kivy.graphics.MatrixInstruction.stack**

Name of the matrix stack to use. Can be ‘modelview_mat’,
‘projection_mat’ or ‘frag_modelview_mat’.
New in version 1.6.0.

**kivy.graphics.Mesh**

Bases: [`kivy.graphics.instructions.VertexInstruction`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.VertexInstruction)
In OpenGL ES 2.0 and in our graphics implementation, you cannot have more
than 65535 indices.
A list of vertices is described as:

If you want to draw a triangle, add 3 vertices. You can then make an
indices list as follows:
indices = [0, 1, 2]
New in version 1.1.0.

Changed in version 1.8.1:Before, vertices and indices would always be converted to a list,
now, they are only converted to a list if they do not implement the
buffer interface. So e.g. numpy arrays, python arrays etc. are used
in place, without creating any additional copies. However, the
buffers cannot be readonly (even though they are not changed, due to
a cython limitation) and must be contiguous in memory.

**kivy.graphics.Mesh.indices**

Vertex indices used to specify the order when drawing the
mesh.

**kivy.graphics.Mesh.mode**

VBO Mode used for drawing vertices/indices. Can be one of ‘points’,
‘line_strip’, ‘line_loop’, ‘lines’, ‘triangles’, ‘triangle_strip’ or
‘triangle_fan’.

**kivy.graphics.Mesh.vertices**

List of x, y, u, v coordinates used to construct the Mesh. Right now,
the Mesh instruction doesn’t allow you to change the format of the
vertices, which means it’s only x, y + one texture coordinate.

**kivy.graphics.Point**

Bases: [`kivy.graphics.instructions.VertexInstruction`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.VertexInstruction)
width/height of 2 times the [`pointsize`](https://kivy.org/doc/stable/#kivy.graphics.Point.pointsize).

**kivy.graphics.Point.add_point**

Add a point to the current [`points`](https://kivy.org/doc/stable/#kivy.graphics.Point.points) list.
If you intend to add multiple points, prefer to use this method instead
of reassigning a new [`points`](https://kivy.org/doc/stable/#kivy.graphics.Point.points) list. Assigning a new [`points`](https://kivy.org/doc/stable/#kivy.graphics.Point.points)
list will recalculate and reupload the whole buffer into the GPU.
If you use add_point, it will only upload the changes.

**kivy.graphics.Point.points**

Property for getting/settings the center points in the points list.
Each pair of coordinates specifies the center of a new point.

**kivy.graphics.Point.pointsize**

Property for getting/setting point size.
The size is measured from the center to the edge, so a value of 1.0
means the real size will be 2.0 x 2.0.

**kivy.graphics.PopMatrix**

Bases: [`kivy.graphics.instructions.ContextInstruction`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.ContextInstruction)

**kivy.graphics.PopMatrix.stack**

Name of the matrix stack to use. Can be ‘modelview_mat’,
‘projection_mat’ or ‘frag_modelview_mat’.
New in version 1.6.0.

**kivy.graphics.PopState**

Bases: [`kivy.graphics.instructions.ContextInstruction`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.ContextInstruction)
state stack.
New in version 1.6.0.

**kivy.graphics.PushMatrix**

Bases: [`kivy.graphics.instructions.ContextInstruction`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.ContextInstruction)

**kivy.graphics.PushMatrix.stack**

Name of the matrix stack to use. Can be ‘modelview_mat’,
‘projection_mat’ or ‘frag_modelview_mat’.
New in version 1.6.0.

**kivy.graphics.PushState**

Bases: [`kivy.graphics.instructions.ContextInstruction`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.ContextInstruction)
state stack.
New in version 1.6.0.

**kivy.graphics.Quad**

Bases: [`kivy.graphics.instructions.VertexInstruction`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.VertexInstruction)

**kivy.graphics.Quad.points**

Property for getting/settings points of the quad.

**kivy.graphics.Rectangle**

Bases: [`kivy.graphics.instructions.VertexInstruction`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.VertexInstruction)

**kivy.graphics.Rectangle.points**

Property for getting the points used to draw the vertices.
New in version 2.3.0.

**kivy.graphics.Rectangle.pos**

Property for getting/settings the position of the rectangle.

**kivy.graphics.Rectangle.size**

Property for getting/settings the size of the rectangle.

**kivy.graphics.RenderContext**

Bases: [`kivy.graphics.instructions.Canvas`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.Canvas)
The vertex shader
The fragment shader
The default texture
The state stack (color, texture, matrix…)

**kivy.graphics.RenderContext.shader**

Return the shader attached to the render context.

**kivy.graphics.RenderContext.use_parent_frag_modelview**

If True, the parent fragment modelview matrix will be used.
New in version 1.10.1:rc = RenderContext(use_parent_frag_modelview=True)

**kivy.graphics.RenderContext.use_parent_modelview**

If True, the parent modelview matrix will be used.
New in version 1.7.0.
Before:

Now:

**kivy.graphics.RenderContext.use_parent_projection**

If True, the parent projection matrix will be used.
New in version 1.7.0.
Before:

Now:

**kivy.graphics.Rotate**

Bases: `kivy.graphics.context_instructions.Transform`
on the modelview matrix. You can set the properties of the instructions
afterwards with e.g.

**kivy.graphics.Rotate.angle**

Property for getting/setting the angle of the rotation.

**kivy.graphics.Rotate.axis**

Property for getting/setting the axis of the rotation.
The format of the axis is (x, y, z).

**kivy.graphics.Rotate.origin**

Origin of the rotation.
New in version 1.7.0.
The format of the origin can be either (x, y) or (x, y, z).

**kivy.graphics.Rotate.set**

Set the angle and axis of rotation.

Deprecated since version 1.7.0:The set() method doesn’t use the new [`origin`](https://kivy.org/doc/stable/#kivy.graphics.Rotate.origin) property.

**kivy.graphics.Scale**

Bases: `kivy.graphics.context_instructions.Transform`
Create using three arguments:

Changed in version 2.3.0:Allowed kwargs to be used to supply x, y and z.
Removed depreciated Scale(s) in favour of Scale(x, y, z).

**kivy.graphics.Scale.origin**

Origin of the scale.
New in version 1.9.0.
The format of the origin can be either (x, y) or (x, y, z).

**kivy.graphics.Scale.x**

Property for getting/setting the scale on the X axis.
Changed in version 1.6.0.

**kivy.graphics.Scale.xyz**

3 tuple scale vector in 3D in x, y, and z axis.
Changed in version 1.6.0.

**kivy.graphics.Scale.y**

Property for getting/setting the scale on the Y axis.
Changed in version 1.6.0.

**kivy.graphics.Scale.z**

Property for getting/setting the scale on Z axis.
Changed in version 1.6.0.

**kivy.graphics.SmoothEllipse**

Bases: [`kivy.graphics.vertex_instructions.Ellipse`](https://kivy.org/doc/stable/api-kivy.graphics.vertex_instructions.html#kivy.graphics.vertex_instructions.Ellipse)
Its usage is the same as [`Ellipse`](https://kivy.org/doc/stable/api-kivy.graphics.vertex_instructions.html#kivy.graphics.vertex_instructions.Ellipse)

New in version 2.3.0.

**kivy.graphics.SmoothEllipse.default_texture**

default_texture: kivy.graphics.texture.Texture

**kivy.graphics.SmoothLine**

Bases: [`kivy.graphics.vertex_instructions.Line`](https://kivy.org/doc/stable/api-kivy.graphics.vertex_instructions.html#kivy.graphics.vertex_instructions.Line)
results. It has few drawbacks:
drawing a line with alpha will probably not have the intended result if
the line crosses itself.
[`cap`](https://kivy.org/doc/stable/#kivy.graphics.Line.cap), [`joint`](https://kivy.org/doc/stable/#kivy.graphics.Line.joint) and `dash` properties
are not supported.
it uses a custom texture with a premultiplied alpha.
lines under 1px in width are not supported: they will look the same.

New in version 1.9.0.

**kivy.graphics.SmoothLine.overdraw_width**

Determine the overdraw width of the line, defaults to 1.2.

**kivy.graphics.SmoothLine.premultiplied_texture**

**kivy.graphics.SmoothQuad**

Bases: [`kivy.graphics.vertex_instructions.Quad`](https://kivy.org/doc/stable/api-kivy.graphics.vertex_instructions.html#kivy.graphics.vertex_instructions.Quad)
Its usage is the same as [`Quad`](https://kivy.org/doc/stable/api-kivy.graphics.vertex_instructions.html#kivy.graphics.vertex_instructions.Quad)

New in version 2.3.0.

**kivy.graphics.SmoothQuad.default_texture**

default_texture: kivy.graphics.texture.Texture

**kivy.graphics.SmoothRectangle**

Bases: [`kivy.graphics.vertex_instructions.Rectangle`](https://kivy.org/doc/stable/api-kivy.graphics.vertex_instructions.html#kivy.graphics.vertex_instructions.Rectangle)
Its usage is the same as [`Rectangle`](https://kivy.org/doc/stable/api-kivy.graphics.vertex_instructions.html#kivy.graphics.vertex_instructions.Rectangle)

New in version 2.3.0.

**kivy.graphics.SmoothRectangle.default_texture**

default_texture: kivy.graphics.texture.Texture

**kivy.graphics.SmoothRoundedRectangle**

Bases: [`kivy.graphics.vertex_instructions.RoundedRectangle`](https://kivy.org/doc/stable/api-kivy.graphics.vertex_instructions.html#kivy.graphics.vertex_instructions.RoundedRectangle)
Its usage is the same as [`RoundedRectangle`](https://kivy.org/doc/stable/api-kivy.graphics.vertex_instructions.html#kivy.graphics.vertex_instructions.RoundedRectangle)

New in version 2.3.0.

**kivy.graphics.SmoothRoundedRectangle.default_texture**

default_texture: kivy.graphics.texture.Texture

**kivy.graphics.SmoothTriangle**

Bases: [`kivy.graphics.vertex_instructions.Triangle`](https://kivy.org/doc/stable/api-kivy.graphics.vertex_instructions.html#kivy.graphics.vertex_instructions.Triangle)
Its usage is the same as [`Triangle`](https://kivy.org/doc/stable/api-kivy.graphics.vertex_instructions.html#kivy.graphics.vertex_instructions.Triangle)

New in version 2.3.0.

**kivy.graphics.SmoothTriangle.default_texture**

default_texture: kivy.graphics.texture.Texture

**kivy.graphics.StencilPop**

Bases: [`kivy.graphics.instructions.Instruction`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.Instruction)
Pop the stencil stack. See the module documentation for more information.

**kivy.graphics.StencilPush**

Bases: [`kivy.graphics.instructions.Instruction`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.Instruction)
information.

**kivy.graphics.StencilPush.clear_stencil**

`clear_stencil` allow to disable stencil clearing in the `StencilPush`
phase. This option essentially disables the invocation of the functions
`cgl.glClearStencil(0)` and `cgl.glClear(GL_STENCIL_BUFFER_BIT).`
If `True`, the stencil will be cleaned in the `StencilPush` phase, if
`False`, it will not be cleaned.

New in version 2.3.0.

**kivy.graphics.StencilUnUse**

Bases: [`kivy.graphics.instructions.Instruction`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.Instruction)
Use current stencil buffer to unset the mask.

**kivy.graphics.StencilUse**

Bases: [`kivy.graphics.instructions.Instruction`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.Instruction)
more information.

**kivy.graphics.StencilUse.func_op**

Determine the stencil operation to use for glStencilFunc(). Can be
one of ‘never’, ‘less’, ‘equal’, ‘lequal’, ‘greater’, ‘notequal’,
‘gequal’ or ‘always’.
By default, the operator is set to ‘equal’.
New in version 1.5.0.

**kivy.graphics.Translate**

Bases: `kivy.graphics.context_instructions.Transform`
Construct by either:

Changed in version 2.3.0:Allowed kwargs to be used to supply x, y and z.

**kivy.graphics.Translate.x**

Property for getting/setting the translation on the X axis.

**kivy.graphics.Translate.xy**

2 tuple with translation vector in 2D for x and y axis.

**kivy.graphics.Translate.xyz**

3 tuple translation vector in 3D in x, y, and z axis.

**kivy.graphics.Translate.y**

Property for getting/setting the translation on the Y axis.

**kivy.graphics.Translate.z**

Property for getting/setting the translation on the Z axis.

**kivy.graphics.Triangle**

Bases: [`kivy.graphics.instructions.VertexInstruction`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.VertexInstruction)

**kivy.graphics.Triangle.points**

Property for getting/settings points of the triangle.

**kivy.graphics.UpdateNormalMatrix**

Bases: [`kivy.graphics.instructions.ContextInstruction`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.ContextInstruction)
Update the normal matrix ‘normal_mat’ based on the current
modelview matrix. This will compute ‘normal_mat’ uniform as:
inverse( transpose( mat3(mvm) ) )
New in version 1.6.0.

**kivy.graphics.VertexInstruction**

Bases: [`kivy.graphics.instructions.Instruction`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.Instruction)
that have a direct visual representation on the canvas, such as Rectangles,
Triangles, Lines, Ellipse and so on.

**kivy.graphics.VertexInstruction.source**

This property represents the filename to load the texture from.
If you want to use an image as source, do it like this:

Here’s the equivalent in Kivy language:

**kivy.graphics.VertexInstruction.tex_coords**

This property represents the texture coordinates used for drawing the
vertex instruction. The value must be a list of 8 values.
A texture coordinate has a position (u, v), and a size (w, h). The size
can be negative, and would represent the ‘flipped’ texture. By default,
the tex_coords are:

You can pass your own texture coordinates if you want to achieve fancy
effects.

**kivy.graphics.VertexInstruction.texture**

Property that represents the texture used for drawing this
Instruction. You can set a new texture like this:

Usually, you will use the [`source`](https://kivy.org/doc/stable/#kivy.graphics.VertexInstruction.source) attribute instead of the
texture.

**kivy.graphics.gl_init_resources**

---

## API - [`kivy.graphics.boxshadow`](https://kivy.org/doc/stable/api-kivy.graphics.boxshadow.html)

**kivy.graphics.boxshadow.BoxShadow**

Bases: [`kivy.graphics.instructions.InstructionGroup`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.InstructionGroup)
New in version 2.2.0.
Changed in version 2.3.0:Fixed [`Canvas`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.Canvas) management using
[`add()`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.Canvas.add),
`insert()` and
[`remove()`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.Canvas.remove).
Previously, using them to manage the [`Canvas`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.Canvas) had no effect.
The base class also changed from [`Fbo`](https://kivy.org/doc/stable/api-kivy.graphics.fbo.html#kivy.graphics.fbo.Fbo)
to [`InstructionGroup`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.InstructionGroup).

**kivy.graphics.boxshadow.BoxShadow.blur_radius**

Define the shadow blur radius. Controls shadow expansion and softness.
Defaults to `15.0`.
In the images below, the start and end positions of the shadow blur
effect length are indicated.
The transition between color and transparency is seamless, and although
the shadow appears to end before before the dotted rectangle, its end
is made to be as smooth as possible.

**kivy.graphics.boxshadow.BoxShadow.border_radius**

Specifies the radii used for the rounded corners clockwise:
top-left, top-right, bottom-right, bottom-left.
Defaults to `(0.0, 0.0, 0.0, 0.0)`.

**kivy.graphics.boxshadow.BoxShadow.inset**

Defines whether the shadow is drawn from the inside out or from the outline to the inside of the `BoxShadow` instruction.
Defaults to `False`.

**Modes:**
`False` (default) - The shadow is drawn inside out the `BoxShadow` instruction, creating a raised effect.
`True` - The shadow is drawn from the outline to the inside of the `BoxShadow` instruction, creating a inset effect.

**kivy.graphics.boxshadow.BoxShadow.offset**

Specifies shadow offsets in [horizontal, vertical] format. 
Positive values for the offset indicate that the shadow should move to
the right and/or top.
The negative ones indicate that the shadow should move to the left
and/or down.
Defaults to `(0.0, 0.0)`.
For this property to work as expected, it is indicated that the value
of [`pos`](https://kivy.org/doc/stable/#kivy.graphics.boxshadow.BoxShadow.pos) coincides with the position of the target element of the
shadow, as in the example below:

**kivy.graphics.boxshadow.BoxShadow.pos**

Define the raw position of the shadow, that is, you should not take
into account changes in the value of the [`offset`](https://kivy.org/doc/stable/#kivy.graphics.boxshadow.BoxShadow.offset) property when
setting this property.

Defaults to `(0.0, 0.0)`.

**kivy.graphics.boxshadow.BoxShadow.size**

Define the raw size of the shadow, that is, you should not take into
account changes in the value of [`blur_radius`](https://kivy.org/doc/stable/#kivy.graphics.boxshadow.BoxShadow.blur_radius) and [`spread_radius`](https://kivy.org/doc/stable/#kivy.graphics.boxshadow.BoxShadow.spread_radius) properties.

Defaults to `(100.0, 100.0)`.

**kivy.graphics.boxshadow.BoxShadow.spread_radius**

Define the shrink/expansion of the shadow in [horizontal, vertical] format.
Defaults to `(0.0, 0.0)`.
This property is especially useful for cases where you want to achieve
a softer shadow around the element, by setting negative values for
[`spread_radius`](https://kivy.org/doc/stable/#kivy.graphics.boxshadow.BoxShadow.spread_radius) and a larger value for [`blur_radius`](https://kivy.org/doc/stable/#kivy.graphics.boxshadow.BoxShadow.blur_radius) as
in the [example](https://kivy.org/doc/stable/#example).

---

## API - [`kivy.graphics.cgl`](https://kivy.org/doc/stable/api-kivy.graphics.cgl.html)

**kivy.graphics.cgl.cgl_get_backend_name**

**kivy.graphics.cgl.cgl_get_initialized_backend_name**

**kivy.graphics.cgl.cgl_init**

---

## API - [`kivy.graphics.context`](https://kivy.org/doc/stable/api-kivy.graphics.context.html)

**kivy.graphics.context.Context**

Bases: `builtins.object`
observer callbacks. See [`add_reload_observer()`](https://kivy.org/doc/stable/#kivy.graphics.context.Context.add_reload_observer) and [`remove_reload_observer()`](https://kivy.org/doc/stable/#kivy.graphics.context.Context.remove_reload_observer)
for more information.

**kivy.graphics.context.Context.add_reload_observer**

(internal) Add a callback to be called after the whole graphics context has
been reloaded. This is where you can reupload your custom data into the
GPU.

Changed in version 1.4.0:before parameter added.

**kivy.graphics.context.Context.flag_update_canvas**

**kivy.graphics.context.Context.flush**

**kivy.graphics.context.Context.gl_dealloc**

**kivy.graphics.context.Context.reload**

**kivy.graphics.context.Context.remove_reload_observer**

(internal) Remove a callback from the observer list previously added by
[`add_reload_observer()`](https://kivy.org/doc/stable/#kivy.graphics.context.Context.add_reload_observer).

**kivy.graphics.context.Context.trigger_gl_dealloc**

---

## API - [`kivy.graphics.context_instructions`](https://kivy.org/doc/stable/api-kivy.graphics.context_instructions.html)

**kivy.graphics.context_instructions.BindTexture**

Bases: [`kivy.graphics.instructions.ContextInstruction`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.ContextInstruction)
The BindTexture Instruction will bind a texture and enable
GL_TEXTURE_2D for subsequent drawing.

**kivy.graphics.context_instructions.BindTexture.source**

Set/get the source (filename) to load for the texture.

**kivy.graphics.context_instructions.Color**

Bases: [`kivy.graphics.instructions.ContextInstruction`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.ContextInstruction)
drawn after it.
This represents a color between 0 and 1, but is applied as a
*multiplier* to the texture of any vertex instructions following
it in a canvas. If no texture is set, the vertex instruction
takes the precise color of the Color instruction.
For instance, if a Rectangle has a texture with uniform color
`(0.5, 0.5, 0.5, 1.0)` and the preceding Color has
`rgba=(1, 0.5, 2, 1)`, the actual visible color will be
`(0.5, 0.25, 1.0, 1.0)` since the Color instruction is applied as
a multiplier to every rgba component. In this case, a Color
component outside the 0-1 range gives a visible result as the
intensity of the blue component is doubled.
To declare a Color in Python, you can do:

You can also set color components that are available as properties
by passing them as keyword arguments:

In kv lang you can set the color properties directly:

**kivy.graphics.context_instructions.Color.a**

Alpha component, between 0 and 1.

**kivy.graphics.context_instructions.Color.b**

Blue component, between 0 and 1.

**kivy.graphics.context_instructions.Color.g**

Green component, between 0 and 1.

**kivy.graphics.context_instructions.Color.h**

Hue component, between 0 and 1.

**kivy.graphics.context_instructions.Color.hsv**

HSV color, list of 3 values in 0-1 range, alpha will be 1.

**kivy.graphics.context_instructions.Color.r**

Red component, between 0 and 1.

**kivy.graphics.context_instructions.Color.rgb**

RGB color, list of 3 values in 0-1 range. The alpha will be 1.

**kivy.graphics.context_instructions.Color.rgba**

RGBA color, list of 4 values in 0-1 range.

**kivy.graphics.context_instructions.Color.s**

Saturation component, between 0 and 1.

**kivy.graphics.context_instructions.Color.v**

Value component, between 0 and 1.

**kivy.graphics.context_instructions.MatrixInstruction**

Bases: [`kivy.graphics.instructions.ContextInstruction`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.ContextInstruction)

**kivy.graphics.context_instructions.MatrixInstruction.matrix**

Matrix property. Matrix from the transformation module.
Setting the matrix using this property when a change is made
is important because it will notify the context about the update.

**kivy.graphics.context_instructions.MatrixInstruction.stack**

Name of the matrix stack to use. Can be ‘modelview_mat’,
‘projection_mat’ or ‘frag_modelview_mat’.
New in version 1.6.0.

**kivy.graphics.context_instructions.PopMatrix**

Bases: [`kivy.graphics.instructions.ContextInstruction`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.ContextInstruction)

**kivy.graphics.context_instructions.PopMatrix.stack**

Name of the matrix stack to use. Can be ‘modelview_mat’,
‘projection_mat’ or ‘frag_modelview_mat’.
New in version 1.6.0.

**kivy.graphics.context_instructions.PushMatrix**

Bases: [`kivy.graphics.instructions.ContextInstruction`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.ContextInstruction)

**kivy.graphics.context_instructions.PushMatrix.stack**

Name of the matrix stack to use. Can be ‘modelview_mat’,
‘projection_mat’ or ‘frag_modelview_mat’.
New in version 1.6.0.

**kivy.graphics.context_instructions.Rotate**

Bases: `kivy.graphics.context_instructions.Transform`
on the modelview matrix. You can set the properties of the instructions
afterwards with e.g.

**kivy.graphics.context_instructions.Rotate.angle**

Property for getting/setting the angle of the rotation.

**kivy.graphics.context_instructions.Rotate.axis**

Property for getting/setting the axis of the rotation.
The format of the axis is (x, y, z).

**kivy.graphics.context_instructions.Rotate.origin**

Origin of the rotation.
New in version 1.7.0.
The format of the origin can be either (x, y) or (x, y, z).

**kivy.graphics.context_instructions.Rotate.set**

Set the angle and axis of rotation.

Deprecated since version 1.7.0:The set() method doesn’t use the new [`origin`](https://kivy.org/doc/stable/#kivy.graphics.context_instructions.Rotate.origin) property.

**kivy.graphics.context_instructions.Scale**

Bases: `kivy.graphics.context_instructions.Transform`
Create using three arguments:

Changed in version 2.3.0:Allowed kwargs to be used to supply x, y and z.
Removed depreciated Scale(s) in favour of Scale(x, y, z).

**kivy.graphics.context_instructions.Scale.origin**

Origin of the scale.
New in version 1.9.0.
The format of the origin can be either (x, y) or (x, y, z).

**kivy.graphics.context_instructions.Scale.x**

Property for getting/setting the scale on the X axis.
Changed in version 1.6.0.

**kivy.graphics.context_instructions.Scale.xyz**

3 tuple scale vector in 3D in x, y, and z axis.
Changed in version 1.6.0.

**kivy.graphics.context_instructions.Scale.y**

Property for getting/setting the scale on the Y axis.
Changed in version 1.6.0.

**kivy.graphics.context_instructions.Scale.z**

Property for getting/setting the scale on Z axis.
Changed in version 1.6.0.

**kivy.graphics.context_instructions.Translate**

Bases: `kivy.graphics.context_instructions.Transform`
Construct by either:

Changed in version 2.3.0:Allowed kwargs to be used to supply x, y and z.

**kivy.graphics.context_instructions.Translate.x**

Property for getting/setting the translation on the X axis.

**kivy.graphics.context_instructions.Translate.xy**

2 tuple with translation vector in 2D for x and y axis.

**kivy.graphics.context_instructions.Translate.xyz**

3 tuple translation vector in 3D in x, y, and z axis.

**kivy.graphics.context_instructions.Translate.y**

Property for getting/setting the translation on the Y axis.

**kivy.graphics.context_instructions.Translate.z**

Property for getting/setting the translation on the Z axis.

**kivy.graphics.context_instructions.gl_init_resources**

---

## API - [`kivy.graphics.fbo`](https://kivy.org/doc/stable/api-kivy.graphics.fbo.html)

**kivy.graphics.fbo.Fbo**

Bases: [`kivy.graphics.instructions.RenderContext`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.RenderContext)
“with” statement.

**kivy.graphics.fbo.Fbo.add_reload_observer**

Add a callback to be called after the whole graphics context has
been reloaded. This is where you can reupload your custom data in GPU.
New in version 1.2.0.

**kivy.graphics.fbo.Fbo.bind**

Bind the FBO to the current opengl context.
Bind mean that you enable the Framebuffer, and all the drawing
operations will act inside the Framebuffer, until [`release()`](https://kivy.org/doc/stable/#kivy.graphics.fbo.Fbo.release) is
called.
The bind/release operations are automatically called when you add
graphics objects into it. If you want to manipulate a Framebuffer
yourself, you can use it like this:

**kivy.graphics.fbo.Fbo.clear_buffer**

Clear the framebuffer with the [`clear_color`](https://kivy.org/doc/stable/#kivy.graphics.fbo.Fbo.clear_color).
You need to bind the framebuffer yourself before calling this
method:

**kivy.graphics.fbo.Fbo.clear_color**

Clear color in (red, green, blue, alpha) format.

**kivy.graphics.fbo.Fbo.get_pixel_color**

Get the color of the pixel with specified window
coordinates wx, wy. It returns result in RGBA format.
New in version 1.8.0.

**kivy.graphics.fbo.Fbo.pixels**

Get the pixels texture, in RGBA format only, unsigned byte. The
origin of the image is at bottom left.
New in version 1.7.0.

**kivy.graphics.fbo.Fbo.release**

Release the Framebuffer (unbind).

**kivy.graphics.fbo.Fbo.remove_reload_observer**

Remove a callback from the observer list, previously added by
[`add_reload_observer()`](https://kivy.org/doc/stable/#kivy.graphics.fbo.Fbo.add_reload_observer).
New in version 1.2.0.

**kivy.graphics.fbo.Fbo.size**

Size of the framebuffer, in (width, height) format.
If you change the size, the framebuffer content will be lost.

**kivy.graphics.fbo.Fbo.texture**

Return the framebuffer texture

---

## API - [`kivy.graphics.gl_instructions`](https://kivy.org/doc/stable/api-kivy.graphics.gl_instructions.html)

**kivy.graphics.gl_instructions.ClearBuffers**

Bases: [`kivy.graphics.instructions.Instruction`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.Instruction)
New in version 1.3.0.
Clear the buffers specified by the instructions buffer mask property.
By default, only the coloc buffer is cleared.

**kivy.graphics.gl_instructions.ClearBuffers.clear_color**

If True, the color buffer will be cleared.

**kivy.graphics.gl_instructions.ClearBuffers.clear_depth**

If True, the depth buffer will be cleared.

**kivy.graphics.gl_instructions.ClearBuffers.clear_stencil**

If True, the stencil buffer will be cleared.

**kivy.graphics.gl_instructions.ClearColor**

Bases: [`kivy.graphics.instructions.Instruction`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.Instruction)
New in version 1.3.0.
Sets the clear color used to clear buffers with the glClear function or
[`ClearBuffers`](https://kivy.org/doc/stable/#kivy.graphics.gl_instructions.ClearBuffers) graphics instructions.

**kivy.graphics.gl_instructions.ClearColor.a**

Alpha component, between 0 and 1.

**kivy.graphics.gl_instructions.ClearColor.b**

Blue component, between 0 and 1.

**kivy.graphics.gl_instructions.ClearColor.g**

Green component, between 0 and 1.

**kivy.graphics.gl_instructions.ClearColor.r**

Red component, between 0 and 1.

**kivy.graphics.gl_instructions.ClearColor.rgb**

RGB color, a list of 3 values in 0-1 range where alpha will be 1.

**kivy.graphics.gl_instructions.ClearColor.rgba**

RGBA color used for the clear color, a list of 4 values in the 0-1
range.

---

## API - [`kivy.graphics.instructions`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html)

**kivy.graphics.instructions.Callback**

Bases: [`kivy.graphics.instructions.Instruction`](https://kivy.org/doc/stable/#kivy.graphics.instructions.Instruction)
A Callback is an instruction that will be called when the drawing
operation is performed. When adding instructions to a canvas, you can do
this:

The definition of the callback must be:

The updating of your canvas does not occur until something new happens.
From your callback, you can ask for an update:

If you use the Callback class to call rendering methods of another
toolkit, you will have issues with the OpenGL context. The OpenGL state may
have been manipulated by the other toolkit, and as soon as program flow
returns to Kivy, it will just break. You can have glitches, crashes, black
holes might occur, etc.
To avoid that, you can activate the [`reset_context`](https://kivy.org/doc/stable/#kivy.graphics.instructions.Callback.reset_context) option. It will
reset the OpenGL context state to make Kivy’s rendering correct after the
call to your callback.

**kivy.graphics.instructions.Callback.ask_update**

Inform the parent canvas that we’d like it to update on the next
frame. This is useful when you need to trigger a redraw due to some
value having changed for example.
New in version 1.0.4.

**kivy.graphics.instructions.Callback.callback**

Property for getting/setting func.

**kivy.graphics.instructions.Callback.reset_context**

Set this to True if you want to reset the OpenGL context for Kivy
after the callback has been called.

**kivy.graphics.instructions.Canvas**

Bases: [`kivy.graphics.instructions.CanvasBase`](https://kivy.org/doc/stable/#kivy.graphics.instructions.CanvasBase)
instructions that you want to be used for drawing.

Usage of a canvas without the `with` statement:

Usage of a canvas with Python’s `with` statement:

**kivy.graphics.instructions.Canvas.add**

Append an [`Instruction`](https://kivy.org/doc/stable/#kivy.graphics.instructions.Instruction) to our list. If the canvas contains
an after group, then this instruction is inserted just before the
after group, which remains last. This is different from how
`insert()` works, which can insert anywhere.

**kivy.graphics.instructions.Canvas.after**

Property for getting the ‘after’ group.

**kivy.graphics.instructions.Canvas.ask_update**

Inform the canvas that we’d like it to update on the next frame.
This is useful when you need to trigger a redraw due to some value
having changed for example.

**kivy.graphics.instructions.Canvas.before**

Property for getting the ‘before’ group.

**kivy.graphics.instructions.Canvas.clear**

Clears every [`Instruction`](https://kivy.org/doc/stable/#kivy.graphics.instructions.Instruction) in the canvas, leaving it clean.

**kivy.graphics.instructions.Canvas.draw**

Apply the instruction to our window.

**kivy.graphics.instructions.Canvas.has_after**

Property to see if the [`after`](https://kivy.org/doc/stable/#kivy.graphics.instructions.Canvas.after) group has already been created.
New in version 1.7.0.

**kivy.graphics.instructions.Canvas.has_before**

Property to see if the [`before`](https://kivy.org/doc/stable/#kivy.graphics.instructions.Canvas.before) group has already been created.
New in version 1.7.0.

**kivy.graphics.instructions.Canvas.opacity**

Property to get/set the opacity value of the canvas.
New in version 1.4.1.
The opacity attribute controls the opacity of the canvas and its
children. Be careful, it’s a cumulative attribute: the value is
multiplied to the current global opacity and the result is applied to
the current context color.
For example: if your parent has an opacity of 0.5 and a child has an
opacity of 0.2, the real opacity of the child will be 0.5 * 0.2 = 0.1.
Then, the opacity is applied on the shader as:

**kivy.graphics.instructions.Canvas.remove**

**kivy.graphics.instructions.CanvasBase**

Bases: [`kivy.graphics.instructions.InstructionGroup`](https://kivy.org/doc/stable/#kivy.graphics.instructions.InstructionGroup)
CanvasBase provides the context manager methods for the
[`Canvas`](https://kivy.org/doc/stable/#kivy.graphics.instructions.Canvas).

**kivy.graphics.instructions.ContextInstruction**

Bases: [`kivy.graphics.instructions.Instruction`](https://kivy.org/doc/stable/#kivy.graphics.instructions.Instruction)
that don’t have a direct visual representation, but instead modify the
current Canvas’ state, e.g. texture binding, setting color parameters,
matrix manipulation and so on.

**kivy.graphics.instructions.Instruction**

Bases: [`kivy.event.ObjectWithUid`](https://kivy.org/doc/stable/api-kivy.event.html#kivy.event.ObjectWithUid)
usage only, don’t use it directly.

**kivy.graphics.instructions.Instruction.flag_data_update**

**kivy.graphics.instructions.Instruction.flag_update**

**kivy.graphics.instructions.Instruction.group**

group: unicode

**kivy.graphics.instructions.Instruction.proxy_ref**

Return a proxy reference to the Instruction i.e. without creating a
reference of the widget. See [weakref.proxy](http://docs.python.org/2/library/weakref.html?highlight=proxy#weakref.proxy)
for more information.
New in version 1.7.2.

**kivy.graphics.instructions.InstructionGroup**

Bases: [`kivy.graphics.instructions.Instruction`](https://kivy.org/doc/stable/#kivy.graphics.instructions.Instruction)
of graphics instructions. It can be used directly as follows:
blue = InstructionGroup()
blue.add(Color(0, 0, 1, 0.2))
blue.add(Rectangle(pos=self.pos, size=(100, 100)))
green = InstructionGroup()
green.add(Color(0, 1, 0, 0.4))
green.add(Rectangle(pos=(100, 100), size=(100, 100)))
# Here, self should be a Widget or subclass
[self.canvas.add(group) for group in [blue, green]]

**kivy.graphics.instructions.InstructionGroup.add**

Add a new [`Instruction`](https://kivy.org/doc/stable/#kivy.graphics.instructions.Instruction) to our list.

**kivy.graphics.instructions.InstructionGroup.children**

children: list

**kivy.graphics.instructions.InstructionGroup.clear**

Remove all the [`Instructions`](https://kivy.org/doc/stable/#kivy.graphics.instructions.Instruction).

**kivy.graphics.instructions.InstructionGroup.get_group**

Return an iterable for all the [`Instructions`](https://kivy.org/doc/stable/#kivy.graphics.instructions.Instruction)
with a specific group name.

**kivy.graphics.instructions.InstructionGroup.indexof**

**kivy.graphics.instructions.InstructionGroup.insert**

Insert a new [`Instruction`](https://kivy.org/doc/stable/#kivy.graphics.instructions.Instruction) into our list at index.

**kivy.graphics.instructions.InstructionGroup.length**

**kivy.graphics.instructions.InstructionGroup.remove**

Remove an existing [`Instruction`](https://kivy.org/doc/stable/#kivy.graphics.instructions.Instruction) from our list.

**kivy.graphics.instructions.InstructionGroup.remove_group**

Remove all [`Instructions`](https://kivy.org/doc/stable/#kivy.graphics.instructions.Instruction) with a specific group
name.

**kivy.graphics.instructions.RenderContext**

Bases: [`kivy.graphics.instructions.Canvas`](https://kivy.org/doc/stable/#kivy.graphics.instructions.Canvas)
The vertex shader
The fragment shader
The default texture
The state stack (color, texture, matrix…)

**kivy.graphics.instructions.RenderContext.shader**

Return the shader attached to the render context.

**kivy.graphics.instructions.RenderContext.use_parent_frag_modelview**

If True, the parent fragment modelview matrix will be used.
New in version 1.10.1:rc = RenderContext(use_parent_frag_modelview=True)

**kivy.graphics.instructions.RenderContext.use_parent_modelview**

If True, the parent modelview matrix will be used.
New in version 1.7.0.
Before:

Now:

**kivy.graphics.instructions.RenderContext.use_parent_projection**

If True, the parent projection matrix will be used.
New in version 1.7.0.
Before:

Now:

**kivy.graphics.instructions.VertexInstruction**

Bases: [`kivy.graphics.instructions.Instruction`](https://kivy.org/doc/stable/#kivy.graphics.instructions.Instruction)
that have a direct visual representation on the canvas, such as Rectangles,
Triangles, Lines, Ellipse and so on.

**kivy.graphics.instructions.VertexInstruction.source**

This property represents the filename to load the texture from.
If you want to use an image as source, do it like this:

Here’s the equivalent in Kivy language:

**kivy.graphics.instructions.VertexInstruction.tex_coords**

This property represents the texture coordinates used for drawing the
vertex instruction. The value must be a list of 8 values.
A texture coordinate has a position (u, v), and a size (w, h). The size
can be negative, and would represent the ‘flipped’ texture. By default,
the tex_coords are:

You can pass your own texture coordinates if you want to achieve fancy
effects.

**kivy.graphics.instructions.VertexInstruction.texture**

Property that represents the texture used for drawing this
Instruction. You can set a new texture like this:

Usually, you will use the [`source`](https://kivy.org/doc/stable/#kivy.graphics.instructions.VertexInstruction.source) attribute instead of the
texture.

---

## API - [`kivy.graphics.opengl`](https://kivy.org/doc/stable/api-kivy.graphics.opengl.html)

**kivy.graphics.opengl.glActiveTexture**

See: [glActiveTexture() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glActiveTexture.xml)

**kivy.graphics.opengl.glAttachShader**

See: [glAttachShader() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glAttachShader.xml)

**kivy.graphics.opengl.glBindAttribLocation**

See: [glBindAttribLocation() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glBindAttribLocation.xml)

**kivy.graphics.opengl.glBindBuffer**

See: [glBindBuffer() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glBindBuffer.xml)

**kivy.graphics.opengl.glBindFramebuffer**

See: [glBindFramebuffer() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glBindFramebuffer.xml)

**kivy.graphics.opengl.glBindRenderbuffer**

See: [glBindRenderbuffer() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glBindRenderbuffer.xml)

**kivy.graphics.opengl.glBindTexture**

See: [glBindTexture() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glBindTexture.xml)

**kivy.graphics.opengl.glBlendColor**

See: [glBlendColor() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glBlendColor.xml)

**kivy.graphics.opengl.glBlendEquation**

See: [glBlendEquation() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glBlendEquation.xml)

**kivy.graphics.opengl.glBlendEquationSeparate**

See: [glBlendEquationSeparate() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glBlendEquationSeparate.xml)

**kivy.graphics.opengl.glBlendFunc**

See: [glBlendFunc() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glBlendFunc.xml)

**kivy.graphics.opengl.glBlendFuncSeparate**

See: [glBlendFuncSeparate() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glBlendFuncSeparate.xml)

**kivy.graphics.opengl.glBufferData**

See: [glBufferData() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glBufferData.xml)

**kivy.graphics.opengl.glBufferSubData**

See: [glBufferSubData() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glBufferSubData.xml)

**kivy.graphics.opengl.glCheckFramebufferStatus**

See: [glCheckFramebufferStatus() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glCheckFramebufferStatus.xml)

**kivy.graphics.opengl.glClear**

See: [glClear() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glClear.xml)

**kivy.graphics.opengl.glClearColor**

See: [glClearColor() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glClearColor.xml)

**kivy.graphics.opengl.glClearStencil**

See: [glClearStencil() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glClearStencil.xml)

**kivy.graphics.opengl.glColorMask**

See: [glColorMask() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glColorMask.xml)

**kivy.graphics.opengl.glCompileShader**

See: [glCompileShader() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glCompileShader.xml)

**kivy.graphics.opengl.glCompressedTexImage2D**

See: [glCompressedTexImage2D() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glCompressedTexImage2D.xml)

**kivy.graphics.opengl.glCompressedTexSubImage2D**

See: [glCompressedTexSubImage2D() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glCompressedTexSubImage2D.xml)

**kivy.graphics.opengl.glCopyTexImage2D**

See: [glCopyTexImage2D() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glCopyTexImage2D.xml)

**kivy.graphics.opengl.glCopyTexSubImage2D**

See: [glCopyTexSubImage2D() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glCopyTexSubImage2D.xml)

**kivy.graphics.opengl.glCreateProgram**

See: [glCreateProgram() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glCreateProgram.xml)

**kivy.graphics.opengl.glCreateShader**

See: [glCreateShader() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glCreateShader.xml)

**kivy.graphics.opengl.glCullFace**

See: [glCullFace() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glCullFace.xml)

**kivy.graphics.opengl.glDeleteBuffers**

See: [glDeleteBuffers() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glDeleteBuffers.xml)

**kivy.graphics.opengl.glDeleteFramebuffers**

See: [glDeleteFramebuffers() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glDeleteFramebuffers.xml)

**kivy.graphics.opengl.glDeleteProgram**

See: [glDeleteProgram() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glDeleteProgram.xml)

**kivy.graphics.opengl.glDeleteRenderbuffers**

See: [glDeleteRenderbuffers() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glDeleteRenderbuffers.xml)

**kivy.graphics.opengl.glDeleteShader**

See: [glDeleteShader() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glDeleteShader.xml)

**kivy.graphics.opengl.glDeleteTextures**

See: [glDeleteTextures() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glDeleteTextures.xml)

**kivy.graphics.opengl.glDepthFunc**

See: [glDepthFunc() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glDepthFunc.xml)

**kivy.graphics.opengl.glDepthMask**

See: [glDepthMask() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glDepthMask.xml)

**kivy.graphics.opengl.glDetachShader**

See: [glDetachShader() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glDetachShader.xml)

**kivy.graphics.opengl.glDisable**

See: [glDisable() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glDisable.xml)

**kivy.graphics.opengl.glDisableVertexAttribArray**

See: [glDisableVertexAttribArray() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glDisableVertexAttribArray.xml)

**kivy.graphics.opengl.glDrawArrays**

See: [glDrawArrays() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glDrawArrays.xml)

**kivy.graphics.opengl.glDrawElements**

See: [glDrawElements() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glDrawElements.xml)

**kivy.graphics.opengl.glEnable**

See: [glEnable() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glEnable.xml)

**kivy.graphics.opengl.glEnableVertexAttribArray**

See: [glEnableVertexAttribArray() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glEnableVertexAttribArray.xml)

**kivy.graphics.opengl.glFinish**

See: [glFinish() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glFinish.xml)

**kivy.graphics.opengl.glFlush**

See: [glFlush() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glFlush.xml)

**kivy.graphics.opengl.glFramebufferRenderbuffer**

See: [glFramebufferRenderbuffer() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glFramebufferRenderbuffer.xml)

**kivy.graphics.opengl.glFramebufferTexture2D**

See: [glFramebufferTexture2D() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glFramebufferTexture2D.xml)

**kivy.graphics.opengl.glFrontFace**

See: [glFrontFace() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glFrontFace.xml)

**kivy.graphics.opengl.glGenBuffers**

See: [glGenBuffers() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glGenBuffers.xml)
Unlike the C specification, the value will be the result of call.

**kivy.graphics.opengl.glGenFramebuffers**

See: [glGenFramebuffers() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glGenFramebuffers.xml)
Unlike the C specification, the value will be the result of call.

**kivy.graphics.opengl.glGenRenderbuffers**

See: [glGenRenderbuffers() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glGenRenderbuffers.xml)
Unlike the C specification, the value will be the result of call.

**kivy.graphics.opengl.glGenTextures**

See: [glGenTextures() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glGenTextures.xml)
Unlike the C specification, the value will be the result of call.

**kivy.graphics.opengl.glGenerateMipmap**

See: [glGenerateMipmap() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glGenerateMipmap.xml)

**kivy.graphics.opengl.glGetActiveAttrib**

See: [glGetActiveAttrib() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glGetActiveAttrib.xml)
Unlike the C specification, the value will be the result of call.

**kivy.graphics.opengl.glGetActiveUniform**

See: [glGetActiveUniform() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glGetActiveUniform.xml)
Unlike the C specification, the value will be the result of call.

**kivy.graphics.opengl.glGetAttachedShaders**

See: [glGetAttachedShaders() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glGetAttachedShaders.xml)
Unlike the C specification, the value will be the result of call.

**kivy.graphics.opengl.glGetAttribLocation**

See: [glGetAttribLocation() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glGetAttribLocation.xml)
Unlike the C specification, the value will be the result of call.

**kivy.graphics.opengl.glGetBooleanv**

See: [glGetBooleanv() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glGetBooleanv.xml)
Unlike the C specification, the value will be the result of call.

**kivy.graphics.opengl.glGetBufferParameteriv**

See: [glGetBufferParameteriv() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glGetBufferParameteriv.xml)
Unlike the C specification, the value will be the result of call.

**kivy.graphics.opengl.glGetError**

See: [glGetError() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glGetError.xml)
Unlike the C specification, the value will be the result of call.

**kivy.graphics.opengl.glGetFloatv**

See: [glGetFloatv() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glGetFloatv.xml)
Unlike the C specification, the value will be the result of call.

**kivy.graphics.opengl.glGetFramebufferAttachmentParameteriv**

See: [glGetFramebufferAttachmentParameteriv() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glGetFramebufferAttachmentParameteriv.xml)
Unlike the C specification, the value will be the result of call.

**kivy.graphics.opengl.glGetIntegerv**

See: [glGetIntegerv() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glGetIntegerv.xml)
Unlike the C specification, the value(s) will be the result of the call

**kivy.graphics.opengl.glGetProgramInfoLog**

See: [glGetProgramInfoLog() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glGetProgramInfoLog.xml)
Unlike the C specification, the source code will be returned as a string.

**kivy.graphics.opengl.glGetProgramiv**

See: [glGetProgramiv() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glGetProgramiv.xml)
Unlike the C specification, the value(s) will be the result of the call

**kivy.graphics.opengl.glGetRenderbufferParameteriv**

See: [glGetRenderbufferParameteriv() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glGetRenderbufferParameteriv.xml)
Unlike the C specification, the value will be the result of call.

**kivy.graphics.opengl.glGetShaderInfoLog**

See: [glGetShaderInfoLog() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glGetShaderInfoLog.xml)
Unlike the C specification, the source code will be returned as a string.

**kivy.graphics.opengl.glGetShaderPrecisionFormat**

See: [glGetShaderPrecisionFormat() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glGetShaderPrecisionFormat.xml)

**kivy.graphics.opengl.glGetShaderSource**

See: [glGetShaderSource() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glGetShaderSource.xml)
Unlike the C specification, the source code will be returned as a string.

**kivy.graphics.opengl.glGetShaderiv**

See: [glGetShaderiv() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glGetShaderiv.xml)
Unlike the C specification, the value will be the result of call.

**kivy.graphics.opengl.glGetString**

See: [glGetString() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glGetString.xml)
Unlike the C specification, the value will be returned as a string.

**kivy.graphics.opengl.glGetTexParameterfv**

See: [glGetTexParameterfv() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glGetTexParameterfv.xml)

**kivy.graphics.opengl.glGetTexParameteriv**

See: [glGetTexParameteriv() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glGetTexParameteriv.xml)

**kivy.graphics.opengl.glGetUniformLocation**

See: [glGetUniformLocation() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glGetUniformLocation.xml)

**kivy.graphics.opengl.glGetUniformfv**

See: [glGetUniformfv() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glGetUniformfv.xml)

**kivy.graphics.opengl.glGetUniformiv**

See: [glGetUniformiv() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glGetUniformiv.xml)

**kivy.graphics.opengl.glGetVertexAttribPointerv**

See: [glGetVertexAttribPointerv() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glGetVertexAttribPointerv.xml)

**kivy.graphics.opengl.glGetVertexAttribfv**

See: [glGetVertexAttribfv() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glGetVertexAttribfv.xml)

**kivy.graphics.opengl.glGetVertexAttribiv**

See: [glGetVertexAttribiv() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glGetVertexAttribiv.xml)

**kivy.graphics.opengl.glHint**

See: [glHint() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glHint.xml)

**kivy.graphics.opengl.glIsBuffer**

See: [glIsBuffer() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glIsBuffer.xml)

**kivy.graphics.opengl.glIsEnabled**

See: [glIsEnabled() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glIsEnabled.xml)

**kivy.graphics.opengl.glIsFramebuffer**

See: [glIsFramebuffer() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glIsFramebuffer.xml)

**kivy.graphics.opengl.glIsProgram**

See: [glIsProgram() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glIsProgram.xml)

**kivy.graphics.opengl.glIsRenderbuffer**

See: [glIsRenderbuffer() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glIsRenderbuffer.xml)

**kivy.graphics.opengl.glIsShader**

See: [glIsShader() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glIsShader.xml)

**kivy.graphics.opengl.glIsTexture**

See: [glIsTexture() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glIsTexture.xml)

**kivy.graphics.opengl.glLineWidth**

See: [glLineWidth() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glLineWidth.xml)

**kivy.graphics.opengl.glLinkProgram**

See: [glLinkProgram() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glLinkProgram.xml)

**kivy.graphics.opengl.glPixelStorei**

See: [glPixelStorei() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glPixelStorei.xml)

**kivy.graphics.opengl.glPolygonOffset**

See: [glPolygonOffset() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glPolygonOffset.xml)

**kivy.graphics.opengl.glReadPixels**

See: [glReadPixels() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glReadPixels.xml)
We support only GL_RGB/GL_RGBA as a format and GL_UNSIGNED_BYTE as a
type.

**kivy.graphics.opengl.glReleaseShaderCompiler**

See: [glReleaseShaderCompiler() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glReleaseShaderCompiler.xml)

**kivy.graphics.opengl.glRenderbufferStorage**

See: [glRenderbufferStorage() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glRenderbufferStorage.xml)

**kivy.graphics.opengl.glSampleCoverage**

See: [glSampleCoverage() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glSampleCoverage.xml)

**kivy.graphics.opengl.glScissor**

See: [glScissor() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glScissor.xml)

**kivy.graphics.opengl.glShaderBinary**

See: [glShaderBinary() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glShaderBinary.xml)

**kivy.graphics.opengl.glShaderSource**

See: [glShaderSource() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glShaderSource.xml)

**kivy.graphics.opengl.glStencilFunc**

See: [glStencilFunc() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glStencilFunc.xml)

**kivy.graphics.opengl.glStencilFuncSeparate**

See: [glStencilFuncSeparate() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glStencilFuncSeparate.xml)

**kivy.graphics.opengl.glStencilMask**

See: [glStencilMask() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glStencilMask.xml)

**kivy.graphics.opengl.glStencilMaskSeparate**

See: [glStencilMaskSeparate() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glStencilMaskSeparate.xml)

**kivy.graphics.opengl.glStencilOp**

See: [glStencilOp() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glStencilOp.xml)

**kivy.graphics.opengl.glStencilOpSeparate**

See: [glStencilOpSeparate() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glStencilOpSeparate.xml)

**kivy.graphics.opengl.glTexImage2D**

See: [glTexImage2D() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glTexImage2D.xml)

**kivy.graphics.opengl.glTexParameterf**

See: [glTexParameterf() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glTexParameterf.xml)

**kivy.graphics.opengl.glTexParameterfv**

See: [glTexParameterfv() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glTexParameterfv.xml)

**kivy.graphics.opengl.glTexParameteri**

See: [glTexParameteri() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glTexParameteri.xml)

**kivy.graphics.opengl.glTexParameteriv**

See: [glTexParameteriv() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glTexParameteriv.xml)

**kivy.graphics.opengl.glTexSubImage2D**

See: [glTexSubImage2D() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glTexSubImage2D.xml)

**kivy.graphics.opengl.glUniform1f**

See: [glUniform1f() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glUniform1f.xml)

**kivy.graphics.opengl.glUniform1fv**

See: [glUniform1fv() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glUniform1fv.xml)

**kivy.graphics.opengl.glUniform1i**

See: [glUniform1i() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glUniform1i.xml)

**kivy.graphics.opengl.glUniform1iv**

See: [glUniform1iv() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glUniform1iv.xml)

**kivy.graphics.opengl.glUniform2f**

See: [glUniform2f() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glUniform2f.xml)

**kivy.graphics.opengl.glUniform2fv**

See: [glUniform2fv() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glUniform2fv.xml)

**kivy.graphics.opengl.glUniform2i**

See: [glUniform2i() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glUniform2i.xml)

**kivy.graphics.opengl.glUniform2iv**

See: [glUniform2iv() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glUniform2iv.xml)

**kivy.graphics.opengl.glUniform3f**

See: [glUniform3f() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glUniform3f.xml)

**kivy.graphics.opengl.glUniform3fv**

See: [glUniform3fv() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glUniform3fv.xml)

**kivy.graphics.opengl.glUniform3i**

See: [glUniform3i() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glUniform3i.xml)

**kivy.graphics.opengl.glUniform3iv**

See: [glUniform3iv() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glUniform3iv.xml)

**kivy.graphics.opengl.glUniform4f**

See: [glUniform4f() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glUniform4f.xml)

**kivy.graphics.opengl.glUniform4fv**

See: [glUniform4fv() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glUniform4fv.xml)

**kivy.graphics.opengl.glUniform4i**

See: [glUniform4i() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glUniform4i.xml)

**kivy.graphics.opengl.glUniform4iv**

See: [glUniform4iv() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glUniform4iv.xml)

**kivy.graphics.opengl.glUniformMatrix2fv**

See: [glUniformMatrix2fv() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glUniformMatrix2fv.xml)

**kivy.graphics.opengl.glUniformMatrix3fv**

See: [glUniformMatrix3fv() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glUniformMatrix3fv.xml)

**kivy.graphics.opengl.glUniformMatrix4fv**

See: [glUniformMatrix4fv() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glUniformMatrix4fv.xml)

**kivy.graphics.opengl.glUseProgram**

See: [glUseProgram() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glUseProgram.xml)

**kivy.graphics.opengl.glValidateProgram**

See: [glValidateProgram() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glValidateProgram.xml)

**kivy.graphics.opengl.glVertexAttrib1f**

See: [glVertexAttrib1f() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glVertexAttrib1f.xml)

**kivy.graphics.opengl.glVertexAttrib1fv**

See: [glVertexAttrib1fv() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glVertexAttrib1fv.xml)

**kivy.graphics.opengl.glVertexAttrib2f**

See: [glVertexAttrib2f() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glVertexAttrib2f.xml)

**kivy.graphics.opengl.glVertexAttrib2fv**

See: [glVertexAttrib2fv() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glVertexAttrib2fv.xml)

**kivy.graphics.opengl.glVertexAttrib3f**

See: [glVertexAttrib3f() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glVertexAttrib3f.xml)

**kivy.graphics.opengl.glVertexAttrib3fv**

See: [glVertexAttrib3fv() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glVertexAttrib3fv.xml)

**kivy.graphics.opengl.glVertexAttrib4f**

See: [glVertexAttrib4f() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glVertexAttrib4f.xml)

**kivy.graphics.opengl.glVertexAttrib4fv**

See: [glVertexAttrib4fv() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glVertexAttrib4fv.xml)

**kivy.graphics.opengl.glVertexAttribPointer**

See: [glVertexAttribPointer() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glVertexAttribPointer.xml)

**kivy.graphics.opengl.glViewport**

See: [glViewport() on Kronos website](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glViewport.xml)

**kivy.graphics.opengl.gl_init_symbols**

---

## API - [`kivy.graphics.opengl_utils`](https://kivy.org/doc/stable/api-kivy.graphics.opengl_utils.html)

**kivy.graphics.opengl_utils.gl_get_extensions**

Return a list of OpenGL extensions available. All the names in the list
have the GL_ stripped at the start (if it exists) and are in lowercase.

**kivy.graphics.opengl_utils.gl_get_texture_formats**

Return a list of texture formats recognized by kivy.
The texture list is informative but might not been supported by your
hardware. If you want a list of supported textures, you must filter that
list as follows:

**kivy.graphics.opengl_utils.gl_get_version**

Return the (major, minor) OpenGL version, parsed from the GL_VERSION.
New in version 1.2.0.

**kivy.graphics.opengl_utils.gl_get_version_major**

Return the major component of the OpenGL version.
New in version 1.2.0.

**kivy.graphics.opengl_utils.gl_get_version_minor**

Return the minor component of the OpenGL version.
New in version 1.2.0.

**kivy.graphics.opengl_utils.gl_has_capability**

Return the status of a OpenGL Capability. This is a wrapper that
auto-discovers all the capabilities that Kivy might need. The current
capabilities tested are:
GLCAP_BGRA: Test the support of BGRA texture format
GLCAP_NPOT: Test the support of Non Power of Two texture
GLCAP_S3TC: Test the support of S3TC texture (DXT1, DXT3, DXT5)
GLCAP_DXT1: Test the support of DXT texture (subset of S3TC)
GLCAP_ETC1: Test the support of ETC1 texture

**kivy.graphics.opengl_utils.gl_has_extension**

Check if an OpenGL extension is available. If the name starts with GL_,
it will be stripped for the test and converted to lowercase.

**kivy.graphics.opengl_utils.gl_has_texture_conversion**

Return 1 if the texture can be converted to a native format.

**kivy.graphics.opengl_utils.gl_has_texture_format**

Return whether a texture format is supported by your system, natively or
by conversion. For example, if your card doesn’t support ‘bgra’, we are able
to convert to ‘rgba’ but only in software mode.

**kivy.graphics.opengl_utils.gl_has_texture_native_format**

Return 1 if the texture format is handled natively.

**kivy.graphics.opengl_utils.gl_register_get_size**

Register an association between an OpenGL Const used in glGet* to a number
of elements.
By example, the GPU_MEMORY_INFO_DEDICATED_VIDMEM_NVX is a special pname that
will return the integer 1 (nvidia only).

---

## API - [`kivy.graphics.scissor_instructions`](https://kivy.org/doc/stable/api-kivy.graphics.scissor_instructions.html)

**kivy.graphics.scissor_instructions.Rect**

Bases: `builtins.object`
Rect class used internally by ScissorStack and ScissorPush to determine
correct clipping area.

**kivy.graphics.scissor_instructions.Rect.intersect**

**kivy.graphics.scissor_instructions.ScissorPop**

Bases: [`kivy.graphics.instructions.Instruction`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.Instruction)
Pop the scissor stack. Call after ScissorPush, once you have completed
the drawing you wish to be clipped.

**kivy.graphics.scissor_instructions.ScissorPush**

Bases: [`kivy.graphics.instructions.Instruction`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.Instruction)
to control the area and position of the scissoring region. Defaults to
0, 0, 100, 100
Scissor works by clipping all drawing outside of a rectangle starting at
int x, int y position and having sides of int width by int height in Window
space coordinates

**kivy.graphics.scissor_instructions.ScissorStack**

Bases: `builtins.object`
Class used internally to keep track of the current state of
glScissors regions. Do not instantiate, prefer to inspect the module’s
scissor_stack.

**kivy.graphics.scissor_instructions.ScissorStack.pop**

**kivy.graphics.scissor_instructions.ScissorStack.push**

---

## API - [`kivy.graphics.shader`](https://kivy.org/doc/stable/api-kivy.graphics.shader.html)

**kivy.graphics.shader.Shader**

Bases: `builtins.object`

**kivy.graphics.shader.Shader.fs**

Fragment shader source code.
If you set a new fragment shader code source, it will be automatically
compiled and will replace the current fragment shader.

**kivy.graphics.shader.Shader.source**

glsl source code.
source should be the filename of a glsl shader that contains both the
vertex and fragment shader sourcecode, each designated by a section
header consisting of one line starting with either “–VERTEX” or
“–FRAGMENT” (case insensitive).
New in version 1.6.0.

**kivy.graphics.shader.Shader.success**

Indicate whether the shader loaded successfully and is ready for
usage or not.

**kivy.graphics.shader.Shader.vs**

Vertex shader source code.
If you set a new vertex shader code source, it will be automatically
compiled and will replace the current vertex shader.

---

## API - [`kivy.graphics.stencil_instructions`](https://kivy.org/doc/stable/api-kivy.graphics.stencil_instructions.html)

**kivy.graphics.stencil_instructions.StencilPop**

Bases: [`kivy.graphics.instructions.Instruction`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.Instruction)
Pop the stencil stack. See the module documentation for more information.

**kivy.graphics.stencil_instructions.StencilPush**

Bases: [`kivy.graphics.instructions.Instruction`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.Instruction)
information.

**kivy.graphics.stencil_instructions.StencilPush.clear_stencil**

`clear_stencil` allow to disable stencil clearing in the `StencilPush`
phase. This option essentially disables the invocation of the functions
`cgl.glClearStencil(0)` and `cgl.glClear(GL_STENCIL_BUFFER_BIT).`
If `True`, the stencil will be cleaned in the `StencilPush` phase, if
`False`, it will not be cleaned.

New in version 2.3.0.

**kivy.graphics.stencil_instructions.StencilUnUse**

Bases: [`kivy.graphics.instructions.Instruction`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.Instruction)
Use current stencil buffer to unset the mask.

**kivy.graphics.stencil_instructions.StencilUse**

Bases: [`kivy.graphics.instructions.Instruction`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.Instruction)
more information.

**kivy.graphics.stencil_instructions.StencilUse.func_op**

Determine the stencil operation to use for glStencilFunc(). Can be
one of ‘never’, ‘less’, ‘equal’, ‘lequal’, ‘greater’, ‘notequal’,
‘gequal’ or ‘always’.
By default, the operator is set to ‘equal’.
New in version 1.5.0.

---

## API - [`kivy.graphics.svg`](https://kivy.org/doc/stable/api-kivy.graphics.svg.html)

**kivy.graphics.svg.Svg**

Bases: [`kivy.graphics.instructions.RenderContext`](https://kivy.org/doc/stable/api-kivy.graphics.instructions.html#kivy.graphics.instructions.RenderContext)

**kivy.graphics.svg.Svg.anchor_x**

Horizontal anchor position for scaling and rotations. Defaults to 0. The
symbolic values ‘left’, ‘center’ and ‘right’ are also accepted.

**kivy.graphics.svg.Svg.anchor_y**

Vertical anchor position for scaling and rotations. Defaults to 0. The
symbolic values ‘bottom’, ‘center’ and ‘top’ are also accepted.

**kivy.graphics.svg.Svg.color**

The default color
Used for SvgElements that specify “currentColor”
Changed in version 1.10.3:The color is gettable and settable
New in version 1.9.1.

**kivy.graphics.svg.Svg.current_color**

current_color: object

**kivy.graphics.svg.Svg.gradients**

gradients: object

**kivy.graphics.svg.Svg.height**

height: ‘double’

**kivy.graphics.svg.Svg.set_tree**

sets the tree used to render the Svg and triggers reloading.

New in version 2.0.0.

**kivy.graphics.svg.Svg.source**

Filename / source to load.
The parsing and rendering is done as soon as you set the source.
Changed in version 2.0.0:The property name is now source instead of filename
Changed in version 1.10.3:You can get the used filename

**kivy.graphics.svg.Svg.width**

width: ‘double’

---

## API - [`kivy.graphics.tesselator`](https://kivy.org/doc/stable/api-kivy.graphics.tesselator.html)

**kivy.graphics.tesselator.Tesselator**

Bases: `builtins.object`
Tesselator class. See module for more information about the usage.

**kivy.graphics.tesselator.Tesselator.add_contour**

Add a contour to the tesselator. It can be:
a list of [x, y, x2, y2, …] coordinates
a float array: array(“f”, [x, y, x2, y2, …])
any buffer with floats in it.

**kivy.graphics.tesselator.Tesselator.element_count**

Returns the number of convex polygon.

**kivy.graphics.tesselator.Tesselator.meshes**

Iterate through the result of the [`tesselate()`](https://kivy.org/doc/stable/#kivy.graphics.tesselator.Tesselator.tesselate) to give a result
that can be easily pushed into Kivy`s Mesh object.
It’s a list of: [[vertices, indices], [vertices, indices], …].
The vertices in the format [x, y, u, v, x2, y2, u2, v2].
Careful, u/v coordinates are the same as x/y.
You are responsible to change them for texture mapping if you need to.
You can create Mesh objects like that:

**kivy.graphics.tesselator.Tesselator.tesselate**

Compute all the contours added with [`add_contour()`](https://kivy.org/doc/stable/#kivy.graphics.tesselator.Tesselator.add_contour), and generate
polygons.

**kivy.graphics.tesselator.Tesselator.vertex_count**

Returns the number of vertex generated.
This is the raw result, however, because the Tesselator format the
result for you with [`meshes`](https://kivy.org/doc/stable/#kivy.graphics.tesselator.Tesselator.meshes) or [`vertices`](https://kivy.org/doc/stable/#kivy.graphics.tesselator.Tesselator.vertices) per polygon,
you’ll have more vertices in the result

**kivy.graphics.tesselator.Tesselator.vertices**

Iterate through the result of the [`tesselate()`](https://kivy.org/doc/stable/#kivy.graphics.tesselator.Tesselator.tesselate) in order to give
only a list of [x, y, x2, y2, …] polygons.

---

## API - [`kivy.graphics.texture`](https://kivy.org/doc/stable/api-kivy.graphics.texture.html)

**kivy.graphics.texture.Texture**

Bases: `builtins.object`
textures or complex textures based on ImageData.

**kivy.graphics.texture.Texture.add_reload_observer**

Add a callback to be called after the whole graphics context has
been reloaded. This is where you can reupload your custom data into
the GPU.
New in version 1.2.0.

**kivy.graphics.texture.Texture.ask_update**

Indicate that the content of the texture should be updated and the
callback function needs to be called when the texture will be
used.

**kivy.graphics.texture.Texture.bind**

Bind the texture to the current opengl state.

**kivy.graphics.texture.Texture.blit_buffer**

Blit a buffer into the texture.

Changed in version 1.0.7:added mipmap_level and mipmap_generation
Changed in version 1.9.0:pbuffer can now be any class instance that implements the python
buffer interface and / or memoryviews thereof.

**kivy.graphics.texture.Texture.blit_data**

Replace a whole texture with image data.

**kivy.graphics.texture.Texture.bufferfmt**

Return the buffer format used in this texture (readonly).
New in version 1.2.0.

**kivy.graphics.texture.Texture.colorfmt**

Return the color format used in this texture (readonly).
New in version 1.0.7.

**kivy.graphics.texture.Texture.create**

texture_create(size=None, colorfmt=None, bufferfmt=None, mipmap=False, callback=None, icolorfmt=None)
Create a texture based on size.
Changed in version 1.7.0:`callback` has been added

**kivy.graphics.texture.Texture.create_from_data**

texture_create_from_data(im, mipmap=False)
Create a texture from an ImageData class.

**kivy.graphics.texture.Texture.flip_horizontal**

Flip tex_coords for horizontal display.
New in version 1.9.0.

**kivy.graphics.texture.Texture.flip_vertical**

Flip tex_coords for vertical display.

**kivy.graphics.texture.Texture.get_region**

Return a part of the texture defined by the rectangular arguments
(x, y, width, height). Returns a [`TextureRegion`](https://kivy.org/doc/stable/#kivy.graphics.texture.TextureRegion) instance.

**kivy.graphics.texture.Texture.height**

Return the height of the texture (readonly).

**kivy.graphics.texture.Texture.id**

Return the OpenGL ID of the texture (readonly).

**kivy.graphics.texture.Texture.mag_filter**

Get/set the mag filter texture. Available values:
linear
nearest
Check the opengl documentation for more information about the behavior
of these values :
[http://www.khronos.org/opengles/sdk/docs/man/xhtml/glTexParameter.xml](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glTexParameter.xml).

**kivy.graphics.texture.Texture.min_filter**

Get/set the min filter texture. Available values:
linear
nearest
linear_mipmap_linear
linear_mipmap_nearest
nearest_mipmap_nearest
nearest_mipmap_linear
Check the opengl documentation for more information about the behavior
of these values :
[http://www.khronos.org/opengles/sdk/docs/man/xhtml/glTexParameter.xml](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glTexParameter.xml).

**kivy.graphics.texture.Texture.mipmap**

Return True if the texture has mipmap enabled (readonly).

**kivy.graphics.texture.Texture.pixels**

Get the pixels texture, in RGBA format only, unsigned byte. The
origin of the image is at bottom left.
New in version 1.7.0.

**kivy.graphics.texture.Texture.remove_reload_observer**

Remove a callback from the observer list, previously added by
[`add_reload_observer()`](https://kivy.org/doc/stable/#kivy.graphics.texture.Texture.add_reload_observer).
New in version 1.2.0.

**kivy.graphics.texture.Texture.save**

Save the texture content to a file. Check
[`kivy.core.image.Image.save()`](https://kivy.org/doc/stable/api-kivy.core.image.html#kivy.core.image.Image.save) for more information.
The flipped parameter flips the saved image vertically, and
defaults to True.
New in version 1.7.0.
Changed in version 1.8.0:Parameter flipped added, defaults to True. All the OpenGL Texture
are read from bottom / left, it need to be flipped before saving.
If you don’t want to flip the image, set flipped to False.
Changed in version 1.11.0:Parameter fmt added, to pass the final format to the image provider.
Used if filename is a BytesIO

**kivy.graphics.texture.Texture.size**

Return the (width, height) of the texture (readonly).

**kivy.graphics.texture.Texture.target**

Return the OpenGL target of the texture (readonly).

**kivy.graphics.texture.Texture.tex_coords**

Return the list of tex_coords (opengl).

**kivy.graphics.texture.Texture.uvpos**

Get/set the UV position inside the texture.

**kivy.graphics.texture.Texture.uvsize**

Get/set the UV size inside the texture.

**kivy.graphics.texture.Texture.width**

Return the width of the texture (readonly).

**kivy.graphics.texture.Texture.wrap**

Get/set the wrap texture. Available values:
repeat
mirrored_repeat
clamp_to_edge
Check the opengl documentation for more information about the behavior
of these values :
[http://www.khronos.org/opengles/sdk/docs/man/xhtml/glTexParameter.xml](http://www.khronos.org/opengles/sdk/docs/man/xhtml/glTexParameter.xml).

**kivy.graphics.texture.TextureRegion**

Bases: [`kivy.graphics.texture.Texture`](https://kivy.org/doc/stable/#kivy.graphics.texture.Texture)
texture handling.

**kivy.graphics.texture.TextureRegion.ask_update**

**kivy.graphics.texture.TextureRegion.bind**

**kivy.graphics.texture.TextureRegion.pixels**

---

## API - [`kivy.graphics.transformation`](https://kivy.org/doc/stable/api-kivy.graphics.transformation.html)

**kivy.graphics.transformation.Matrix**

Bases: `builtins.object`

[ 0 1 2 3]
[ 4 5 6 7]
[ 8 9 10 11]
[ 12 13 14 15]

**kivy.graphics.transformation.Matrix.get**

Retrieve the value of the current as a flat list.
New in version 1.9.1.

**kivy.graphics.transformation.Matrix.identity**

Reset the matrix to the identity matrix (inplace).

**kivy.graphics.transformation.Matrix.inverse**

Return the inverse of the matrix as a new Matrix.

**kivy.graphics.transformation.Matrix.look_at**

Returns a new lookat Matrix (similar to
[gluLookAt](http://www.opengl.org/sdk/docs/man2/xhtml/gluLookAt.xml)).

New in version 1.6.0.

**kivy.graphics.transformation.Matrix.multiply**

Multiply the given matrix with self (from the left)
i.e. we premultiply the given matrix by the current matrix and return
the result (not inplace):

**kivy.graphics.transformation.Matrix.normal_matrix**

Computes the normal matrix, which is the inverse transpose
of the top left 3x3 modelview matrix used to transform normals
into eye/camera space.
New in version 1.6.0.

**kivy.graphics.transformation.Matrix.perspective**

Creates a perspective matrix (inplace).

New in version 1.6.0.

**kivy.graphics.transformation.Matrix.project**

Project a point from 3d space into a 2d viewport.

New in version 1.7.0.

**kivy.graphics.transformation.Matrix.rotate**

Rotate the matrix through the angle around the axis (x, y, z)
(inplace).

**kivy.graphics.transformation.Matrix.scale**

Scale the current matrix by the specified factors over
each dimension (inplace).

**kivy.graphics.transformation.Matrix.set**

Insert custom values into the matrix in a flat list format
or 4x4 array format like below:

New in version 1.9.0.

**kivy.graphics.transformation.Matrix.tolist**

Retrieve the value of the current matrix in numpy format.
for example m.tolist() will return:

you can use this format to plug the result straight into numpy
in this way numpy.array(m.tolist())
New in version 1.9.0.

**kivy.graphics.transformation.Matrix.transform_point**

Transforms the point by the matrix and returns the transformed point
as a `(x, y, z)` tuple. If the point is a vector `v`, the returned
values is `v2 = matrix * v`.
If `t` is provided, it multiplies it with the last column of the matrix
and returns the transformed `(x, y, z, t)`.

**kivy.graphics.transformation.Matrix.translate**

Translate the matrix.

**kivy.graphics.transformation.Matrix.transpose**

Return the transposed matrix as a new Matrix.
New in version 1.6.0.

**kivy.graphics.transformation.Matrix.view_clip**

Create a clip matrix (inplace).

Changed in version 1.6.0:Enable support for perspective parameter.

---

## API - [`kivy.input`](https://kivy.org/doc/stable/api-kivy.input.html)

**kivy.input.MotionEvent**

Bases: [`kivy.input.motionevent.MotionEvent`](https://kivy.org/doc/stable/api-kivy.input.motionevent.html#kivy.input.motionevent.MotionEvent)
Abstract class that represents an input event.

**kivy.input.MotionEvent.apply_transform_2d**

Apply a transformation on x, y, z, px, py, pz,
ox, oy, oz, dx, dy, dz.

**kivy.input.MotionEvent.button**

Currently pressed button.

**kivy.input.MotionEvent.copy_to**

Copy some attribute to another motion event object.

**kivy.input.MotionEvent.depack**

Depack args into attributes of the class

**kivy.input.MotionEvent.device**

Device used for creating this event.

**kivy.input.MotionEvent.dispatch_done**

Notify that dispatch to the listeners is done.
Called by the `EventLoopBase.post_dispatch_input()`.
New in version 2.1.0.

**kivy.input.MotionEvent.dispatch_mode**

(Experimental) Used by a event manager or a widget to assign
the dispatching mode. Defaults to
[`MODE_DEFAULT_DISPATCH`](https://kivy.org/doc/stable/api-kivy.eventmanager.html#kivy.eventmanager.MODE_DEFAULT_DISPATCH). See
[`eventmanager`](https://kivy.org/doc/stable/api-kivy.eventmanager.html#module-kivy.eventmanager) for available modes.
New in version 2.1.0.

**kivy.input.MotionEvent.distance**

Return the distance between the two events.

**kivy.input.MotionEvent.double_tap_time**

If the touch is a [`is_double_tap`](https://kivy.org/doc/stable/#kivy.input.MotionEvent.is_double_tap), this is the time
between the previous tap and the current touch.

**kivy.input.MotionEvent.dpos**

Return delta between last position and current position, in the
screen coordinate system (self.dx, self.dy).

**kivy.input.MotionEvent.dsx**

Delta between self.sx and self.psx, in 0-1 range.

**kivy.input.MotionEvent.dsy**

Delta between self.sy and self.psy, in 0-1 range.

**kivy.input.MotionEvent.dsz**

Delta between self.sz and self.psz, in 0-1 range.

**kivy.input.MotionEvent.dx**

Delta between self.x and self.px, in window range.

**kivy.input.MotionEvent.dy**

Delta between self.y and self.py, in window range.

**kivy.input.MotionEvent.dz**

Delta between self.z and self.pz, in window range.

**kivy.input.MotionEvent.grab**

Grab this motion event.
If this event is a touch you can grab it if you want to receive
subsequent [`on_touch_move()`](https://kivy.org/doc/stable/api-kivy.uix.widget.html#kivy.uix.widget.Widget.on_touch_move) and
[`on_touch_up()`](https://kivy.org/doc/stable/api-kivy.uix.widget.html#kivy.uix.widget.Widget.on_touch_up) events, even if the touch
is not dispatched by the parent:

Changed in version 2.1.0:Allowed grab for non-touch events.

**kivy.input.MotionEvent.grab_current**

Used to determine which widget the event is being dispatched to.
Check the [`grab()`](https://kivy.org/doc/stable/#kivy.input.MotionEvent.grab) function for more information.

**kivy.input.MotionEvent.id**

Id of the event, not unique. This is generally the Id set by the
input provider, like ID in TUIO. If you have multiple TUIO sources,
then same id can be used. Prefer to use [`uid`](https://kivy.org/doc/stable/#kivy.input.MotionEvent.uid) attribute
instead.

**kivy.input.MotionEvent.is_double_tap**

Indicate if the touch event is a double tap or not.

**kivy.input.MotionEvent.is_mouse_scrolling**

Returns True if the touch event is a mousewheel scrolling
New in version 1.6.0.

**kivy.input.MotionEvent.is_touch**

True if the MotionEvent is a touch.

**kivy.input.MotionEvent.is_triple_tap**

Indicate if the touch event is a triple tap or not.
New in version 1.7.0.

**kivy.input.MotionEvent.move**

Move to another position.

**kivy.input.MotionEvent.opos**

Return the initial position of the motion event in the screen
coordinate system (self.ox, self.oy).

**kivy.input.MotionEvent.osx**

Origin X position, in 0-1 range.

**kivy.input.MotionEvent.osy**

Origin Y position, in 0-1 range.

**kivy.input.MotionEvent.osz**

Origin Z position, in 0-1 range.

**kivy.input.MotionEvent.ox**

Origin X position, in window range.

**kivy.input.MotionEvent.oy**

Origin Y position, in window range.

**kivy.input.MotionEvent.oz**

Origin Z position, in window range.

**kivy.input.MotionEvent.pop**

Pop attributes values from the stack.

**kivy.input.MotionEvent.pos**

Position (X, Y), in window range.

**kivy.input.MotionEvent.ppos**

Return the previous position of the motion event in the screen
coordinate system (self.px, self.py).

**kivy.input.MotionEvent.profile**

Profiles currently used in the event.

**kivy.input.MotionEvent.psx**

Previous X position, in 0-1 range.

**kivy.input.MotionEvent.psy**

Previous Y position, in 0-1 range.

**kivy.input.MotionEvent.psz**

Previous Z position, in 0-1 range.

**kivy.input.MotionEvent.push**

Push attribute values in attrs onto the stack.

**kivy.input.MotionEvent.push_attrs_stack**

Attributes to push by default, when we use [`push()`](https://kivy.org/doc/stable/#kivy.input.MotionEvent.push) : x, y, z,
dx, dy, dz, ox, oy, oz, px, py, pz.

**kivy.input.MotionEvent.px**

Previous X position, in window range.

**kivy.input.MotionEvent.py**

Previous Y position, in window range.

**kivy.input.MotionEvent.pz**

Previous Z position, in window range.

**kivy.input.MotionEvent.scale_for_screen**

Scale position for the screen.
Changed in version 2.1.0:Max value for x, y and z is changed respectively to w - 1,
h - 1 and p - 1.

**kivy.input.MotionEvent.shape**

Shape of the touch event, subclass of
[`Shape`](https://kivy.org/doc/stable/api-kivy.input.shape.html#kivy.input.shape.Shape).
By default, the property is set to None.

**kivy.input.MotionEvent.spos**

Return the position in the 0-1 coordinate system (self.sx, self.sy).

**kivy.input.MotionEvent.sx**

X position, in 0-1 range.

**kivy.input.MotionEvent.sy**

Y position, in 0-1 range.

**kivy.input.MotionEvent.sync_with_dispatch**

If set to True (default) keeps first previous position
(X, Y, Z in 0-1 range) and ignore all other until
[`MotionEvent.dispatch_done()`](https://kivy.org/doc/stable/#kivy.input.MotionEvent.dispatch_done) is called from the EventLoop.
This attribute is needed because event provider can make many calls
to [`MotionEvent.move()`](https://kivy.org/doc/stable/#kivy.input.MotionEvent.move), but for all those calls event is
dispatched to the listeners only once. Assigning False will keep
latest previous position. See [`MotionEvent.move()`](https://kivy.org/doc/stable/#kivy.input.MotionEvent.move).
New in version 2.1.0.

**kivy.input.MotionEvent.sz**

Z position, in 0-1 range.

**kivy.input.MotionEvent.time_end**

Time of the end event (last event usage).

**kivy.input.MotionEvent.time_start**

Initial time of the event creation.

**kivy.input.MotionEvent.time_update**

Time of the last update.

**kivy.input.MotionEvent.to_absolute_pos**

Transforms normalized (0-1) coordinates nx and ny to absolute
coordinates using x_max, y_max and rotation.

New in version 2.1.0.

**kivy.input.MotionEvent.triple_tap_time**

If the touch is a [`is_triple_tap`](https://kivy.org/doc/stable/#kivy.input.MotionEvent.is_triple_tap), this is the time
between the first tap and the current touch.
New in version 1.7.0.

**kivy.input.MotionEvent.type_id**

(Experimental) String to identify event type.
New in version 2.1.0.

**kivy.input.MotionEvent.ud**

User data dictionary. Use this dictionary to save your own data on
the event.

**kivy.input.MotionEvent.uid**

Uniq ID of the event. You can safely use this property, it will be
never the same across all existing events.

**kivy.input.MotionEvent.ungrab**

Ungrab a previously grabbed motion event.

**kivy.input.MotionEvent.x**

X position, in window range.

**kivy.input.MotionEvent.y**

Y position, in window range.

**kivy.input.MotionEvent.z**

Z position, in window range.

**kivy.input.MotionEventFactory**

Bases: `builtins.object`
MotionEvent factory is a class that registers all availables input
factories. If you create a new input factory, you need to register
it here:

**kivy.input.MotionEventFactory.get**

Get a provider class from the provider id

**kivy.input.MotionEventFactory.list**

Get a list of all available providers

**kivy.input.MotionEventFactory.register**

Register a input provider in the database

**kivy.input.MotionEventProvider**

Bases: `builtins.object`
Base class for a provider.

**kivy.input.MotionEventProvider.start**

Start the provider. This method is automatically called when the
application is started and if the configuration uses the current
provider.

**kivy.input.MotionEventProvider.stop**

Stop the provider.

**kivy.input.MotionEventProvider.update**

Update the provider and dispatch all the new touch events though the
dispatch_fn argument.

---

## API - [`kivy.input.factory`](https://kivy.org/doc/stable/api-kivy.input.factory.html)

**kivy.input.factory.MotionEventFactory**

Bases: `builtins.object`
MotionEvent factory is a class that registers all availables input
factories. If you create a new input factory, you need to register
it here:

**kivy.input.factory.MotionEventFactory.get**

Get a provider class from the provider id

**kivy.input.factory.MotionEventFactory.list**

Get a list of all available providers

**kivy.input.factory.MotionEventFactory.register**

Register a input provider in the database

---

## API - [`kivy.input.motionevent`](https://kivy.org/doc/stable/api-kivy.input.motionevent.html)

**kivy.input.motionevent.MotionEvent**

Bases: [`kivy.input.motionevent.MotionEvent`](https://kivy.org/doc/stable/#kivy.input.motionevent.MotionEvent)
Abstract class that represents an input event.

**kivy.input.motionevent.MotionEvent.apply_transform_2d**

Apply a transformation on x, y, z, px, py, pz,
ox, oy, oz, dx, dy, dz.

**kivy.input.motionevent.MotionEvent.button**

Currently pressed button.

**kivy.input.motionevent.MotionEvent.copy_to**

Copy some attribute to another motion event object.

**kivy.input.motionevent.MotionEvent.depack**

Depack args into attributes of the class

**kivy.input.motionevent.MotionEvent.device**

Device used for creating this event.

**kivy.input.motionevent.MotionEvent.dispatch_done**

Notify that dispatch to the listeners is done.
Called by the `EventLoopBase.post_dispatch_input()`.
New in version 2.1.0.

**kivy.input.motionevent.MotionEvent.dispatch_mode**

(Experimental) Used by a event manager or a widget to assign
the dispatching mode. Defaults to
[`MODE_DEFAULT_DISPATCH`](https://kivy.org/doc/stable/api-kivy.eventmanager.html#kivy.eventmanager.MODE_DEFAULT_DISPATCH). See
[`eventmanager`](https://kivy.org/doc/stable/api-kivy.eventmanager.html#module-kivy.eventmanager) for available modes.
New in version 2.1.0.

**kivy.input.motionevent.MotionEvent.distance**

Return the distance between the two events.

**kivy.input.motionevent.MotionEvent.double_tap_time**

If the touch is a [`is_double_tap`](https://kivy.org/doc/stable/#kivy.input.motionevent.MotionEvent.is_double_tap), this is the time
between the previous tap and the current touch.

**kivy.input.motionevent.MotionEvent.dpos**

Return delta between last position and current position, in the
screen coordinate system (self.dx, self.dy).

**kivy.input.motionevent.MotionEvent.dsx**

Delta between self.sx and self.psx, in 0-1 range.

**kivy.input.motionevent.MotionEvent.dsy**

Delta between self.sy and self.psy, in 0-1 range.

**kivy.input.motionevent.MotionEvent.dsz**

Delta between self.sz and self.psz, in 0-1 range.

**kivy.input.motionevent.MotionEvent.dx**

Delta between self.x and self.px, in window range.

**kivy.input.motionevent.MotionEvent.dy**

Delta between self.y and self.py, in window range.

**kivy.input.motionevent.MotionEvent.dz**

Delta between self.z and self.pz, in window range.

**kivy.input.motionevent.MotionEvent.grab**

Grab this motion event.
If this event is a touch you can grab it if you want to receive
subsequent [`on_touch_move()`](https://kivy.org/doc/stable/api-kivy.uix.widget.html#kivy.uix.widget.Widget.on_touch_move) and
[`on_touch_up()`](https://kivy.org/doc/stable/api-kivy.uix.widget.html#kivy.uix.widget.Widget.on_touch_up) events, even if the touch
is not dispatched by the parent:

Changed in version 2.1.0:Allowed grab for non-touch events.

**kivy.input.motionevent.MotionEvent.grab_current**

Used to determine which widget the event is being dispatched to.
Check the [`grab()`](https://kivy.org/doc/stable/#kivy.input.motionevent.MotionEvent.grab) function for more information.

**kivy.input.motionevent.MotionEvent.id**

Id of the event, not unique. This is generally the Id set by the
input provider, like ID in TUIO. If you have multiple TUIO sources,
then same id can be used. Prefer to use [`uid`](https://kivy.org/doc/stable/#kivy.input.motionevent.MotionEvent.uid) attribute
instead.

**kivy.input.motionevent.MotionEvent.is_double_tap**

Indicate if the touch event is a double tap or not.

**kivy.input.motionevent.MotionEvent.is_mouse_scrolling**

Returns True if the touch event is a mousewheel scrolling
New in version 1.6.0.

**kivy.input.motionevent.MotionEvent.is_touch**

True if the MotionEvent is a touch.

**kivy.input.motionevent.MotionEvent.is_triple_tap**

Indicate if the touch event is a triple tap or not.
New in version 1.7.0.

**kivy.input.motionevent.MotionEvent.move**

Move to another position.

**kivy.input.motionevent.MotionEvent.opos**

Return the initial position of the motion event in the screen
coordinate system (self.ox, self.oy).

**kivy.input.motionevent.MotionEvent.osx**

Origin X position, in 0-1 range.

**kivy.input.motionevent.MotionEvent.osy**

Origin Y position, in 0-1 range.

**kivy.input.motionevent.MotionEvent.osz**

Origin Z position, in 0-1 range.

**kivy.input.motionevent.MotionEvent.ox**

Origin X position, in window range.

**kivy.input.motionevent.MotionEvent.oy**

Origin Y position, in window range.

**kivy.input.motionevent.MotionEvent.oz**

Origin Z position, in window range.

**kivy.input.motionevent.MotionEvent.pop**

Pop attributes values from the stack.

**kivy.input.motionevent.MotionEvent.pos**

Position (X, Y), in window range.

**kivy.input.motionevent.MotionEvent.ppos**

Return the previous position of the motion event in the screen
coordinate system (self.px, self.py).

**kivy.input.motionevent.MotionEvent.profile**

Profiles currently used in the event.

**kivy.input.motionevent.MotionEvent.psx**

Previous X position, in 0-1 range.

**kivy.input.motionevent.MotionEvent.psy**

Previous Y position, in 0-1 range.

**kivy.input.motionevent.MotionEvent.psz**

Previous Z position, in 0-1 range.

**kivy.input.motionevent.MotionEvent.push**

Push attribute values in attrs onto the stack.

**kivy.input.motionevent.MotionEvent.push_attrs_stack**

Attributes to push by default, when we use [`push()`](https://kivy.org/doc/stable/#kivy.input.motionevent.MotionEvent.push) : x, y, z,
dx, dy, dz, ox, oy, oz, px, py, pz.

**kivy.input.motionevent.MotionEvent.px**

Previous X position, in window range.

**kivy.input.motionevent.MotionEvent.py**

Previous Y position, in window range.

**kivy.input.motionevent.MotionEvent.pz**

Previous Z position, in window range.

**kivy.input.motionevent.MotionEvent.scale_for_screen**

Scale position for the screen.
Changed in version 2.1.0:Max value for x, y and z is changed respectively to w - 1,
h - 1 and p - 1.

**kivy.input.motionevent.MotionEvent.shape**

Shape of the touch event, subclass of
[`Shape`](https://kivy.org/doc/stable/api-kivy.input.shape.html#kivy.input.shape.Shape).
By default, the property is set to None.

**kivy.input.motionevent.MotionEvent.spos**

Return the position in the 0-1 coordinate system (self.sx, self.sy).

**kivy.input.motionevent.MotionEvent.sx**

X position, in 0-1 range.

**kivy.input.motionevent.MotionEvent.sy**

Y position, in 0-1 range.

**kivy.input.motionevent.MotionEvent.sync_with_dispatch**

If set to True (default) keeps first previous position
(X, Y, Z in 0-1 range) and ignore all other until
[`MotionEvent.dispatch_done()`](https://kivy.org/doc/stable/#kivy.input.motionevent.MotionEvent.dispatch_done) is called from the EventLoop.
This attribute is needed because event provider can make many calls
to [`MotionEvent.move()`](https://kivy.org/doc/stable/#kivy.input.motionevent.MotionEvent.move), but for all those calls event is
dispatched to the listeners only once. Assigning False will keep
latest previous position. See [`MotionEvent.move()`](https://kivy.org/doc/stable/#kivy.input.motionevent.MotionEvent.move).
New in version 2.1.0.

**kivy.input.motionevent.MotionEvent.sz**

Z position, in 0-1 range.

**kivy.input.motionevent.MotionEvent.time_end**

Time of the end event (last event usage).

**kivy.input.motionevent.MotionEvent.time_start**

Initial time of the event creation.

**kivy.input.motionevent.MotionEvent.time_update**

Time of the last update.

**kivy.input.motionevent.MotionEvent.to_absolute_pos**

Transforms normalized (0-1) coordinates nx and ny to absolute
coordinates using x_max, y_max and rotation.

New in version 2.1.0.

**kivy.input.motionevent.MotionEvent.triple_tap_time**

If the touch is a [`is_triple_tap`](https://kivy.org/doc/stable/#kivy.input.motionevent.MotionEvent.is_triple_tap), this is the time
between the first tap and the current touch.
New in version 1.7.0.

**kivy.input.motionevent.MotionEvent.type_id**

(Experimental) String to identify event type.
New in version 2.1.0.

**kivy.input.motionevent.MotionEvent.ud**

User data dictionary. Use this dictionary to save your own data on
the event.

**kivy.input.motionevent.MotionEvent.uid**

Uniq ID of the event. You can safely use this property, it will be
never the same across all existing events.

**kivy.input.motionevent.MotionEvent.ungrab**

Ungrab a previously grabbed motion event.

**kivy.input.motionevent.MotionEvent.x**

X position, in window range.

**kivy.input.motionevent.MotionEvent.y**

Y position, in window range.

**kivy.input.motionevent.MotionEvent.z**

Z position, in window range.

---

## API - [`kivy.input.postproc.calibration`](https://kivy.org/doc/stable/api-kivy.input.postproc.calibration.html)

**kivy.input.postproc.calibration.InputPostprocCalibration**

Bases: `builtins.object`
Recalibrate the inputs.
The configuration must go within a section named postproc:calibration.
Within the section, you must have a line like:

If you wish to match by provider, you must have a line like:

Changed in version 1.11.0:Added auto parameter

---

## API - [`kivy.input.postproc.dejitter`](https://kivy.org/doc/stable/api-kivy.input.postproc.dejitter.html)

**kivy.input.postproc.dejitter.InputPostprocDejitter**

Bases: `builtins.object`
Get rid of jitterish BLOBs.
Example:

---

## API - [`kivy.input.postproc.doubletap`](https://kivy.org/doc/stable/api-kivy.input.postproc.doubletap.html)

**kivy.input.postproc.doubletap.InputPostprocDoubleTap**

Bases: `builtins.object`
InputPostProcDoubleTap is a post-processor to check if
a touch is a double tap or not.
Double tap can be configured in the Kivy config file:

Distance parameter is in the range 0-1000 and time is in milliseconds.

**kivy.input.postproc.doubletap.InputPostprocDoubleTap.find_double_tap**

Find a double tap touch within self.touches.
The touch must be not a previous double tap and the distance must be
within the specified threshold. Additionally, the touch profiles
must be the same kind of touch.

---

## API - [`kivy.input.postproc.ignorelist`](https://kivy.org/doc/stable/api-kivy.input.postproc.ignorelist.html)

**kivy.input.postproc.ignorelist.InputPostprocIgnoreList**

Bases: `builtins.object`
InputPostprocIgnoreList is a post-processor which removes touches in the
Ignore list. The Ignore list can be configured in the Kivy config file:

The Ignore list coordinates are in the range 0-1, not in screen pixels.

---

## API - [`kivy.input.postproc.retaintouch`](https://kivy.org/doc/stable/api-kivy.input.postproc.retaintouch.html)

**kivy.input.postproc.retaintouch.InputPostprocRetainTouch**

Bases: `builtins.object`
InputPostprocRetainTouch is a post-processor to delay the ‘up’ event of a
touch, to reuse it under certains conditions. This module is designed to
prevent lost finger touches on some hardware/setups.
Retain touch can be configured in the Kivy config file:

The distance parameter is in the range 0-1000 and time is in milliseconds.

---

## API - [`kivy.input.postproc.tripletap`](https://kivy.org/doc/stable/api-kivy.input.postproc.tripletap.html)

**kivy.input.postproc.tripletap.InputPostprocTripleTap**

Bases: `builtins.object`
InputPostProcTripleTap is a post-processor to check if
a touch is a triple tap or not.
Triple tap can be configured in the Kivy config file:

The distance parameter is in the range 0-1000 and time is in milliseconds.

**kivy.input.postproc.tripletap.InputPostprocTripleTap.find_triple_tap**

Find a triple tap touch within *self.touches*.
The touch must be not be a previous triple tap and the distance
must be within the bounds specified. Additionally, the touch profile
must be the same kind of touch.

---

## API - [`kivy.input.provider`](https://kivy.org/doc/stable/api-kivy.input.provider.html)

**kivy.input.provider.MotionEventProvider**

Bases: `builtins.object`
Base class for a provider.

**kivy.input.provider.MotionEventProvider.start**

Start the provider. This method is automatically called when the
application is started and if the configuration uses the current
provider.

**kivy.input.provider.MotionEventProvider.stop**

Stop the provider.

**kivy.input.provider.MotionEventProvider.update**

Update the provider and dispatch all the new touch events though the
dispatch_fn argument.

---

## API - [`kivy.input.providers.androidjoystick`](https://kivy.org/doc/stable/api-kivy.input.providers.androidjoystick.html)

**kivy.input.providers.androidjoystick.AndroidMotionEventProvider**

Bases: [`kivy.input.provider.MotionEventProvider`](https://kivy.org/doc/stable/api-kivy.input.provider.html#kivy.input.provider.MotionEventProvider)

**kivy.input.providers.androidjoystick.AndroidMotionEventProvider.start**

Start the provider. This method is automatically called when the
application is started and if the configuration uses the current
provider.

**kivy.input.providers.androidjoystick.AndroidMotionEventProvider.stop**

Stop the provider.

**kivy.input.providers.androidjoystick.AndroidMotionEventProvider.update**

Update the provider and dispatch all the new touch events though the
dispatch_fn argument.

---

## API - [`kivy.input.providers.hidinput`](https://kivy.org/doc/stable/api-kivy.input.providers.hidinput.html)

**kivy.input.providers.hidinput.HIDMotionEvent**

Bases: [`kivy.input.motionevent.MotionEvent`](https://kivy.org/doc/stable/api-kivy.input.motionevent.html#kivy.input.motionevent.MotionEvent)

**kivy.input.providers.hidinput.HIDMotionEvent.depack**

Depack args into attributes of the class

---

## API - [`kivy.input.providers.leapfinger`](https://kivy.org/doc/stable/api-kivy.input.providers.leapfinger.html)

**kivy.input.providers.leapfinger.LeapFingerEvent**

Bases: [`kivy.input.motionevent.MotionEvent`](https://kivy.org/doc/stable/api-kivy.input.motionevent.html#kivy.input.motionevent.MotionEvent)

**kivy.input.providers.leapfinger.LeapFingerEvent.depack**

Depack args into attributes of the class

**kivy.input.providers.leapfinger.LeapFingerEventProvider**

Bases: [`kivy.input.provider.MotionEventProvider`](https://kivy.org/doc/stable/api-kivy.input.provider.html#kivy.input.provider.MotionEventProvider)

**kivy.input.providers.leapfinger.LeapFingerEventProvider.start**

Start the provider. This method is automatically called when the
application is started and if the configuration uses the current
provider.

**kivy.input.providers.leapfinger.LeapFingerEventProvider.update**

Update the provider and dispatch all the new touch events though the
dispatch_fn argument.

---

## API - [`kivy.input.providers.linuxwacom`](https://kivy.org/doc/stable/api-kivy.input.providers.linuxwacom.html)

**kivy.input.providers.linuxwacom.LinuxWacomMotionEvent**

Bases: [`kivy.input.motionevent.MotionEvent`](https://kivy.org/doc/stable/api-kivy.input.motionevent.html#kivy.input.motionevent.MotionEvent)

**kivy.input.providers.linuxwacom.LinuxWacomMotionEvent.depack**

Depack args into attributes of the class

---

## API - [`kivy.input.providers.mactouch`](https://kivy.org/doc/stable/api-kivy.input.providers.mactouch.html)

**kivy.input.providers.mactouch.MacMotionEventProvider**

Bases: [`kivy.input.provider.MotionEventProvider`](https://kivy.org/doc/stable/api-kivy.input.provider.html#kivy.input.provider.MotionEventProvider)

**kivy.input.providers.mactouch.MacMotionEventProvider.start**

Start the provider. This method is automatically called when the
application is started and if the configuration uses the current
provider.

**kivy.input.providers.mactouch.MacMotionEventProvider.stop**

Stop the provider.

**kivy.input.providers.mactouch.MacMotionEventProvider.update**

Update the provider and dispatch all the new touch events though the
dispatch_fn argument.

---

## API - [`kivy.input.providers.mouse`](https://kivy.org/doc/stable/api-kivy.input.providers.mouse.html)

**kivy.input.providers.mouse.MouseMotionEventProvider**

Bases: [`kivy.input.provider.MotionEventProvider`](https://kivy.org/doc/stable/api-kivy.input.provider.html#kivy.input.provider.MotionEventProvider)

**kivy.input.providers.mouse.MouseMotionEventProvider.disable_hover**

Disables dispatching of hover events if set to `True`.
Hover events are enabled by default (disable_hover is `False`). See
module documentation if you want to enable/disable hover events through
config file.
New in version 2.1.0.

**kivy.input.providers.mouse.MouseMotionEventProvider.start**

Start the mouse provider

**kivy.input.providers.mouse.MouseMotionEventProvider.stop**

Stop the mouse provider

**kivy.input.providers.mouse.MouseMotionEventProvider.update**

Update the mouse provider (pop event from the queue)

---

## API - [`kivy.input.providers.mtdev`](https://kivy.org/doc/stable/api-kivy.input.providers.mtdev.html)

**kivy.input.providers.mtdev.MTDMotionEvent**

Bases: [`kivy.input.motionevent.MotionEvent`](https://kivy.org/doc/stable/api-kivy.input.motionevent.html#kivy.input.motionevent.MotionEvent)

**kivy.input.providers.mtdev.MTDMotionEvent.depack**

Depack args into attributes of the class

---

## API - [`kivy.input.providers.tuio`](https://kivy.org/doc/stable/api-kivy.input.providers.tuio.html)

**kivy.input.providers.tuio.Tuio2dCurMotionEvent**

Bases: `kivy.input.providers.tuio.TuioMotionEvent`
A 2dCur TUIO touch.

**kivy.input.providers.tuio.Tuio2dCurMotionEvent.depack**

Depack args into attributes of the class

**kivy.input.providers.tuio.Tuio2dObjMotionEvent**

Bases: `kivy.input.providers.tuio.TuioMotionEvent`
A 2dObj TUIO object.

**kivy.input.providers.tuio.Tuio2dObjMotionEvent.depack**

Depack args into attributes of the class

**kivy.input.providers.tuio.TuioMotionEventProvider**

Bases: [`kivy.input.provider.MotionEventProvider`](https://kivy.org/doc/stable/api-kivy.input.provider.html#kivy.input.provider.MotionEventProvider)
The TUIO provider listens to a socket and handles some of the incoming
OSC messages:
/tuio/2Dcur
/tuio/2Dobj
You can easily extend the provider to handle new TUIO paths like so:

**kivy.input.providers.tuio.TuioMotionEventProvider.create**

Create a touch event from a TUIO path

**kivy.input.providers.tuio.TuioMotionEventProvider.register**

Register a new path to handle in TUIO provider

**kivy.input.providers.tuio.TuioMotionEventProvider.start**

Start the TUIO provider

**kivy.input.providers.tuio.TuioMotionEventProvider.stop**

Stop the TUIO provider

**kivy.input.providers.tuio.TuioMotionEventProvider.unregister**

Unregister a path to stop handling it in the TUIO provider

**kivy.input.providers.tuio.TuioMotionEventProvider.update**

Update the TUIO provider (pop events from the queue)

---

## API - [`kivy.input.recorder`](https://kivy.org/doc/stable/api-kivy.input.recorder.html)

**kivy.input.recorder.Recorder**

Bases: [`kivy.event.EventDispatcher`](https://kivy.org/doc/stable/api-kivy.event.html#kivy.event.EventDispatcher)
Recorder class. Please check module documentation for more information.

Changed in version 1.10.0:Event on_stop added.

**kivy.input.recorder.Recorder.counter**

Number of events recorded in the last session.
[`counter`](https://kivy.org/doc/stable/#kivy.input.recorder.Recorder.counter) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and defaults
to 0, read-only.

**kivy.input.recorder.Recorder.filename**

Filename to save the output of the recorder.
[`filename`](https://kivy.org/doc/stable/#kivy.input.recorder.Recorder.filename) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults
to ‘recorder.kvi’.

**kivy.input.recorder.Recorder.play**

Boolean to start/stop the replay of the current file (if it exists).
[`play`](https://kivy.org/doc/stable/#kivy.input.recorder.Recorder.play) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and defaults to
False.

**kivy.input.recorder.Recorder.record**

Boolean to start/stop the recording of input events.
[`record`](https://kivy.org/doc/stable/#kivy.input.recorder.Recorder.record) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and defaults
to False.

**kivy.input.recorder.Recorder.record_attrs**

Attributes to record from the motion event.
[`record_attrs`](https://kivy.org/doc/stable/#kivy.input.recorder.Recorder.record_attrs) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) and
defaults to [‘is_touch’, ‘sx’, ‘sy’].

**kivy.input.recorder.Recorder.record_profile_mask**

Profile to save in the fake motion event when replayed.
[`record_profile_mask`](https://kivy.org/doc/stable/#kivy.input.recorder.Recorder.record_profile_mask) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) and
defaults to [‘pos’].

**kivy.input.recorder.Recorder.window**

Window instance to attach the recorder. If None, it will use the
default instance.
[`window`](https://kivy.org/doc/stable/#kivy.input.recorder.Recorder.window) is a [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to None.

---

## API - [`kivy.input.shape`](https://kivy.org/doc/stable/api-kivy.input.shape.html)

**kivy.input.shape.Shape**

Bases: `builtins.object`
Abstract class for all implementations of a shape

**kivy.input.shape.ShapeRect**

Bases: [`kivy.input.shape.Shape`](https://kivy.org/doc/stable/#kivy.input.shape.Shape)
Class for the representation of a rectangle.

**kivy.input.shape.ShapeRect.height**

Height of the rect

**kivy.input.shape.ShapeRect.width**

Width of the rect

---

## API - [`kivy.interactive`](https://kivy.org/doc/stable/api-kivy.interactive.html)

**kivy.interactive.InteractiveLauncher**

Bases: [`kivy.interactive.SafeMembrane`](https://kivy.org/doc/stable/#kivy.interactive.SafeMembrane)
Proxy to an application instance that launches it in a thread and
then returns and acts as a proxy to the application in the thread.

**kivy.interactive.SafeMembrane**

Bases: `builtins.object`
This help is for a proxy object. Did you want help on the proxy’s referent
instead? Try using help(<instance>._ref)
The SafeMembrane is a threadsafe proxy that also returns attributes as new
thread-safe objects
and makes thread-safe method calls, preventing thread-unsafe objects
from leaking into the user’s environment.

**kivy.interactive.SafeMembrane.safeIn**

Provides a thread-safe entry point for interactive launching.

**kivy.interactive.SafeMembrane.safeOut**

Provides a thread-safe exit point for interactive launching.

---

## API - [`kivy.lang`](https://kivy.org/doc/stable/api-kivy.lang.html)

**kivy.lang.BuilderBase**

Bases: `builtins.object`
The Builder is responsible for creating a [`Parser`](https://kivy.org/doc/stable/#kivy.lang.Parser) for parsing a
kv file, merging the results into its internal rules, templates, etc.
By default, `Builder` is a global Kivy instance used in widgets
that you can use to load other kv files in addition to the default ones.

**kivy.lang.BuilderBase.apply**

Search all the rules that match the widget and apply them.

**kivy.lang.BuilderBase.apply_rules**

Search all the rules that match the name rule_name
and apply them to widget.
New in version 1.10.0.

**kivy.lang.BuilderBase.create_from**

Creates a instance of the class, and initializes to the state of
`builder`.

**kivy.lang.BuilderBase.load_file**

Insert a file into the language builder and return the root widget
(if defined) of the kv file.

**kivy.lang.BuilderBase.load_string**

Insert a string into the Language Builder and return the root widget
(if defined) of the kv string.

The filename parameter can be used to unload kv strings in the same way
as you unload kv files. This can be achieved using pseudo file names
e.g.:

can be unloaded via:

**kivy.lang.BuilderBase.match**

Return a list of `ParserRule` objects matching the widget.

**kivy.lang.BuilderBase.match_rule_name**

Return a list of `ParserRule` objects matching the widget.

**kivy.lang.BuilderBase.sync**

Execute all the waiting operations, such as the execution of all the
expressions related to the canvas.
New in version 1.7.0.

**kivy.lang.BuilderBase.template**

Create a specialized template using a specific context.
New in version 1.0.5.
With templates, you can construct custom widgets from a kv lang
definition by giving them a context. Check [Template usage](https://kivy.org/doc/stable/#template-usage).

**kivy.lang.BuilderBase.unbind_property**

Unbind the handlers created by all the rules of the widget that set
the name.
This effectively clears all the rules of widget that take the form:

For example:

New in version 1.9.1.

**kivy.lang.BuilderBase.unbind_widget**

Unbind all the handlers created by the KV rules of the
widget. The `kivy.uix.widget.Widget.uid` is passed here
instead of the widget itself, because Builder is using it in the
widget destructor.
This effectively clears all the KV rules associated with this widget.
For example:

New in version 1.7.2.

**kivy.lang.BuilderBase.unload_file**

Unload all rules associated with a previously imported file.
New in version 1.0.8.

**kivy.lang.BuilderException**

Bases: [`ParserException`](https://kivy.org/doc/stable/api-kivy.lang.parser.html#kivy.lang.parser.ParserException)
Exception raised when the Builder fails to apply a rule on a widget.

**kivy.lang.Observable**

Bases: [`kivy.event.ObjectWithUid`](https://kivy.org/doc/stable/api-kivy.event.html#kivy.event.ObjectWithUid)
[`Observable`](https://kivy.org/doc/stable/#kivy.lang.Observable) is a stub class defining the methods required
for binding. `EventDispatcher` is (the) one example of a class that
implements the binding interface. See `EventDispatcher` for details.
New in version 1.9.0.

**kivy.lang.Observable.bind**

**kivy.lang.Observable.fbind**

See `EventDispatcher.fbind()`.

**kivy.lang.Observable.funbind**

See [`fbind()`](https://kivy.org/doc/stable/#kivy.lang.Observable.fbind) and `EventDispatcher.funbind()`.

**kivy.lang.Observable.unbind**

**kivy.lang.Observable.unbind_uid**

See [`fbind()`](https://kivy.org/doc/stable/#kivy.lang.Observable.fbind) and `EventDispatcher.unbind_uid()`.

**kivy.lang.Parser**

Bases: `builtins.object`
Create a Parser object to parse a Kivy language file or Kivy content.

**kivy.lang.Parser.parse**

Parse the contents of a Parser file and return a list
of root objects.

**kivy.lang.Parser.parse_level**

Parse the current level (level * spaces) indentation.

**kivy.lang.Parser.strip_comments**

Remove all comments from all lines in-place.
Comments need to be on a single line and not at the end of a line.
i.e. a comment line’s first non-whitespace character must be a #.

**kivy.lang.ParserException**

Bases: `Exception`
Exception raised when something wrong happened in a kv file.

---

## API - [`kivy.lang.builder`](https://kivy.org/doc/stable/api-kivy.lang.builder.html)

**kivy.lang.builder.Builder**

Main instance of a [`BuilderBase`](https://kivy.org/doc/stable/#kivy.lang.builder.BuilderBase).

**kivy.lang.builder.BuilderBase**

Bases: `builtins.object`
The Builder is responsible for creating a `Parser` for parsing a
kv file, merging the results into its internal rules, templates, etc.
By default, [`Builder`](https://kivy.org/doc/stable/#kivy.lang.builder.Builder) is a global Kivy instance used in widgets
that you can use to load other kv files in addition to the default ones.

**kivy.lang.builder.BuilderBase.apply**

Search all the rules that match the widget and apply them.

**kivy.lang.builder.BuilderBase.apply_rules**

Search all the rules that match the name rule_name
and apply them to widget.
New in version 1.10.0.

**kivy.lang.builder.BuilderBase.create_from**

Creates a instance of the class, and initializes to the state of
`builder`.

**kivy.lang.builder.BuilderBase.load_file**

Insert a file into the language builder and return the root widget
(if defined) of the kv file.

**kivy.lang.builder.BuilderBase.load_string**

Insert a string into the Language Builder and return the root widget
(if defined) of the kv string.

The filename parameter can be used to unload kv strings in the same way
as you unload kv files. This can be achieved using pseudo file names
e.g.:

can be unloaded via:

**kivy.lang.builder.BuilderBase.match**

Return a list of `ParserRule` objects matching the widget.

**kivy.lang.builder.BuilderBase.match_rule_name**

Return a list of `ParserRule` objects matching the widget.

**kivy.lang.builder.BuilderBase.sync**

Execute all the waiting operations, such as the execution of all the
expressions related to the canvas.
New in version 1.7.0.

**kivy.lang.builder.BuilderBase.template**

Create a specialized template using a specific context.
New in version 1.0.5.
With templates, you can construct custom widgets from a kv lang
definition by giving them a context. Check [Template usage](https://kivy.org/doc/stable/api-kivy.lang.html#template-usage).

**kivy.lang.builder.BuilderBase.unbind_property**

Unbind the handlers created by all the rules of the widget that set
the name.
This effectively clears all the rules of widget that take the form:

For example:

New in version 1.9.1.

**kivy.lang.builder.BuilderBase.unbind_widget**

Unbind all the handlers created by the KV rules of the
widget. The `kivy.uix.widget.Widget.uid` is passed here
instead of the widget itself, because Builder is using it in the
widget destructor.
This effectively clears all the KV rules associated with this widget.
For example:

New in version 1.7.2.

**kivy.lang.builder.BuilderBase.unload_file**

Unload all rules associated with a previously imported file.
New in version 1.0.8.

**kivy.lang.builder.BuilderException**

Bases: [`ParserException`](https://kivy.org/doc/stable/api-kivy.lang.parser.html#kivy.lang.parser.ParserException)
Exception raised when the Builder fails to apply a rule on a widget.

**kivy.lang.builder.Observable**

Bases: [`kivy.event.ObjectWithUid`](https://kivy.org/doc/stable/api-kivy.event.html#kivy.event.ObjectWithUid)
[`Observable`](https://kivy.org/doc/stable/#kivy.lang.builder.Observable) is a stub class defining the methods required
for binding. `EventDispatcher` is (the) one example of a class that
implements the binding interface. See `EventDispatcher` for details.
New in version 1.9.0.

**kivy.lang.builder.Observable.bind**

**kivy.lang.builder.Observable.fbind**

See `EventDispatcher.fbind()`.

**kivy.lang.builder.Observable.funbind**

See [`fbind()`](https://kivy.org/doc/stable/#kivy.lang.builder.Observable.fbind) and `EventDispatcher.funbind()`.

**kivy.lang.builder.Observable.unbind**

**kivy.lang.builder.Observable.unbind_uid**

See [`fbind()`](https://kivy.org/doc/stable/#kivy.lang.builder.Observable.fbind) and `EventDispatcher.unbind_uid()`.

---

## API - [`kivy.lang.parser`](https://kivy.org/doc/stable/api-kivy.lang.parser.html)

**kivy.lang.parser.Parser**

Bases: `builtins.object`
Create a Parser object to parse a Kivy language file or Kivy content.

**kivy.lang.parser.Parser.parse**

Parse the contents of a Parser file and return a list
of root objects.

**kivy.lang.parser.Parser.parse_level**

Parse the current level (level * spaces) indentation.

**kivy.lang.parser.Parser.strip_comments**

Remove all comments from all lines in-place.
Comments need to be on a single line and not at the end of a line.
i.e. a comment line’s first non-whitespace character must be a #.

**kivy.lang.parser.ParserException**

Bases: `Exception`
Exception raised when something wrong happened in a kv file.

---

## API - [`kivy.lib.ddsfile`](https://kivy.org/doc/stable/api-kivy.lib.ddsfile.html)

**kivy.lib.ddsfile.DDSException**

Bases: `Exception`

**kivy.lib.ddsfile.QueryDict**

Bases: `builtins.dict`

---

## API - [`kivy.lib.mtdev`](https://kivy.org/doc/stable/api-kivy.lib.mtdev.html)

**kivy.lib.mtdev.input_absinfo**

Bases: `_ctypes.Structure`

**kivy.lib.mtdev.input_event**

Bases: `_ctypes.Structure`

**kivy.lib.mtdev.mtdev**

Bases: `_ctypes.Structure`

**kivy.lib.mtdev.mtdev_caps**

Bases: `_ctypes.Structure`

**kivy.lib.mtdev.timeval**

Bases: `_ctypes.Structure`

---

## API - [`kivy.loader`](https://kivy.org/doc/stable/api-kivy.loader.html)

**kivy.loader.LoaderBase**

Bases: `builtins.object`
Common base for the Loader and specific implementations.
By default, the Loader will be the best available loader implementation.
The _update() function is called every 1 / 25.s or each frame if we have
less than 25 FPS.

**kivy.loader.LoaderBase.error_image**

Image used for error.
You can change it by doing:

Changed in version 1.6.0:Not readonly anymore.

**kivy.loader.LoaderBase.image**

Load a image using the Loader. A ProxyImage is returned with a
loading image. You can use it as follows:

In order to cancel all background loading, call *Loader.stop()*.

**kivy.loader.LoaderBase.loading_image**

Image used for loading.
You can change it by doing:

Changed in version 1.6.0:Not readonly anymore.

**kivy.loader.LoaderBase.max_upload_per_frame**

The number of images to upload per frame. By default, we’ll
upload only 2 images to the GPU per frame. If you are uploading many
small images, you can easily increase this parameter to 10 or more.
If you are loading multiple full HD images, the upload time may have
consequences and block the application. If you want a
smooth experience, use the default.
As a matter of fact, a Full-HD RGB image will take ~6MB in memory,
so it may take time. If you have activated mipmap=True too, then the
GPU must calculate the mipmap of these big images too, in real time.
Then it may be best to reduce the [`max_upload_per_frame`](https://kivy.org/doc/stable/#kivy.loader.LoaderBase.max_upload_per_frame) to 1
or 2. If you want to get rid of that (or reduce it a lot), take a
look at the DDS format.
New in version 1.6.0.

**kivy.loader.LoaderBase.num_workers**

Number of workers to use while loading (used only if the loader
implementation supports it). This setting impacts the loader only on
initialization. Once the loader is started, the setting has no impact:

The default value is 2 for giving a smooth user experience. You could
increase the number of workers, then all the images will be loaded faster,
but the user will not been able to use the application while loading.
Prior to 1.6.0, the default number was 20, and loading many full-hd images
was completely blocking the application.
New in version 1.6.0.

**kivy.loader.LoaderBase.pause**

Pause the loader, can be useful during interactions.
New in version 1.6.0.

**kivy.loader.LoaderBase.resume**

Resume the loader, after a [`pause()`](https://kivy.org/doc/stable/#kivy.loader.LoaderBase.pause).
New in version 1.6.0.

**kivy.loader.LoaderBase.run**

Main loop for the loader.

**kivy.loader.LoaderBase.start**

Start the loader thread/process.

**kivy.loader.LoaderBase.stop**

Stop the loader thread/process.

**kivy.loader.ProxyImage**

Bases: [`kivy.core.image.Image`](https://kivy.org/doc/stable/api-kivy.core.image.html#kivy.core.image.Image)
Image returned by the Loader.image() function.

---

## API - [`kivy.logger`](https://kivy.org/doc/stable/api-kivy.logger.html)

**kivy.logger.ColonSplittingLogRecord**

Bases: `logging.LogRecord`
Clones an existing logRecord, but reformats the message field
if it contains a colon.
New in version 2.2.0.

**kivy.logger.ColoredLogRecord**

Bases: `logging.LogRecord`
Clones an existing logRecord, but reformats the levelname to add
color, and the message to add bolding (where indicated by $BOLD
and $RESET in the message).
New in version 2.2.0.

**kivy.logger.ConsoleHandler**

Bases: `logging.StreamHandler`
Emits records to a stream (by default, stderr).
However, if the msg starts with “stderr:” it is not formatted, but
written straight to the stream.
New in version 2.2.0.

**kivy.logger.ConsoleHandler.filter**

Determine if a record is loggable by consulting all the filters.
The default is to allow the record to be logged; any filter can veto
this by returning a false value.
If a filter attached to a handler returns a log record instance,
then that instance is used in place of the original log record in
any further processing of the event by that handler.
If a filter returns any other true value, the original log record
is used in any further processing of the event by that handler.
If none of the filters return false values, this method returns
a log record.
If any of the filters return a false value, this method returns
a false value.
Changed in version 3.2:Allow filters to be just callables.
Changed in version 3.12:Allow filters to return a LogRecord instead of
modifying it in place.

**kivy.logger.FileHandler**

Bases: `logging.Handler`

**kivy.logger.FileHandler.emit**

Do whatever it takes to actually log the specified logging record.
This version is intended to be implemented by subclasses and so
raises a NotImplementedError.

**kivy.logger.FileHandler.purge_logs**

Purge logs which exceed the maximum amount of log files,
starting with the oldest creation timestamp (or edit-timestamp on Linux)

**kivy.logger.KivyFormatter**

Bases: `logging.Formatter`
Split out first field in message marked with a colon,
and either apply terminal color codes to the record, or strip
out color markup if colored logging is not available.
New in version 2.2.0.

**kivy.logger.KivyFormatter.format**

Format the specified record as text.
The record’s attribute dictionary is used as the operand to a
string formatting operation which yields the returned string.
Before formatting the dictionary, a couple of preparatory steps
are carried out. The message attribute of the record is computed
using LogRecord.getMessage(). If the formatting string uses the
time (as determined by a call to usesTime(), formatTime() is
called to format the event time. If there is exception information,
it is formatted using formatException() and appended to the message.

**kivy.logger.LoggerHistory**

Bases: `logging.Handler`

**kivy.logger.LoggerHistory.emit**

Do whatever it takes to actually log the specified logging record.
This version is intended to be implemented by subclasses and so
raises a NotImplementedError.

**kivy.logger.LoggerHistory.flush**

Ensure all logging output has been flushed.
This version does nothing and is intended to be implemented by
subclasses.

**kivy.logger.ProcessingStream**

Bases: `builtins.object`
Stream-like object that takes each completed line written to it,
adds a given prefix, and applies the given function to it.
New in version 2.2.0.

**kivy.logger.UncoloredLogRecord**

Bases: `logging.LogRecord`
Clones an existing logRecord, but reformats the message
to remove $BOLD/$RESET markup.
New in version 2.2.0.

**kivy.logger.add_kivy_handlers**

Add Kivy-specific handlers to a logger.
New in version 2.2.0.

**kivy.logger.is_color_terminal**

Detect whether the environment supports color codes in output.
New in version 2.2.0.

---

## API - [`kivy.metrics`](https://kivy.org/doc/stable/api-kivy.metrics.html)

**kivy.metrics.Metrics**

The metrics object storing the window scaling factors.
New in version 1.7.0.
Changed in version 2.1.0:[`Metrics`](https://kivy.org/doc/stable/#kivy.metrics.Metrics) is now a Context registered variable (like e.g.
[`Clock`](https://kivy.org/doc/stable/api-kivy.clock.html#kivy.clock.Clock)).

**kivy.metrics.MetricsBase**

Bases: [`kivy.event.EventDispatcher`](https://kivy.org/doc/stable/api-kivy.event.html#kivy.event.EventDispatcher)
Class that contains the default attributes for Metrics. Don’t use this
class directly, but use the Metrics instance.

**kivy.metrics.MetricsBase.cm**

The scaling factor that converts from centimeters to pixels.
[`cm`](https://kivy.org/doc/stable/#kivy.metrics.cm) is a [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) containing the
factor. E.g in KV: `width: self.texture_size[0] + 10 * Metrics.cm` will
update width when [`cm`](https://kivy.org/doc/stable/#kivy.metrics.cm) changes from a screen configuration change.

**kivy.metrics.MetricsBase.density**

The density of the screen.
This value is 1 by default on desktops but varies on android depending on
the screen.
[`density`](https://kivy.org/doc/stable/#kivy.metrics.MetricsBase.density) is a [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) and can be
set to change the value. But, the [`density`](https://kivy.org/doc/stable/#kivy.metrics.MetricsBase.density) is reloaded and reset if
we got it from the Window and the Window `density` changed.

**kivy.metrics.MetricsBase.dp**

The scaling factor that converts from density-independent pixels to
pixels.
[`dp`](https://kivy.org/doc/stable/#kivy.metrics.dp) is a [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) containing the
factor. E.g in KV: `width: self.texture_size[0] + 10 * Metrics.dp` will
update width when [`dp`](https://kivy.org/doc/stable/#kivy.metrics.dp) changes from a screen configuration change.

**kivy.metrics.MetricsBase.dpi**

The DPI of the screen.
Depending on the platform, the DPI can be taken from the Window provider
(Desktop mainly) or from a platform-specific module (like android/ios).
[`dpi`](https://kivy.org/doc/stable/#kivy.metrics.MetricsBase.dpi) is a [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) and can be
set to change the value. But, the [`density`](https://kivy.org/doc/stable/#kivy.metrics.MetricsBase.density) is reloaded and reset if
we got it from the Window and the Window `dpi` changed.

**kivy.metrics.MetricsBase.dpi_rounded**

Return the [`dpi`](https://kivy.org/doc/stable/#kivy.metrics.MetricsBase.dpi) of the screen, rounded to the nearest of 120,
160, 240 or 320.
[`dpi_rounded`](https://kivy.org/doc/stable/#kivy.metrics.MetricsBase.dpi_rounded) is a [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) and
updates when [`dpi`](https://kivy.org/doc/stable/#kivy.metrics.MetricsBase.dpi) changes.

**kivy.metrics.MetricsBase.fontscale**

The fontscale user preference.
This value is 1 by default but can vary between 0.8 and 1.2.
[`fontscale`](https://kivy.org/doc/stable/#kivy.metrics.MetricsBase.fontscale) is a [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) and can be
set to change the value.

**kivy.metrics.MetricsBase.inch**

The scaling factor that converts from inches to pixels.
[`inch`](https://kivy.org/doc/stable/#kivy.metrics.inch) is a [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) containing the
factor. E.g in KV: `width: self.texture_size[0] + 10 * Metrics.inch` will
update width when [`inch`](https://kivy.org/doc/stable/#kivy.metrics.inch) changes from a screen configuration change.

**kivy.metrics.MetricsBase.mm**

The scaling factor that converts from millimeters to pixels.
[`mm`](https://kivy.org/doc/stable/#kivy.metrics.mm) is a [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) containing the
factor. E.g in KV: `width: self.texture_size[0] + 10 * Metrics.mm` will
update width when [`mm`](https://kivy.org/doc/stable/#kivy.metrics.mm) changes from a screen configuration change.

**kivy.metrics.MetricsBase.pt**

The scaling factor that converts from points to pixels.
[`pt`](https://kivy.org/doc/stable/#kivy.metrics.pt) is a [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) containing the
factor. E.g in KV: `width: self.texture_size[0] + 10 * Metrics.pt` will
update width when [`pt`](https://kivy.org/doc/stable/#kivy.metrics.pt) changes from a screen configuration change.

**kivy.metrics.MetricsBase.reset_dpi**

Resets the dpi (and possibly density) to the platform values,
overwriting any manually set values.

**kivy.metrics.MetricsBase.reset_metrics**

Resets the dpi/density/fontscale to the platform values, overwriting
any manually set values.

**kivy.metrics.MetricsBase.sp**

The scaling factor that converts from scale-independent pixels to
pixels.
[`sp`](https://kivy.org/doc/stable/#kivy.metrics.sp) is a [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) containing the
factor. E.g in KV: `width: self.texture_size[0] + 10 * Metrics.sp` will
update width when [`sp`](https://kivy.org/doc/stable/#kivy.metrics.sp) changes from a screen configuration change.

**kivy.metrics.cm**

Convert from centimeters to pixels

**kivy.metrics.dp**

Convert from density-independent pixels to pixels

**kivy.metrics.dpi2px**

Converts the value according to the ext.

**kivy.metrics.inch**

Convert from inches to pixels

**kivy.metrics.mm**

Convert from millimeters to pixels

**kivy.metrics.pt**

Convert from points to pixels

**kivy.metrics.sp**

Convert from scale-independent pixels to pixels

---

## API - [`kivy.modules.console`](https://kivy.org/doc/stable/api-kivy.modules.console.html)

**kivy.modules.console.Console**

Bases: [`kivy.uix.relativelayout.RelativeLayout`](https://kivy.org/doc/stable/api-kivy.uix.relativelayout.html#kivy.uix.relativelayout.RelativeLayout)
Console interface
This widget is created by create_console(), when the module is loaded.
During that time, you can add addons on the console to extend the
functionalities, or add your own application stats / debugging module.

**kivy.modules.console.Console.activated**

True if the Console is activated (showed)

**kivy.modules.console.Console.add_panel**

Add a new panel in the Console.
cb_activate is a callable that will be called when the panel is
activated by the user.
cb_deactivate is a callable that will be called when the panel is
deactivated or when the console will hide.
cb_refresh is an optional callable that is called if the user
click again on the button for display the panel
When activated, it’s up to the panel to display a content in the
Console by using [`set_content()`](https://kivy.org/doc/stable/#kivy.modules.console.Console.set_content).

**kivy.modules.console.Console.add_toolbar_widget**

Add a widget in the top left toolbar of the Console.
Use right=True if you wanna add the widget at the right instead.

**kivy.modules.console.Console.addons**

Array of addons that will be created at Console creation

**kivy.modules.console.Console.highlight_at**

Select a widget from a x/y window coordinate.
This is mostly used internally when Select mode is activated

**kivy.modules.console.Console.inspect_enabled**

Indicate if the inspector inspection is enabled. If yes, the next
touch down will select a the widget under the touch

**kivy.modules.console.Console.mode**

Display mode of the Console, either docked at the bottom, or as a
floating window.

**kivy.modules.console.Console.on_touch_down**

Receive a touch down event.

**kivy.modules.console.Console.on_touch_move**

Receive a touch move event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivy.org/doc/stable/#kivy.modules.console.Console.on_touch_down) for more information.

**kivy.modules.console.Console.on_touch_up**

Receive a touch up event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivy.org/doc/stable/#kivy.modules.console.Console.on_touch_down) for more information.

**kivy.modules.console.Console.pick**

Pick a widget at x/y, given a root widget

**kivy.modules.console.Console.remove_toolbar_widget**

Remove a widget from the toolbar

**kivy.modules.console.Console.set_content**

Replace the Console content with a new one.

**kivy.modules.console.Console.widget**

Current widget being selected

**kivy.modules.console.ConsoleAddon**

Bases: `builtins.object`
Base class for implementing addons

**kivy.modules.console.ConsoleAddon.activate**

Method called when the addon is activated by the console
(when the console is displayed)

**kivy.modules.console.ConsoleAddon.console**

Console instance

**kivy.modules.console.ConsoleAddon.deactivate**

Method called when the addon is deactivated by the console
(when the console is hidden)

**kivy.modules.console.ConsoleAddon.init**

Method called when the addon is instantiated by the Console

**kivy.modules.console.ConsoleButton**

Bases: [`kivy.uix.button.Button`](https://kivy.org/doc/stable/api-kivy.uix.button.html#kivy.uix.button.Button)
Button specialized for the Console

**kivy.modules.console.ConsoleLabel**

Bases: [`kivy.uix.label.Label`](https://kivy.org/doc/stable/api-kivy.uix.label.html#kivy.uix.label.Label)
LabelButton specialized for the Console

**kivy.modules.console.ConsoleToggleButton**

Bases: [`kivy.uix.togglebutton.ToggleButton`](https://kivy.org/doc/stable/api-kivy.uix.togglebutton.html#kivy.uix.togglebutton.ToggleButton)
ToggleButton specialized for the Console

**kivy.modules.console.start**

Create an Console instance attached to the *ctx* and bound to the
Window’s [`on_keyboard()`](https://kivy.org/doc/stable/api-kivy.core.window.html#kivy.core.window.WindowBase.on_keyboard) event for
capturing the keyboard shortcut.

**kivy.modules.console.stop**

Stop and unload any active Inspectors for the given *ctx*.

---

## API - [`kivy.modules.inspector`](https://kivy.org/doc/stable/api-kivy.modules.inspector.html)

**kivy.modules.inspector.create_inspector**

Create an Inspector instance attached to the *ctx* and bound to the
Window’s [`on_keyboard()`](https://kivy.org/doc/stable/api-kivy.core.window.html#kivy.core.window.WindowBase.on_keyboard) event for
capturing the keyboard shortcut.

**kivy.modules.inspector.stop**

Stop and unload any active Inspectors for the given *ctx*.

---

## API - [`kivy.modules.joycursor`](https://kivy.org/doc/stable/api-kivy.modules.joycursor.html)

**kivy.modules.joycursor.create_joycursor**

Create a JoyCursor instance attached to the *ctx* and bound to the
Window’s [`on_keyboard()`](https://kivy.org/doc/stable/api-kivy.core.window.html#kivy.core.window.WindowBase.on_keyboard) event for
capturing the keyboard shortcuts.

**kivy.modules.joycursor.stop**

Stop and unload any active JoyCursors for the given *ctx*.

---

## API - [`kivy.multistroke`](https://kivy.org/doc/stable/api-kivy.multistroke.html)

**kivy.multistroke.Candidate**

Bases: `builtins.object`
Represents a set of unistroke paths of user input, ie data to be matched
against a [`UnistrokeTemplate`](https://kivy.org/doc/stable/#kivy.multistroke.UnistrokeTemplate) object using the Protractor algorithm.
By default, data is precomputed to match both rotation bounded and fully
invariant [`UnistrokeTemplate`](https://kivy.org/doc/stable/#kivy.multistroke.UnistrokeTemplate) objects.

Note that you WILL get errors if you set a skip-flag and then attempt to
retrieve the data.

**kivy.multistroke.Candidate.add_stroke**

Add a stroke to the candidate; this will invalidate all
previously computed vectors

**kivy.multistroke.Candidate.get_angle_similarity**

(Internal use only) Compute the angle similarity between this
Candidate and a UnistrokeTemplate object. Returns a number that
represents the angle similarity (lower is more similar).

**kivy.multistroke.Candidate.get_protractor_vector**

(Internal use only) Return vector for comparing to a
UnistrokeTemplate with Protractor

**kivy.multistroke.Candidate.get_start_unit_vector**

(Internal use only) Get the start vector for this Candidate,
with the path resampled to numpoints points. This is the first
step in the matching process. It is compared to a
UnistrokeTemplate object’s start vector to determine angle
similarity.

**kivy.multistroke.Candidate.prepare**

Prepare the Candidate vectors. self.strokes is combined to a single
unistroke (connected end-to-end), resampled to `numpoints`
points, and then the vectors are calculated and stored in self.db (for
use by get_distance and get_angle_similarity)

**kivy.multistroke.MultistrokeGesture**

Bases: `builtins.object`
[`MultistrokeGesture`](https://kivy.org/doc/stable/#kivy.multistroke.MultistrokeGesture) represents a gesture. It maintains a set of
strokes and generates unistroke (ie [`UnistrokeTemplate`](https://kivy.org/doc/stable/#kivy.multistroke.UnistrokeTemplate))
permutations that are used for evaluating candidates against this gesture
later.

**kivy.multistroke.MultistrokeGesture.add_stroke**

Add a stroke to the self.strokes list. If permute is True, the
[`permute()`](https://kivy.org/doc/stable/#kivy.multistroke.MultistrokeGesture.permute) method is called to generate new unistroke templates

**kivy.multistroke.MultistrokeGesture.get_distance**

Compute the distance from this Candidate to a UnistrokeTemplate.
Returns the Cosine distance between the stroke paths.
numpoints will prepare both the UnistrokeTemplate and Candidate path
to n points (when necessary), you probably don’t want to do this.

**kivy.multistroke.MultistrokeGesture.match_candidate**

Match a given candidate against this MultistrokeGesture object. Will
test against all templates and report results as a list of four
items:

**kivy.multistroke.MultistrokeGesture.permute**

Generate all possible unistroke permutations from self.strokes and
save the resulting list of UnistrokeTemplate objects in self.templates.
Quote from [http://faculty.washington.edu/wobbrock/pubs/gi-10.2.pdf](http://faculty.washington.edu/wobbrock/pubs/gi-10.2.pdf)

See section 4.1: “$N Algorithm” of the linked paper for details.

**kivy.multistroke.ProgressTracker**

Bases: [`kivy.event.EventDispatcher`](https://kivy.org/doc/stable/api-kivy.event.html#kivy.event.EventDispatcher)
Represents an ongoing (or completed) search operation. Instantiated and
returned by the [`Recognizer.recognize()`](https://kivy.org/doc/stable/#kivy.multistroke.Recognizer.recognize) method when it is called. The
results attribute is a dictionary that is updated as the recognition
operation progresses.

**kivy.multistroke.ProgressTracker.best**

Return the best match found by recognize() so far. It returns a
dictionary with three keys, ‘name’, ‘dist’ and ‘score’ representing
the template’s name, distance (from candidate path) and the
computed score value. This is a Python property.

**kivy.multistroke.ProgressTracker.progress**

Returns the progress as a float, 0 is 0% done, 1 is 100%. This
is a Python property.

**kivy.multistroke.ProgressTracker.stop**

Raises a stop flag that is checked by the search process. It will
be stopped on the next clock tick (if it is still running).

**kivy.multistroke.Recognizer**

Bases: [`kivy.event.EventDispatcher`](https://kivy.org/doc/stable/api-kivy.event.html#kivy.event.EventDispatcher)
[`Recognizer`](https://kivy.org/doc/stable/#kivy.multistroke.Recognizer) provides a gesture database with matching
facilities.

**kivy.multistroke.Recognizer.add_gesture**

Add a new gesture to the database. This will instantiate a new
[`MultistrokeGesture`](https://kivy.org/doc/stable/#kivy.multistroke.MultistrokeGesture) with strokes and append it to self.db.

**kivy.multistroke.Recognizer.export_gesture**

Export a list of [`MultistrokeGesture`](https://kivy.org/doc/stable/#kivy.multistroke.MultistrokeGesture) objects. Outputs a
base64-encoded string that can be decoded to a Python list with
the [`parse_gesture()`](https://kivy.org/doc/stable/#kivy.multistroke.Recognizer.parse_gesture) function or imported directly to
`self.db` using [`Recognizer.import_gesture()`](https://kivy.org/doc/stable/#kivy.multistroke.Recognizer.import_gesture). If
filename is specified, the output is written to disk, otherwise
returned.
This method accepts optional [`Recognizer.filter()`](https://kivy.org/doc/stable/#kivy.multistroke.Recognizer.filter) arguments.

**kivy.multistroke.Recognizer.filter**

[`filter()`](https://kivy.org/doc/stable/#kivy.multistroke.Recognizer.filter) returns a subset of objects in `self.db`,
according to given criteria. This is used by many other methods of
the [`Recognizer`](https://kivy.org/doc/stable/#kivy.multistroke.Recognizer); the arguments below can for example be
used when calling [`Recognizer.recognize()`](https://kivy.org/doc/stable/#kivy.multistroke.Recognizer.recognize) or
[`Recognizer.export_gesture()`](https://kivy.org/doc/stable/#kivy.multistroke.Recognizer.export_gesture). You normally don’t need to call
this directly.

**kivy.multistroke.Recognizer.import_gesture**

Import a list of gestures as formatted by [`export_gesture()`](https://kivy.org/doc/stable/#kivy.multistroke.Recognizer.export_gesture).
One of data or filename must be specified.
This method accepts optional [`Recognizer.filter()`](https://kivy.org/doc/stable/#kivy.multistroke.Recognizer.filter) arguments,
if none are specified then all gestures in specified data are
imported.

**kivy.multistroke.Recognizer.parse_gesture**

Parse data formatted by export_gesture(). Returns a list of
[`MultistrokeGesture`](https://kivy.org/doc/stable/#kivy.multistroke.MultistrokeGesture) objects. This is used internally by
[`import_gesture()`](https://kivy.org/doc/stable/#kivy.multistroke.Recognizer.import_gesture), you normally don’t need to call this
directly.

**kivy.multistroke.Recognizer.prepare_templates**

This method is used to prepare [`UnistrokeTemplate`](https://kivy.org/doc/stable/#kivy.multistroke.UnistrokeTemplate) objects
within the gestures in self.db. This is useful if you want to minimize
punishment of lazy resampling by preparing all vectors in advance. If
you do this before a call to [`Recognizer.export_gesture()`](https://kivy.org/doc/stable/#kivy.multistroke.Recognizer.export_gesture), you
will have the vectors computed when you load the data later.
This method accepts optional [`Recognizer.filter()`](https://kivy.org/doc/stable/#kivy.multistroke.Recognizer.filter) arguments.
force_numpoints, if specified, will prepare all templates to the
given number of points (instead of each template’s preferred n; ie
`UnistrokeTemplate.numpoints`). You normally don’t want to
do this.

**kivy.multistroke.Recognizer.recognize**

Search for gestures matching strokes. Returns a
[`ProgressTracker`](https://kivy.org/doc/stable/#kivy.multistroke.ProgressTracker) instance.
This method accepts optional [`Recognizer.filter()`](https://kivy.org/doc/stable/#kivy.multistroke.Recognizer.filter) arguments.

**kivy.multistroke.Recognizer.transfer_gesture**

Transfers [`MultistrokeGesture`](https://kivy.org/doc/stable/#kivy.multistroke.MultistrokeGesture) objects from
`Recognizer.db` to another [`Recognizer`](https://kivy.org/doc/stable/#kivy.multistroke.Recognizer) instance tgt.
This method accepts optional [`Recognizer.filter()`](https://kivy.org/doc/stable/#kivy.multistroke.Recognizer.filter) arguments.

**kivy.multistroke.UnistrokeTemplate**

Bases: `builtins.object`
Represents a (uni)stroke path as a list of Vectors. Normally, this class
is instantiated by MultistrokeGesture and not by the programmer directly.
However, it is possible to manually compose UnistrokeTemplate objects.

**kivy.multistroke.UnistrokeTemplate.add_point**

Add a point to the unistroke/path. This invalidates all previously
computed vectors.

**kivy.multistroke.UnistrokeTemplate.prepare**

This function prepares the UnistrokeTemplate for matching given a
target number of points (for resample). 16 is optimal.

---

## API - [`kivy.network.urlrequest`](https://kivy.org/doc/stable/api-kivy.network.urlrequest.html)

**kivy.network.urlrequest.UrlRequest**

alias of [`UrlRequestUrllib`](https://kivy.org/doc/stable/#kivy.network.urlrequest.UrlRequestUrllib)

**kivy.network.urlrequest.UrlRequestBase**

Bases: `threading.Thread`
A UrlRequest. See module documentation for usage.
Changed in version 1.5.1:Add debug parameter
Changed in version 1.0.10:Add method parameter
Changed in version 1.8.0:Parameter decode added.
Parameter file_path added.
Parameter on_redirect added.
Parameter on_failure added.
Changed in version 1.9.1:Parameter ca_file added.
Parameter verify added.
Changed in version 1.10.0:Parameters proxy_host, proxy_port and proxy_headers added.
Changed in version 1.11.0:Parameters on_cancel added.
Changed in version 2.2.0:Parameters on_finish added.
Parameters auth added.

**kivy.network.urlrequest.UrlRequestBase.cancel**

Cancel the current request. It will be aborted, and the result
will not be dispatched. Once cancelled, the callback on_cancel will
be called.
New in version 1.11.0.

**kivy.network.urlrequest.UrlRequestBase.chunk_size**

Return the size of a chunk, used only in “progress” mode (when
on_progress callback is set.)

**kivy.network.urlrequest.UrlRequestBase.decode_result**

Decode the result fetched from url according to his Content-Type.
Currently supports only application/json.

**kivy.network.urlrequest.UrlRequestBase.error**

Return the error of the request.
This value is not determined until the request is completed.

**kivy.network.urlrequest.UrlRequestBase.is_finished**

Return True if the request has finished, whether it’s a
success or a failure.

**kivy.network.urlrequest.UrlRequestBase.req_body**

Request body passed in __init__

**kivy.network.urlrequest.UrlRequestBase.req_headers**

Request headers passed in __init__

**kivy.network.urlrequest.UrlRequestBase.resp_headers**

If the request has been completed, return a dictionary containing
the headers of the response. Otherwise, it will return None.

**kivy.network.urlrequest.UrlRequestBase.resp_status**

Return the status code of the response if the request is complete,
otherwise return None.

**kivy.network.urlrequest.UrlRequestBase.result**

Return the result of the request.
This value is not determined until the request is finished.

**kivy.network.urlrequest.UrlRequestBase.run**

Method representing the thread’s activity.
You may override this method in a subclass. The standard run() method
invokes the callable object passed to the object’s constructor as the
target argument, if any, with sequential and keyword arguments taken
from the args and kwargs arguments, respectively.

**kivy.network.urlrequest.UrlRequestBase.url**

Url of the request

**kivy.network.urlrequest.UrlRequestBase.wait**

Wait for the request to finish (until [`resp_status`](https://kivy.org/doc/stable/#kivy.network.urlrequest.UrlRequestBase.resp_status) is not
None)

New in version 1.1.0.

**kivy.network.urlrequest.UrlRequestRequests**

Bases: [`kivy.network.urlrequest.UrlRequestBase`](https://kivy.org/doc/stable/#kivy.network.urlrequest.UrlRequestBase)

**kivy.network.urlrequest.UrlRequestUrllib**

Bases: [`kivy.network.urlrequest.UrlRequestBase`](https://kivy.org/doc/stable/#kivy.network.urlrequest.UrlRequestBase)

---

## API - [`kivy.parser`](https://kivy.org/doc/stable/api-kivy.parser.html)

**kivy.parser.parse_bool**

Parse a string to a boolean, ignoring case. “true”/”1” is True,
“false”/”0” is False. Anything else throws an exception.

**kivy.parser.parse_color**

Parse a string to a kivy color. Supported formats:
rgb(r, g, b)
rgba(r, g, b, a)
rgb
rgba
rrggbb
rrggbbaa
For hexadecimal values, you case also use:
#rgb
#rgba
#rrggbb
#rrggbbaa

**kivy.parser.parse_filename**

Parse a filename and search for it using resource_find().
If found, the resource path is returned, otherwise return the unmodified
filename (as specified by the caller).

**kivy.parser.parse_float**

alias of `float`

**kivy.parser.parse_float4**

Parse a string to a list of exactly 4 floats.

**kivy.parser.parse_int**

alias of `int`

**kivy.parser.parse_int2**

Parse a string to a list of exactly 2 integers.

**kivy.parser.parse_string**

Parse a string to a string (removing single and double quotes).

---

## API - [`kivy.properties`](https://kivy.org/doc/stable/api-kivy.properties.html)

**kivy.properties.AliasProperty**

Bases: [`kivy.properties.Property`](https://kivy.org/doc/stable/#kivy.properties.Property)
If you don’t find a Property class that fits to your needs, you can make
your own by creating custom Python getter and setter methods.
Example from kivy/uix/widget.py where x and width are instances of
[`NumericProperty`](https://kivy.org/doc/stable/#kivy.properties.NumericProperty):

If x were a non Kivy property then you have to return True from setter
to dispatch new value of right:

Usually bind list should contain all Kivy properties used in getter
method. If you return True it will cause a dispatch which one should do
when the property value has changed, but keep in mind that the property
could already have dispatched the changed value if a kivy property the
alias property is bound was set in the setter, causing a second dispatch
if the setter returns True.
If you want to cache the value returned by getter then pass cache=True.
This way getter will only be called if new value is set or one of the
binded properties changes. In both cases new value of alias property will
be cached again.
To make property readonly pass None as setter. This way AttributeError
will be raised on every set attempt:

Changed in version 1.9.0:rebind has been introduced.
Changed in version 1.4.0:Parameter cache added.

**kivy.properties.AliasProperty.get**

**kivy.properties.AliasProperty.link_deps**

**kivy.properties.AliasProperty.link_eagerly**

**kivy.properties.AliasProperty.rebind**

rebind: ‘int’

**kivy.properties.AliasProperty.set**

**kivy.properties.AliasProperty.trigger_change**

**kivy.properties.BooleanProperty**

Bases: [`kivy.properties.Property`](https://kivy.org/doc/stable/#kivy.properties.Property)

**kivy.properties.BoundedNumericProperty**

Bases: [`kivy.properties.Property`](https://kivy.org/doc/stable/#kivy.properties.Property)
maximum bound – within a numeric range.

**kivy.properties.BoundedNumericProperty.bounds**

Return min/max of the value.
New in version 1.0.9.

**kivy.properties.BoundedNumericProperty.get_max**

Return the maximum value acceptable for the BoundedNumericProperty
in obj. Return None if no maximum value is set. Check
[`get_min`](https://kivy.org/doc/stable/#kivy.properties.BoundedNumericProperty.get_min) for a usage example.
New in version 1.1.0.

**kivy.properties.BoundedNumericProperty.get_min**

Return the minimum value acceptable for the BoundedNumericProperty
in obj. Return None if no minimum value is set:

New in version 1.1.0.

**kivy.properties.BoundedNumericProperty.set_max**

Change the maximum value acceptable for the BoundedNumericProperty,
only for the obj instance. Set to None if you want to disable it.
Check [`set_min`](https://kivy.org/doc/stable/#kivy.properties.BoundedNumericProperty.set_min) for a usage example.

New in version 1.1.0.

**kivy.properties.BoundedNumericProperty.set_min**

Change the minimum value acceptable for the BoundedNumericProperty,
only for the obj instance. Set to None if you want to disable it:

New in version 1.1.0.

**kivy.properties.ColorProperty**

Bases: [`kivy.properties.Property`](https://kivy.org/doc/stable/#kivy.properties.Property)
a collection of 3 or 4 float values between 0-1 (kivy default)
a string in the format #rrggbb or #rrggbbaa
a string representing color name (eg. ‘red’, ‘yellow’, ‘green’)
Object `colormap` is used to retrieve color from color
name and names definitions can be found at this
[link](https://www.w3.org/TR/SVG11/types.html#ColorKeywords). Color can
be assigned in different formats, but it will be returned as
`ObservableList` of 4 float elements with values
between 0-1.

New in version 1.10.0.
Changed in version 2.0.0:Color value will be dispatched when set through indexing or slicing,
but when setting with slice you must ensure that slice has 4 components
with float values between 0-1.
Assingning color name as value is now supported.
Value None is allowed as default value for property.

**kivy.properties.ConfigParserProperty**

Bases: [`kivy.properties.Property`](https://kivy.org/doc/stable/#kivy.properties.Property)
of a [`ConfigParser`](https://kivy.org/doc/stable/api-kivy.config.html#kivy.config.ConfigParser) as well as to bind the ConfigParser
values to other properties.
A ConfigParser is composed of sections, where each section has a number of
keys and values associated with these keys. ConfigParserProperty lets
you automatically listen to and change the values of specified keys based
on other kivy properties.
For example, say we want to have a TextInput automatically write
its value, represented as an int, in the info section of a ConfigParser.
Also, the textinputs should update its values from the ConfigParser’s
fields. Finally, their values should be displayed in a label. In py:

The above code creates a property that is connected to the number key in
the info section of the ConfigParser named example. Initially, this
ConfigParser doesn’t exist. Then, in __init__, a ConfigParser is created
with name example, which is then automatically linked with this property.
then in kv:

You’ll notice that we have to do text: str(info.number), this is because
the value of this property is always an int, because we specified int as
the val_type. However, we can assign anything to the property, e.g.
number: number.text which assigns a string, because it is instantly
converted with the val_type callback.

New in version 1.9.0.

**kivy.properties.ConfigParserProperty.link_deps**

**kivy.properties.ConfigParserProperty.set**

**kivy.properties.ConfigParserProperty.set_config**

Sets the ConfigParser object to be used by this property. Normally,
the ConfigParser is set when initializing the Property using the
config parameter.

**kivy.properties.DictProperty**

Bases: [`kivy.properties.Property`](https://kivy.org/doc/stable/#kivy.properties.Property)

Changed in version 1.9.0:rebind has been introduced.

**kivy.properties.DictProperty.link**

**kivy.properties.DictProperty.rebind**

rebind: ‘int’

**kivy.properties.DictProperty.set**

**kivy.properties.ListProperty**

Bases: [`kivy.properties.Property`](https://kivy.org/doc/stable/#kivy.properties.Property)

**kivy.properties.ListProperty.link**

**kivy.properties.ListProperty.set**

**kivy.properties.NumericProperty**

Bases: [`kivy.properties.Property`](https://kivy.org/doc/stable/#kivy.properties.Property)
It only accepts the int or float numeric data type or a string that can be
converted to a number as shown below. For other numeric types use ObjectProperty
or use errorhandler to convert it to an int/float.
It does not support numpy numbers so they must be manually converted to int/float.
E.g. `widget.num = np.arange(4)[0]` will raise an exception. Numpy arrays are not
supported at all, even by ObjectProperty because their comparison does not return
a bool. But if you must use a Kivy property, use a ObjectProperty with `comparator`
set to `np.array_equal`. E.g.:

Changed in version 1.4.1:NumericProperty can now accept custom text and tuple value to indicate a
type, like “in”, “pt”, “px”, “cm”, “mm”, in the format: ‘10pt’ or (10,
‘pt’).

**kivy.properties.NumericProperty.get_format**

Return the format used for Numeric calculation. Default is px (mean
the value have not been changed at all). Otherwise, it can be one of
‘in’, ‘pt’, ‘cm’, ‘mm’.

**kivy.properties.ObjectProperty**

Bases: [`kivy.properties.Property`](https://kivy.org/doc/stable/#kivy.properties.Property)

Changed in version 1.9.0:rebind has been introduced.
Changed in version 1.7.0:baseclass parameter added.

**kivy.properties.ObjectProperty.rebind**

rebind: ‘int’

**kivy.properties.OptionProperty**

Bases: [`kivy.properties.Property`](https://kivy.org/doc/stable/#kivy.properties.Property)
options.
If the string set in the property is not in the list of valid options
(passed at property creation time), a ValueError exception will be raised.

For example:

**kivy.properties.OptionProperty.options**

Return the options available.
New in version 1.0.9.

**kivy.properties.Property**

Bases: `builtins.object`
This class handles all the basic setters and getters, None type handling,
the observer list and storage initialisation. This class should not be
directly instantiated.
By default, a [`Property`](https://kivy.org/doc/stable/#kivy.properties.Property) always takes a default value:

The default value must be a value that agrees with the Property type. For
example, you can’t set a list to a [`StringProperty`](https://kivy.org/doc/stable/#kivy.properties.StringProperty) because the
StringProperty will check the default value.
None is a special case: you can set the default value of a Property to
None, but you can’t set None to a property afterward. If you really want
to do that, you must declare the Property with allownone=True:

Changed in version 1.4.2:Parameters errorhandler and errorvalue added
Changed in version 1.9.0:Parameter force_dispatch added
Changed in version 1.11.0:Parameter deprecated added

**kivy.properties.Property.bind**

Add a new observer to be called only when the value is changed.

**kivy.properties.Property.defaultvalue**

defaultvalue: object

**kivy.properties.Property.dispatch**

Dispatch the value change to all observers.
Changed in version 1.1.0:The method is now accessible from Python.
This can be used to force the dispatch of the property, even if the
value didn’t change:

**kivy.properties.Property.fbind**

Similar to bind, except it doesn’t check if the observer already
exists. It also expands and forwards largs and kwargs to the callback.
funbind or unbind_uid should be called when unbinding.
It returns a unique positive uid to be used with unbind_uid.

**kivy.properties.Property.funbind**

Remove the observer from our widget observer list bound with
fbind. It removes the first match it finds, as opposed to unbind
which searches for all matches.

**kivy.properties.Property.get**

Return the value of the property.

**kivy.properties.Property.link**

Link the instance with its real name.

When a widget is defined and uses a [`Property`](https://kivy.org/doc/stable/#kivy.properties.Property) class, the
creation of the property object happens, but the instance doesn’t know
anything about its name in the widget class:

In this example, the uid will be a NumericProperty() instance, but the
property instance doesn’t know its name. That’s why [`link()`](https://kivy.org/doc/stable/#kivy.properties.Property.link) is
used in Widget.__new__. The link function is also used to create the
storage space of the property for this specific widget instance.

**kivy.properties.Property.link_deps**

**kivy.properties.Property.link_eagerly**

**kivy.properties.Property.set**

Set a new value for the property.

**kivy.properties.Property.set_name**

**kivy.properties.Property.unbind**

Remove the observer from our widget observer list.

**kivy.properties.Property.unbind_uid**

Remove the observer from our widget observer list bound with
fbind using the uid.

**kivy.properties.ReferenceListProperty**

Bases: [`kivy.properties.Property`](https://kivy.org/doc/stable/#kivy.properties.Property)
For example, if x and y are [`NumericProperty`](https://kivy.org/doc/stable/#kivy.properties.NumericProperty)s, we can create a
[`ReferenceListProperty`](https://kivy.org/doc/stable/#kivy.properties.ReferenceListProperty) for the pos. If you change the value of
pos, it will automatically change the values of x and y accordingly.
If you read the value of pos, it will return a tuple with the values of
x and y.
For example:

**kivy.properties.ReferenceListProperty.get**

**kivy.properties.ReferenceListProperty.link**

**kivy.properties.ReferenceListProperty.link_deps**

**kivy.properties.ReferenceListProperty.set**

**kivy.properties.ReferenceListProperty.setitem**

**kivy.properties.ReferenceListProperty.trigger_change**

**kivy.properties.StringProperty**

Bases: [`kivy.properties.Property`](https://kivy.org/doc/stable/#kivy.properties.Property)

**kivy.properties.VariableListProperty**

Bases: [`kivy.properties.Property`](https://kivy.org/doc/stable/#kivy.properties.Property)
list items and to expand them to the desired list size.
For example, GridLayout’s padding used to just accept one numeric value
which was applied equally to the left, top, right and bottom of the
GridLayout. Now padding can be given one, two or four values, which are
expanded into a length four list [left, top, right, bottom] and stored
in the property.

Keeping in mind that the default list is expanded to a list of length 4,
here are some examples of how VariableListProperty is handled.
VariableListProperty([1]) represents [1, 1, 1, 1].
VariableListProperty([1, 2]) represents [1, 2, 1, 2].
VariableListProperty([‘1px’, (2, ‘px’), 3, 4.0]) represents [1, 2, 3, 4.0].
VariableListProperty(5) represents [5, 5, 5, 5].
VariableListProperty(3, length=2) represents [3, 3].
New in version 1.7.0.

**kivy.properties.VariableListProperty.length**

length: ‘int’

**kivy.properties.VariableListProperty.link**

---

## API - [`kivy.resources`](https://kivy.org/doc/stable/api-kivy.resources.html)

**kivy.resources.resource_add_path**

Add a custom path to search in.

**kivy.resources.resource_find**

Search for a resource in the list of paths.
Use resource_add_path to add a custom path to the search.
By default, results are cached for 60 seconds.
This can be disabled using use_cache=False.
Changed in version 2.1.0:use_cache parameter added and made True by default.

**kivy.resources.resource_remove_path**

Remove a search path.
New in version 1.0.8.

---

## API - [`kivy.storage`](https://kivy.org/doc/stable/api-kivy.storage.html)

**kivy.storage.AbstractStore**

Bases: [`kivy.event.EventDispatcher`](https://kivy.org/doc/stable/api-kivy.event.html#kivy.event.EventDispatcher)
Abstract class used to implement a Store

**kivy.storage.AbstractStore.async_clear**

Asynchronous version of [`clear()`](https://kivy.org/doc/stable/#kivy.storage.AbstractStore.clear).

**kivy.storage.AbstractStore.async_count**

Asynchronously return the number of entries in the storage.

**kivy.storage.AbstractStore.async_delete**

Asynchronous version of [`delete()`](https://kivy.org/doc/stable/#kivy.storage.AbstractStore.delete).

**kivy.storage.AbstractStore.async_exists**

Asynchronous version of [`exists()`](https://kivy.org/doc/stable/#kivy.storage.AbstractStore.exists).

**kivy.storage.AbstractStore.async_find**

Asynchronous version of [`find()`](https://kivy.org/doc/stable/#kivy.storage.AbstractStore.find).
The callback will be called for each entry in the result.

**kivy.storage.AbstractStore.async_get**

Asynchronous version of [`get()`](https://kivy.org/doc/stable/#kivy.storage.AbstractStore.get).

**kivy.storage.AbstractStore.async_keys**

Asynchronously return all the keys in the storage.

**kivy.storage.AbstractStore.async_put**

Asynchronous version of [`put()`](https://kivy.org/doc/stable/#kivy.storage.AbstractStore.put).

**kivy.storage.AbstractStore.clear**

Wipe the whole storage.

**kivy.storage.AbstractStore.count**

Return the number of entries in the storage.

**kivy.storage.AbstractStore.delete**

Delete a key from the storage. If the key is not found, a KeyError
exception will be thrown.

**kivy.storage.AbstractStore.exists**

Check if a key exists in the store.

**kivy.storage.AbstractStore.find**

Return all the entries matching the filters. The entries are
returned through a generator as a list of (key, entry) pairs
where *entry* is a dict of key-value pairs

Because it’s a generator, you cannot directly use it as a list. You can
do:

**kivy.storage.AbstractStore.get**

Get the key-value pairs stored at key. If the key is not found, a
KeyError exception will be thrown.

**kivy.storage.AbstractStore.keys**

Return a list of all the keys in the storage.

**kivy.storage.AbstractStore.put**

Put new key-value pairs (given in *values*) into the storage. Any
existing key-value pairs will be removed.

---

## API - [`kivy.storage.dictstore`](https://kivy.org/doc/stable/api-kivy.storage.dictstore.html)

**kivy.storage.dictstore.DictStore**

Bases: [`kivy.storage.AbstractStore`](https://kivy.org/doc/stable/api-kivy.storage.html#kivy.storage.AbstractStore)
Store implementation using a pickled dict.
See the [`kivy.storage`](https://kivy.org/doc/stable/api-kivy.storage.html#module-kivy.storage) module documentation for more information.

---

## API - [`kivy.storage.jsonstore`](https://kivy.org/doc/stable/api-kivy.storage.jsonstore.html)

**kivy.storage.jsonstore.JsonStore**

Bases: [`kivy.storage.AbstractStore`](https://kivy.org/doc/stable/api-kivy.storage.html#kivy.storage.AbstractStore)
Store implementation using a json file for storing the key-value pairs.
See the [`kivy.storage`](https://kivy.org/doc/stable/api-kivy.storage.html#module-kivy.storage) module documentation for more information.

---

## API - [`kivy.storage.redisstore`](https://kivy.org/doc/stable/api-kivy.storage.redisstore.html)

**kivy.storage.redisstore.RedisStore**

Bases: [`kivy.storage.AbstractStore`](https://kivy.org/doc/stable/api-kivy.storage.html#kivy.storage.AbstractStore)
Store implementation using a Redis database.
See the [`kivy.storage`](https://kivy.org/doc/stable/api-kivy.storage.html#module-kivy.storage) module documentation for more information.

---

## API - [`kivy.support`](https://kivy.org/doc/stable/api-kivy.support.html)

**kivy.support.install_android**

Install hooks for the android platform.
Automatically sleep when the device is paused.
Automatically kill the application when the return key is pressed.

**kivy.support.install_gobject_iteration**

Import and install gobject context iteration inside our event loop.
This is used as soon as gobject is used (like gstreamer).

**kivy.support.install_twisted_reactor**

Installs a threaded twisted reactor, which will schedule one
reactor iteration before the next frame only when twisted needs
to do some work.
Any arguments or keyword arguments passed to this function will be
passed on the threadedselect reactors interleave function. These
are the arguments one would usually pass to twisted’s reactor.startRunning.
Unlike the default twisted reactor, the installed reactor will not handle
any signals unless you set the ‘installSignalHandlers’ keyword argument
to 1 explicitly. This is done to allow kivy to handle the signals as
usual unless you specifically want the twisted reactor to handle the
signals (e.g. SIGINT).

**kivy.support.uninstall_twisted_reactor**

Uninstalls the Kivy’s threaded Twisted Reactor. No more Twisted
tasks will run after this got called. Use this to clean the
twisted.internet.reactor .
New in version 1.9.0.

---

## API - [`kivy.tools.packaging.pyinstaller_hooks`](https://kivy.org/doc/stable/api-kivy.tools.packaging.pyinstaller_hooks.html)

**kivy.tools.packaging.pyinstaller_hooks.add_dep_paths**

Should be called by the hook. It adds the paths with the binary
dependencies to the system path so that pyinstaller can find the binaries
during its crawling stage.

**kivy.tools.packaging.pyinstaller_hooks.get_deps_all**

Similar to [`get_deps_minimal()`](https://kivy.org/doc/stable/#kivy.tools.packaging.pyinstaller_hooks.get_deps_minimal), but this returns all the
kivy modules that can indirectly imported. Which includes all
the possible kivy providers.
This can be used to get a list of all the possible providers
which can then manually be included/excluded by commenting out elements
in the list instead of passing on all the items. See module description.

**kivy.tools.packaging.pyinstaller_hooks.get_deps_minimal**

Returns Kivy hidden modules as well as excluded modules to be used
with `Analysis`.
The function takes core modules as keyword arguments and their value
indicates which of the providers to include/exclude from the compiled app.
The possible keyword names are `audio, camera, clipboard, image, spelling,
text, video, and window`. Their values can be:

For example, `get_deps_minimal(video=None, window=True,
audio=['gstplayer', 'ffpyplayer'], spelling='enchant')` will exclude all
the video providers, will include the gstreamer and ffpyplayer providers
for audio, will include the enchant provider for spelling, and will use the
current default provider for `window`.
`exclude_ignored`, if `True` (the default), if the value for a core
library is `None`, then if `exclude_ignored` is True, not only will the
library not be included in the hiddenimports but it’ll also added to the
excluded imports to prevent it being included accidentally by pyinstaller.

**kivy.tools.packaging.pyinstaller_hooks.get_factory_modules**

Returns a list of all the modules registered in the kivy factory.

**kivy.tools.packaging.pyinstaller_hooks.get_hooks**

Returns the dict for the spec `hookspath` and `runtime_hooks`
values.

**kivy.tools.packaging.pyinstaller_hooks.hookspath**

Returns a list with the directory that contains the alternate (not
the default included with pyinstaller) pyinstaller hook for kivy,
`kivy/tools/packaging/pyinstaller_hooks/kivy-hook.py`. It is
typically used with `hookspath=hookspath()` in the spec
file.
The default pyinstaller hook returns all the core providers used using
[`get_deps_minimal()`](https://kivy.org/doc/stable/#kivy.tools.packaging.pyinstaller_hooks.get_deps_minimal) to add to its list of hidden imports. This
alternate hook only included the essential modules and leaves the core
providers to be included additionally with [`get_deps_minimal()`](https://kivy.org/doc/stable/#kivy.tools.packaging.pyinstaller_hooks.get_deps_minimal)
or [`get_deps_all()`](https://kivy.org/doc/stable/#kivy.tools.packaging.pyinstaller_hooks.get_deps_all).

**kivy.tools.packaging.pyinstaller_hooks.runtime_hooks**

Returns a list with the runtime hooks for kivy. It can be used with
`runtime_hooks=runtime_hooks()` in the spec file. Pyinstaller comes
preinstalled with this hook.

---

## API - [`kivy.uix.accordion`](https://kivy.org/doc/stable/api-kivy.uix.accordion.html)

**kivy.uix.accordion.Accordion**

Bases: [`kivy.uix.widget.Widget`](https://kivy.org/doc/stable/api-kivy.uix.widget.html#kivy.uix.widget.Widget)
Accordion class. See module documentation for more information.

**kivy.uix.accordion.Accordion.add_widget**

Add a new widget as a child of this widget.

**kivy.uix.accordion.Accordion.anim_duration**

Duration of the animation in seconds when a new accordion item is
selected.
[`anim_duration`](https://kivy.org/doc/stable/#kivy.uix.accordion.Accordion.anim_duration) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to .25 (250ms).

**kivy.uix.accordion.Accordion.anim_func**

Easing function to use for the animation. Check
[`kivy.animation.AnimationTransition`](https://kivy.org/doc/stable/api-kivy.animation.html#kivy.animation.AnimationTransition) for more information about
available animation functions.
[`anim_func`](https://kivy.org/doc/stable/#kivy.uix.accordion.Accordion.anim_func) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to ‘out_expo’. You can set a string or a function to use as an
easing function.

**kivy.uix.accordion.Accordion.min_space**

Minimum space to use for the title of each item. This value is
automatically set for each child every time the layout event occurs.
[`min_space`](https://kivy.org/doc/stable/#kivy.uix.accordion.Accordion.min_space) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 44 (px).

**kivy.uix.accordion.Accordion.orientation**

Orientation of the layout.
[`orientation`](https://kivy.org/doc/stable/#kivy.uix.accordion.Accordion.orientation) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to ‘horizontal’. Can take a value of ‘vertical’ or
‘horizontal’.

**kivy.uix.accordion.AccordionException**

Bases: `Exception`
AccordionException class.

**kivy.uix.accordion.AccordionItem**

Bases: [`kivy.uix.floatlayout.FloatLayout`](https://kivy.org/doc/stable/api-kivy.uix.floatlayout.html#kivy.uix.floatlayout.FloatLayout)
AccordionItem class that must be used in conjunction with the
[`Accordion`](https://kivy.org/doc/stable/#kivy.uix.accordion.Accordion) class. See the module documentation for more
information.

**kivy.uix.accordion.AccordionItem.accordion**

Instance of the [`Accordion`](https://kivy.org/doc/stable/#kivy.uix.accordion.Accordion) that the item belongs to.
[`accordion`](https://kivy.org/doc/stable/#kivy.uix.accordion.AccordionItem.accordion) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to None.

**kivy.uix.accordion.AccordionItem.add_widget**

Add a new widget as a child of this widget.

**kivy.uix.accordion.AccordionItem.background_disabled_normal**

Background image of the accordion item used for the default graphical
representation when the item is collapsed and disabled.
New in version 1.8.0.
`background__disabled_normal` is a
[`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults to
‘atlas://data/images/defaulttheme/button_disabled’.

**kivy.uix.accordion.AccordionItem.background_disabled_selected**

Background image of the accordion item used for the default graphical
representation when the item is selected (not collapsed) and disabled.
New in version 1.8.0.
[`background_disabled_selected`](https://kivy.org/doc/stable/#kivy.uix.accordion.AccordionItem.background_disabled_selected) is a
[`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults to
‘atlas://data/images/defaulttheme/button_disabled_pressed’.

**kivy.uix.accordion.AccordionItem.background_normal**

Background image of the accordion item used for the default graphical
representation when the item is collapsed.
[`background_normal`](https://kivy.org/doc/stable/#kivy.uix.accordion.AccordionItem.background_normal) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to ‘atlas://data/images/defaulttheme/button’.

**kivy.uix.accordion.AccordionItem.background_selected**

Background image of the accordion item used for the default graphical
representation when the item is selected (not collapsed).
[`background_normal`](https://kivy.org/doc/stable/#kivy.uix.accordion.AccordionItem.background_normal) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to ‘atlas://data/images/defaulttheme/button_pressed’.

**kivy.uix.accordion.AccordionItem.collapse**

Boolean to indicate if the current item is collapsed or not.
[`collapse`](https://kivy.org/doc/stable/#kivy.uix.accordion.AccordionItem.collapse) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to True.

**kivy.uix.accordion.AccordionItem.collapse_alpha**

Value between 0 and 1 to indicate how much the item is collapsed (1) or
whether it is selected (0). It’s mostly used for animation.
[`collapse_alpha`](https://kivy.org/doc/stable/#kivy.uix.accordion.AccordionItem.collapse_alpha) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 1.

**kivy.uix.accordion.AccordionItem.container**

(internal) Property that will be set to the container of children inside
the AccordionItem representation.

**kivy.uix.accordion.AccordionItem.container_title**

(internal) Property that will be set to the container of title inside
the AccordionItem representation.

**kivy.uix.accordion.AccordionItem.content_size**

(internal) Set by the [`Accordion`](https://kivy.org/doc/stable/#kivy.uix.accordion.Accordion) to the size allocated for the
content.

**kivy.uix.accordion.AccordionItem.min_space**

Link to the [`Accordion.min_space`](https://kivy.org/doc/stable/#kivy.uix.accordion.Accordion.min_space) property.

**kivy.uix.accordion.AccordionItem.on_touch_down**

Receive a touch down event.

**kivy.uix.accordion.AccordionItem.orientation**

Link to the [`Accordion.orientation`](https://kivy.org/doc/stable/#kivy.uix.accordion.Accordion.orientation) property.

**kivy.uix.accordion.AccordionItem.remove_widget**

Remove a widget from the children of this widget.

**kivy.uix.accordion.AccordionItem.title**

Title string of the item. The title might be used in conjunction with the
AccordionItemTitle template. If you are using a custom template, you can
use that property as a text entry, or not. By default, it’s used for the
title text. See title_template and the example below.
[`title`](https://kivy.org/doc/stable/#kivy.uix.accordion.AccordionItem.title) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults
to ‘’.

**kivy.uix.accordion.AccordionItem.title_args**

Default arguments that will be passed to the
`kivy.lang.Builder.template()` method.
[`title_args`](https://kivy.org/doc/stable/#kivy.uix.accordion.AccordionItem.title_args) is a [`DictProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.DictProperty) and defaults
to {}.

**kivy.uix.accordion.AccordionItem.title_template**

Template to use for creating the title part of the accordion item. The
default template is a simple Label, not customizable (except the text) that
supports vertical and horizontal orientation and different backgrounds for
collapse and selected mode.
It’s better to create and use your own template if the default template
does not suffice.
[`title`](https://kivy.org/doc/stable/#kivy.uix.accordion.AccordionItem.title) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults to
‘AccordionItemTitle’. The current default template lives in the
kivy/data/style.kv file.
Here is the code if you want to build your own template:

---

## API - [`kivy.uix.actionbar`](https://kivy.org/doc/stable/api-kivy.uix.actionbar.html)

**kivy.uix.actionbar.ActionBar**

Bases: [`kivy.uix.boxlayout.BoxLayout`](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html#kivy.uix.boxlayout.BoxLayout)
ActionBar class, which acts as the main container for an
[`ActionView`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionView) instance. The ActionBar determines the overall
styling aspects of the bar. [`ActionItem`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionItem)s are not added to
this class directly, but to the contained [`ActionView`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionView) instance.

Please see the module documentation for more information.

**kivy.uix.actionbar.ActionBar.action_view**

action_view of the ActionBar.
[`action_view`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionBar.action_view) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to None or the last ActionView instance added to the ActionBar.

**kivy.uix.actionbar.ActionBar.add_widget**

Changed in version 2.1.0:Renamed argument view to widget.

**kivy.uix.actionbar.ActionBar.background_color**

Background color, in the format (r, g, b, a).
[`background_color`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionBar.background_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty) and
defaults to [1, 1, 1, 1].
Changed in version 2.0.0:Changed from [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) to
[`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty).

**kivy.uix.actionbar.ActionBar.background_image**

Background image of the ActionBars default graphical representation.
[`background_image`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionBar.background_image) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘atlas://data/images/defaulttheme/action_bar’.

**kivy.uix.actionbar.ActionBar.border**

The border to be applied to the [`background_image`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionBar.background_image).
[`border`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionBar.border) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) and defaults to
[2, 2, 2, 2]

**kivy.uix.actionbar.ActionBarException**

Bases: `Exception`
ActionBarException class

**kivy.uix.actionbar.ActionButton**

Bases: [`kivy.uix.button.Button`](https://kivy.org/doc/stable/api-kivy.uix.button.html#kivy.uix.button.Button), [`kivy.uix.actionbar.ActionItem`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionItem)
ActionButton class, see module documentation for more information.
The text color, width and size_hint_x are set manually via the Kv language
file. It covers a lot of cases: with/without an icon, with/without a group
and takes care of the padding between elements.
You don’t have much control over these properties, so if you want to
customize its appearance, we suggest you create you own button
representation. You can do this by creating a class that subclasses an
existing widget and an [`ActionItem`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionItem):

You can then create your own style using the Kv language.

**kivy.uix.actionbar.ActionButton.icon**

Source image to use when the Button is part of the ActionBar. If the
Button is in a group, the text will be preferred.
[`icon`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionButton.icon) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults
to None.

**kivy.uix.actionbar.ActionCheck**

Bases: [`kivy.uix.actionbar.ActionItem`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionItem), [`kivy.uix.checkbox.CheckBox`](https://kivy.org/doc/stable/api-kivy.uix.checkbox.html#kivy.uix.checkbox.CheckBox)
ActionCheck class, see module documentation for more information.

**kivy.uix.actionbar.ActionDropDown**

Bases: [`kivy.uix.dropdown.DropDown`](https://kivy.org/doc/stable/api-kivy.uix.dropdown.html#kivy.uix.dropdown.DropDown)
ActionDropDown class, see module documentation for more information.

**kivy.uix.actionbar.ActionGroup**

Bases: [`kivy.uix.actionbar.ActionItem`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionItem), [`kivy.uix.button.Button`](https://kivy.org/doc/stable/api-kivy.uix.button.html#kivy.uix.button.Button)
ActionGroup class, see module documentation for more information.

**kivy.uix.actionbar.ActionGroup.add_widget**

Changed in version 2.1.0:Renamed argument item to widget.

**kivy.uix.actionbar.ActionGroup.clear_widgets**

Remove all (or the specified) `children` of this widget.
If the ‘children’ argument is specified, it should be a list (or
filtered list) of children of the current widget.
Changed in version 1.8.0:The children argument can be used to specify the children you
want to remove.
Changed in version 2.1.0:Specifying an empty `children` list leaves the widgets unchanged.
Previously it was treated like `None` and all children were
removed.

**kivy.uix.actionbar.ActionGroup.dropdown_width**

If non zero, provides the width for the associated DropDown. This is
useful when some items in the ActionGroup’s DropDown are wider than usual
and you don’t want to make the ActionGroup widget itself wider.
[`dropdown_width`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionGroup.dropdown_width) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.
New in version 1.10.0.

**kivy.uix.actionbar.ActionGroup.is_open**

By default, the DropDown is not open. Set to True to open it.
[`is_open`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionGroup.is_open) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to False.

**kivy.uix.actionbar.ActionGroup.mode**

Sets the current mode of an ActionGroup. If mode is ‘normal’, the
ActionGroups children will be displayed normally if there is enough
space, otherwise they will be displayed in a spinner. If mode is
‘spinner’, then the children will always be displayed in a spinner.
[`mode`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionGroup.mode) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty) and defaults
to ‘normal’.

**kivy.uix.actionbar.ActionGroup.separator_image**

Background Image for an ActionSeparator in an ActionView.
[`separator_image`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionGroup.separator_image) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘atlas://data/images/defaulttheme/separator’.

**kivy.uix.actionbar.ActionGroup.separator_width**

Width of the ActionSeparator in an ActionView.
[`separator_width`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionGroup.separator_width) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.

**kivy.uix.actionbar.ActionGroup.use_separator**

Specifies whether to use a separator after/before this group or not.
[`use_separator`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionGroup.use_separator) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to False.

**kivy.uix.actionbar.ActionItem**

Bases: `builtins.object`
ActionItem class, an abstract class for all ActionBar widgets. To create a
custom widget for an ActionBar, inherit from this class. See module
documentation for more information.

**kivy.uix.actionbar.ActionItem.background_down**

Background image of the ActionItem used for the default graphical
representation when an ActionItem is pressed.
[`background_down`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionItem.background_down) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘atlas://data/images/defaulttheme/action_item_down’.

**kivy.uix.actionbar.ActionItem.background_normal**

Background image of the ActionItem used for the default graphical
representation when the ActionItem is not pressed.
[`background_normal`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionItem.background_normal) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘atlas://data/images/defaulttheme/action_item’.

**kivy.uix.actionbar.ActionItem.important**

Determines if an ActionItem is important or not. If an item is important
and space is limited, this item will be displayed in preference to others.
[`important`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionItem.important) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to False.

**kivy.uix.actionbar.ActionItem.inside_group**

(internal) Determines if an ActionItem is displayed inside an
ActionGroup or not.
[`inside_group`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionItem.inside_group) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to False.

**kivy.uix.actionbar.ActionItem.minimum_width**

Minimum Width required by an ActionItem.
[`minimum_width`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionItem.minimum_width) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to ’90sp’.

**kivy.uix.actionbar.ActionItem.mipmap**

Defines whether the image/icon dispayed on top of the button uses a
mipmap or not.
[`mipmap`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionItem.mipmap) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to True.

**kivy.uix.actionbar.ActionItem.pack_width**

(read-only) The actual width to use when packing the items. Equal to the
greater of minimum_width and width.
[`pack_width`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionItem.pack_width) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty).

**kivy.uix.actionbar.ActionOverflow**

Bases: [`kivy.uix.actionbar.ActionGroup`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionGroup)
ActionOverflow class, see module documentation for more information.

**kivy.uix.actionbar.ActionOverflow.add_widget**

Changed in version 2.1.0:Renamed argument action_item to widget.

**kivy.uix.actionbar.ActionOverflow.overflow_image**

Image to be used as an Overflow Image.
[`overflow_image`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionOverflow.overflow_image) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘atlas://data/images/defaulttheme/overflow’.

**kivy.uix.actionbar.ActionPrevious**

Bases: [`kivy.uix.boxlayout.BoxLayout`](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html#kivy.uix.boxlayout.BoxLayout), [`kivy.uix.actionbar.ActionItem`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionItem)
ActionPrevious class, see module documentation for more information.

**kivy.uix.actionbar.ActionPrevious.app_icon**

Application icon for the ActionView.
[`app_icon`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionPrevious.app_icon) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to the window icon if set, otherwise
‘data/logo/kivy-icon-32.png’.

**kivy.uix.actionbar.ActionPrevious.app_icon_height**

Height of app_icon image.
[`app_icon_height`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionPrevious.app_icon_height) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.

**kivy.uix.actionbar.ActionPrevious.app_icon_width**

Width of app_icon image.
[`app_icon_width`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionPrevious.app_icon_width) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0.

**kivy.uix.actionbar.ActionPrevious.color**

Text color, in the format (r, g, b, a)
[`color`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionPrevious.color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty) and defaults
to [1, 1, 1, 1].
Changed in version 2.0.0:Changed from [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) to
[`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty).

**kivy.uix.actionbar.ActionPrevious.markup**

If True, the text will be rendered using the
[`MarkupLabel`](https://kivy.org/doc/stable/api-kivy.core.text.markup.html#kivy.core.text.markup.MarkupLabel): you can change the style of
the text using tags. Check the [Text Markup](https://kivy.org/doc/stable/api-kivy.core.text.markup.html)
documentation for more information.
[`markup`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionPrevious.markup) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to False.

**kivy.uix.actionbar.ActionPrevious.previous_image**

Image for the ‘previous’ ActionButtons default graphical representation.
[`previous_image`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionPrevious.previous_image) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to ‘atlas://data/images/defaulttheme/previous_normal’.

**kivy.uix.actionbar.ActionPrevious.previous_image_height**

Height of previous_image image.
[`app_icon_width`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionPrevious.app_icon_width) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0.

**kivy.uix.actionbar.ActionPrevious.previous_image_width**

Width of previous_image image.
`width` is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0.

**kivy.uix.actionbar.ActionPrevious.title**

Title for ActionView.
[`title`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionPrevious.title) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to ‘’.

**kivy.uix.actionbar.ActionPrevious.with_previous**

Specifies whether the previous_icon will be shown or not. Note that it is
up to the user to implement the desired behavior using the *on_press* or
similar events.
[`with_previous`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionPrevious.with_previous) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to True.

**kivy.uix.actionbar.ActionSeparator**

Bases: [`kivy.uix.actionbar.ActionItem`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionItem), [`kivy.uix.widget.Widget`](https://kivy.org/doc/stable/api-kivy.uix.widget.html#kivy.uix.widget.Widget)
ActionSeparator class, see module documentation for more information.

**kivy.uix.actionbar.ActionSeparator.background_image**

Background image for the separators default graphical representation.
[`background_image`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionSeparator.background_image) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘atlas://data/images/defaulttheme/separator’.

**kivy.uix.actionbar.ActionToggleButton**

Bases: [`kivy.uix.actionbar.ActionItem`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionItem), [`kivy.uix.togglebutton.ToggleButton`](https://kivy.org/doc/stable/api-kivy.uix.togglebutton.html#kivy.uix.togglebutton.ToggleButton)
ActionToggleButton class, see module documentation for more information.

**kivy.uix.actionbar.ActionToggleButton.icon**

Source image to use when the Button is part of the ActionBar. If the
Button is in a group, the text will be preferred.

**kivy.uix.actionbar.ActionView**

Bases: [`kivy.uix.boxlayout.BoxLayout`](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html#kivy.uix.boxlayout.BoxLayout)
ActionView class, see module documentation for more information.

**kivy.uix.actionbar.ActionView.action_previous**

Previous button for an ActionView.
[`action_previous`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionView.action_previous) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty)
and defaults to None.

**kivy.uix.actionbar.ActionView.add_widget**

Changed in version 2.1.0:Renamed argument action_item to widget.

**kivy.uix.actionbar.ActionView.background_color**

Background color in the format (r, g, b, a).
[`background_color`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionView.background_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty) and
defaults to [1, 1, 1, 1].
Changed in version 2.0.0:Changed from [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) to
[`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty).

**kivy.uix.actionbar.ActionView.background_image**

Background image of an ActionViews default graphical representation.
[`background_image`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionView.background_image) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘atlas://data/images/defaulttheme/action_view’.

**kivy.uix.actionbar.ActionView.overflow_group**

Widget to be used for the overflow.
[`overflow_group`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionView.overflow_group) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to an instance of [`ActionOverflow`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionOverflow).

**kivy.uix.actionbar.ActionView.remove_widget**

Remove a widget from the children of this widget.

**kivy.uix.actionbar.ActionView.use_separator**

Specify whether to use a separator before every ActionGroup or not.
[`use_separator`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionView.use_separator) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to False.

**kivy.uix.actionbar.ContextualActionView**

Bases: [`kivy.uix.actionbar.ActionView`](https://kivy.org/doc/stable/#kivy.uix.actionbar.ActionView)
ContextualActionView class, see the module documentation for more
information.

---

## API - [`kivy.uix.anchorlayout`](https://kivy.org/doc/stable/api-kivy.uix.anchorlayout.html)

**kivy.uix.anchorlayout.AnchorLayout**

Bases: [`kivy.uix.layout.Layout`](https://kivy.org/doc/stable/api-kivy.uix.layout.html#kivy.uix.layout.Layout)
Anchor layout class. See the module documentation for more information.

**kivy.uix.anchorlayout.AnchorLayout.anchor_x**

Horizontal anchor.
[`anchor_x`](https://kivy.org/doc/stable/#kivy.uix.anchorlayout.AnchorLayout.anchor_x) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty) and
defaults to ‘center’. It accepts values of ‘left’, ‘center’ or
‘right’.

**kivy.uix.anchorlayout.AnchorLayout.anchor_y**

Vertical anchor.
[`anchor_y`](https://kivy.org/doc/stable/#kivy.uix.anchorlayout.AnchorLayout.anchor_y) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty) and
defaults to ‘center’. It accepts values of ‘top’, ‘center’ or
‘bottom’.

**kivy.uix.anchorlayout.AnchorLayout.do_layout**

This function is called when a layout is called by a trigger.
If you are writing a new Layout subclass, don’t call this function
directly but use `_trigger_layout()` instead.
The function is by default called *before* the next frame, therefore
the layout isn’t updated immediately. Anything depending on the
positions of e.g. children should be scheduled for the next frame.
New in version 1.0.8.

**kivy.uix.anchorlayout.AnchorLayout.padding**

Padding between the widget box and its children, in pixels:
[padding_left, padding_top, padding_right, padding_bottom].
padding also accepts a two argument form [padding_horizontal,
padding_vertical] and a one argument form [padding].
[`padding`](https://kivy.org/doc/stable/#kivy.uix.anchorlayout.AnchorLayout.padding) is a [`VariableListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.VariableListProperty) and
defaults to [0, 0, 0, 0].

---

## API - [`kivy.uix.behaviors`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.html)

**kivy.uix.behaviors.ButtonBehavior**

Bases: `builtins.object`
This [mixin](https://en.wikipedia.org/wiki/Mixin) class provides
[`Button`](https://kivy.org/doc/stable/api-kivy.uix.button.html#kivy.uix.button.Button) behavior. Please see the
[`button behaviors module`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.button.html#module-kivy.uix.behaviors.button) documentation
for more information.

**kivy.uix.behaviors.ButtonBehavior.always_release**

This determines whether or not the widget fires an on_release event if
the touch_up is outside the widget.
New in version 1.9.0.
Changed in version 1.10.0:The default value is now False.
[`always_release`](https://kivy.org/doc/stable/#kivy.uix.behaviors.ButtonBehavior.always_release) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to False.

**kivy.uix.behaviors.ButtonBehavior.last_touch**

Contains the last relevant touch received by the Button. This can
be used in on_press or on_release in order to know which touch
dispatched the event.
New in version 1.8.0.
[`last_touch`](https://kivy.org/doc/stable/#kivy.uix.behaviors.ButtonBehavior.last_touch) is a [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to None.

**kivy.uix.behaviors.ButtonBehavior.min_state_time**

The minimum period of time which the widget must remain in the
‘down’ state.
New in version 1.9.1.
[`min_state_time`](https://kivy.org/doc/stable/#kivy.uix.behaviors.ButtonBehavior.min_state_time) is a float and defaults to 0.035. This value is
taken from [`Config`](https://kivy.org/doc/stable/api-kivy.config.html#kivy.config.Config).

**kivy.uix.behaviors.ButtonBehavior.state**

The state of the button, must be one of ‘normal’ or ‘down’.
The state is ‘down’ only when the button is currently touched/clicked,
otherwise its ‘normal’.
[`state`](https://kivy.org/doc/stable/#kivy.uix.behaviors.ButtonBehavior.state) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty) and defaults
to ‘normal’.

**kivy.uix.behaviors.ButtonBehavior.trigger_action**

Trigger whatever action(s) have been bound to the button by calling
both the on_press and on_release callbacks.
This is similar to a quick button press without using any touch events,
but note that like most kivy code, this is not guaranteed to be safe to
call from external threads. If needed use
[`Clock`](https://kivy.org/doc/stable/api-kivy.clock.html#kivy.clock.Clock) to safely schedule this function and
the resulting callbacks to be called from the main thread.
Duration is the length of the press in seconds. Pass 0 if you want
the action to happen instantly.
New in version 1.8.0.

**kivy.uix.behaviors.CodeNavigationBehavior**

Bases: [`kivy.event.EventDispatcher`](https://kivy.org/doc/stable/api-kivy.event.html#kivy.event.EventDispatcher)
Code navigation behavior. Modifies the navigation behavior in TextInput
to work like an IDE instead of a word processor. Please see the
[`code navigation behaviors module`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.codenavigation.html#module-kivy.uix.behaviors.codenavigation)
documentation for more information.
New in version 1.9.1.

**kivy.uix.behaviors.CompoundSelectionBehavior**

Bases: `builtins.object`
The Selection behavior [mixin](https://en.wikipedia.org/wiki/Mixin)
implements the logic behind keyboard and touch
selection of selectable widgets managed by the derived widget. Please see
the [`compound selection behaviors module`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.compoundselection.html#module-kivy.uix.behaviors.compoundselection) documentation
for more information.
New in version 1.9.0.

**kivy.uix.behaviors.CompoundSelectionBehavior.clear_selection**

Deselects all the currently selected nodes.

**kivy.uix.behaviors.CompoundSelectionBehavior.deselect_node**

Deselects a possibly selected node.
It is called by the controller when it deselects a node and can also
be called from the outside to deselect a node directly. The derived
widget should overwrite this method and change the node to its
unselected state when this is called

**kivy.uix.behaviors.CompoundSelectionBehavior.get_index_of_node**

(internal) Returns the index of the node within the
selectable_nodes returned by [`get_selectable_nodes()`](https://kivy.org/doc/stable/#kivy.uix.behaviors.CompoundSelectionBehavior.get_selectable_nodes).

**kivy.uix.behaviors.CompoundSelectionBehavior.get_selectable_nodes**

(internal) Returns a list of the nodes that can be selected. It can
be overwritten by the derived widget to return the correct list.
This list is used to determine which nodes to select with group
selection. E.g. the last element in the list will be selected when
home is pressed, pagedown will move (or add to, if shift is held) the
selection from the current position by negative [`page_count`](https://kivy.org/doc/stable/#kivy.uix.behaviors.CompoundSelectionBehavior.page_count)
nodes starting from the position of the currently selected node in
this list and so on. Still, nodes can be selected even if they are not
in this list.

Defaults to returning [`children`](https://kivy.org/doc/stable/api-kivy.uix.widget.html#kivy.uix.widget.Widget.children).

**kivy.uix.behaviors.CompoundSelectionBehavior.goto_node**

(internal) Used by the controller to get the node at the position
indicated by key. The key can be keyboard inputs, e.g. pageup,
or scroll inputs from the mouse scroll wheel, e.g. scrollup.
‘last_node’ is the last node selected and is used to find the resulting
node. For example, if the key is up, the returned node is one node
up from the last node.
It can be overwritten by the derived widget.

**kivy.uix.behaviors.CompoundSelectionBehavior.keyboard_select**

Determines whether the keyboard can be used for selection. If False,
keyboard inputs will be ignored.
[`keyboard_select`](https://kivy.org/doc/stable/#kivy.uix.behaviors.CompoundSelectionBehavior.keyboard_select) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to True.

**kivy.uix.behaviors.CompoundSelectionBehavior.multiselect**

Determines whether multiple nodes can be selected. If enabled, keyboard
shift and ctrl selection, optionally combined with touch, for example, will
be able to select multiple widgets in the normally expected manner.
This dominates [`touch_multiselect`](https://kivy.org/doc/stable/#kivy.uix.behaviors.CompoundSelectionBehavior.touch_multiselect) when False.
[`multiselect`](https://kivy.org/doc/stable/#kivy.uix.behaviors.CompoundSelectionBehavior.multiselect) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to False.

**kivy.uix.behaviors.CompoundSelectionBehavior.nodes_order_reversed**

(Internal) Indicates whether the order of the nodes as displayed top-
down is reversed compared to their order in [`get_selectable_nodes()`](https://kivy.org/doc/stable/#kivy.uix.behaviors.CompoundSelectionBehavior.get_selectable_nodes)
(e.g. how the children property is reversed compared to how
it’s displayed).

**kivy.uix.behaviors.CompoundSelectionBehavior.page_count**

Determines by how much the selected node is moved up or down, relative
to the position of the last selected node, when pageup (or pagedown) is
pressed.
[`page_count`](https://kivy.org/doc/stable/#kivy.uix.behaviors.CompoundSelectionBehavior.page_count) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 10.

**kivy.uix.behaviors.CompoundSelectionBehavior.right_count**

Determines by how much the selected node is moved up or down, relative
to the position of the last selected node, when the right (or left) arrow
on the keyboard is pressed.
[`right_count`](https://kivy.org/doc/stable/#kivy.uix.behaviors.CompoundSelectionBehavior.right_count) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 1.

**kivy.uix.behaviors.CompoundSelectionBehavior.scroll_count**

Determines by how much the selected node is moved up or down, relative
to the position of the last selected node, when the mouse scroll wheel is
scrolled.
[`right_count`](https://kivy.org/doc/stable/#kivy.uix.behaviors.CompoundSelectionBehavior.right_count) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0.

**kivy.uix.behaviors.CompoundSelectionBehavior.select_node**

Selects a node.
It is called by the controller when it selects a node and can be
called from the outside to select a node directly. The derived widget
should overwrite this method and change the node state to selected
when called.

**kivy.uix.behaviors.CompoundSelectionBehavior.select_with_key_down**

Processes a key press. This is called when a key press is to be used
for selection. Depending on the keyboard keys pressed and the
configuration, it could select or deselect nodes or node ranges
from the selectable nodes list, [`get_selectable_nodes()`](https://kivy.org/doc/stable/#kivy.uix.behaviors.CompoundSelectionBehavior.get_selectable_nodes).
The parameters are such that it could be bound directly to the
on_key_down event of a keyboard. Therefore, it is safe to be called
repeatedly when the key is held down as is done by the keyboard.

**kivy.uix.behaviors.CompoundSelectionBehavior.select_with_key_up**

(internal) Processes a key release. This must be called by the
derived widget when a key that [`select_with_key_down()`](https://kivy.org/doc/stable/#kivy.uix.behaviors.CompoundSelectionBehavior.select_with_key_down) returned
True is released.
The parameters are such that it could be bound directly to the
on_key_up event of a keyboard.

**kivy.uix.behaviors.CompoundSelectionBehavior.select_with_touch**

(internal) Processes a touch on the node. This should be called by
the derived widget when a node is touched and is to be used for
selection. Depending on the keyboard keys pressed and the
configuration, it could select or deslect this and other nodes in the
selectable nodes list, [`get_selectable_nodes()`](https://kivy.org/doc/stable/#kivy.uix.behaviors.CompoundSelectionBehavior.get_selectable_nodes).

**kivy.uix.behaviors.CompoundSelectionBehavior.selected_nodes**

The list of selected nodes.

[`selected_nodes`](https://kivy.org/doc/stable/#kivy.uix.behaviors.CompoundSelectionBehavior.selected_nodes) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) and
defaults to the empty list, []. It is read-only and should not be modified.

**kivy.uix.behaviors.CompoundSelectionBehavior.text_entry_timeout**

When typing characters in rapid succession (i.e. the time difference
since the last character is less than [`text_entry_timeout`](https://kivy.org/doc/stable/#kivy.uix.behaviors.CompoundSelectionBehavior.text_entry_timeout)), the
keys get concatenated and the combined text is passed as the key argument
of [`goto_node()`](https://kivy.org/doc/stable/#kivy.uix.behaviors.CompoundSelectionBehavior.goto_node).
New in version 1.10.0.

**kivy.uix.behaviors.CompoundSelectionBehavior.touch_deselect_last**

Determines whether the last selected node can be deselected when
[`multiselect`](https://kivy.org/doc/stable/#kivy.uix.behaviors.CompoundSelectionBehavior.multiselect) or [`touch_multiselect`](https://kivy.org/doc/stable/#kivy.uix.behaviors.CompoundSelectionBehavior.touch_multiselect) is False.
New in version 1.10.0.
[`touch_deselect_last`](https://kivy.org/doc/stable/#kivy.uix.behaviors.CompoundSelectionBehavior.touch_deselect_last) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to True on mobile, False on desktop platforms.

**kivy.uix.behaviors.CompoundSelectionBehavior.touch_multiselect**

A special touch mode which determines whether touch events, as
processed by [`select_with_touch()`](https://kivy.org/doc/stable/#kivy.uix.behaviors.CompoundSelectionBehavior.select_with_touch), will add the currently touched
node to the selection, or if it will clear the selection before adding the
node. This allows the selection of multiple nodes by simply touching them.
This is different from [`multiselect`](https://kivy.org/doc/stable/#kivy.uix.behaviors.CompoundSelectionBehavior.multiselect) because when it is True,
simply touching an unselected node will select it, even if ctrl is not
pressed. If it is False, however, ctrl must be pressed in order to
add to the selection when [`multiselect`](https://kivy.org/doc/stable/#kivy.uix.behaviors.CompoundSelectionBehavior.multiselect) is True.

[`touch_multiselect`](https://kivy.org/doc/stable/#kivy.uix.behaviors.CompoundSelectionBehavior.touch_multiselect) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivy.uix.behaviors.CompoundSelectionBehavior.up_count**

Determines by how much the selected node is moved up or down, relative
to the position of the last selected node, when the up (or down) arrow on
the keyboard is pressed.
[`up_count`](https://kivy.org/doc/stable/#kivy.uix.behaviors.CompoundSelectionBehavior.up_count) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 1.

**kivy.uix.behaviors.CoverBehavior**

Bases: `builtins.object`
The CoverBehavior [mixin](https://en.wikipedia.org/wiki/Mixin)
provides rendering a texture covering full widget size keeping aspect ratio
of the original texture.
New in version 1.10.0.

**kivy.uix.behaviors.CoverBehavior.cover_pos**

Position of the aspect ratio aware texture. Gets calculated in
`CoverBehavior.calculate_cover`.
[`cover_pos`](https://kivy.org/doc/stable/#kivy.uix.behaviors.CoverBehavior.cover_pos) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) and
defaults to [0, 0].

**kivy.uix.behaviors.CoverBehavior.cover_size**

Size of the aspect ratio aware texture. Gets calculated in
`CoverBehavior.calculate_cover`.
[`cover_size`](https://kivy.org/doc/stable/#kivy.uix.behaviors.CoverBehavior.cover_size) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) and
defaults to [0, 0].

**kivy.uix.behaviors.CoverBehavior.reference_size**

Reference size used for aspect ratio approximation calculation.
[`reference_size`](https://kivy.org/doc/stable/#kivy.uix.behaviors.CoverBehavior.reference_size) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) and
defaults to [].

**kivy.uix.behaviors.DragBehavior**

Bases: `builtins.object`
The DragBehavior [mixin](https://en.wikipedia.org/wiki/Mixin) provides
Drag behavior. When combined with a widget, dragging in the rectangle
defined by [`drag_rectangle`](https://kivy.org/doc/stable/#kivy.uix.behaviors.DragBehavior.drag_rectangle) will drag the widget. Please see
the [`drag behaviors module`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.drag.html#module-kivy.uix.behaviors.drag) documentation
for more information.
New in version 1.8.0.

**kivy.uix.behaviors.DragBehavior.drag_distance**

Distance to move before dragging the [`DragBehavior`](https://kivy.org/doc/stable/#kivy.uix.behaviors.DragBehavior), in pixels.
As soon as the distance has been traveled, the [`DragBehavior`](https://kivy.org/doc/stable/#kivy.uix.behaviors.DragBehavior) will
start to drag, and no touch event will be dispatched to the children.
It is advisable that you base this value on the dpi of your target device’s
screen.
[`drag_distance`](https://kivy.org/doc/stable/#kivy.uix.behaviors.DragBehavior.drag_distance) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to the scroll_distance as defined in the user
[`Config`](https://kivy.org/doc/stable/api-kivy.config.html#kivy.config.Config) (20 pixels by default).

**kivy.uix.behaviors.DragBehavior.drag_rect_height**

Height of the axis aligned bounding rectangle where dragging is allowed.
[`drag_rect_height`](https://kivy.org/doc/stable/#kivy.uix.behaviors.DragBehavior.drag_rect_height) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 100.

**kivy.uix.behaviors.DragBehavior.drag_rect_width**

Width of the axis aligned bounding rectangle where dragging is allowed.
[`drag_rect_width`](https://kivy.org/doc/stable/#kivy.uix.behaviors.DragBehavior.drag_rect_width) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 100.

**kivy.uix.behaviors.DragBehavior.drag_rect_x**

X position of the axis aligned bounding rectangle where dragging
is allowed (in window coordinates).
[`drag_rect_x`](https://kivy.org/doc/stable/#kivy.uix.behaviors.DragBehavior.drag_rect_x) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0.

**kivy.uix.behaviors.DragBehavior.drag_rect_y**

Y position of the axis aligned bounding rectangle where dragging
is allowed (in window coordinates).
`drag_rect_Y` is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0.

**kivy.uix.behaviors.DragBehavior.drag_rectangle**

Position and size of the axis aligned bounding rectangle where dragging
is allowed.
[`drag_rectangle`](https://kivy.org/doc/stable/#kivy.uix.behaviors.DragBehavior.drag_rectangle) is a [`ReferenceListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ReferenceListProperty)
of ([`drag_rect_x`](https://kivy.org/doc/stable/#kivy.uix.behaviors.DragBehavior.drag_rect_x), [`drag_rect_y`](https://kivy.org/doc/stable/#kivy.uix.behaviors.DragBehavior.drag_rect_y), [`drag_rect_width`](https://kivy.org/doc/stable/#kivy.uix.behaviors.DragBehavior.drag_rect_width),
[`drag_rect_height`](https://kivy.org/doc/stable/#kivy.uix.behaviors.DragBehavior.drag_rect_height)) properties.

**kivy.uix.behaviors.DragBehavior.drag_timeout**

Timeout allowed to trigger the [`drag_distance`](https://kivy.org/doc/stable/#kivy.uix.behaviors.DragBehavior.drag_distance), in milliseconds.
If the user has not moved [`drag_distance`](https://kivy.org/doc/stable/#kivy.uix.behaviors.DragBehavior.drag_distance) within the timeout,
dragging will be disabled, and the touch event will be dispatched to the
children.
[`drag_timeout`](https://kivy.org/doc/stable/#kivy.uix.behaviors.DragBehavior.drag_timeout) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to the scroll_timeout as defined in the user
[`Config`](https://kivy.org/doc/stable/api-kivy.config.html#kivy.config.Config) (55 milliseconds by default).

**kivy.uix.behaviors.EmacsBehavior**

Bases: `builtins.object`
A [mixin](https://en.wikipedia.org/wiki/Mixin) that enables Emacs-style
keyboard shortcuts for the [`TextInput`](https://kivy.org/doc/stable/api-kivy.uix.textinput.html#kivy.uix.textinput.TextInput) widget.
Please see the [`Emacs behaviors module`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.emacs.html#module-kivy.uix.behaviors.emacs)
documentation for more information.
New in version 1.9.1.

**kivy.uix.behaviors.EmacsBehavior.delete_word_left**

Delete text left of the cursor to the beginning of word

**kivy.uix.behaviors.EmacsBehavior.delete_word_right**

Delete text right of the cursor to the end of the word

**kivy.uix.behaviors.EmacsBehavior.key_bindings**

String name which determines the type of key bindings to use with the
[`TextInput`](https://kivy.org/doc/stable/api-kivy.uix.textinput.html#kivy.uix.textinput.TextInput). This allows Emacs key bindings to
be enabled/disabled programmatically for widgets that inherit from
[`EmacsBehavior`](https://kivy.org/doc/stable/#kivy.uix.behaviors.EmacsBehavior). If the value is not `'emacs'`, Emacs bindings
will be disabled. Use `'default'` for switching to the default key
bindings of TextInput.
[`key_bindings`](https://kivy.org/doc/stable/#kivy.uix.behaviors.EmacsBehavior.key_bindings) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to `'emacs'`.
New in version 1.10.0.

**kivy.uix.behaviors.FocusBehavior**

Bases: `builtins.object`
Provides keyboard focus behavior. When combined with other
FocusBehavior widgets it allows one to cycle focus among them by pressing
tab. Please see the
[`focus behavior module documentation`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.focus.html#module-kivy.uix.behaviors.focus)
for more information.
New in version 1.9.0.

**kivy.uix.behaviors.FocusBehavior.focus**

Whether the instance currently has focus.
Setting it to True will bind to and/or request the keyboard, and input
will be forwarded to the instance. Setting it to False will unbind
and/or release the keyboard. For a given keyboard, only one widget can
have its focus, so focusing one will automatically unfocus the other
instance holding its focus.
When using a software keyboard, please refer to the
[`softinput_mode`](https://kivy.org/doc/stable/api-kivy.core.window.html#kivy.core.window.WindowBase.softinput_mode) property to determine
how the keyboard display is handled.
[`focus`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.focus.html#module-kivy.uix.behaviors.focus) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and defaults
to False.

**kivy.uix.behaviors.FocusBehavior.focus_next**

The [`FocusBehavior`](https://kivy.org/doc/stable/#kivy.uix.behaviors.FocusBehavior) instance to acquire focus when
tab is pressed and this instance has focus, if not None or
StopIteration.
When tab is pressed, focus cycles through all the [`FocusBehavior`](https://kivy.org/doc/stable/#kivy.uix.behaviors.FocusBehavior)
widgets that are linked through [`focus_next`](https://kivy.org/doc/stable/#kivy.uix.behaviors.FocusBehavior.focus_next) and are focusable. If
[`focus_next`](https://kivy.org/doc/stable/#kivy.uix.behaviors.FocusBehavior.focus_next) is None, it instead walks the children lists to find
the next focusable widget. Finally, if [`focus_next`](https://kivy.org/doc/stable/#kivy.uix.behaviors.FocusBehavior.focus_next) is
the StopIteration class, focus won’t move forward, but end here.
[`focus_next`](https://kivy.org/doc/stable/#kivy.uix.behaviors.FocusBehavior.focus_next) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to None.

**kivy.uix.behaviors.FocusBehavior.focus_previous**

The [`FocusBehavior`](https://kivy.org/doc/stable/#kivy.uix.behaviors.FocusBehavior) instance to acquire focus when
shift+tab is pressed on this instance, if not None or StopIteration.
When shift+tab is pressed, focus cycles through all the
[`FocusBehavior`](https://kivy.org/doc/stable/#kivy.uix.behaviors.FocusBehavior) widgets that are linked through
[`focus_previous`](https://kivy.org/doc/stable/#kivy.uix.behaviors.FocusBehavior.focus_previous) and are focusable. If [`focus_previous`](https://kivy.org/doc/stable/#kivy.uix.behaviors.FocusBehavior.focus_previous) is
None, it instead walks the children tree to find the
previous focusable widget. Finally, if [`focus_previous`](https://kivy.org/doc/stable/#kivy.uix.behaviors.FocusBehavior.focus_previous) is the
StopIteration class, focus won’t move backward, but end here.
[`focus_previous`](https://kivy.org/doc/stable/#kivy.uix.behaviors.FocusBehavior.focus_previous) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to None.

**kivy.uix.behaviors.FocusBehavior.focused**

An alias of [`focus`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.focus.html#module-kivy.uix.behaviors.focus).
[`focused`](https://kivy.org/doc/stable/#kivy.uix.behaviors.FocusBehavior.focused) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and defaults
to False.

**kivy.uix.behaviors.FocusBehavior.get_focus_next**

Returns the next focusable widget using either [`focus_next`](https://kivy.org/doc/stable/#kivy.uix.behaviors.FocusBehavior.focus_next)
or the `children` similar to the order when tabbing forwards
with the `tab` key.

**kivy.uix.behaviors.FocusBehavior.get_focus_previous**

Returns the previous focusable widget using either
[`focus_previous`](https://kivy.org/doc/stable/#kivy.uix.behaviors.FocusBehavior.focus_previous) or the `children` similar to the
order when the `tab` + `shift` keys are triggered together.

**kivy.uix.behaviors.FocusBehavior.hide_keyboard**

Convenience function to hide the keyboard in managed mode.

**kivy.uix.behaviors.FocusBehavior.ignored_touch**

A list of touches that should not be used to defocus. After on_touch_up,
every touch that is not in [`ignored_touch`](https://kivy.org/doc/stable/#kivy.uix.behaviors.FocusBehavior.ignored_touch) will defocus all the
focused widgets if the config keyboard mode is not multi. Touches on
focusable widgets that were used to focus are automatically added here.
Example usage:

Notice that you need to access this as a class, not an instance variable.

**kivy.uix.behaviors.FocusBehavior.input_type**

The kind of input keyboard to request.
New in version 1.8.0.
Changed in version 2.1.0:Changed default value from text to null. Added null to options.
[`input_type`](https://kivy.org/doc/stable/#kivy.uix.behaviors.FocusBehavior.input_type) is an `OptionsProperty` and
defaults to ‘null’. Can be one of ‘null’, ‘text’, ‘number’, ‘url’, ‘mail’,
‘datetime’, ‘tel’ or ‘address’.

**kivy.uix.behaviors.FocusBehavior.is_focusable**

Whether the instance can become focused. If focused, it’ll lose focus
when set to False.
[`is_focusable`](https://kivy.org/doc/stable/#kivy.uix.behaviors.FocusBehavior.is_focusable) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to True on a desktop (i.e. desktop is True in
[`config`](https://kivy.org/doc/stable/api-kivy.config.html#module-kivy.config)), False otherwise.

**kivy.uix.behaviors.FocusBehavior.keyboard**

The keyboard to bind to (or bound to the widget) when focused.
When None, a keyboard is requested and released whenever the widget comes
into and out of focus. If not None, it must be a keyboard, which gets
bound and unbound from the widget whenever it’s in or out of focus. It is
useful only when more than one keyboard is available, so it is recommended
to be set to None when only one keyboard is available.
If more than one keyboard is available, whenever an instance gets focused
a new keyboard will be requested if None. Unless the other instances lose
focus (e.g. if tab was used), a new keyboard will appear. When this is
undesired, the keyboard property can be used. For example, if there are
two users with two keyboards, then each keyboard can be assigned to
different groups of instances of FocusBehavior, ensuring that within
each group, only one FocusBehavior will have focus, and will receive input
from the correct keyboard. See keyboard_mode in [`config`](https://kivy.org/doc/stable/api-kivy.config.html#module-kivy.config) for
more information on the keyboard modes.
**Keyboard and focus behavior**
When using the keyboard, there are some important default behaviors you
should keep in mind.
When Config’s keyboard_mode is multi, each new touch is considered
a touch by a different user and will set the focus (if clicked on a
focusable) with a new keyboard. Already focused elements will not lose
their focus (even if an unfocusable widget is touched).
If the keyboard property is set, that keyboard will be used when the
instance gets focused. If widgets with different keyboards are linked
through [`focus_next`](https://kivy.org/doc/stable/#kivy.uix.behaviors.FocusBehavior.focus_next) and [`focus_previous`](https://kivy.org/doc/stable/#kivy.uix.behaviors.FocusBehavior.focus_previous), then as they are
tabbed through, different keyboards will become active. Therefore,
typically it’s undesirable to link instances which are assigned
different keyboards.
When a widget has focus, setting its keyboard to None will remove its
keyboard, but the widget will then immediately try to get
another keyboard. In order to remove its keyboard, rather set its
[`focus`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.focus.html#module-kivy.uix.behaviors.focus) to False.
When using a software keyboard, typical on mobile and touch devices, the
keyboard display behavior is determined by the
[`softinput_mode`](https://kivy.org/doc/stable/api-kivy.core.window.html#kivy.core.window.WindowBase.softinput_mode) property. You can use
this property to ensure the focused widget is not covered or obscured.
[`keyboard`](https://kivy.org/doc/stable/#kivy.uix.behaviors.FocusBehavior.keyboard) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) and defaults
to None.

**kivy.uix.behaviors.FocusBehavior.keyboard_mode**

Determines how the keyboard visibility should be managed. ‘auto’ will
result in the standard behavior of showing/hiding on focus. ‘managed’
requires setting the keyboard visibility manually, or calling the helper
functions [`show_keyboard()`](https://kivy.org/doc/stable/#kivy.uix.behaviors.FocusBehavior.show_keyboard) and [`hide_keyboard()`](https://kivy.org/doc/stable/#kivy.uix.behaviors.FocusBehavior.hide_keyboard).
[`keyboard_mode`](https://kivy.org/doc/stable/#kivy.uix.behaviors.FocusBehavior.keyboard_mode) is an `OptionsProperty` and
defaults to ‘auto’. Can be one of ‘auto’ or ‘managed’.

**kivy.uix.behaviors.FocusBehavior.keyboard_on_key_down**

The method bound to the keyboard when the instance has focus.
When the instance becomes focused, this method is bound to the
keyboard and will be called for every input press. The parameters are
the same as [`kivy.core.window.WindowBase.on_key_down()`](https://kivy.org/doc/stable/api-kivy.core.window.html#kivy.core.window.WindowBase.on_key_down).
When overwriting the method in the derived widget, super should be
called to enable tab cycling. If the derived widget wishes to use tab
for its own purposes, it can call super after it has processed the
character (if it does not wish to consume the tab).
Similar to other keyboard functions, it should return True if the
key was consumed.

**kivy.uix.behaviors.FocusBehavior.keyboard_on_key_up**

The method bound to the keyboard when the instance has focus.
When the instance becomes focused, this method is bound to the
keyboard and will be called for every input release. The parameters are
the same as [`kivy.core.window.WindowBase.on_key_up()`](https://kivy.org/doc/stable/api-kivy.core.window.html#kivy.core.window.WindowBase.on_key_up).
When overwriting the method in the derived widget, super should be
called to enable de-focusing on escape. If the derived widget wishes
to use escape for its own purposes, it can call super after it has
processed the character (if it does not wish to consume the escape).
See [`keyboard_on_key_down()`](https://kivy.org/doc/stable/#kivy.uix.behaviors.FocusBehavior.keyboard_on_key_down)

**kivy.uix.behaviors.FocusBehavior.keyboard_suggestions**

If True provides auto suggestions on top of keyboard.
This will only work if [`input_type`](https://kivy.org/doc/stable/#kivy.uix.behaviors.FocusBehavior.input_type) is set to text, url, mail or
address.

New in version 2.1.0.
[`keyboard_suggestions`](https://kivy.org/doc/stable/#kivy.uix.behaviors.FocusBehavior.keyboard_suggestions) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to True

**kivy.uix.behaviors.FocusBehavior.show_keyboard**

Convenience function to show the keyboard in managed mode.

**kivy.uix.behaviors.FocusBehavior.unfocus_on_touch**

Whether a instance should lose focus when clicked outside the instance.
When a user clicks on a widget that is focus aware and shares the same
keyboard as this widget (which in the case with only one keyboard),
then as the other widgets gain focus, this widget loses focus. In addition
to that, if this property is True, clicking on any widget other than this
widget, will remove focus from this widget.
[`unfocus_on_touch`](https://kivy.org/doc/stable/#kivy.uix.behaviors.FocusBehavior.unfocus_on_touch) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to False if the keyboard_mode in [`Config`](https://kivy.org/doc/stable/api-kivy.config.html#kivy.config.Config)
is ‘multi’ or ‘systemandmulti’, otherwise it defaults to True.

**kivy.uix.behaviors.ToggleButtonBehavior**

Bases: [`kivy.uix.behaviors.button.ButtonBehavior`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.button.html#kivy.uix.behaviors.button.ButtonBehavior)
This [mixin](https://en.wikipedia.org/wiki/Mixin) class provides
[`togglebutton`](https://kivy.org/doc/stable/api-kivy.uix.togglebutton.html#module-kivy.uix.togglebutton) behavior. Please see the
[`togglebutton behaviors module`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.togglebutton.html#module-kivy.uix.behaviors.togglebutton)
documentation for more information.
New in version 1.8.0.

**kivy.uix.behaviors.ToggleButtonBehavior.allow_no_selection**

This specifies whether the widgets in a group allow no selection i.e.
everything to be deselected.
New in version 1.9.0.
[`allow_no_selection`](https://kivy.org/doc/stable/#kivy.uix.behaviors.ToggleButtonBehavior.allow_no_selection) is a `BooleanProperty` and defaults to
True

**kivy.uix.behaviors.ToggleButtonBehavior.get_widgets**

Return a list of the widgets contained in a specific group. If the
group doesn’t exist, an empty list will be returned.

**kivy.uix.behaviors.ToggleButtonBehavior.group**

Group of the button. If None, no group will be used (the button will be
independent). If specified, [`group`](https://kivy.org/doc/stable/#kivy.uix.behaviors.ToggleButtonBehavior.group) must be a hashable object, like
a string. Only one button in a group can be in a ‘down’ state.
[`group`](https://kivy.org/doc/stable/#kivy.uix.behaviors.ToggleButtonBehavior.group) is a [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and defaults to
None.

**kivy.uix.behaviors.TouchRippleBehavior**

Bases: `builtins.object`
Touch ripple behavior.
Supposed to be used as mixin on widget classes.
Ripple behavior does not trigger automatically, concrete implementation
needs to call [`ripple_show()`](https://kivy.org/doc/stable/#kivy.uix.behaviors.TouchRippleBehavior.ripple_show) respective [`ripple_fade()`](https://kivy.org/doc/stable/#kivy.uix.behaviors.TouchRippleBehavior.ripple_fade) manually.
Example[¶](https://kivy.org/doc/stable/#example)
Here we create a Label which renders the touch ripple animation on
interaction:

**kivy.uix.behaviors.TouchRippleBehavior.ripple_duration_in**

Animation duration taken to show the overlay.
[`ripple_duration_in`](https://kivy.org/doc/stable/#kivy.uix.behaviors.TouchRippleBehavior.ripple_duration_in) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.5.

**kivy.uix.behaviors.TouchRippleBehavior.ripple_duration_out**

Animation duration taken to fade the overlay.
[`ripple_duration_out`](https://kivy.org/doc/stable/#kivy.uix.behaviors.TouchRippleBehavior.ripple_duration_out) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.2.

**kivy.uix.behaviors.TouchRippleBehavior.ripple_fade**

Finish ripple animation on current widget.

**kivy.uix.behaviors.TouchRippleBehavior.ripple_fade_from_alpha**

Alpha channel for ripple color the animation starts with.
[`ripple_fade_from_alpha`](https://kivy.org/doc/stable/#kivy.uix.behaviors.TouchRippleBehavior.ripple_fade_from_alpha) is a
[`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and defaults to 0.5.

**kivy.uix.behaviors.TouchRippleBehavior.ripple_fade_to_alpha**

Alpha channel for ripple color the animation targets to.
[`ripple_fade_to_alpha`](https://kivy.org/doc/stable/#kivy.uix.behaviors.TouchRippleBehavior.ripple_fade_to_alpha) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.8.

**kivy.uix.behaviors.TouchRippleBehavior.ripple_func_in**

Animation callback for showing the overlay.
[`ripple_func_in`](https://kivy.org/doc/stable/#kivy.uix.behaviors.TouchRippleBehavior.ripple_func_in) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to in_cubic.

**kivy.uix.behaviors.TouchRippleBehavior.ripple_func_out**

Animation callback for hiding the overlay.
[`ripple_func_out`](https://kivy.org/doc/stable/#kivy.uix.behaviors.TouchRippleBehavior.ripple_func_out) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to out_quad.

**kivy.uix.behaviors.TouchRippleBehavior.ripple_rad_default**

Default radius the animation starts from.
[`ripple_rad_default`](https://kivy.org/doc/stable/#kivy.uix.behaviors.TouchRippleBehavior.ripple_rad_default) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 10.

**kivy.uix.behaviors.TouchRippleBehavior.ripple_scale**

Max scale of the animation overlay calculated from max(width/height) of
the decorated widget.
[`ripple_scale`](https://kivy.org/doc/stable/#kivy.uix.behaviors.TouchRippleBehavior.ripple_scale) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 2.0.

**kivy.uix.behaviors.TouchRippleBehavior.ripple_show**

Begin ripple animation on current widget.
Expects touch event as argument.

**kivy.uix.behaviors.TouchRippleButtonBehavior**

Bases: [`kivy.uix.behaviors.touchripple.TouchRippleBehavior`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.touchripple.html#kivy.uix.behaviors.touchripple.TouchRippleBehavior)
This [mixin](https://en.wikipedia.org/wiki/Mixin) class provides
a similar behavior to [`ButtonBehavior`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.button.html#kivy.uix.behaviors.button.ButtonBehavior)
but provides touch ripple animation instead of button pressed/released as
visual effect.

**kivy.uix.behaviors.TouchRippleButtonBehavior.always_release**

This determines whether or not the widget fires an on_release event if
the touch_up is outside the widget.
[`always_release`](https://kivy.org/doc/stable/#kivy.uix.behaviors.TouchRippleButtonBehavior.always_release) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to False.

**kivy.uix.behaviors.TouchRippleButtonBehavior.last_touch**

Contains the last relevant touch received by the Button. This can
be used in on_press or on_release in order to know which touch
dispatched the event.
[`last_touch`](https://kivy.org/doc/stable/#kivy.uix.behaviors.TouchRippleButtonBehavior.last_touch) is a [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to None.

---

## API - [`kivy.uix.behaviors.button`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.button.html)

**kivy.uix.behaviors.button.ButtonBehavior**

Bases: `builtins.object`
This [mixin](https://en.wikipedia.org/wiki/Mixin) class provides
[`Button`](https://kivy.org/doc/stable/api-kivy.uix.button.html#kivy.uix.button.Button) behavior. Please see the
[`button behaviors module`](https://kivy.org/doc/stable/#module-kivy.uix.behaviors.button) documentation
for more information.

**kivy.uix.behaviors.button.ButtonBehavior.always_release**

This determines whether or not the widget fires an on_release event if
the touch_up is outside the widget.
New in version 1.9.0.
Changed in version 1.10.0:The default value is now False.
[`always_release`](https://kivy.org/doc/stable/#kivy.uix.behaviors.button.ButtonBehavior.always_release) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to False.

**kivy.uix.behaviors.button.ButtonBehavior.last_touch**

Contains the last relevant touch received by the Button. This can
be used in on_press or on_release in order to know which touch
dispatched the event.
New in version 1.8.0.
[`last_touch`](https://kivy.org/doc/stable/#kivy.uix.behaviors.button.ButtonBehavior.last_touch) is a [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to None.

**kivy.uix.behaviors.button.ButtonBehavior.min_state_time**

The minimum period of time which the widget must remain in the
‘down’ state.
New in version 1.9.1.
[`min_state_time`](https://kivy.org/doc/stable/#kivy.uix.behaviors.button.ButtonBehavior.min_state_time) is a float and defaults to 0.035. This value is
taken from [`Config`](https://kivy.org/doc/stable/api-kivy.config.html#kivy.config.Config).

**kivy.uix.behaviors.button.ButtonBehavior.state**

The state of the button, must be one of ‘normal’ or ‘down’.
The state is ‘down’ only when the button is currently touched/clicked,
otherwise its ‘normal’.
[`state`](https://kivy.org/doc/stable/#kivy.uix.behaviors.button.ButtonBehavior.state) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty) and defaults
to ‘normal’.

**kivy.uix.behaviors.button.ButtonBehavior.trigger_action**

Trigger whatever action(s) have been bound to the button by calling
both the on_press and on_release callbacks.
This is similar to a quick button press without using any touch events,
but note that like most kivy code, this is not guaranteed to be safe to
call from external threads. If needed use
[`Clock`](https://kivy.org/doc/stable/api-kivy.clock.html#kivy.clock.Clock) to safely schedule this function and
the resulting callbacks to be called from the main thread.
Duration is the length of the press in seconds. Pass 0 if you want
the action to happen instantly.
New in version 1.8.0.

---

## API - [`kivy.uix.behaviors.codenavigation`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.codenavigation.html)

**kivy.uix.behaviors.codenavigation.CodeNavigationBehavior**

Bases: [`kivy.event.EventDispatcher`](https://kivy.org/doc/stable/api-kivy.event.html#kivy.event.EventDispatcher)
Code navigation behavior. Modifies the navigation behavior in TextInput
to work like an IDE instead of a word processor. Please see the
[`code navigation behaviors module`](https://kivy.org/doc/stable/#module-kivy.uix.behaviors.codenavigation)
documentation for more information.
New in version 1.9.1.

---

## API - [`kivy.uix.behaviors.compoundselection`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.compoundselection.html)

**kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior**

Bases: `builtins.object`
The Selection behavior [mixin](https://en.wikipedia.org/wiki/Mixin)
implements the logic behind keyboard and touch
selection of selectable widgets managed by the derived widget. Please see
the [`compound selection behaviors module`](https://kivy.org/doc/stable/#module-kivy.uix.behaviors.compoundselection) documentation
for more information.
New in version 1.9.0.

**kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.clear_selection**

Deselects all the currently selected nodes.

**kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.deselect_node**

Deselects a possibly selected node.
It is called by the controller when it deselects a node and can also
be called from the outside to deselect a node directly. The derived
widget should overwrite this method and change the node to its
unselected state when this is called

**kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.get_index_of_node**

(internal) Returns the index of the node within the
selectable_nodes returned by [`get_selectable_nodes()`](https://kivy.org/doc/stable/#kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.get_selectable_nodes).

**kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.get_selectable_nodes**

(internal) Returns a list of the nodes that can be selected. It can
be overwritten by the derived widget to return the correct list.
This list is used to determine which nodes to select with group
selection. E.g. the last element in the list will be selected when
home is pressed, pagedown will move (or add to, if shift is held) the
selection from the current position by negative [`page_count`](https://kivy.org/doc/stable/#kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.page_count)
nodes starting from the position of the currently selected node in
this list and so on. Still, nodes can be selected even if they are not
in this list.

Defaults to returning [`children`](https://kivy.org/doc/stable/api-kivy.uix.widget.html#kivy.uix.widget.Widget.children).

**kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.goto_node**

(internal) Used by the controller to get the node at the position
indicated by key. The key can be keyboard inputs, e.g. pageup,
or scroll inputs from the mouse scroll wheel, e.g. scrollup.
‘last_node’ is the last node selected and is used to find the resulting
node. For example, if the key is up, the returned node is one node
up from the last node.
It can be overwritten by the derived widget.

**kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.keyboard_select**

Determines whether the keyboard can be used for selection. If False,
keyboard inputs will be ignored.
[`keyboard_select`](https://kivy.org/doc/stable/#kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.keyboard_select) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to True.

**kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.multiselect**

Determines whether multiple nodes can be selected. If enabled, keyboard
shift and ctrl selection, optionally combined with touch, for example, will
be able to select multiple widgets in the normally expected manner.
This dominates [`touch_multiselect`](https://kivy.org/doc/stable/#kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.touch_multiselect) when False.
[`multiselect`](https://kivy.org/doc/stable/#kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.multiselect) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to False.

**kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.nodes_order_reversed**

(Internal) Indicates whether the order of the nodes as displayed top-
down is reversed compared to their order in [`get_selectable_nodes()`](https://kivy.org/doc/stable/#kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.get_selectable_nodes)
(e.g. how the children property is reversed compared to how
it’s displayed).

**kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.page_count**

Determines by how much the selected node is moved up or down, relative
to the position of the last selected node, when pageup (or pagedown) is
pressed.
[`page_count`](https://kivy.org/doc/stable/#kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.page_count) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 10.

**kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.right_count**

Determines by how much the selected node is moved up or down, relative
to the position of the last selected node, when the right (or left) arrow
on the keyboard is pressed.
[`right_count`](https://kivy.org/doc/stable/#kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.right_count) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 1.

**kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.scroll_count**

Determines by how much the selected node is moved up or down, relative
to the position of the last selected node, when the mouse scroll wheel is
scrolled.
[`right_count`](https://kivy.org/doc/stable/#kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.right_count) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0.

**kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.select_node**

Selects a node.
It is called by the controller when it selects a node and can be
called from the outside to select a node directly. The derived widget
should overwrite this method and change the node state to selected
when called.

**kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.select_with_key_down**

Processes a key press. This is called when a key press is to be used
for selection. Depending on the keyboard keys pressed and the
configuration, it could select or deselect nodes or node ranges
from the selectable nodes list, [`get_selectable_nodes()`](https://kivy.org/doc/stable/#kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.get_selectable_nodes).
The parameters are such that it could be bound directly to the
on_key_down event of a keyboard. Therefore, it is safe to be called
repeatedly when the key is held down as is done by the keyboard.

**kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.select_with_key_up**

(internal) Processes a key release. This must be called by the
derived widget when a key that [`select_with_key_down()`](https://kivy.org/doc/stable/#kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.select_with_key_down) returned
True is released.
The parameters are such that it could be bound directly to the
on_key_up event of a keyboard.

**kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.select_with_touch**

(internal) Processes a touch on the node. This should be called by
the derived widget when a node is touched and is to be used for
selection. Depending on the keyboard keys pressed and the
configuration, it could select or deslect this and other nodes in the
selectable nodes list, [`get_selectable_nodes()`](https://kivy.org/doc/stable/#kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.get_selectable_nodes).

**kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.selected_nodes**

The list of selected nodes.

[`selected_nodes`](https://kivy.org/doc/stable/#kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.selected_nodes) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) and
defaults to the empty list, []. It is read-only and should not be modified.

**kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.text_entry_timeout**

When typing characters in rapid succession (i.e. the time difference
since the last character is less than [`text_entry_timeout`](https://kivy.org/doc/stable/#kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.text_entry_timeout)), the
keys get concatenated and the combined text is passed as the key argument
of [`goto_node()`](https://kivy.org/doc/stable/#kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.goto_node).
New in version 1.10.0.

**kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.touch_deselect_last**

Determines whether the last selected node can be deselected when
[`multiselect`](https://kivy.org/doc/stable/#kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.multiselect) or [`touch_multiselect`](https://kivy.org/doc/stable/#kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.touch_multiselect) is False.
New in version 1.10.0.
[`touch_deselect_last`](https://kivy.org/doc/stable/#kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.touch_deselect_last) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to True on mobile, False on desktop platforms.

**kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.touch_multiselect**

A special touch mode which determines whether touch events, as
processed by [`select_with_touch()`](https://kivy.org/doc/stable/#kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.select_with_touch), will add the currently touched
node to the selection, or if it will clear the selection before adding the
node. This allows the selection of multiple nodes by simply touching them.
This is different from [`multiselect`](https://kivy.org/doc/stable/#kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.multiselect) because when it is True,
simply touching an unselected node will select it, even if ctrl is not
pressed. If it is False, however, ctrl must be pressed in order to
add to the selection when [`multiselect`](https://kivy.org/doc/stable/#kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.multiselect) is True.

[`touch_multiselect`](https://kivy.org/doc/stable/#kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.touch_multiselect) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.up_count**

Determines by how much the selected node is moved up or down, relative
to the position of the last selected node, when the up (or down) arrow on
the keyboard is pressed.
[`up_count`](https://kivy.org/doc/stable/#kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior.up_count) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 1.

---

## API - [`kivy.uix.behaviors.cover`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.cover.html)

**kivy.uix.behaviors.cover.CoverBehavior**

Bases: `builtins.object`
The CoverBehavior [mixin](https://en.wikipedia.org/wiki/Mixin)
provides rendering a texture covering full widget size keeping aspect ratio
of the original texture.
New in version 1.10.0.

**kivy.uix.behaviors.cover.CoverBehavior.cover_pos**

Position of the aspect ratio aware texture. Gets calculated in
`CoverBehavior.calculate_cover`.
[`cover_pos`](https://kivy.org/doc/stable/#kivy.uix.behaviors.cover.CoverBehavior.cover_pos) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) and
defaults to [0, 0].

**kivy.uix.behaviors.cover.CoverBehavior.cover_size**

Size of the aspect ratio aware texture. Gets calculated in
`CoverBehavior.calculate_cover`.
[`cover_size`](https://kivy.org/doc/stable/#kivy.uix.behaviors.cover.CoverBehavior.cover_size) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) and
defaults to [0, 0].

**kivy.uix.behaviors.cover.CoverBehavior.reference_size**

Reference size used for aspect ratio approximation calculation.
[`reference_size`](https://kivy.org/doc/stable/#kivy.uix.behaviors.cover.CoverBehavior.reference_size) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) and
defaults to [].

---

## API - [`kivy.uix.behaviors.drag`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.drag.html)

**kivy.uix.behaviors.drag.DragBehavior**

Bases: `builtins.object`
The DragBehavior [mixin](https://en.wikipedia.org/wiki/Mixin) provides
Drag behavior. When combined with a widget, dragging in the rectangle
defined by [`drag_rectangle`](https://kivy.org/doc/stable/#kivy.uix.behaviors.drag.DragBehavior.drag_rectangle) will drag the widget. Please see
the [`drag behaviors module`](https://kivy.org/doc/stable/#module-kivy.uix.behaviors.drag) documentation
for more information.
New in version 1.8.0.

**kivy.uix.behaviors.drag.DragBehavior.drag_distance**

Distance to move before dragging the [`DragBehavior`](https://kivy.org/doc/stable/#kivy.uix.behaviors.drag.DragBehavior), in pixels.
As soon as the distance has been traveled, the [`DragBehavior`](https://kivy.org/doc/stable/#kivy.uix.behaviors.drag.DragBehavior) will
start to drag, and no touch event will be dispatched to the children.
It is advisable that you base this value on the dpi of your target device’s
screen.
[`drag_distance`](https://kivy.org/doc/stable/#kivy.uix.behaviors.drag.DragBehavior.drag_distance) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to the scroll_distance as defined in the user
[`Config`](https://kivy.org/doc/stable/api-kivy.config.html#kivy.config.Config) (20 pixels by default).

**kivy.uix.behaviors.drag.DragBehavior.drag_rect_height**

Height of the axis aligned bounding rectangle where dragging is allowed.
[`drag_rect_height`](https://kivy.org/doc/stable/#kivy.uix.behaviors.drag.DragBehavior.drag_rect_height) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 100.

**kivy.uix.behaviors.drag.DragBehavior.drag_rect_width**

Width of the axis aligned bounding rectangle where dragging is allowed.
[`drag_rect_width`](https://kivy.org/doc/stable/#kivy.uix.behaviors.drag.DragBehavior.drag_rect_width) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 100.

**kivy.uix.behaviors.drag.DragBehavior.drag_rect_x**

X position of the axis aligned bounding rectangle where dragging
is allowed (in window coordinates).
[`drag_rect_x`](https://kivy.org/doc/stable/#kivy.uix.behaviors.drag.DragBehavior.drag_rect_x) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0.

**kivy.uix.behaviors.drag.DragBehavior.drag_rect_y**

Y position of the axis aligned bounding rectangle where dragging
is allowed (in window coordinates).
`drag_rect_Y` is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0.

**kivy.uix.behaviors.drag.DragBehavior.drag_rectangle**

Position and size of the axis aligned bounding rectangle where dragging
is allowed.
[`drag_rectangle`](https://kivy.org/doc/stable/#kivy.uix.behaviors.drag.DragBehavior.drag_rectangle) is a [`ReferenceListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ReferenceListProperty)
of ([`drag_rect_x`](https://kivy.org/doc/stable/#kivy.uix.behaviors.drag.DragBehavior.drag_rect_x), [`drag_rect_y`](https://kivy.org/doc/stable/#kivy.uix.behaviors.drag.DragBehavior.drag_rect_y), [`drag_rect_width`](https://kivy.org/doc/stable/#kivy.uix.behaviors.drag.DragBehavior.drag_rect_width),
[`drag_rect_height`](https://kivy.org/doc/stable/#kivy.uix.behaviors.drag.DragBehavior.drag_rect_height)) properties.

**kivy.uix.behaviors.drag.DragBehavior.drag_timeout**

Timeout allowed to trigger the [`drag_distance`](https://kivy.org/doc/stable/#kivy.uix.behaviors.drag.DragBehavior.drag_distance), in milliseconds.
If the user has not moved [`drag_distance`](https://kivy.org/doc/stable/#kivy.uix.behaviors.drag.DragBehavior.drag_distance) within the timeout,
dragging will be disabled, and the touch event will be dispatched to the
children.
[`drag_timeout`](https://kivy.org/doc/stable/#kivy.uix.behaviors.drag.DragBehavior.drag_timeout) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to the scroll_timeout as defined in the user
[`Config`](https://kivy.org/doc/stable/api-kivy.config.html#kivy.config.Config) (55 milliseconds by default).

---

## API - [`kivy.uix.behaviors.emacs`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.emacs.html)

**kivy.uix.behaviors.emacs.EmacsBehavior**

Bases: `builtins.object`
A [mixin](https://en.wikipedia.org/wiki/Mixin) that enables Emacs-style
keyboard shortcuts for the [`TextInput`](https://kivy.org/doc/stable/api-kivy.uix.textinput.html#kivy.uix.textinput.TextInput) widget.
Please see the [`Emacs behaviors module`](https://kivy.org/doc/stable/#module-kivy.uix.behaviors.emacs)
documentation for more information.
New in version 1.9.1.

**kivy.uix.behaviors.emacs.EmacsBehavior.delete_word_left**

Delete text left of the cursor to the beginning of word

**kivy.uix.behaviors.emacs.EmacsBehavior.delete_word_right**

Delete text right of the cursor to the end of the word

**kivy.uix.behaviors.emacs.EmacsBehavior.key_bindings**

String name which determines the type of key bindings to use with the
[`TextInput`](https://kivy.org/doc/stable/api-kivy.uix.textinput.html#kivy.uix.textinput.TextInput). This allows Emacs key bindings to
be enabled/disabled programmatically for widgets that inherit from
[`EmacsBehavior`](https://kivy.org/doc/stable/#kivy.uix.behaviors.emacs.EmacsBehavior). If the value is not `'emacs'`, Emacs bindings
will be disabled. Use `'default'` for switching to the default key
bindings of TextInput.
[`key_bindings`](https://kivy.org/doc/stable/#kivy.uix.behaviors.emacs.EmacsBehavior.key_bindings) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to `'emacs'`.
New in version 1.10.0.

---

## API - [`kivy.uix.behaviors.focus`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.focus.html)

**kivy.uix.behaviors.focus.FocusBehavior**

Bases: `builtins.object`
Provides keyboard focus behavior. When combined with other
FocusBehavior widgets it allows one to cycle focus among them by pressing
tab. Please see the
[`focus behavior module documentation`](https://kivy.org/doc/stable/#module-kivy.uix.behaviors.focus)
for more information.
New in version 1.9.0.

**kivy.uix.behaviors.focus.FocusBehavior.focus**

Whether the instance currently has focus.
Setting it to True will bind to and/or request the keyboard, and input
will be forwarded to the instance. Setting it to False will unbind
and/or release the keyboard. For a given keyboard, only one widget can
have its focus, so focusing one will automatically unfocus the other
instance holding its focus.
When using a software keyboard, please refer to the
[`softinput_mode`](https://kivy.org/doc/stable/api-kivy.core.window.html#kivy.core.window.WindowBase.softinput_mode) property to determine
how the keyboard display is handled.
[`focus`](https://kivy.org/doc/stable/#kivy.uix.behaviors.focus.FocusBehavior.focus) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and defaults
to False.

**kivy.uix.behaviors.focus.FocusBehavior.focus_next**

The [`FocusBehavior`](https://kivy.org/doc/stable/#kivy.uix.behaviors.focus.FocusBehavior) instance to acquire focus when
tab is pressed and this instance has focus, if not None or
StopIteration.
When tab is pressed, focus cycles through all the [`FocusBehavior`](https://kivy.org/doc/stable/#kivy.uix.behaviors.focus.FocusBehavior)
widgets that are linked through [`focus_next`](https://kivy.org/doc/stable/#kivy.uix.behaviors.focus.FocusBehavior.focus_next) and are focusable. If
[`focus_next`](https://kivy.org/doc/stable/#kivy.uix.behaviors.focus.FocusBehavior.focus_next) is None, it instead walks the children lists to find
the next focusable widget. Finally, if [`focus_next`](https://kivy.org/doc/stable/#kivy.uix.behaviors.focus.FocusBehavior.focus_next) is
the StopIteration class, focus won’t move forward, but end here.
[`focus_next`](https://kivy.org/doc/stable/#kivy.uix.behaviors.focus.FocusBehavior.focus_next) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to None.

**kivy.uix.behaviors.focus.FocusBehavior.focus_previous**

The [`FocusBehavior`](https://kivy.org/doc/stable/#kivy.uix.behaviors.focus.FocusBehavior) instance to acquire focus when
shift+tab is pressed on this instance, if not None or StopIteration.
When shift+tab is pressed, focus cycles through all the
[`FocusBehavior`](https://kivy.org/doc/stable/#kivy.uix.behaviors.focus.FocusBehavior) widgets that are linked through
[`focus_previous`](https://kivy.org/doc/stable/#kivy.uix.behaviors.focus.FocusBehavior.focus_previous) and are focusable. If [`focus_previous`](https://kivy.org/doc/stable/#kivy.uix.behaviors.focus.FocusBehavior.focus_previous) is
None, it instead walks the children tree to find the
previous focusable widget. Finally, if [`focus_previous`](https://kivy.org/doc/stable/#kivy.uix.behaviors.focus.FocusBehavior.focus_previous) is the
StopIteration class, focus won’t move backward, but end here.
[`focus_previous`](https://kivy.org/doc/stable/#kivy.uix.behaviors.focus.FocusBehavior.focus_previous) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to None.

**kivy.uix.behaviors.focus.FocusBehavior.focused**

An alias of [`focus`](https://kivy.org/doc/stable/#kivy.uix.behaviors.focus.FocusBehavior.focus).
[`focused`](https://kivy.org/doc/stable/#kivy.uix.behaviors.focus.FocusBehavior.focused) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and defaults
to False.

**kivy.uix.behaviors.focus.FocusBehavior.get_focus_next**

Returns the next focusable widget using either [`focus_next`](https://kivy.org/doc/stable/#kivy.uix.behaviors.focus.FocusBehavior.focus_next)
or the `children` similar to the order when tabbing forwards
with the `tab` key.

**kivy.uix.behaviors.focus.FocusBehavior.get_focus_previous**

Returns the previous focusable widget using either
[`focus_previous`](https://kivy.org/doc/stable/#kivy.uix.behaviors.focus.FocusBehavior.focus_previous) or the `children` similar to the
order when the `tab` + `shift` keys are triggered together.

**kivy.uix.behaviors.focus.FocusBehavior.hide_keyboard**

Convenience function to hide the keyboard in managed mode.

**kivy.uix.behaviors.focus.FocusBehavior.ignored_touch**

A list of touches that should not be used to defocus. After on_touch_up,
every touch that is not in [`ignored_touch`](https://kivy.org/doc/stable/#kivy.uix.behaviors.focus.FocusBehavior.ignored_touch) will defocus all the
focused widgets if the config keyboard mode is not multi. Touches on
focusable widgets that were used to focus are automatically added here.
Example usage:

Notice that you need to access this as a class, not an instance variable.

**kivy.uix.behaviors.focus.FocusBehavior.input_type**

The kind of input keyboard to request.
New in version 1.8.0.
Changed in version 2.1.0:Changed default value from text to null. Added null to options.
[`input_type`](https://kivy.org/doc/stable/#kivy.uix.behaviors.focus.FocusBehavior.input_type) is an `OptionsProperty` and
defaults to ‘null’. Can be one of ‘null’, ‘text’, ‘number’, ‘url’, ‘mail’,
‘datetime’, ‘tel’ or ‘address’.

**kivy.uix.behaviors.focus.FocusBehavior.is_focusable**

Whether the instance can become focused. If focused, it’ll lose focus
when set to False.
[`is_focusable`](https://kivy.org/doc/stable/#kivy.uix.behaviors.focus.FocusBehavior.is_focusable) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to True on a desktop (i.e. desktop is True in
[`config`](https://kivy.org/doc/stable/api-kivy.config.html#module-kivy.config)), False otherwise.

**kivy.uix.behaviors.focus.FocusBehavior.keyboard**

The keyboard to bind to (or bound to the widget) when focused.
When None, a keyboard is requested and released whenever the widget comes
into and out of focus. If not None, it must be a keyboard, which gets
bound and unbound from the widget whenever it’s in or out of focus. It is
useful only when more than one keyboard is available, so it is recommended
to be set to None when only one keyboard is available.
If more than one keyboard is available, whenever an instance gets focused
a new keyboard will be requested if None. Unless the other instances lose
focus (e.g. if tab was used), a new keyboard will appear. When this is
undesired, the keyboard property can be used. For example, if there are
two users with two keyboards, then each keyboard can be assigned to
different groups of instances of FocusBehavior, ensuring that within
each group, only one FocusBehavior will have focus, and will receive input
from the correct keyboard. See keyboard_mode in [`config`](https://kivy.org/doc/stable/api-kivy.config.html#module-kivy.config) for
more information on the keyboard modes.
**Keyboard and focus behavior**
When using the keyboard, there are some important default behaviors you
should keep in mind.
When Config’s keyboard_mode is multi, each new touch is considered
a touch by a different user and will set the focus (if clicked on a
focusable) with a new keyboard. Already focused elements will not lose
their focus (even if an unfocusable widget is touched).
If the keyboard property is set, that keyboard will be used when the
instance gets focused. If widgets with different keyboards are linked
through [`focus_next`](https://kivy.org/doc/stable/#kivy.uix.behaviors.focus.FocusBehavior.focus_next) and [`focus_previous`](https://kivy.org/doc/stable/#kivy.uix.behaviors.focus.FocusBehavior.focus_previous), then as they are
tabbed through, different keyboards will become active. Therefore,
typically it’s undesirable to link instances which are assigned
different keyboards.
When a widget has focus, setting its keyboard to None will remove its
keyboard, but the widget will then immediately try to get
another keyboard. In order to remove its keyboard, rather set its
[`focus`](https://kivy.org/doc/stable/#kivy.uix.behaviors.focus.FocusBehavior.focus) to False.
When using a software keyboard, typical on mobile and touch devices, the
keyboard display behavior is determined by the
[`softinput_mode`](https://kivy.org/doc/stable/api-kivy.core.window.html#kivy.core.window.WindowBase.softinput_mode) property. You can use
this property to ensure the focused widget is not covered or obscured.
[`keyboard`](https://kivy.org/doc/stable/#kivy.uix.behaviors.focus.FocusBehavior.keyboard) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) and defaults
to None.

**kivy.uix.behaviors.focus.FocusBehavior.keyboard_mode**

Determines how the keyboard visibility should be managed. ‘auto’ will
result in the standard behavior of showing/hiding on focus. ‘managed’
requires setting the keyboard visibility manually, or calling the helper
functions [`show_keyboard()`](https://kivy.org/doc/stable/#kivy.uix.behaviors.focus.FocusBehavior.show_keyboard) and [`hide_keyboard()`](https://kivy.org/doc/stable/#kivy.uix.behaviors.focus.FocusBehavior.hide_keyboard).
[`keyboard_mode`](https://kivy.org/doc/stable/#kivy.uix.behaviors.focus.FocusBehavior.keyboard_mode) is an `OptionsProperty` and
defaults to ‘auto’. Can be one of ‘auto’ or ‘managed’.

**kivy.uix.behaviors.focus.FocusBehavior.keyboard_on_key_down**

The method bound to the keyboard when the instance has focus.
When the instance becomes focused, this method is bound to the
keyboard and will be called for every input press. The parameters are
the same as [`kivy.core.window.WindowBase.on_key_down()`](https://kivy.org/doc/stable/api-kivy.core.window.html#kivy.core.window.WindowBase.on_key_down).
When overwriting the method in the derived widget, super should be
called to enable tab cycling. If the derived widget wishes to use tab
for its own purposes, it can call super after it has processed the
character (if it does not wish to consume the tab).
Similar to other keyboard functions, it should return True if the
key was consumed.

**kivy.uix.behaviors.focus.FocusBehavior.keyboard_on_key_up**

The method bound to the keyboard when the instance has focus.
When the instance becomes focused, this method is bound to the
keyboard and will be called for every input release. The parameters are
the same as [`kivy.core.window.WindowBase.on_key_up()`](https://kivy.org/doc/stable/api-kivy.core.window.html#kivy.core.window.WindowBase.on_key_up).
When overwriting the method in the derived widget, super should be
called to enable de-focusing on escape. If the derived widget wishes
to use escape for its own purposes, it can call super after it has
processed the character (if it does not wish to consume the escape).
See [`keyboard_on_key_down()`](https://kivy.org/doc/stable/#kivy.uix.behaviors.focus.FocusBehavior.keyboard_on_key_down)

**kivy.uix.behaviors.focus.FocusBehavior.keyboard_suggestions**

If True provides auto suggestions on top of keyboard.
This will only work if [`input_type`](https://kivy.org/doc/stable/#kivy.uix.behaviors.focus.FocusBehavior.input_type) is set to text, url, mail or
address.

New in version 2.1.0.
[`keyboard_suggestions`](https://kivy.org/doc/stable/#kivy.uix.behaviors.focus.FocusBehavior.keyboard_suggestions) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to True

**kivy.uix.behaviors.focus.FocusBehavior.show_keyboard**

Convenience function to show the keyboard in managed mode.

**kivy.uix.behaviors.focus.FocusBehavior.unfocus_on_touch**

Whether a instance should lose focus when clicked outside the instance.
When a user clicks on a widget that is focus aware and shares the same
keyboard as this widget (which in the case with only one keyboard),
then as the other widgets gain focus, this widget loses focus. In addition
to that, if this property is True, clicking on any widget other than this
widget, will remove focus from this widget.
[`unfocus_on_touch`](https://kivy.org/doc/stable/#kivy.uix.behaviors.focus.FocusBehavior.unfocus_on_touch) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to False if the keyboard_mode in [`Config`](https://kivy.org/doc/stable/api-kivy.config.html#kivy.config.Config)
is ‘multi’ or ‘systemandmulti’, otherwise it defaults to True.

---

## API - [`kivy.uix.behaviors.knspace`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.knspace.html)

**kivy.uix.behaviors.knspace.KNSpace**

Bases: [`kivy.event.EventDispatcher`](https://kivy.org/doc/stable/api-kivy.event.html#kivy.event.EventDispatcher)
Each [`KNSpace`](https://kivy.org/doc/stable/#kivy.uix.behaviors.knspace.KNSpace) instance is a namespace that stores the named Kivy
objects associated with this namespace. Each named object is
stored as the value of a Kivy [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) of
this instance whose property name is the object’s given name. Both rebind
and allownone are set to True for the property.
See [`KNSpaceBehavior.knspace`](https://kivy.org/doc/stable/#kivy.uix.behaviors.knspace.KNSpaceBehavior.knspace) for details on how a namespace is
associated with a named object.
When storing an object in the namespace, the object’s proxy_ref is
stored if the object has such an attribute.

**kivy.uix.behaviors.knspace.KNSpace.fork**

Returns a new [`KNSpace`](https://kivy.org/doc/stable/#kivy.uix.behaviors.knspace.KNSpace) instance which will have access to
all the named objects in the current namespace but will also have a
namespace of its own that is unique to it.
For example:

Now, any names added to knspace will be accessible by the
forked_knspace1 and forked_knspace2 namespaces by the normal means.
However, any names added to forked_knspace1 will not be accessible
from knspace or forked_knspace2. Similar for forked_knspace2.

**kivy.uix.behaviors.knspace.KNSpace.keep_ref**

Whether a direct reference should be kept to the stored objects.
If `True`, we use the direct object, otherwise we use
`proxy_ref` when present.
Defaults to False.

**kivy.uix.behaviors.knspace.KNSpace.parent**

(internal) The parent namespace instance, [`KNSpace`](https://kivy.org/doc/stable/#kivy.uix.behaviors.knspace.KNSpace), or None. See
[`fork()`](https://kivy.org/doc/stable/#kivy.uix.behaviors.knspace.KNSpace.fork).

**kivy.uix.behaviors.knspace.KNSpace.property**

Get a property instance from the property name. If quiet is True,
None is returned instead of raising an exception when name is not a
property. Defaults to False.
New in version 1.0.9.

Changed in version 1.9.0:quiet was added.

**kivy.uix.behaviors.knspace.KNSpaceBehavior**

Bases: `builtins.object`
Inheriting from this class allows naming of the inherited objects, which
are then added to the associated namespace [`knspace`](https://kivy.org/doc/stable/#kivy.uix.behaviors.knspace.knspace) and accessible
through it.
Please see the [`knspace behaviors module`](https://kivy.org/doc/stable/#module-kivy.uix.behaviors.knspace)
documentation for more information.

**kivy.uix.behaviors.knspace.KNSpaceBehavior.knsname**

The name given to this instance. If named, the name will be added to the
associated [`knspace`](https://kivy.org/doc/stable/#kivy.uix.behaviors.knspace.knspace) namespace, which will then point to the
proxy_ref of this instance.
When named, one can access this object by e.g. self.knspace.name, where
name is the given name of this instance. See [`knspace`](https://kivy.org/doc/stable/#kivy.uix.behaviors.knspace.knspace) and the
module description for more details.

**kivy.uix.behaviors.knspace.KNSpaceBehavior.knspace**

The namespace instance, [`KNSpace`](https://kivy.org/doc/stable/#kivy.uix.behaviors.knspace.KNSpace), associated with this widget.
The [`knspace`](https://kivy.org/doc/stable/#kivy.uix.behaviors.knspace.knspace) namespace stores this widget when naming this widget
with [`knsname`](https://kivy.org/doc/stable/#kivy.uix.behaviors.knspace.KNSpaceBehavior.knsname).
If the namespace has been set with a [`KNSpace`](https://kivy.org/doc/stable/#kivy.uix.behaviors.knspace.KNSpace) instance, e.g. with
self.knspace = KNSpace(), then that instance is returned (setting with
None doesn’t count). Otherwise, if [`knspace_key`](https://kivy.org/doc/stable/#kivy.uix.behaviors.knspace.KNSpaceBehavior.knspace_key) is not None, we
look for a namespace to use in the object that is stored in the property
named [`knspace_key`](https://kivy.org/doc/stable/#kivy.uix.behaviors.knspace.KNSpaceBehavior.knspace_key), of this instance. I.e.
object = getattr(self, self.knspace_key).
If that object has a knspace property, then we return its value. Otherwise,
we go further up, e.g. with getattr(object, self.knspace_key) and look
for its knspace property.
Finally, if we reach a value of None, or [`knspace_key`](https://kivy.org/doc/stable/#kivy.uix.behaviors.knspace.KNSpaceBehavior.knspace_key) was None,
the default [`knspace`](https://kivy.org/doc/stable/#kivy.uix.behaviors.knspace.knspace) namespace is
returned.
If [`knspace`](https://kivy.org/doc/stable/#kivy.uix.behaviors.knspace.knspace) is set to the string ‘fork’, the current namespace
in [`knspace`](https://kivy.org/doc/stable/#kivy.uix.behaviors.knspace.knspace) will be forked with [`KNSpace.fork()`](https://kivy.org/doc/stable/#kivy.uix.behaviors.knspace.KNSpace.fork) and the
resulting namespace will be assigned to this instance’s [`knspace`](https://kivy.org/doc/stable/#kivy.uix.behaviors.knspace.knspace).
See the module examples for a motivating example.
Both rebind and allownone are True.

**kivy.uix.behaviors.knspace.KNSpaceBehavior.knspace_key**

The name of the property of this instance, to use to search upwards for
a namespace to use by this instance. Defaults to ‘parent’ so that we’ll
search the parent tree. See [`knspace`](https://kivy.org/doc/stable/#kivy.uix.behaviors.knspace.knspace).
When None, we won’t search the parent tree for the namespace.
allownone is True.

**kivy.uix.behaviors.knspace.knspace**

The default [`KNSpace`](https://kivy.org/doc/stable/#kivy.uix.behaviors.knspace.KNSpace) namespace. See [`KNSpaceBehavior.knspace`](https://kivy.org/doc/stable/#kivy.uix.behaviors.knspace.KNSpaceBehavior.knspace)
for more details.

---

## API - [`kivy.uix.behaviors.togglebutton`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.togglebutton.html)

**kivy.uix.behaviors.togglebutton.ToggleButtonBehavior**

Bases: [`kivy.uix.behaviors.button.ButtonBehavior`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.button.html#kivy.uix.behaviors.button.ButtonBehavior)
This [mixin](https://en.wikipedia.org/wiki/Mixin) class provides
[`togglebutton`](https://kivy.org/doc/stable/api-kivy.uix.togglebutton.html#module-kivy.uix.togglebutton) behavior. Please see the
[`togglebutton behaviors module`](https://kivy.org/doc/stable/#module-kivy.uix.behaviors.togglebutton)
documentation for more information.
New in version 1.8.0.

**kivy.uix.behaviors.togglebutton.ToggleButtonBehavior.allow_no_selection**

This specifies whether the widgets in a group allow no selection i.e.
everything to be deselected.
New in version 1.9.0.
[`allow_no_selection`](https://kivy.org/doc/stable/#kivy.uix.behaviors.togglebutton.ToggleButtonBehavior.allow_no_selection) is a `BooleanProperty` and defaults to
True

**kivy.uix.behaviors.togglebutton.ToggleButtonBehavior.get_widgets**

Return a list of the widgets contained in a specific group. If the
group doesn’t exist, an empty list will be returned.

**kivy.uix.behaviors.togglebutton.ToggleButtonBehavior.group**

Group of the button. If None, no group will be used (the button will be
independent). If specified, [`group`](https://kivy.org/doc/stable/#kivy.uix.behaviors.togglebutton.ToggleButtonBehavior.group) must be a hashable object, like
a string. Only one button in a group can be in a ‘down’ state.
[`group`](https://kivy.org/doc/stable/#kivy.uix.behaviors.togglebutton.ToggleButtonBehavior.group) is a [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and defaults to
None.

---

## API - [`kivy.uix.behaviors.touchripple`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.touchripple.html)

**kivy.uix.behaviors.touchripple.TouchRippleBehavior**

Bases: `builtins.object`
Touch ripple behavior.
Supposed to be used as mixin on widget classes.
Ripple behavior does not trigger automatically, concrete implementation
needs to call [`ripple_show()`](https://kivy.org/doc/stable/#kivy.uix.behaviors.touchripple.TouchRippleBehavior.ripple_show) respective [`ripple_fade()`](https://kivy.org/doc/stable/#kivy.uix.behaviors.touchripple.TouchRippleBehavior.ripple_fade) manually.
Example[¶](https://kivy.org/doc/stable/#example)
Here we create a Label which renders the touch ripple animation on
interaction:

**kivy.uix.behaviors.touchripple.TouchRippleBehavior.ripple_duration_in**

Animation duration taken to show the overlay.
[`ripple_duration_in`](https://kivy.org/doc/stable/#kivy.uix.behaviors.touchripple.TouchRippleBehavior.ripple_duration_in) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.5.

**kivy.uix.behaviors.touchripple.TouchRippleBehavior.ripple_duration_out**

Animation duration taken to fade the overlay.
[`ripple_duration_out`](https://kivy.org/doc/stable/#kivy.uix.behaviors.touchripple.TouchRippleBehavior.ripple_duration_out) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.2.

**kivy.uix.behaviors.touchripple.TouchRippleBehavior.ripple_fade**

Finish ripple animation on current widget.

**kivy.uix.behaviors.touchripple.TouchRippleBehavior.ripple_fade_from_alpha**

Alpha channel for ripple color the animation starts with.
[`ripple_fade_from_alpha`](https://kivy.org/doc/stable/#kivy.uix.behaviors.touchripple.TouchRippleBehavior.ripple_fade_from_alpha) is a
[`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and defaults to 0.5.

**kivy.uix.behaviors.touchripple.TouchRippleBehavior.ripple_fade_to_alpha**

Alpha channel for ripple color the animation targets to.
[`ripple_fade_to_alpha`](https://kivy.org/doc/stable/#kivy.uix.behaviors.touchripple.TouchRippleBehavior.ripple_fade_to_alpha) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.8.

**kivy.uix.behaviors.touchripple.TouchRippleBehavior.ripple_func_in**

Animation callback for showing the overlay.
[`ripple_func_in`](https://kivy.org/doc/stable/#kivy.uix.behaviors.touchripple.TouchRippleBehavior.ripple_func_in) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to in_cubic.

**kivy.uix.behaviors.touchripple.TouchRippleBehavior.ripple_func_out**

Animation callback for hiding the overlay.
[`ripple_func_out`](https://kivy.org/doc/stable/#kivy.uix.behaviors.touchripple.TouchRippleBehavior.ripple_func_out) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to out_quad.

**kivy.uix.behaviors.touchripple.TouchRippleBehavior.ripple_rad_default**

Default radius the animation starts from.
[`ripple_rad_default`](https://kivy.org/doc/stable/#kivy.uix.behaviors.touchripple.TouchRippleBehavior.ripple_rad_default) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 10.

**kivy.uix.behaviors.touchripple.TouchRippleBehavior.ripple_scale**

Max scale of the animation overlay calculated from max(width/height) of
the decorated widget.
[`ripple_scale`](https://kivy.org/doc/stable/#kivy.uix.behaviors.touchripple.TouchRippleBehavior.ripple_scale) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 2.0.

**kivy.uix.behaviors.touchripple.TouchRippleBehavior.ripple_show**

Begin ripple animation on current widget.
Expects touch event as argument.

**kivy.uix.behaviors.touchripple.TouchRippleButtonBehavior**

Bases: [`kivy.uix.behaviors.touchripple.TouchRippleBehavior`](https://kivy.org/doc/stable/#kivy.uix.behaviors.touchripple.TouchRippleBehavior)
This [mixin](https://en.wikipedia.org/wiki/Mixin) class provides
a similar behavior to [`ButtonBehavior`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.button.html#kivy.uix.behaviors.button.ButtonBehavior)
but provides touch ripple animation instead of button pressed/released as
visual effect.

**kivy.uix.behaviors.touchripple.TouchRippleButtonBehavior.always_release**

This determines whether or not the widget fires an on_release event if
the touch_up is outside the widget.
[`always_release`](https://kivy.org/doc/stable/#kivy.uix.behaviors.touchripple.TouchRippleButtonBehavior.always_release) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to False.

**kivy.uix.behaviors.touchripple.TouchRippleButtonBehavior.last_touch**

Contains the last relevant touch received by the Button. This can
be used in on_press or on_release in order to know which touch
dispatched the event.
[`last_touch`](https://kivy.org/doc/stable/#kivy.uix.behaviors.touchripple.TouchRippleButtonBehavior.last_touch) is a [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to None.

---

## API - [`kivy.uix.boxlayout`](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html)

**kivy.uix.boxlayout.BoxLayout**

Bases: [`kivy.uix.layout.Layout`](https://kivy.org/doc/stable/api-kivy.uix.layout.html#kivy.uix.layout.Layout)
Box layout class. See module documentation for more information.

**kivy.uix.boxlayout.BoxLayout.add_widget**

Add a new widget as a child of this widget.

**kivy.uix.boxlayout.BoxLayout.do_layout**

This function is called when a layout is called by a trigger.
If you are writing a new Layout subclass, don’t call this function
directly but use `_trigger_layout()` instead.
The function is by default called *before* the next frame, therefore
the layout isn’t updated immediately. Anything depending on the
positions of e.g. children should be scheduled for the next frame.
New in version 1.0.8.

**kivy.uix.boxlayout.BoxLayout.minimum_height**

Automatically computed minimum height needed to contain all children.
New in version 1.10.0.
[`minimum_height`](https://kivy.org/doc/stable/#kivy.uix.boxlayout.BoxLayout.minimum_height) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0. It is read only.

**kivy.uix.boxlayout.BoxLayout.minimum_size**

Automatically computed minimum size needed to contain all children.
New in version 1.10.0.
[`minimum_size`](https://kivy.org/doc/stable/#kivy.uix.boxlayout.BoxLayout.minimum_size) is a
[`ReferenceListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ReferenceListProperty) of
([`minimum_width`](https://kivy.org/doc/stable/#kivy.uix.boxlayout.BoxLayout.minimum_width), [`minimum_height`](https://kivy.org/doc/stable/#kivy.uix.boxlayout.BoxLayout.minimum_height)) properties. It is read
only.

**kivy.uix.boxlayout.BoxLayout.minimum_width**

Automatically computed minimum width needed to contain all children.
New in version 1.10.0.
[`minimum_width`](https://kivy.org/doc/stable/#kivy.uix.boxlayout.BoxLayout.minimum_width) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0. It is read only.

**kivy.uix.boxlayout.BoxLayout.orientation**

Orientation of the layout.
[`orientation`](https://kivy.org/doc/stable/#kivy.uix.boxlayout.BoxLayout.orientation) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty) and
defaults to ‘horizontal’. Can be ‘vertical’ or ‘horizontal’.

**kivy.uix.boxlayout.BoxLayout.padding**

Padding between layout box and children: [padding_left, padding_top,
padding_right, padding_bottom].
padding also accepts a two argument form [padding_horizontal,
padding_vertical] and a one argument form [padding].
Changed in version 1.7.0:Replaced NumericProperty with VariableListProperty.
[`padding`](https://kivy.org/doc/stable/#kivy.uix.boxlayout.BoxLayout.padding) is a [`VariableListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.VariableListProperty) and
defaults to [0, 0, 0, 0].

**kivy.uix.boxlayout.BoxLayout.remove_widget**

Remove a widget from the children of this widget.

**kivy.uix.boxlayout.BoxLayout.spacing**

Spacing between children, in pixels.
[`spacing`](https://kivy.org/doc/stable/#kivy.uix.boxlayout.BoxLayout.spacing) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and defaults
to 0.

---

## API - [`kivy.uix.bubble`](https://kivy.org/doc/stable/api-kivy.uix.bubble.html)

**kivy.uix.bubble.Bubble**

Bases: [`kivy.uix.boxlayout.BoxLayout`](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html#kivy.uix.boxlayout.BoxLayout)
Bubble class. See module documentation for more information.

**kivy.uix.bubble.Bubble.add_widget**

Add a new widget as a child of this widget.

**kivy.uix.bubble.Bubble.arrow_color**

Arrow color, in the format (r, g, b, a). To use it you have to set
[`arrow_image`](https://kivy.org/doc/stable/#kivy.uix.bubble.Bubble.arrow_image) first.
New in version 2.2.0.
[`arrow_color`](https://kivy.org/doc/stable/#kivy.uix.bubble.Bubble.arrow_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty) and
defaults to [1, 1, 1, 1].

**kivy.uix.bubble.Bubble.arrow_image**

Image of the arrow pointing to the bubble.
[`arrow_image`](https://kivy.org/doc/stable/#kivy.uix.bubble.Bubble.arrow_image) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to ‘atlas://data/images/defaulttheme/bubble_arrow’.

**kivy.uix.bubble.Bubble.arrow_margin**

Automatically computed margin that the arrow widget occupies in
x and y direction in pixel.
Check the description of [`arrow_margin_x`](https://kivy.org/doc/stable/#kivy.uix.bubble.Bubble.arrow_margin_x) and [`arrow_margin_y`](https://kivy.org/doc/stable/#kivy.uix.bubble.Bubble.arrow_margin_y).
New in version 2.2.0.
[`arrow_margin`](https://kivy.org/doc/stable/#kivy.uix.bubble.Bubble.arrow_margin) is a [`ReferenceListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ReferenceListProperty)
of ([`arrow_margin_x`](https://kivy.org/doc/stable/#kivy.uix.bubble.Bubble.arrow_margin_x), [`arrow_margin_y`](https://kivy.org/doc/stable/#kivy.uix.bubble.Bubble.arrow_margin_y)) properties.
It is read only.

**kivy.uix.bubble.Bubble.arrow_margin_x**

Automatically computed margin in x direction that the arrow widget
occupies in pixel.
In combination with the [`content_width`](https://kivy.org/doc/stable/#kivy.uix.bubble.Bubble.content_width), this property can be used
to determine the correct width of the Bubble to exactly enclose the
arrow + content by adding [`content_width`](https://kivy.org/doc/stable/#kivy.uix.bubble.Bubble.content_width) and [`arrow_margin_x`](https://kivy.org/doc/stable/#kivy.uix.bubble.Bubble.arrow_margin_x)
New in version 2.2.0.
[`arrow_margin_x`](https://kivy.org/doc/stable/#kivy.uix.bubble.Bubble.arrow_margin_x) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
represents the added margin in x direction due to the arrow widget.
It defaults to 0 and is read only.

**kivy.uix.bubble.Bubble.arrow_margin_y**

Automatically computed margin in y direction that the arrow widget
occupies in pixel.
In combination with the [`content_height`](https://kivy.org/doc/stable/#kivy.uix.bubble.Bubble.content_height), this property can be used
to determine the correct height of the Bubble to exactly enclose the
arrow + content by adding [`content_height`](https://kivy.org/doc/stable/#kivy.uix.bubble.Bubble.content_height) and [`arrow_margin_y`](https://kivy.org/doc/stable/#kivy.uix.bubble.Bubble.arrow_margin_y)
New in version 2.2.0.
[`arrow_margin_y`](https://kivy.org/doc/stable/#kivy.uix.bubble.Bubble.arrow_margin_y) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
represents the added margin in y direction due to the arrow widget.
It defaults to 0 and is read only.

**kivy.uix.bubble.Bubble.arrow_pos**

Specifies the position of the arrow as predefined relative position to
the bubble.
Can be one of: left_top, left_mid, left_bottom top_left, top_mid, top_right
right_top, right_mid, right_bottom bottom_left, bottom_mid, bottom_right.
[`arrow_pos`](https://kivy.org/doc/stable/#kivy.uix.bubble.Bubble.arrow_pos) is a [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty) and
defaults to ‘bottom_mid’.

**kivy.uix.bubble.Bubble.content**

This is the object where the main content of the bubble is held.
The content of the Bubble set by ‘add_widget’ and removed with
‘remove_widget’ similarly to the `ActionView` which is placed into
a class:ActionBar
[`content`](https://kivy.org/doc/stable/#kivy.uix.bubble.Bubble.content) is a [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and defaults
to None.

**kivy.uix.bubble.Bubble.content_height**

The height of the content Widget.
New in version 2.2.0.
[`content_height`](https://kivy.org/doc/stable/#kivy.uix.bubble.Bubble.content_height) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
is the same as self.content.height if content is not None, else it defaults
to 0. It is read only.

**kivy.uix.bubble.Bubble.content_size**

The size of the content Widget.
New in version 2.2.0.
[`content_size`](https://kivy.org/doc/stable/#kivy.uix.bubble.Bubble.content_size) is a [`ReferenceListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ReferenceListProperty)
of ([`content_width`](https://kivy.org/doc/stable/#kivy.uix.bubble.Bubble.content_width), [`content_height`](https://kivy.org/doc/stable/#kivy.uix.bubble.Bubble.content_height)) properties.
It is read only.

**kivy.uix.bubble.Bubble.content_width**

The width of the content Widget.
New in version 2.2.0.
[`content_width`](https://kivy.org/doc/stable/#kivy.uix.bubble.Bubble.content_width) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
is the same as self.content.width if content is not None, else it defaults
to 0. It is read only.

**kivy.uix.bubble.Bubble.flex_arrow_pos**

Specifies the position of the arrow as flex coordinate around the
border of the [`Bubble`](https://kivy.org/doc/stable/#kivy.uix.bubble.Bubble) Widget.
If this property is set to a proper position (relative pixel coordinates
within the [`Bubble`](https://kivy.org/doc/stable/#kivy.uix.bubble.Bubble) widget, it overwrites the setting
[`arrow_pos`](https://kivy.org/doc/stable/#kivy.uix.bubble.Bubble.arrow_pos).
New in version 2.2.0.
[`flex_arrow_pos`](https://kivy.org/doc/stable/#kivy.uix.bubble.Bubble.flex_arrow_pos) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) and
defaults to None.

**kivy.uix.bubble.Bubble.limit_to**

Specifies the widget to which the bubbles position is restricted.
New in version 1.6.0.
[`limit_to`](https://kivy.org/doc/stable/#kivy.uix.bubble.Bubble.limit_to) is a [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and defaults
to ‘None’.

**kivy.uix.bubble.Bubble.remove_widget**

Remove a widget from the children of this widget.

**kivy.uix.bubble.Bubble.show_arrow**

Indicates whether to show arrow.
New in version 1.8.0.
[`show_arrow`](https://kivy.org/doc/stable/#kivy.uix.bubble.Bubble.show_arrow) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to True.

**kivy.uix.bubble.BubbleButton**

Bases: [`kivy.uix.button.Button`](https://kivy.org/doc/stable/api-kivy.uix.button.html#kivy.uix.button.Button)
A button intended for use in a BubbleContent widget.
You can use a “normal” button class, but it will not look good unless the
background is changed.
Rather use this BubbleButton widget that is already defined and provides a
suitable background for you.

**kivy.uix.bubble.BubbleContent**

Bases: [`kivy.uix.boxlayout.BoxLayout`](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html#kivy.uix.boxlayout.BoxLayout)
A styled BoxLayout that can be used as the content widget of a Bubble.
Changed in version 2.2.0.
The graphical appearance of [`BubbleContent`](https://kivy.org/doc/stable/#kivy.uix.bubble.BubbleContent) is now based on it’s
own properties [`background_image`](https://kivy.org/doc/stable/#kivy.uix.bubble.BubbleContent.background_image), [`background_color`](https://kivy.org/doc/stable/#kivy.uix.bubble.BubbleContent.background_color),
[`border`](https://kivy.org/doc/stable/#kivy.uix.bubble.BubbleContent.border) and [`border_auto_scale`](https://kivy.org/doc/stable/#kivy.uix.bubble.BubbleContent.border_auto_scale). The parent widget properties
are no longer considered. This makes the BubbleContent a standalone themed
BoxLayout.

**kivy.uix.bubble.BubbleContent.background_color**

Background color, in the format (r, g, b, a). To use it you have to set
[`background_image`](https://kivy.org/doc/stable/#kivy.uix.bubble.BubbleContent.background_image) first.
New in version 2.2.0.
[`background_color`](https://kivy.org/doc/stable/#kivy.uix.bubble.BubbleContent.background_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty) and
defaults to [1, 1, 1, 1].

**kivy.uix.bubble.BubbleContent.background_image**

Background image of the bubble.
New in version 2.2.0.
[`background_image`](https://kivy.org/doc/stable/#kivy.uix.bubble.BubbleContent.background_image) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to ‘atlas://data/images/defaulttheme/bubble’.

**kivy.uix.bubble.BubbleContent.border**

Border used for [`BorderImage`](https://kivy.org/doc/stable/api-kivy.graphics.vertex_instructions.html#kivy.graphics.vertex_instructions.BorderImage)
graphics instruction. Used with the [`background_image`](https://kivy.org/doc/stable/#kivy.uix.bubble.BubbleContent.background_image).
It should be used when using custom backgrounds.
It must be a list of 4 values: (bottom, right, top, left). Read the
BorderImage instructions for more information about how to use it.
New in version 2.2.0.
[`border`](https://kivy.org/doc/stable/#kivy.uix.bubble.BubbleContent.border) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) and defaults to
(16, 16, 16, 16)

**kivy.uix.bubble.BubbleContent.border_auto_scale**

Specifies the [`kivy.graphics.BorderImage.auto_scale`](https://kivy.org/doc/stable/api-kivy.graphics.html#kivy.graphics.BorderImage.auto_scale)
value on the background BorderImage.
New in version 2.2.0.
[`border_auto_scale`](https://kivy.org/doc/stable/#kivy.uix.bubble.BubbleContent.border_auto_scale) is a
[`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty) and defaults to
‘both_lower’.

---

## API - [`kivy.uix.button`](https://kivy.org/doc/stable/api-kivy.uix.button.html)

**kivy.uix.button.Button**

Bases: [`kivy.uix.behaviors.button.ButtonBehavior`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.button.html#kivy.uix.behaviors.button.ButtonBehavior), [`kivy.uix.label.Label`](https://kivy.org/doc/stable/api-kivy.uix.label.html#kivy.uix.label.Label)
Button class, see module documentation for more information.
Changed in version 1.8.0:The behavior / logic of the button has been moved to
`ButtonBehaviors`.

**kivy.uix.button.Button.background_color**

Background color, in the format (r, g, b, a).
This acts as a *multiplier* to the texture color. The default
texture is grey, so just setting the background color will give
a darker result. To set a plain color, set the
[`background_normal`](https://kivy.org/doc/stable/#kivy.uix.button.Button.background_normal) to `''`.
New in version 1.0.8.
The [`background_color`](https://kivy.org/doc/stable/#kivy.uix.button.Button.background_color) is a
[`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty) and defaults to [1, 1, 1, 1].
Changed in version 2.0.0:Changed from [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) to
[`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty).

**kivy.uix.button.Button.background_disabled_down**

Background image of the button used for the default graphical
representation when the button is disabled and pressed.
New in version 1.8.0.
[`background_disabled_down`](https://kivy.org/doc/stable/#kivy.uix.button.Button.background_disabled_down) is a
[`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults to
‘atlas://data/images/defaulttheme/button_disabled_pressed’.

**kivy.uix.button.Button.background_disabled_normal**

Background image of the button used for the default graphical
representation when the button is disabled and not pressed.
New in version 1.8.0.
[`background_disabled_normal`](https://kivy.org/doc/stable/#kivy.uix.button.Button.background_disabled_normal) is a
[`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults to
‘atlas://data/images/defaulttheme/button_disabled’.

**kivy.uix.button.Button.background_down**

Background image of the button used for the default graphical
representation when the button is pressed.
New in version 1.0.4.
[`background_down`](https://kivy.org/doc/stable/#kivy.uix.button.Button.background_down) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to ‘atlas://data/images/defaulttheme/button_pressed’.

**kivy.uix.button.Button.background_normal**

Background image of the button used for the default graphical
representation when the button is not pressed.
New in version 1.0.4.
[`background_normal`](https://kivy.org/doc/stable/#kivy.uix.button.Button.background_normal) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘atlas://data/images/defaulttheme/button’.

**kivy.uix.button.Button.border**

Border used for [`BorderImage`](https://kivy.org/doc/stable/api-kivy.graphics.vertex_instructions.html#kivy.graphics.vertex_instructions.BorderImage)
graphics instruction. Used with [`background_normal`](https://kivy.org/doc/stable/#kivy.uix.button.Button.background_normal) and
[`background_down`](https://kivy.org/doc/stable/#kivy.uix.button.Button.background_down). Can be used for custom backgrounds.
It must be a list of four values: (bottom, right, top, left). Read the
BorderImage instruction for more information about how to use it.
[`border`](https://kivy.org/doc/stable/#kivy.uix.button.Button.border) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) and defaults to
(16, 16, 16, 16)

---

## API - [`kivy.uix.camera`](https://kivy.org/doc/stable/api-kivy.uix.camera.html)

**kivy.uix.camera.Camera**

Bases: [`kivy.uix.image.Image`](https://kivy.org/doc/stable/api-kivy.uix.image.html#kivy.uix.image.Image)
Camera class. See module documentation for more information.

**kivy.uix.camera.Camera.index**

Index of the used camera, starting from 0.
[`index`](https://kivy.org/doc/stable/#kivy.uix.camera.Camera.index) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and defaults
to -1 to allow auto selection.

**kivy.uix.camera.Camera.play**

Boolean indicating whether the camera is playing or not.
You can start/stop the camera by setting this property:

[`play`](https://kivy.org/doc/stable/#kivy.uix.camera.Camera.play) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and defaults to
False.

**kivy.uix.camera.Camera.resolution**

Preferred resolution to use when invoking the camera. If you are using
[-1, -1], the resolution will be the default one:

[`resolution`](https://kivy.org/doc/stable/#kivy.uix.camera.Camera.resolution) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) and defaults
to [-1, -1].

---

## API - [`kivy.uix.carousel`](https://kivy.org/doc/stable/api-kivy.uix.carousel.html)

**kivy.uix.carousel.Carousel**

Bases: [`kivy.uix.stencilview.StencilView`](https://kivy.org/doc/stable/api-kivy.uix.stencilview.html#kivy.uix.stencilview.StencilView)
Carousel class. See module documentation for more information.

**kivy.uix.carousel.Carousel.add_widget**

Add a new widget as a child of this widget.

**kivy.uix.carousel.Carousel.anim_cancel_duration**

Defines the duration of the animation when a swipe movement is not
accepted. This is generally when the user does not make a large enough
swipe. See [`min_move`](https://kivy.org/doc/stable/#kivy.uix.carousel.Carousel.min_move).
[`anim_cancel_duration`](https://kivy.org/doc/stable/#kivy.uix.carousel.Carousel.anim_cancel_duration) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.3.

**kivy.uix.carousel.Carousel.anim_move_duration**

Defines the duration of the Carousel animation between pages.
[`anim_move_duration`](https://kivy.org/doc/stable/#kivy.uix.carousel.Carousel.anim_move_duration) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.5.

**kivy.uix.carousel.Carousel.anim_type**

Type of animation to use while animating to the next/previous slide.
This should be the name of an
[`AnimationTransition`](https://kivy.org/doc/stable/api-kivy.animation.html#kivy.animation.AnimationTransition) function.
[`anim_type`](https://kivy.org/doc/stable/#kivy.uix.carousel.Carousel.anim_type) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to ‘out_quad’.
New in version 1.8.0.

**kivy.uix.carousel.Carousel.clear_widgets**

Remove all (or the specified) `children` of this widget.
If the ‘children’ argument is specified, it should be a list (or
filtered list) of children of the current widget.
Changed in version 1.8.0:The children argument can be used to specify the children you
want to remove.
Changed in version 2.1.0:Specifying an empty `children` list leaves the widgets unchanged.
Previously it was treated like `None` and all children were
removed.

**kivy.uix.carousel.Carousel.current_slide**

The currently shown slide.
[`current_slide`](https://kivy.org/doc/stable/#kivy.uix.carousel.Carousel.current_slide) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty).
Changed in version 1.5.0:The property no longer exposes the slides container. It returns
the widget you have added.

**kivy.uix.carousel.Carousel.direction**

Specifies the direction in which the slides are ordered. This
corresponds to the direction from which the user swipes to go from one
slide to the next. It
can be right, left, top, or bottom. For example, with
the default value of right, the second slide is to the right
of the first and the user would swipe from the right towards the
left to get to the second slide.
[`direction`](https://kivy.org/doc/stable/#kivy.uix.carousel.Carousel.direction) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty) and
defaults to ‘right’.

**kivy.uix.carousel.Carousel.ignore_perpendicular_swipes**

Ignore swipes on axis perpendicular to direction.
[`ignore_perpendicular_swipes`](https://kivy.org/doc/stable/#kivy.uix.carousel.Carousel.ignore_perpendicular_swipes) is a
[`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and defaults to False.
New in version 1.10.0.

**kivy.uix.carousel.Carousel.index**

Get/Set the current slide based on the index.
[`index`](https://kivy.org/doc/stable/#kivy.uix.carousel.Carousel.index) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) and defaults
to 0 (the first item).

**kivy.uix.carousel.Carousel.load_next**

Animate to the next slide.
New in version 1.7.0.

**kivy.uix.carousel.Carousel.load_previous**

Animate to the previous slide.
New in version 1.7.0.

**kivy.uix.carousel.Carousel.load_slide**

Animate to the slide that is passed as the argument.
Changed in version 1.8.0.

**kivy.uix.carousel.Carousel.loop**

Allow the Carousel to loop infinitely. If True, when the user tries to
swipe beyond last page, it will return to the first. If False, it will
remain on the last page.
[`loop`](https://kivy.org/doc/stable/#kivy.uix.carousel.Carousel.loop) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to False.

**kivy.uix.carousel.Carousel.min_move**

Defines the minimum distance to be covered before the touch is
considered a swipe gesture and the Carousel content changed.
This is a expressed as a fraction of the Carousel’s width.
If the movement doesn’t reach this minimum value, the movement is
cancelled and the content is restored to its original position.
[`min_move`](https://kivy.org/doc/stable/#kivy.uix.carousel.Carousel.min_move) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0.2.

**kivy.uix.carousel.Carousel.next_slide**

The next slide in the Carousel. It is None if the current slide is
the last slide in the Carousel. This ordering reflects the order in which
the slides are added: their presentation varies according to the
[`direction`](https://kivy.org/doc/stable/#kivy.uix.carousel.Carousel.direction) property.
[`next_slide`](https://kivy.org/doc/stable/#kivy.uix.carousel.Carousel.next_slide) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty).
Changed in version 1.5.0:The property no longer exposes the slides container.
It returns the widget you have added.

**kivy.uix.carousel.Carousel.on_touch_down**

Receive a touch down event.

**kivy.uix.carousel.Carousel.on_touch_move**

Receive a touch move event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivy.org/doc/stable/#kivy.uix.carousel.Carousel.on_touch_down) for more information.

**kivy.uix.carousel.Carousel.on_touch_up**

Receive a touch up event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivy.org/doc/stable/#kivy.uix.carousel.Carousel.on_touch_down) for more information.

**kivy.uix.carousel.Carousel.previous_slide**

The previous slide in the Carousel. It is None if the current slide is
the first slide in the Carousel. This ordering reflects the order in which
the slides are added: their presentation varies according to the
[`direction`](https://kivy.org/doc/stable/#kivy.uix.carousel.Carousel.direction) property.
[`previous_slide`](https://kivy.org/doc/stable/#kivy.uix.carousel.Carousel.previous_slide) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty).
Changed in version 1.5.0:This property no longer exposes the slides container. It returns
the widget you have added.

**kivy.uix.carousel.Carousel.remove_widget**

Remove a widget from the children of this widget.

**kivy.uix.carousel.Carousel.scroll_distance**

Distance to move before scrolling the [`Carousel`](https://kivy.org/doc/stable/#kivy.uix.carousel.Carousel) in pixels. As
soon as the distance has been traveled, the [`Carousel`](https://kivy.org/doc/stable/#kivy.uix.carousel.Carousel) will start
to scroll, and no touch event will go to children.
It is advisable that you base this value on the dpi of your target device’s
screen.
[`scroll_distance`](https://kivy.org/doc/stable/#kivy.uix.carousel.Carousel.scroll_distance) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 20dp.
New in version 1.5.0.

**kivy.uix.carousel.Carousel.scroll_timeout**

Timeout allowed to trigger the [`scroll_distance`](https://kivy.org/doc/stable/#kivy.uix.carousel.Carousel.scroll_distance), in milliseconds.
If the user has not moved [`scroll_distance`](https://kivy.org/doc/stable/#kivy.uix.carousel.Carousel.scroll_distance) within the timeout,
no scrolling will occur and the touch event will go to the children.
[`scroll_timeout`](https://kivy.org/doc/stable/#kivy.uix.carousel.Carousel.scroll_timeout) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 200 (milliseconds)
New in version 1.5.0.

**kivy.uix.carousel.Carousel.slides**

List of slides inside the Carousel. The slides are the
widgets added to the Carousel using the [`add_widget`](https://kivy.org/doc/stable/#kivy.uix.carousel.Carousel.add_widget) method.
[`slides`](https://kivy.org/doc/stable/#kivy.uix.carousel.Carousel.slides) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) and is
read-only.

---

## API - [`kivy.uix.checkbox`](https://kivy.org/doc/stable/api-kivy.uix.checkbox.html)

**kivy.uix.checkbox.CheckBox**

Bases: [`kivy.uix.behaviors.togglebutton.ToggleButtonBehavior`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.togglebutton.html#kivy.uix.behaviors.togglebutton.ToggleButtonBehavior), [`kivy.uix.widget.Widget`](https://kivy.org/doc/stable/api-kivy.uix.widget.html#kivy.uix.widget.Widget)
CheckBox class, see module documentation for more information.

**kivy.uix.checkbox.CheckBox.active**

Indicates if the switch is active or inactive.
[`active`](https://kivy.org/doc/stable/#kivy.uix.checkbox.CheckBox.active) is a boolean and reflects and sets whether the underlying
`state` is ‘down’ (True) or ‘normal’ (False).
It is a [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty), which accepts boolean
values and defaults to False.
Changed in version 1.11.0:It changed from a BooleanProperty to a AliasProperty.

**kivy.uix.checkbox.CheckBox.background_checkbox_disabled_down**

Background image of the checkbox used for the default graphical
representation when the checkbox is disabled and active.
New in version 1.9.0.
[`background_checkbox_disabled_down`](https://kivy.org/doc/stable/#kivy.uix.checkbox.CheckBox.background_checkbox_disabled_down) is a
[`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults to
‘atlas://data/images/defaulttheme/checkbox_disabled_on’.

**kivy.uix.checkbox.CheckBox.background_checkbox_disabled_normal**

Background image of the checkbox used for the default graphical
representation when the checkbox is disabled and not active.
New in version 1.9.0.
[`background_checkbox_disabled_normal`](https://kivy.org/doc/stable/#kivy.uix.checkbox.CheckBox.background_checkbox_disabled_normal) is a
[`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults to
‘atlas://data/images/defaulttheme/checkbox_disabled_off’.

**kivy.uix.checkbox.CheckBox.background_checkbox_down**

Background image of the checkbox used for the default graphical
representation when the checkbox is active.
New in version 1.9.0.
[`background_checkbox_down`](https://kivy.org/doc/stable/#kivy.uix.checkbox.CheckBox.background_checkbox_down) is a
[`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults to
‘atlas://data/images/defaulttheme/checkbox_on’.

**kivy.uix.checkbox.CheckBox.background_checkbox_normal**

Background image of the checkbox used for the default graphical
representation when the checkbox is not active.
New in version 1.9.0.
[`background_checkbox_normal`](https://kivy.org/doc/stable/#kivy.uix.checkbox.CheckBox.background_checkbox_normal) is a
[`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults to
‘atlas://data/images/defaulttheme/checkbox_off’.

**kivy.uix.checkbox.CheckBox.background_radio_disabled_down**

Background image of the radio button used for the default graphical
representation when the radio button is disabled and active.
New in version 1.9.0.
[`background_radio_disabled_down`](https://kivy.org/doc/stable/#kivy.uix.checkbox.CheckBox.background_radio_disabled_down) is a
[`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults to
‘atlas://data/images/defaulttheme/checkbox_radio_disabled_on’.

**kivy.uix.checkbox.CheckBox.background_radio_disabled_normal**

Background image of the radio button used for the default graphical
representation when the radio button is disabled and not active.
New in version 1.9.0.
[`background_radio_disabled_normal`](https://kivy.org/doc/stable/#kivy.uix.checkbox.CheckBox.background_radio_disabled_normal) is a
[`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults to
‘atlas://data/images/defaulttheme/checkbox_radio_disabled_off’.

**kivy.uix.checkbox.CheckBox.background_radio_down**

Background image of the radio button used for the default graphical
representation when the radio button is active.
New in version 1.9.0.
[`background_radio_down`](https://kivy.org/doc/stable/#kivy.uix.checkbox.CheckBox.background_radio_down) is a
[`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults to
‘atlas://data/images/defaulttheme/checkbox_radio_on’.

**kivy.uix.checkbox.CheckBox.background_radio_normal**

Background image of the radio button used for the default graphical
representation when the radio button is not active.
New in version 1.9.0.
[`background_radio_normal`](https://kivy.org/doc/stable/#kivy.uix.checkbox.CheckBox.background_radio_normal) is a
[`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults to
‘atlas://data/images/defaulttheme/checkbox_radio_off’.

**kivy.uix.checkbox.CheckBox.color**

Color is used for tinting the default graphical representation
of checkbox and radio button (images).
Color is in the format (r, g, b, a).
New in version 1.10.0.
[`color`](https://kivy.org/doc/stable/#kivy.uix.checkbox.CheckBox.color) is a
[`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty) and defaults to
‘[1, 1, 1, 1]’.
Changed in version 2.0.0:Changed from [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) to
[`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty).

---

## API - [`kivy.uix.codeinput`](https://kivy.org/doc/stable/api-kivy.uix.codeinput.html)

**kivy.uix.codeinput.CodeInput**

Bases: [`kivy.uix.behaviors.codenavigation.CodeNavigationBehavior`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.codenavigation.html#kivy.uix.behaviors.codenavigation.CodeNavigationBehavior), [`kivy.uix.textinput.TextInput`](https://kivy.org/doc/stable/api-kivy.uix.textinput.html#kivy.uix.textinput.TextInput)
CodeInput class, used for displaying highlighted code.

**kivy.uix.codeinput.CodeInput.lexer**

This holds the selected Lexer used by pygments to highlight the code.
[`lexer`](https://kivy.org/doc/stable/#kivy.uix.codeinput.CodeInput.lexer) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to PythonLexer.

**kivy.uix.codeinput.CodeInput.style**

The pygments style object to use for formatting.
When `style_name` is set, this will be changed to the
corresponding style object.
[`style`](https://kivy.org/doc/stable/#kivy.uix.codeinput.CodeInput.style) is a [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to `None`

**kivy.uix.codeinput.CodeInput.style_name**

Name of the pygments style to use for formatting.
[`style_name`](https://kivy.org/doc/stable/#kivy.uix.codeinput.CodeInput.style_name) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to `'default'`.

---

## API - [`kivy.uix.colorpicker`](https://kivy.org/doc/stable/api-kivy.uix.colorpicker.html)

**kivy.uix.colorpicker.ColorPicker**

Bases: [`kivy.uix.relativelayout.RelativeLayout`](https://kivy.org/doc/stable/api-kivy.uix.relativelayout.html#kivy.uix.relativelayout.RelativeLayout)
See module documentation.

**kivy.uix.colorpicker.ColorPicker.color**

The [`color`](https://kivy.org/doc/stable/#kivy.uix.colorpicker.ColorPicker.color) holds the color currently selected in rgba format.
[`color`](https://kivy.org/doc/stable/#kivy.uix.colorpicker.ColorPicker.color) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) and defaults to
(1, 1, 1, 1).

**kivy.uix.colorpicker.ColorPicker.font_name**

Specifies the font used on the ColorPicker.
[`font_name`](https://kivy.org/doc/stable/#kivy.uix.colorpicker.ColorPicker.font_name) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to ‘data/fonts/RobotoMono-Regular.ttf’.

**kivy.uix.colorpicker.ColorPicker.hex_color**

The [`hex_color`](https://kivy.org/doc/stable/#kivy.uix.colorpicker.ColorPicker.hex_color) holds the currently selected color in hex.
[`hex_color`](https://kivy.org/doc/stable/#kivy.uix.colorpicker.ColorPicker.hex_color) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) and
defaults to #ffffffff.

**kivy.uix.colorpicker.ColorPicker.hsv**

The [`hsv`](https://kivy.org/doc/stable/#kivy.uix.colorpicker.ColorPicker.hsv) holds the color currently selected in hsv format.
[`hsv`](https://kivy.org/doc/stable/#kivy.uix.colorpicker.ColorPicker.hsv) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) and defaults to
(1, 1, 1).

**kivy.uix.colorpicker.ColorPicker.wheel**

The [`wheel`](https://kivy.org/doc/stable/#kivy.uix.colorpicker.ColorPicker.wheel) holds the color wheel.
[`wheel`](https://kivy.org/doc/stable/#kivy.uix.colorpicker.ColorPicker.wheel) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to None.

**kivy.uix.colorpicker.ColorWheel**

Bases: [`kivy.uix.widget.Widget`](https://kivy.org/doc/stable/api-kivy.uix.widget.html#kivy.uix.widget.Widget)
Chromatic wheel for the ColorPicker.
Changed in version 1.7.1:font_size, font_name and foreground_color have been removed. The
sizing is now the same as others widget, based on ‘sp’. Orientation is
also automatically determined according to the width/height ratio.

**kivy.uix.colorpicker.ColorWheel.a**

The Alpha value of the color currently selected.
[`a`](https://kivy.org/doc/stable/#kivy.uix.colorpicker.ColorWheel.a) is a [`BoundedNumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BoundedNumericProperty) and
can be a value from 0 to 1. It defaults to 0.

**kivy.uix.colorpicker.ColorWheel.b**

The Blue value of the color currently selected.
[`b`](https://kivy.org/doc/stable/#kivy.uix.colorpicker.ColorWheel.b) is a [`BoundedNumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BoundedNumericProperty) and
can be a value from 0 to 1. It defaults to 0.

**kivy.uix.colorpicker.ColorWheel.color**

The holds the color currently selected.
[`color`](https://kivy.org/doc/stable/#kivy.uix.colorpicker.ColorWheel.color) is a [`ReferenceListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ReferenceListProperty) and
contains a list of r, g, b, a values. It defaults to [0, 0, 0, 0].

**kivy.uix.colorpicker.ColorWheel.g**

The Green value of the color currently selected.
[`g`](https://kivy.org/doc/stable/#kivy.uix.colorpicker.ColorWheel.g) is a [`BoundedNumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BoundedNumericProperty)
and can be a value from 0 to 1. It defaults to 0.

**kivy.uix.colorpicker.ColorWheel.on_touch_down**

Receive a touch down event.

**kivy.uix.colorpicker.ColorWheel.on_touch_move**

Receive a touch move event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivy.org/doc/stable/#kivy.uix.colorpicker.ColorWheel.on_touch_down) for more information.

**kivy.uix.colorpicker.ColorWheel.on_touch_up**

Receive a touch up event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivy.org/doc/stable/#kivy.uix.colorpicker.ColorWheel.on_touch_down) for more information.

**kivy.uix.colorpicker.ColorWheel.r**

The Red value of the color currently selected.
[`r`](https://kivy.org/doc/stable/#kivy.uix.colorpicker.ColorWheel.r) is a [`BoundedNumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BoundedNumericProperty) and
can be a value from 0 to 1. It defaults to 0.

---

## API - [`kivy.uix.dropdown`](https://kivy.org/doc/stable/api-kivy.uix.dropdown.html)

**kivy.uix.dropdown.DropDown**

Bases: [`kivy.uix.scrollview.ScrollView`](https://kivy.org/doc/stable/api-kivy.uix.scrollview.html#kivy.uix.scrollview.ScrollView)
DropDown class. See module documentation for more information.

**kivy.uix.dropdown.DropDown.add_widget**

Add a new widget as a child of this widget.

**kivy.uix.dropdown.DropDown.attach_to**

(internal) Property that will be set to the widget to which the
drop down list is attached.
The [`open()`](https://kivy.org/doc/stable/#kivy.uix.dropdown.DropDown.open) method will automatically set this property whilst
[`dismiss()`](https://kivy.org/doc/stable/#kivy.uix.dropdown.DropDown.dismiss) will set it back to None.

**kivy.uix.dropdown.DropDown.auto_dismiss**

By default, the dropdown will be automatically dismissed when a
touch happens outside of it, this option allows to disable this
feature
[`auto_dismiss`](https://kivy.org/doc/stable/#kivy.uix.dropdown.DropDown.auto_dismiss) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to True.
New in version 1.8.0.

**kivy.uix.dropdown.DropDown.auto_width**

By default, the width of the dropdown will be the same as the width of
the attached widget. Set to False if you want to provide your own width.
[`auto_width`](https://kivy.org/doc/stable/#kivy.uix.dropdown.DropDown.auto_width) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to True.

**kivy.uix.dropdown.DropDown.clear_widgets**

Remove all (or the specified) `children` of this widget.
If the ‘children’ argument is specified, it should be a list (or
filtered list) of children of the current widget.
Changed in version 1.8.0:The children argument can be used to specify the children you
want to remove.
Changed in version 2.1.0:Specifying an empty `children` list leaves the widgets unchanged.
Previously it was treated like `None` and all children were
removed.

**kivy.uix.dropdown.DropDown.container**

(internal) Property that will be set to the container of the dropdown
list. It is a [`GridLayout`](https://kivy.org/doc/stable/api-kivy.uix.gridlayout.html#kivy.uix.gridlayout.GridLayout) by default.

**kivy.uix.dropdown.DropDown.dismiss**

Remove the dropdown widget from the window and detach it from
the attached widget.

**kivy.uix.dropdown.DropDown.dismiss_on_select**

By default, the dropdown will be automatically dismissed when a
selection has been done. Set to False to prevent the dismiss.
[`dismiss_on_select`](https://kivy.org/doc/stable/#kivy.uix.dropdown.DropDown.dismiss_on_select) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to True.

**kivy.uix.dropdown.DropDown.max_height**

Indicate the maximum height that the dropdown can take. If None, it will
take the maximum height available until the top or bottom of the screen
is reached.
[`max_height`](https://kivy.org/doc/stable/#kivy.uix.dropdown.DropDown.max_height) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to None.

**kivy.uix.dropdown.DropDown.min_state_time**

Minimum time before the `DropDown` is dismissed.
This is used to allow for the widget inside the dropdown to display
a down state or for the `DropDown` itself to
display a animation for closing.
[`min_state_time`](https://kivy.org/doc/stable/#kivy.uix.dropdown.DropDown.min_state_time) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to the Config value min_state_time.
New in version 1.10.0.

**kivy.uix.dropdown.DropDown.on_motion**

Called when a motion event is received.

New in version 2.1.0.

**kivy.uix.dropdown.DropDown.on_touch_down**

Receive a touch down event.

**kivy.uix.dropdown.DropDown.on_touch_move**

Receive a touch move event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivy.org/doc/stable/#kivy.uix.dropdown.DropDown.on_touch_down) for more information.

**kivy.uix.dropdown.DropDown.on_touch_up**

Receive a touch up event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivy.org/doc/stable/#kivy.uix.dropdown.DropDown.on_touch_down) for more information.

**kivy.uix.dropdown.DropDown.open**

Open the dropdown list and attach it to a specific widget.
Depending on the position of the widget within the window and
the height of the dropdown, the dropdown might be above or below
that widget.

**kivy.uix.dropdown.DropDown.remove_widget**

Remove a widget from the children of this widget.

**kivy.uix.dropdown.DropDown.select**

Call this method to trigger the on_select event with the data
selection. The data can be anything you want.

---

## API - [`kivy.uix.effectwidget`](https://kivy.org/doc/stable/api-kivy.uix.effectwidget.html)

**kivy.uix.effectwidget.AdvancedEffectBase**

Bases: [`kivy.uix.effectwidget.EffectBase`](https://kivy.org/doc/stable/#kivy.uix.effectwidget.EffectBase)
An [`EffectBase`](https://kivy.org/doc/stable/#kivy.uix.effectwidget.EffectBase) with additional behavior to easily
set and update uniform variables in your shader.
This class is provided for convenience when implementing your own
effects: it is not used by any of those provided with Kivy.
In addition to your base glsl string that must be provided as
normal, the [`AdvancedEffectBase`](https://kivy.org/doc/stable/#kivy.uix.effectwidget.AdvancedEffectBase) has an extra property
[`uniforms`](https://kivy.org/doc/stable/#kivy.uix.effectwidget.AdvancedEffectBase.uniforms), a dictionary of name-value pairs. Whenever
a value is changed, the new value for the uniform variable is
uploaded to the shader.
You must still manually declare your uniform variables at the top
of your glsl string.

**kivy.uix.effectwidget.AdvancedEffectBase.set_fbo_shader**

Sets the [`Fbo`](https://kivy.org/doc/stable/api-kivy.graphics.html#kivy.graphics.Fbo)’s shader by splicing
the `glsl` string into a full fragment shader.
The full shader is made up of `shader_header +
shader_uniforms + self.glsl + shader_footer_effect`.

**kivy.uix.effectwidget.AdvancedEffectBase.uniforms**

A dictionary of uniform variable names and their values. These
are automatically uploaded to the `fbo` shader if appropriate.
uniforms is a [`DictProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.DictProperty) and
defaults to {}.

**kivy.uix.effectwidget.ChannelMixEffect**

Bases: [`kivy.uix.effectwidget.EffectBase`](https://kivy.org/doc/stable/#kivy.uix.effectwidget.EffectBase)
Mixes the color channels of the input according to the order
property. Channels may be arbitrarily rearranged or repeated.

**kivy.uix.effectwidget.ChannelMixEffect.order**

The new sorted order of the rgb channels.
order is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) and defaults to
[1, 2, 0], corresponding to (g, b, r).

**kivy.uix.effectwidget.EffectBase**

Bases: [`kivy.event.EventDispatcher`](https://kivy.org/doc/stable/api-kivy.event.html#kivy.event.EventDispatcher)
The base class for GLSL effects. It simply returns its input.
See the module documentation for more details.

**kivy.uix.effectwidget.EffectBase.fbo**

The fbo currently using this effect. The [`EffectBase`](https://kivy.org/doc/stable/#kivy.uix.effectwidget.EffectBase)
automatically handles this.
[`fbo`](https://kivy.org/doc/stable/#kivy.uix.effectwidget.EffectBase.fbo) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to None.

**kivy.uix.effectwidget.EffectBase.glsl**

The glsl string defining your effect function. See the
module documentation for more details.
[`glsl`](https://kivy.org/doc/stable/#kivy.uix.effectwidget.EffectBase.glsl) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to
a trivial effect that returns its input.

**kivy.uix.effectwidget.EffectBase.set_fbo_shader**

Sets the [`Fbo`](https://kivy.org/doc/stable/api-kivy.graphics.html#kivy.graphics.Fbo)’s shader by splicing
the [`glsl`](https://kivy.org/doc/stable/#kivy.uix.effectwidget.EffectBase.glsl) string into a full fragment shader.
The full shader is made up of `shader_header +
shader_uniforms + self.glsl + shader_footer_effect`.

**kivy.uix.effectwidget.EffectBase.source**

The (optional) filename from which to load the [`glsl`](https://kivy.org/doc/stable/#kivy.uix.effectwidget.EffectBase.glsl)
string.
[`source`](https://kivy.org/doc/stable/#kivy.uix.effectwidget.EffectBase.source) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to ‘’.

**kivy.uix.effectwidget.EffectWidget**

Bases: [`kivy.uix.relativelayout.RelativeLayout`](https://kivy.org/doc/stable/api-kivy.uix.relativelayout.html#kivy.uix.relativelayout.RelativeLayout)
Widget with the ability to apply a series of graphical effects to
its children. See the module documentation for more information on
setting effects and creating your own.

**kivy.uix.effectwidget.EffectWidget.add_widget**

Add a new widget as a child of this widget.

**kivy.uix.effectwidget.EffectWidget.background_color**

This defines the background color to be used for the fbo in the
EffectWidget.
[`background_color`](https://kivy.org/doc/stable/#kivy.uix.effectwidget.EffectWidget.background_color) is a `ListProperty` defaults to
(0, 0, 0, 0)

**kivy.uix.effectwidget.EffectWidget.clear_widgets**

Remove all (or the specified) `children` of this widget.
If the ‘children’ argument is specified, it should be a list (or
filtered list) of children of the current widget.
Changed in version 1.8.0:The children argument can be used to specify the children you
want to remove.
Changed in version 2.1.0:Specifying an empty `children` list leaves the widgets unchanged.
Previously it was treated like `None` and all children were
removed.

**kivy.uix.effectwidget.EffectWidget.effects**

List of all the effects to be applied. These should all be
instances or subclasses of [`EffectBase`](https://kivy.org/doc/stable/#kivy.uix.effectwidget.EffectBase).
effects is a `ListProperty` and defaults to [].

**kivy.uix.effectwidget.EffectWidget.fbo_list**

(internal) List of all the fbos that are being used to apply
the effects.
fbo_list is a `ListProperty` and defaults to [].

**kivy.uix.effectwidget.EffectWidget.refresh_fbo_setup**

(internal) Creates and assigns one [`Fbo`](https://kivy.org/doc/stable/api-kivy.graphics.html#kivy.graphics.Fbo)
per effect, and makes sure all sizes etc. are correct and
consistent.

**kivy.uix.effectwidget.EffectWidget.remove_widget**

Remove a widget from the children of this widget.

**kivy.uix.effectwidget.EffectWidget.texture**

The output texture of the final [`Fbo`](https://kivy.org/doc/stable/api-kivy.graphics.html#kivy.graphics.Fbo) after
all effects have been applied.
texture is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and defaults
to None.

**kivy.uix.effectwidget.FXAAEffect**

Bases: [`kivy.uix.effectwidget.EffectBase`](https://kivy.org/doc/stable/#kivy.uix.effectwidget.EffectBase)
Applies very simple anti-aliasing via fxaa.

**kivy.uix.effectwidget.HorizontalBlurEffect**

Bases: [`kivy.uix.effectwidget.EffectBase`](https://kivy.org/doc/stable/#kivy.uix.effectwidget.EffectBase)
Blurs the input horizontally, with the width given by
[`size`](https://kivy.org/doc/stable/#kivy.uix.effectwidget.HorizontalBlurEffect.size).

**kivy.uix.effectwidget.HorizontalBlurEffect.size**

The blur width in pixels.
size is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and defaults to
4.0.

**kivy.uix.effectwidget.InvertEffect**

Bases: [`kivy.uix.effectwidget.EffectBase`](https://kivy.org/doc/stable/#kivy.uix.effectwidget.EffectBase)
Inverts the colors in the input.

**kivy.uix.effectwidget.MonochromeEffect**

Bases: [`kivy.uix.effectwidget.EffectBase`](https://kivy.org/doc/stable/#kivy.uix.effectwidget.EffectBase)
Returns its input colors in monochrome.

**kivy.uix.effectwidget.PixelateEffect**

Bases: [`kivy.uix.effectwidget.EffectBase`](https://kivy.org/doc/stable/#kivy.uix.effectwidget.EffectBase)
Pixelates the input according to its
[`pixel_size`](https://kivy.org/doc/stable/#kivy.uix.effectwidget.PixelateEffect.pixel_size)

**kivy.uix.effectwidget.PixelateEffect.pixel_size**

Sets the size of a new ‘pixel’ in the effect, in terms of number of
‘real’ pixels.
pixel_size is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 10.

**kivy.uix.effectwidget.ScanlinesEffect**

Bases: [`kivy.uix.effectwidget.EffectBase`](https://kivy.org/doc/stable/#kivy.uix.effectwidget.EffectBase)
Adds scanlines to the input.

**kivy.uix.effectwidget.VerticalBlurEffect**

Bases: [`kivy.uix.effectwidget.EffectBase`](https://kivy.org/doc/stable/#kivy.uix.effectwidget.EffectBase)
Blurs the input vertically, with the width given by
[`size`](https://kivy.org/doc/stable/#kivy.uix.effectwidget.VerticalBlurEffect.size).

**kivy.uix.effectwidget.VerticalBlurEffect.size**

The blur width in pixels.
size is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and defaults to
4.0.

---

## API - [`kivy.uix.filechooser`](https://kivy.org/doc/stable/api-kivy.uix.filechooser.html)

**kivy.uix.filechooser.FileChooser**

Bases: [`kivy.uix.filechooser.FileChooserController`](https://kivy.org/doc/stable/#kivy.uix.filechooser.FileChooserController)
Implementation of a [`FileChooserController`](https://kivy.org/doc/stable/#kivy.uix.filechooser.FileChooserController) which supports
switching between multiple, synced layout views.
The FileChooser can be used as follows:

New in version 1.9.0.

**kivy.uix.filechooser.FileChooser.add_widget**

Add a new widget as a child of this widget.

**kivy.uix.filechooser.FileChooser.manager**

Reference to the [`ScreenManager`](https://kivy.org/doc/stable/api-kivy.uix.screenmanager.html#kivy.uix.screenmanager.ScreenManager) instance.
manager is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty).

**kivy.uix.filechooser.FileChooser.view_list**

List of views added to this FileChooser.
view_list is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) of type
`list`.

**kivy.uix.filechooser.FileChooser.view_mode**

Current layout view mode.
view_mode is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) of type
`str`.

**kivy.uix.filechooser.FileChooserController**

Bases: [`kivy.uix.relativelayout.RelativeLayout`](https://kivy.org/doc/stable/api-kivy.uix.relativelayout.html#kivy.uix.relativelayout.RelativeLayout)
Base for implementing a FileChooser. Don’t use this class directly, but
prefer using an implementation such as the [`FileChooser`](https://kivy.org/doc/stable/#kivy.uix.filechooser.FileChooser),
[`FileChooserListView`](https://kivy.org/doc/stable/#kivy.uix.filechooser.FileChooserListView) or [`FileChooserIconView`](https://kivy.org/doc/stable/#kivy.uix.filechooser.FileChooserIconView).

**kivy.uix.filechooser.FileChooserController.cancel**

Cancel any background action started by filechooser, such as loading
a new directory.
New in version 1.2.0.

**kivy.uix.filechooser.FileChooserController.dirselect**

Determines whether directories are valid selections or not.
dirselect is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and defaults to
False.
New in version 1.1.0.

**kivy.uix.filechooser.FileChooserController.entry_released**

(internal) This method must be called by the template when an entry
is touched by the user.
New in version 1.1.0.

**kivy.uix.filechooser.FileChooserController.entry_touched**

(internal) This method must be called by the template when an entry
is touched by the user.

**kivy.uix.filechooser.FileChooserController.file_encodings**

Possible encodings for decoding a filename to unicode. In the case that
the user has a non-ascii filename, undecodable without knowing its
initial encoding, we have no other choice than to guess it.
Please note that if you encounter an issue because of a missing encoding
here, we’ll be glad to add it to this list.
file_encodings is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) and defaults to
[‘utf-8’, ‘latin1’, ‘cp1252’].
New in version 1.3.0.
Deprecated since version 1.8.0:This property is no longer used as the filechooser no longer decodes
the file names.

**kivy.uix.filechooser.FileChooserController.file_system**

The file system object used to access the file system. This should be a
subclass of [`FileSystemAbstract`](https://kivy.org/doc/stable/#kivy.uix.filechooser.FileSystemAbstract).
file_system is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and defaults to
[`FileSystemLocal()`](https://kivy.org/doc/stable/#kivy.uix.filechooser.FileSystemLocal)
New in version 1.8.0.

**kivy.uix.filechooser.FileChooserController.files**

The list of files in the directory specified by path after applying the
filters.
files is a read-only [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty).

**kivy.uix.filechooser.FileChooserController.filter_dirs**

Indicates whether filters should also apply to directories.
filter_dirs is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and defaults to
False.

**kivy.uix.filechooser.FileChooserController.filters**

filters specifies the filters to be applied to the files in the directory.
filters is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) and defaults to [].
This is equivalent to ‘*’ i.e. nothing is filtered.
The filters are not reset when the path changes. You need to do that
yourself if desired.
There are two kinds of filters: patterns and callbacks.
Patterns
e.g. [’*.png’].
You can use the following patterns:
Pattern
Meaning
*
matches everything
?
matches any single character
[seq]
matches any character in seq
[!seq]
matches any character not in seq
Callbacks
You can specify a function that will be called for each file. The
callback will be passed the folder and file name as the first
and second parameters respectively. It should return True to
indicate a match and False otherwise.
Changed in version 1.4.0:Added the option to specify the filter as a callback.

**kivy.uix.filechooser.FileChooserController.font_name**

Filename of the font to use in UI components. The path can be
absolute or relative. Relative paths are resolved by the
[`resource_find()`](https://kivy.org/doc/stable/api-kivy.resources.html#kivy.resources.resource_find) function.
[`font_name`](https://kivy.org/doc/stable/#kivy.uix.filechooser.FileChooserController.font_name) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to ‘Roboto’. This value is taken
from [`Config`](https://kivy.org/doc/stable/api-kivy.config.html#kivy.config.Config).

**kivy.uix.filechooser.FileChooserController.get_nice_size**

Pass the filepath. Returns the size in the best human readable
format or ‘’ if it is a directory (Don’t recursively calculate size).

**kivy.uix.filechooser.FileChooserController.layout**

Reference to the layout widget instance.
layout is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty).
New in version 1.9.0.

**kivy.uix.filechooser.FileChooserController.multiselect**

Determines whether the user is able to select multiple files or not.
multiselect is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and defaults to
False.

**kivy.uix.filechooser.FileChooserController.on_touch_down**

Receive a touch down event.

**kivy.uix.filechooser.FileChooserController.on_touch_up**

Receive a touch up event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivy.org/doc/stable/#kivy.uix.filechooser.FileChooserController.on_touch_down) for more information.

**kivy.uix.filechooser.FileChooserController.path**

path is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults to the
current working directory as a unicode string. It specifies the path on the
filesystem that this controller should refer to.

**kivy.uix.filechooser.FileChooserController.progress_cls**

Class to use for displaying a progress indicator for filechooser
loading.
progress_cls is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and defaults to
`FileChooserProgress`.
New in version 1.2.0.
Changed in version 1.8.0:If set to a string, the [`Factory`](https://kivy.org/doc/stable/api-kivy.factory.html#kivy.factory.Factory) will be used to
resolve the class name.

**kivy.uix.filechooser.FileChooserController.rootpath**

Root path to use instead of the system root path. If set, it will not show
a “..” directory to go up to the root path. For example, if you set
rootpath to /users/foo, the user will be unable to go to /users or to any
other directory not starting with /users/foo.
rootpath is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults
to None.
New in version 1.2.0.

**kivy.uix.filechooser.FileChooserController.selection**

Contains the list of files that are currently selected.
selection is a read-only [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) and
defaults to [].

**kivy.uix.filechooser.FileChooserController.show_hidden**

Determines whether hidden files and folders should be shown.
show_hidden is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and defaults to
False.

**kivy.uix.filechooser.FileChooserController.sort_func**

Provides a function to be called with a list of filenames as the first
argument and the filesystem implementation as the second argument. It
returns a list of filenames sorted for display in the view.
sort_func is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and defaults to a
function returning alphanumerically named folders first.
Changed in version 1.8.0:The signature needs now 2 arguments: first the list of files,
second the filesystem class to use.

**kivy.uix.filechooser.FileChooserIconLayout**

Bases: `kivy.uix.filechooser.FileChooserLayout`
File chooser layout using an icon view.
New in version 1.9.0.

**kivy.uix.filechooser.FileChooserIconView**

Bases: [`kivy.uix.filechooser.FileChooserController`](https://kivy.org/doc/stable/#kivy.uix.filechooser.FileChooserController)
Implementation of a [`FileChooserController`](https://kivy.org/doc/stable/#kivy.uix.filechooser.FileChooserController) using an icon view.
New in version 1.9.0.

**kivy.uix.filechooser.FileChooserListLayout**

Bases: `kivy.uix.filechooser.FileChooserLayout`
File chooser layout using a list view.
New in version 1.9.0.

**kivy.uix.filechooser.FileChooserListView**

Bases: [`kivy.uix.filechooser.FileChooserController`](https://kivy.org/doc/stable/#kivy.uix.filechooser.FileChooserController)
Implementation of a [`FileChooserController`](https://kivy.org/doc/stable/#kivy.uix.filechooser.FileChooserController) using a list view.
New in version 1.9.0.

**kivy.uix.filechooser.FileChooserProgressBase**

Bases: [`kivy.uix.floatlayout.FloatLayout`](https://kivy.org/doc/stable/api-kivy.uix.floatlayout.html#kivy.uix.floatlayout.FloatLayout)
Base for implementing a progress view. This view is used when too many
entries need to be created and are delayed over multiple frames.
New in version 1.2.0.

**kivy.uix.filechooser.FileChooserProgressBase.cancel**

Cancel any action from the FileChooserController.

**kivy.uix.filechooser.FileChooserProgressBase.index**

Current index of [`total`](https://kivy.org/doc/stable/#kivy.uix.filechooser.FileChooserProgressBase.total) entries to be loaded.

**kivy.uix.filechooser.FileChooserProgressBase.on_touch_down**

Receive a touch down event.

**kivy.uix.filechooser.FileChooserProgressBase.on_touch_move**

Receive a touch move event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivy.org/doc/stable/#kivy.uix.filechooser.FileChooserProgressBase.on_touch_down) for more information.

**kivy.uix.filechooser.FileChooserProgressBase.on_touch_up**

Receive a touch up event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivy.org/doc/stable/#kivy.uix.filechooser.FileChooserProgressBase.on_touch_down) for more information.

**kivy.uix.filechooser.FileChooserProgressBase.path**

Current path of the FileChooser, read-only.

**kivy.uix.filechooser.FileChooserProgressBase.total**

Total number of entries to load.

**kivy.uix.filechooser.FileSystemAbstract**

Bases: `builtins.object`
Class for implementing a File System view that can be used with the
[`FileChooser`](https://kivy.org/doc/stable/#kivy.uix.filechooser.FileChooser).
New in version 1.8.0.

**kivy.uix.filechooser.FileSystemAbstract.getsize**

Return the size in bytes of a file

**kivy.uix.filechooser.FileSystemAbstract.is_dir**

Return True if the argument passed to this method is a directory

**kivy.uix.filechooser.FileSystemAbstract.is_hidden**

Return True if the file is hidden

**kivy.uix.filechooser.FileSystemAbstract.listdir**

Return the list of files in the directory fn

**kivy.uix.filechooser.FileSystemLocal**

Bases: [`kivy.uix.filechooser.FileSystemAbstract`](https://kivy.org/doc/stable/#kivy.uix.filechooser.FileSystemAbstract)
Implementation of [`FileSystemAbstract`](https://kivy.org/doc/stable/#kivy.uix.filechooser.FileSystemAbstract) for local files.
New in version 1.8.0.

**kivy.uix.filechooser.FileSystemLocal.getsize**

Return the size in bytes of a file

**kivy.uix.filechooser.FileSystemLocal.is_dir**

Return True if the argument passed to this method is a directory

**kivy.uix.filechooser.FileSystemLocal.is_hidden**

Return True if the file is hidden

**kivy.uix.filechooser.FileSystemLocal.listdir**

Return the list of files in the directory fn

---

## API - [`kivy.uix.floatlayout`](https://kivy.org/doc/stable/api-kivy.uix.floatlayout.html)

**kivy.uix.floatlayout.FloatLayout**

Bases: [`kivy.uix.layout.Layout`](https://kivy.org/doc/stable/api-kivy.uix.layout.html#kivy.uix.layout.Layout)
Float layout class. See module documentation for more information.

**kivy.uix.floatlayout.FloatLayout.add_widget**

Add a new widget as a child of this widget.

**kivy.uix.floatlayout.FloatLayout.do_layout**

This function is called when a layout is called by a trigger.
If you are writing a new Layout subclass, don’t call this function
directly but use `_trigger_layout()` instead.
The function is by default called *before* the next frame, therefore
the layout isn’t updated immediately. Anything depending on the
positions of e.g. children should be scheduled for the next frame.
New in version 1.0.8.

**kivy.uix.floatlayout.FloatLayout.remove_widget**

Remove a widget from the children of this widget.

---

## API - [`kivy.uix.gesturesurface`](https://kivy.org/doc/stable/api-kivy.uix.gesturesurface.html)

**kivy.uix.gesturesurface.GestureContainer**

Bases: [`kivy.event.EventDispatcher`](https://kivy.org/doc/stable/api-kivy.event.html#kivy.event.EventDispatcher)
Container object that stores information about a gesture. It has
various properties that are updated by GestureSurface as drawing
progresses.

**kivy.uix.gesturesurface.GestureContainer.accept_stroke**

Returns True if this container can accept count new strokes

**kivy.uix.gesturesurface.GestureContainer.add_stroke**

Associate a list of points with a touch.uid; the line itself is
created by the caller, but subsequent move/up events look it
up via us. This is done to avoid problems during merge.

**kivy.uix.gesturesurface.GestureContainer.complete_stroke**

Called on touch up events to keep track of how many strokes
are active in the gesture (we only want to dispatch event when
the *last* stroke in the gesture is released)

**kivy.uix.gesturesurface.GestureContainer.get_vectors**

Return strokes in a format that is acceptable for
kivy.multistroke.Recognizer as a gesture candidate or template. The
result is cached automatically; the cache is invalidated at the start
and end of a stroke and if update_bbox is called. If you are going
to analyze a gesture mid-stroke, you may need to set the no_cache
argument to True.

**kivy.uix.gesturesurface.GestureContainer.handles**

Returns True if this container handles the given touch

**kivy.uix.gesturesurface.GestureContainer.single_points_test**

Returns True if the gesture consists only of single-point strokes,
we must discard it in this case, or an exception will be raised

**kivy.uix.gesturesurface.GestureContainer.update_bbox**

Update gesture bbox from a touch coordinate

**kivy.uix.gesturesurface.GestureSurface**

Bases: [`kivy.uix.floatlayout.FloatLayout`](https://kivy.org/doc/stable/api-kivy.uix.floatlayout.html#kivy.uix.floatlayout.FloatLayout)
Simple gesture surface to track/draw touch movements. Typically used
to gather user input suitable for [`kivy.multistroke.Recognizer`](https://kivy.org/doc/stable/api-kivy.multistroke.html#kivy.multistroke.Recognizer).

**kivy.uix.gesturesurface.GestureSurface.find_colliding_gesture**

Checks if a touch x/y collides with the bounding box of an existing
gesture. If so, return it (otherwise returns None)

**kivy.uix.gesturesurface.GestureSurface.get_gesture**

Returns GestureContainer associated with given touch

**kivy.uix.gesturesurface.GestureSurface.init_gesture**

Create a new gesture from touch, i.e. it’s the first on
surface, or was not close enough to any existing gesture (yet)

**kivy.uix.gesturesurface.GestureSurface.merge_gestures**

Merges two gestures together, the oldest one is retained and the
newer one gets the GestureContainer.was_merged flag raised.

**kivy.uix.gesturesurface.GestureSurface.on_touch_down**

When a new touch is registered, the first thing we do is to test if
it collides with the bounding box of another known gesture. If so, it
is assumed to be part of that gesture.

**kivy.uix.gesturesurface.GestureSurface.on_touch_move**

When a touch moves, we add a point to the line on the canvas so the
path is updated. We must also check if the new point collides with the
bounding box of another gesture - if so, they should be merged.

**kivy.uix.gesturesurface.GestureSurface.on_touch_up**

Receive a touch up event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivy.org/doc/stable/#kivy.uix.gesturesurface.GestureSurface.on_touch_down) for more information.

---

## API - [`kivy.uix.gridlayout`](https://kivy.org/doc/stable/api-kivy.uix.gridlayout.html)

**kivy.uix.gridlayout.GridLayout**

Bases: [`kivy.uix.layout.Layout`](https://kivy.org/doc/stable/api-kivy.uix.layout.html#kivy.uix.layout.Layout)
Grid layout class. See module documentation for more information.

**kivy.uix.gridlayout.GridLayout.col_default_width**

Default minimum size to use for a column.
New in version 1.0.7.
[`col_default_width`](https://kivy.org/doc/stable/#kivy.uix.gridlayout.GridLayout.col_default_width) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.

**kivy.uix.gridlayout.GridLayout.col_force_default**

If True, ignore the width and size_hint_x of the child and use the
default column width.
New in version 1.0.7.
[`col_force_default`](https://kivy.org/doc/stable/#kivy.uix.gridlayout.GridLayout.col_force_default) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivy.uix.gridlayout.GridLayout.cols**

Number of columns in the grid.
Changed in version 1.0.8:Changed from a NumericProperty to BoundedNumericProperty. You can no
longer set this to a negative value.
[`cols`](https://kivy.org/doc/stable/#kivy.uix.gridlayout.GridLayout.cols) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and defaults to
None.

**kivy.uix.gridlayout.GridLayout.cols_minimum**

Dict of minimum width for each column. The dictionary keys are the
column numbers, e.g. 0, 1, 2…
New in version 1.0.7.
[`cols_minimum`](https://kivy.org/doc/stable/#kivy.uix.gridlayout.GridLayout.cols_minimum) is a [`DictProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.DictProperty) and
defaults to {}.

**kivy.uix.gridlayout.GridLayout.do_layout**

This function is called when a layout is called by a trigger.
If you are writing a new Layout subclass, don’t call this function
directly but use `_trigger_layout()` instead.
The function is by default called *before* the next frame, therefore
the layout isn’t updated immediately. Anything depending on the
positions of e.g. children should be scheduled for the next frame.
New in version 1.0.8.

**kivy.uix.gridlayout.GridLayout.minimum_height**

Automatically computed minimum height needed to contain all children.
New in version 1.0.8.
[`minimum_height`](https://kivy.org/doc/stable/#kivy.uix.gridlayout.GridLayout.minimum_height) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0. It is read only.

**kivy.uix.gridlayout.GridLayout.minimum_size**

Automatically computed minimum size needed to contain all children.
New in version 1.0.8.
[`minimum_size`](https://kivy.org/doc/stable/#kivy.uix.gridlayout.GridLayout.minimum_size) is a
[`ReferenceListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ReferenceListProperty) of
([`minimum_width`](https://kivy.org/doc/stable/#kivy.uix.gridlayout.GridLayout.minimum_width), [`minimum_height`](https://kivy.org/doc/stable/#kivy.uix.gridlayout.GridLayout.minimum_height)) properties. It is read
only.

**kivy.uix.gridlayout.GridLayout.minimum_width**

Automatically computed minimum width needed to contain all children.
New in version 1.0.8.
[`minimum_width`](https://kivy.org/doc/stable/#kivy.uix.gridlayout.GridLayout.minimum_width) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0. It is read only.

**kivy.uix.gridlayout.GridLayout.orientation**

Orientation of the layout.
[`orientation`](https://kivy.org/doc/stable/#kivy.uix.gridlayout.GridLayout.orientation) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty) and
defaults to ‘lr-tb’.
Valid orientations are ‘lr-tb’, ‘tb-lr’, ‘rl-tb’, ‘tb-rl’, ‘lr-bt’,
‘bt-lr’, ‘rl-bt’ and ‘bt-rl’.
New in version 2.0.0.

**kivy.uix.gridlayout.GridLayout.padding**

Padding between the layout box and its children: [padding_left,
padding_top, padding_right, padding_bottom].
padding also accepts a two argument form [padding_horizontal,
padding_vertical] and a one argument form [padding].
Changed in version 1.7.0:Replaced NumericProperty with VariableListProperty.
[`padding`](https://kivy.org/doc/stable/#kivy.uix.gridlayout.GridLayout.padding) is a [`VariableListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.VariableListProperty) and
defaults to [0, 0, 0, 0].

**kivy.uix.gridlayout.GridLayout.row_default_height**

Default minimum size to use for row.
New in version 1.0.7.
[`row_default_height`](https://kivy.org/doc/stable/#kivy.uix.gridlayout.GridLayout.row_default_height) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.

**kivy.uix.gridlayout.GridLayout.row_force_default**

If True, ignore the height and size_hint_y of the child and use the
default row height.
New in version 1.0.7.
[`row_force_default`](https://kivy.org/doc/stable/#kivy.uix.gridlayout.GridLayout.row_force_default) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivy.uix.gridlayout.GridLayout.rows**

Number of rows in the grid.
Changed in version 1.0.8:Changed from a NumericProperty to a BoundedNumericProperty. You can no
longer set this to a negative value.
[`rows`](https://kivy.org/doc/stable/#kivy.uix.gridlayout.GridLayout.rows) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and defaults to
None.

**kivy.uix.gridlayout.GridLayout.rows_minimum**

Dict of minimum height for each row. The dictionary keys are the
row numbers, e.g. 0, 1, 2…
New in version 1.0.7.
[`rows_minimum`](https://kivy.org/doc/stable/#kivy.uix.gridlayout.GridLayout.rows_minimum) is a [`DictProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.DictProperty) and
defaults to {}.

**kivy.uix.gridlayout.GridLayout.spacing**

Spacing between children: [spacing_horizontal, spacing_vertical].
spacing also accepts a one argument form [spacing].
[`spacing`](https://kivy.org/doc/stable/#kivy.uix.gridlayout.GridLayout.spacing) is a
[`VariableListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.VariableListProperty) and defaults to [0, 0].

**kivy.uix.gridlayout.GridLayoutException**

Bases: `Exception`
Exception for errors if the grid layout manipulation fails.

---

## API - [`kivy.uix.image`](https://kivy.org/doc/stable/api-kivy.uix.image.html)

**kivy.uix.image.AsyncImage**

Bases: [`kivy.uix.image.Image`](https://kivy.org/doc/stable/#kivy.uix.image.Image)
Asynchronous Image class. See the module documentation for more
information.

**kivy.uix.image.AsyncImage.remove_from_cache**

Remove image from cache.
New in version 2.0.0.

**kivy.uix.image.Image**

Bases: [`kivy.uix.widget.Widget`](https://kivy.org/doc/stable/api-kivy.uix.widget.html#kivy.uix.widget.Widget)
Image class, see module documentation for more information.

**kivy.uix.image.Image.allow_stretch**

If True, the normalized image size will be maximized to fit in the image
box. Otherwise, if the box is too tall, the image will not be
stretched more than 1:1 pixels.
New in version 1.0.7.
Deprecated since version 2.2.0:[`allow_stretch`](https://kivy.org/doc/stable/#kivy.uix.image.Image.allow_stretch) have been deprecated. Please use fit_mode
instead.
[`allow_stretch`](https://kivy.org/doc/stable/#kivy.uix.image.Image.allow_stretch) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to False.

**kivy.uix.image.Image.anim_delay**

Delay the animation if the image is sequenced (like an animated gif).
If anim_delay is set to -1, the animation will be stopped.
New in version 1.0.8.
[`anim_delay`](https://kivy.org/doc/stable/#kivy.uix.image.Image.anim_delay) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0.25 (4 FPS).

**kivy.uix.image.Image.anim_loop**

Number of loops to play then stop animating. 0 means keep animating.
New in version 1.9.0.
[`anim_loop`](https://kivy.org/doc/stable/#kivy.uix.image.Image.anim_loop) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0.

**kivy.uix.image.Image.color**

Image color, in the format (r, g, b, a). This attribute can be used to
‘tint’ an image. Be careful: if the source image is not gray/white, the
color will not really work as expected.
New in version 1.0.6.
[`color`](https://kivy.org/doc/stable/#kivy.uix.image.Image.color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty) and defaults to
[1, 1, 1, 1].
Changed in version 2.0.0:Changed from [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) to
[`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty).

**kivy.uix.image.Image.fit_mode**

If the size of the image is different than the size of the widget,
determine how the image should be resized to fit inside the widget box.
Available options:
`"scale-down"`: the image will be scaled down to fit inside the widget
box, **maintaining its aspect ratio and without stretching**. If the size
of the image is smaller than the widget, it will be displayed at its
original size. If the image has a different aspect ratio than the widget,
there will be blank areas on the widget box.
`"fill"`: the image is stretched to fill the widget, [**](https://kivy.org/doc/stable/#id1)regardless of
its aspect ratio or dimensions**. If the image has a different aspect ratio
than the widget, this option can lead to distortion of the image.
`"contain"`: the image is resized to fit inside the widget box,
**maintaining its aspect ratio**. If the image size is larger than the
widget size, the behavior will be similar to `"scale-down"`. However, if
the size of the image is smaller than the widget size, unlike
`"scale-down`, the image will be resized to fit inside the widget.
If the image has a different aspect ratio than the widget, there will be
blank areas on the widget box.
`"cover"`: the image will be stretched horizontally or vertically to
fill the widget box, **maintaining its aspect ratio**. If the image has a
different aspect ratio than the widget, then the image will be clipped to
fit.
[`fit_mode`](https://kivy.org/doc/stable/#kivy.uix.image.Image.fit_mode) is a [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty) and
defaults to `"scale-down"`.

**kivy.uix.image.Image.image_ratio**

Ratio of the image (width / float(height).
[`image_ratio`](https://kivy.org/doc/stable/#kivy.uix.image.Image.image_ratio) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) and is
read-only.

**kivy.uix.image.Image.keep_data**

If True, the underlying _coreimage will store the raw image data.
This is useful when performing pixel based collision detection.
New in version 1.3.0.
[`keep_data`](https://kivy.org/doc/stable/#kivy.uix.image.Image.keep_data) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to False.

**kivy.uix.image.Image.keep_ratio**

If False along with allow_stretch being True, the normalized image
size will be maximized to fit in the image box and ignores the aspect
ratio of the image.
Otherwise, if the box is too tall, the image will not be stretched more
than 1:1 pixels.
New in version 1.0.8.
Deprecated since version 2.2.0:[`keep_ratio`](https://kivy.org/doc/stable/#kivy.uix.image.Image.keep_ratio) have been deprecated. Please use fit_mode
instead.
[`keep_ratio`](https://kivy.org/doc/stable/#kivy.uix.image.Image.keep_ratio) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to True.

**kivy.uix.image.Image.mipmap**

Indicate if you want OpenGL mipmapping to be applied to the texture.
Read [Mipmapping](https://kivy.org/doc/stable/api-kivy.graphics.texture.html#mipmap) for more information.
New in version 1.0.7.
[`mipmap`](https://kivy.org/doc/stable/#kivy.uix.image.Image.mipmap) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and defaults
to False.

**kivy.uix.image.Image.nocache**

If this property is set True, the image will not be added to the
internal cache. The cache will simply ignore any calls trying to
append the core image.
New in version 1.6.0.
[`nocache`](https://kivy.org/doc/stable/#kivy.uix.image.Image.nocache) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and defaults
to False.

**kivy.uix.image.Image.norm_image_size**

Normalized image size within the widget box.
This size will always fit the widget size and will preserve the image
ratio.
[`norm_image_size`](https://kivy.org/doc/stable/#kivy.uix.image.Image.norm_image_size) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) and
is read-only.

**kivy.uix.image.Image.reload**

Reload image from disk. This facilitates re-loading of
images from disk in case the image content changes.
New in version 1.3.0.
Usage:

**kivy.uix.image.Image.remove_from_cache**

Remove image from cache.
New in version 2.0.0.

**kivy.uix.image.Image.source**

Filename / source of your image.
[`source`](https://kivy.org/doc/stable/#kivy.uix.image.Image.source) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to None.

**kivy.uix.image.Image.texture**

Texture object of the image. The texture represents the original, loaded
image texture. It is stretched and positioned during rendering according to
the [`fit_mode`](https://kivy.org/doc/stable/#kivy.uix.image.Image.fit_mode) property.
Depending of the texture creation, the value will be a
[`Texture`](https://kivy.org/doc/stable/api-kivy.graphics.texture.html#kivy.graphics.texture.Texture) or a
[`TextureRegion`](https://kivy.org/doc/stable/api-kivy.graphics.texture.html#kivy.graphics.texture.TextureRegion) object.
[`texture`](https://kivy.org/doc/stable/#kivy.uix.image.Image.texture) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and defaults
to None.

**kivy.uix.image.Image.texture_size**

Texture size of the image. This represents the original, loaded image
texture size.

---

## API - [`kivy.uix.label`](https://kivy.org/doc/stable/api-kivy.uix.label.html)

**kivy.uix.label.Label**

Bases: [`kivy.uix.widget.Widget`](https://kivy.org/doc/stable/api-kivy.uix.widget.html#kivy.uix.widget.Widget)
Label class, see module documentation for more information.

**kivy.uix.label.Label.anchors**

New in version 1.1.0.
Position of all the `[anchor=xxx]` markup in the text.
These coordinates are relative to the top left corner of the text, with
the y value increasing downwards. Anchors names should be unique and only
the first occurrence of any duplicate anchors will be recorded.
You can place anchors in your markup text as follows:

Then, all the `[anchor=]` references will be removed and you’ll get all
the anchor positions in this property (only after rendering):

**kivy.uix.label.Label.base_direction**

Base direction of text, this impacts horizontal alignment when
[`halign`](https://kivy.org/doc/stable/#kivy.uix.label.Label.halign) is auto (the default). Available options are: None,
“ltr” (left to right), “rtl” (right to left) plus “weak_ltr” and
“weak_rtl”.

New in version 1.11.0.
[`base_direction`](https://kivy.org/doc/stable/#kivy.uix.label.Label.base_direction) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty) and
defaults to None (autodetect RTL if possible, otherwise LTR).

**kivy.uix.label.Label.bold**

Indicates use of the bold version of your font.

[`bold`](https://kivy.org/doc/stable/#kivy.uix.label.Label.bold) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and defaults to
False.

**kivy.uix.label.Label.color**

Text color, in the format (r, g, b, a).
[`color`](https://kivy.org/doc/stable/#kivy.uix.label.Label.color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty) and defaults to
[1, 1, 1, 1].
Changed in version 2.0.0:Changed from [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) to
[`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty).

**kivy.uix.label.Label.disabled_color**

The color of the text when the widget is disabled, in the (r, g, b, a)
format.
New in version 1.8.0.
[`disabled_color`](https://kivy.org/doc/stable/#kivy.uix.label.Label.disabled_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty) and
defaults to [1, 1, 1, .3].
Changed in version 2.0.0:Changed from [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) to
[`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty).

**kivy.uix.label.Label.disabled_outline_color**

The color of the text outline when the widget is disabled, in the
(r, g, b) format.

New in version 1.10.0.
[`disabled_outline_color`](https://kivy.org/doc/stable/#kivy.uix.label.Label.disabled_outline_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to [0, 0, 0].
Changed in version 2.0.0:Changed from [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) to
[`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty). Alpha component is ignored
and assigning value to it has no effect.

**kivy.uix.label.Label.ellipsis_options**

Font options for the ellipsis string(’…’) used to split the text.
Accepts a dict as option name with the value. Only applied when
[`markup`](https://kivy.org/doc/stable/#kivy.uix.label.Label.markup) is true and text is shortened. All font options which work
for [`Label`](https://kivy.org/doc/stable/#kivy.uix.label.Label) will work for [`ellipsis_options`](https://kivy.org/doc/stable/#kivy.uix.label.Label.ellipsis_options). Defaults for
the options not specified are taken from the surronding text.

New in version 2.0.0.
[`ellipsis_options`](https://kivy.org/doc/stable/#kivy.uix.label.Label.ellipsis_options) is a [`DictProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.DictProperty) and
defaults to {} (the empty dict).

**kivy.uix.label.Label.font_blended**

Whether blended or solid font rendering should be used.

New in version 1.10.0.
[`font_blended`](https://kivy.org/doc/stable/#kivy.uix.label.Label.font_blended) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to True.

**kivy.uix.label.Label.font_context**

Font context. None means the font is used in isolation, so you are
guaranteed to be drawing with the TTF file resolved by [`font_name`](https://kivy.org/doc/stable/#kivy.uix.label.Label.font_name).
Specifying a value here will load the font file into a named context,
enabling fallback between all fonts in the same context. If a font
context is set, you are not guaranteed that rendering will actually use
the specified TTF file for all glyphs (Pango will pick the one it
thinks is best).
If Kivy is linked against a system-wide installation of FontConfig,
you can load the system fonts by specifying a font context starting
with the special string system://. This will load the system
fontconfig configuration, and add your application-specific fonts on
top of it (this imposes a significant risk of family name collision,
Pango may not use your custom font file, but pick one from the system)

New in version 1.11.0.
[`font_context`](https://kivy.org/doc/stable/#kivy.uix.label.Label.font_context) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to None.

**kivy.uix.label.Label.font_direction**

Direction for the specific font, can be one of ltr, rtl, ttb,`btt`.
font_direction currently only works with SDL2 ttf providers.
New in version 2.2.0.
[`font_direction`](https://kivy.org/doc/stable/#kivy.uix.label.Label.font_direction) is a [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty) and
defults to ‘ltr’.

**kivy.uix.label.Label.font_family**

Font family, this is only applicable when using [`font_context`](https://kivy.org/doc/stable/#kivy.uix.label.Label.font_context)
option. The specified font family will be requested, but note that it may
not be available, or there could be multiple fonts registered with the
same family. The value can be a family name (string) available in the
font context (for example a system font in a system:// context, or a
custom font file added using `kivy.core.text.FontContextManager`).
If set to None, font selection is controlled by the [`font_name`](https://kivy.org/doc/stable/#kivy.uix.label.Label.font_name)
setting.

New in version 1.11.0.
[`font_family`](https://kivy.org/doc/stable/#kivy.uix.label.Label.font_family) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to None.

**kivy.uix.label.Label.font_features**

OpenType font features, in CSS format, this is passed straight
through to Pango. The effects of requesting a feature depends on loaded
fonts, library versions, etc. For a complete list of features, see:
[https://en.wikipedia.org/wiki/List_of_typographic_features](https://en.wikipedia.org/wiki/List_of_typographic_features)

New in version 1.11.0.
[`font_features`](https://kivy.org/doc/stable/#kivy.uix.label.Label.font_features) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to an empty string.

**kivy.uix.label.Label.font_hinting**

What hinting option to use for font rendering.
Can be one of ‘normal’, ‘light’, ‘mono’ or None.

New in version 1.10.0.
[`font_hinting`](https://kivy.org/doc/stable/#kivy.uix.label.Label.font_hinting) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty) and
defaults to ‘normal’.

**kivy.uix.label.Label.font_kerning**

Whether kerning is enabled for font rendering. You should normally
only disable this if rendering is broken with a particular font file.

New in version 1.10.0.
[`font_kerning`](https://kivy.org/doc/stable/#kivy.uix.label.Label.font_kerning) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to True.

**kivy.uix.label.Label.font_name**

Filename of the font to use. The path can be absolute or relative.
Relative paths are resolved by the [`resource_find()`](https://kivy.org/doc/stable/api-kivy.resources.html#kivy.resources.resource_find)
function.

[`font_name`](https://kivy.org/doc/stable/#kivy.uix.label.Label.font_name) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to ‘Roboto’. This value is taken
from [`Config`](https://kivy.org/doc/stable/api-kivy.config.html#kivy.config.Config).

**kivy.uix.label.Label.font_script_name**

script_code from [https://bit.ly/TypeScriptCodes](https://bit.ly/TypeScriptCodes) .
New in version 2.2.0.

[`font_script_name`](https://kivy.org/doc/stable/#kivy.uix.label.Label.font_script_name) is a [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty) and
defaults to ‘Latn’.

**kivy.uix.label.Label.font_size**

Font size of the text, in pixels.
[`font_size`](https://kivy.org/doc/stable/#kivy.uix.label.Label.font_size) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 15sp.

**kivy.uix.label.Label.halign**

Horizontal alignment of the text.
[`halign`](https://kivy.org/doc/stable/#kivy.uix.label.Label.halign) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty) and
defaults to ‘auto’. Available options are : auto, left, center, right and
justify. Auto will attempt to autodetect horizontal alignment for RTL text
(Pango only), otherwise it behaves like left.

Changed in version 1.10.1:Added auto option
Changed in version 1.6.0:A new option was added to [`halign`](https://kivy.org/doc/stable/#kivy.uix.label.Label.halign), namely justify.

**kivy.uix.label.Label.is_shortened**

This property indicates if [`text`](https://kivy.org/doc/stable/#kivy.uix.label.Label.text) was rendered with or without
shortening when [`shorten`](https://kivy.org/doc/stable/#kivy.uix.label.Label.shorten) is True.
New in version 1.10.0.
[`is_shortened`](https://kivy.org/doc/stable/#kivy.uix.label.Label.is_shortened) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to False.

**kivy.uix.label.Label.italic**

Indicates use of the italic version of your font.

[`italic`](https://kivy.org/doc/stable/#kivy.uix.label.Label.italic) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and defaults
to False.

**kivy.uix.label.Label.limit_render_to_text_bbox**

If set to `True`, this parameter indicates that rendering should be
limited to the bounding box of the text, excluding any additional white
spaces designated for ascent and descent.
By limiting the rendering to the bounding box of the text, it ensures a
more precise alignment with surrounding elements when utilizing properties
such as valign, y, pos, pos_hint, etc.

[`limit_render_to_text_bbox`](https://kivy.org/doc/stable/#kivy.uix.label.Label.limit_render_to_text_bbox) is a
[`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and defaults to False.

**kivy.uix.label.Label.line_height**

Line Height for the text. e.g. line_height = 2 will cause the spacing
between lines to be twice the size.
[`line_height`](https://kivy.org/doc/stable/#kivy.uix.label.Label.line_height) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 1.0.
New in version 1.5.0.

**kivy.uix.label.Label.markup**

New in version 1.1.0.
If True, the text will be rendered using the
[`MarkupLabel`](https://kivy.org/doc/stable/api-kivy.core.text.markup.html#kivy.core.text.markup.MarkupLabel): you can change the
style of the text using tags. Check the
[Text Markup](https://kivy.org/doc/stable/api-kivy.core.text.markup.html) documentation for more information.
[`markup`](https://kivy.org/doc/stable/#kivy.uix.label.Label.markup) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and defaults
to False.

**kivy.uix.label.Label.max_lines**

Maximum number of lines to use, defaults to 0, which means unlimited.
Please note that [`shorten`](https://kivy.org/doc/stable/#kivy.uix.label.Label.shorten) take over this property. (with
shorten, the text is always one line.)
New in version 1.8.0.
[`max_lines`](https://kivy.org/doc/stable/#kivy.uix.label.Label.max_lines) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0.

**kivy.uix.label.Label.mipmap**

Indicates whether OpenGL mipmapping is applied to the texture or not.
Read [Mipmapping](https://kivy.org/doc/stable/api-kivy.graphics.texture.html#mipmap) for more information.
New in version 1.0.7.
[`mipmap`](https://kivy.org/doc/stable/#kivy.uix.label.Label.mipmap) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and defaults
to False.

**kivy.uix.label.Label.on_touch_down**

Receive a touch down event.

**kivy.uix.label.Label.outline_color**

The color of the text outline, in the (r, g, b) format.

New in version 1.10.0.
[`outline_color`](https://kivy.org/doc/stable/#kivy.uix.label.Label.outline_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty) and
defaults to [0, 0, 0, 1].
Changed in version 2.0.0:Changed from [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) to
[`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty). Alpha component is ignored
and assigning value to it has no effect.

**kivy.uix.label.Label.outline_width**

Width in pixels for the outline around the text. No outline will be
rendered if the value is None.

New in version 1.10.0.
[`outline_width`](https://kivy.org/doc/stable/#kivy.uix.label.Label.outline_width) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to None.

**kivy.uix.label.Label.padding**

Padding of the text in the format [padding_left, padding_top,
padding_right, padding_bottom]
`padding` also accepts a two argument form [padding_horizontal,
padding_vertical] and a one argument form [padding].
Changed in version 2.2.0:Replaced ReferenceListProperty with VariableListProperty.
[`padding`](https://kivy.org/doc/stable/#kivy.uix.label.Label.padding) is a [`VariableListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.VariableListProperty) and
defaults to [0, 0, 0, 0].

**kivy.uix.label.Label.padding_x**

Horizontal padding of the text inside the widget box.
[`padding_x`](https://kivy.org/doc/stable/#kivy.uix.label.Label.padding_x) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0.
Changed in version 1.9.0:padding_x has been fixed to work as expected.
In the past, the text was padded by the negative of its values.
Deprecated since version 2.2.0:Please use [`padding`](https://kivy.org/doc/stable/#kivy.uix.label.Label.padding) instead.

**kivy.uix.label.Label.padding_y**

Vertical padding of the text inside the widget box.
[`padding_y`](https://kivy.org/doc/stable/#kivy.uix.label.Label.padding_y) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0.
Changed in version 1.9.0:padding_y has been fixed to work as expected.
In the past, the text was padded by the negative of its values.
Deprecated since version 2.2.0:Please use [`padding`](https://kivy.org/doc/stable/#kivy.uix.label.Label.padding) instead.

**kivy.uix.label.Label.refs**

New in version 1.1.0.
List of `[ref=xxx]` markup items in the text with the bounding box of
all the words contained in a ref, available only after rendering.
For example, if you wrote:

The refs will be set with:

The references marked “hello” have a bounding box at (x1, y1, x2, y2).
These coordinates are relative to the top left corner of the text, with
the y value increasing downwards. You can define multiple refs with the
same name: each occurrence will be added as another (x1, y1, x2, y2) tuple
to this list.
The current Label implementation uses these references if they exist in
your markup text, automatically doing the collision with the touch and
dispatching an on_ref_press event.
You can bind a ref event like this:

**kivy.uix.label.Label.shorten**

Indicates whether the label should attempt to shorten its textual contents
as much as possible if a [`text_size`](https://kivy.org/doc/stable/#kivy.uix.label.Label.text_size) is given. Setting this to True
without an appropriately set [`text_size`](https://kivy.org/doc/stable/#kivy.uix.label.Label.text_size) will lead to unexpected
results.
[`shorten_from`](https://kivy.org/doc/stable/#kivy.uix.label.Label.shorten_from) and [`split_str`](https://kivy.org/doc/stable/#kivy.uix.label.Label.split_str) control the direction from
which the [`text`](https://kivy.org/doc/stable/#kivy.uix.label.Label.text) is split, as well as where in the [`text`](https://kivy.org/doc/stable/#kivy.uix.label.Label.text) we
are allowed to split.
[`shorten`](https://kivy.org/doc/stable/#kivy.uix.label.Label.shorten) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and defaults
to False.

**kivy.uix.label.Label.shorten_from**

The side from which we should shorten the text from, can be left,
right, or center.
For example, if left, the ellipsis will appear towards the left side and we
will display as much text starting from the right as possible. Similar to
[`shorten`](https://kivy.org/doc/stable/#kivy.uix.label.Label.shorten), this option only applies when [`text_size`](https://kivy.org/doc/stable/#kivy.uix.label.Label.text_size) [0] is
not None, In this case, the string is shortened to fit within the specified
width.
New in version 1.9.0.
[`shorten_from`](https://kivy.org/doc/stable/#kivy.uix.label.Label.shorten_from) is a [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty) and
defaults to center.

**kivy.uix.label.Label.split_str**

The string used to split the [`text`](https://kivy.org/doc/stable/#kivy.uix.label.Label.text) while shortening the string
when [`shorten`](https://kivy.org/doc/stable/#kivy.uix.label.Label.shorten) is True.
For example, if it’s a space, the string will be broken into words and as
many whole words that can fit into a single line will be displayed. If
[`split_str`](https://kivy.org/doc/stable/#kivy.uix.label.Label.split_str) is the empty string, ‘’, we split on every character
fitting as much text as possible into the line.
New in version 1.9.0.
[`split_str`](https://kivy.org/doc/stable/#kivy.uix.label.Label.split_str) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to ‘’ (the empty string).

**kivy.uix.label.Label.strikethrough**

Adds a strikethrough line to the text.

New in version 1.10.0.
[`strikethrough`](https://kivy.org/doc/stable/#kivy.uix.label.Label.strikethrough) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to False.

**kivy.uix.label.Label.strip**

Whether leading and trailing spaces and newlines should be stripped from
each displayed line. If True, every line will start at the right or left
edge, depending on [`halign`](https://kivy.org/doc/stable/#kivy.uix.label.Label.halign). If [`halign`](https://kivy.org/doc/stable/#kivy.uix.label.Label.halign) is justify it is
implicitly True.
New in version 1.9.0.
[`strip`](https://kivy.org/doc/stable/#kivy.uix.label.Label.strip) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to False.

**kivy.uix.label.Label.text**

Text of the label.
Creation of a simple hello world:

[`text`](https://kivy.org/doc/stable/#kivy.uix.label.Label.text) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults to
‘’.

**kivy.uix.label.Label.text_language**

Language of the text, if None Pango will determine it from locale.
This is an RFC-3066 format language tag (as a string), for example
“en_US”, “zh_CN”, “fr” or “ja”. This can impact font selection, metrics
and rendering. For example, the same bytes of text can look different
for ur and ar languages, though both use Arabic script.

New in version 1.11.0.
[`text_language`](https://kivy.org/doc/stable/#kivy.uix.label.Label.text_language) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to None.

**kivy.uix.label.Label.text_size**

By default, the label is not constrained to any bounding box.
You can set the size constraint of the label with this property.
The text will autoflow into the constraints. So although the font size
will not be reduced, the text will be arranged to fit into the box as best
as possible, with any text still outside the box clipped.
This sets and clips [`texture_size`](https://kivy.org/doc/stable/#kivy.uix.label.Label.texture_size) to text_size if not None.
New in version 1.0.4.
For example, whatever your current widget size is, if you want the label to
be created in a box with width=200 and unlimited height:

[`text_size`](https://kivy.org/doc/stable/#kivy.uix.label.Label.text_size) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) and
defaults to (None, None), meaning no size restriction by default.

**kivy.uix.label.Label.texture**

Texture object of the text.
The text is rendered automatically when a property changes. The OpenGL
texture created in this operation is stored in this property. You can use
this [`texture`](https://kivy.org/doc/stable/#kivy.uix.label.Label.texture) for any graphics elements.
Depending on the texture creation, the value will be a
[`Texture`](https://kivy.org/doc/stable/api-kivy.graphics.texture.html#kivy.graphics.texture.Texture) or
[`TextureRegion`](https://kivy.org/doc/stable/api-kivy.graphics.texture.html#kivy.graphics.texture.TextureRegion) object.

[`texture`](https://kivy.org/doc/stable/#kivy.uix.label.Label.texture) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and defaults
to None.

**kivy.uix.label.Label.texture_size**

Texture size of the text. The size is determined by the font size and
text. If [`text_size`](https://kivy.org/doc/stable/#kivy.uix.label.Label.text_size) is [None, None], the texture will be the size
required to fit the text, otherwise it’s clipped to fit [`text_size`](https://kivy.org/doc/stable/#kivy.uix.label.Label.text_size).
When [`text_size`](https://kivy.org/doc/stable/#kivy.uix.label.Label.text_size) is [None, None], one can bind to texture_size
and rescale it proportionally to fit the size of the label in order to
make the text fit maximally in the label.

**kivy.uix.label.Label.texture_update**

Force texture recreation with the current Label properties.
After this function call, the [`texture`](https://kivy.org/doc/stable/#kivy.uix.label.Label.texture) and [`texture_size`](https://kivy.org/doc/stable/#kivy.uix.label.Label.texture_size)
will be updated in this order.

**kivy.uix.label.Label.underline**

Adds an underline to the text.

New in version 1.10.0.
[`underline`](https://kivy.org/doc/stable/#kivy.uix.label.Label.underline) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to False.

**kivy.uix.label.Label.unicode_errors**

How to handle unicode decode errors. Can be ‘strict’, ‘replace’ or
‘ignore’.
New in version 1.9.0.
[`unicode_errors`](https://kivy.org/doc/stable/#kivy.uix.label.Label.unicode_errors) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty) and
defaults to ‘replace’.

**kivy.uix.label.Label.valign**

Vertical alignment of the text.
[`valign`](https://kivy.org/doc/stable/#kivy.uix.label.Label.valign) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty) and defaults
to ‘bottom’. Available options are : ‘bottom’,
‘middle’ (or ‘center’) and ‘top’.
Changed in version 1.10.0:The ‘center’ option has been added as an alias of ‘middle’.

---

## API - [`kivy.uix.layout`](https://kivy.org/doc/stable/api-kivy.uix.layout.html)

**kivy.uix.layout.Layout**

Bases: [`kivy.uix.widget.Widget`](https://kivy.org/doc/stable/api-kivy.uix.widget.html#kivy.uix.widget.Widget)
Layout interface class, used to implement every layout. See module
documentation for more information.

**kivy.uix.layout.Layout.add_widget**

Add a new widget as a child of this widget.

**kivy.uix.layout.Layout.do_layout**

This function is called when a layout is called by a trigger.
If you are writing a new Layout subclass, don’t call this function
directly but use `_trigger_layout()` instead.
The function is by default called *before* the next frame, therefore
the layout isn’t updated immediately. Anything depending on the
positions of e.g. children should be scheduled for the next frame.
New in version 1.0.8.

**kivy.uix.layout.Layout.layout_hint_with_bounds**

(internal) Computes the appropriate (size) hint for all the
widgets given (potential) min or max bounds on the widgets’ size.
The `hint` list is updated with appropriate sizes.
It walks through the hints and for any widgets whose hint will result
in violating min or max constraints, it fixes the hint. Any remaining
or missing space after all the widgets are fixed get distributed
to the widgets making them smaller or larger according to their
size hint.
This algorithms knows nothing about the widgets other than what is
passed through the input params, so it’s fairly generic for laying
things out according to constraints using size hints.

**kivy.uix.layout.Layout.remove_widget**

Remove a widget from the children of this widget.

---

## API - [`kivy.uix.modalview`](https://kivy.org/doc/stable/api-kivy.uix.modalview.html)

**kivy.uix.modalview.ModalView**

Bases: [`kivy.uix.anchorlayout.AnchorLayout`](https://kivy.org/doc/stable/api-kivy.uix.anchorlayout.html#kivy.uix.anchorlayout.AnchorLayout)
ModalView class. See module documentation for more information.

Changed in version 1.11.0:Added events on_pre_open and on_pre_dismiss.
Changed in version 2.0.0:Added property ‘overlay_color’.
Changed in version 2.1.0:Marked attach_to property as deprecated.

**kivy.uix.modalview.ModalView.attach_to**

If a widget is set on attach_to, the view will attach to the nearest
parent window of the widget. If none is found, it will attach to the
main/global Window.
[`attach_to`](https://kivy.org/doc/stable/#kivy.uix.modalview.ModalView.attach_to) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to None.

**kivy.uix.modalview.ModalView.auto_dismiss**

This property determines if the view is automatically
dismissed when the user clicks outside it.
[`auto_dismiss`](https://kivy.org/doc/stable/#kivy.uix.modalview.ModalView.auto_dismiss) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to True.

**kivy.uix.modalview.ModalView.background**

Background image of the view used for the view background.
[`background`](https://kivy.org/doc/stable/#kivy.uix.modalview.ModalView.background) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to ‘atlas://data/images/defaulttheme/modalview-background’.

**kivy.uix.modalview.ModalView.background_color**

Background color, in the format (r, g, b, a).
This acts as a *multiplier* to the texture color. The default
texture is grey, so just setting the background color will give
a darker result. To set a plain color, set the
`background_normal` to `''`.
The [`background_color`](https://kivy.org/doc/stable/#kivy.uix.modalview.ModalView.background_color) is a
[`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty) and defaults to [1, 1, 1, 1].
Changed in version 2.0.0:Changed behavior to affect the background of the widget itself, not
the overlay dimming.
Changed from [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) to
[`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty).

**kivy.uix.modalview.ModalView.border**

Border used for [`BorderImage`](https://kivy.org/doc/stable/api-kivy.graphics.vertex_instructions.html#kivy.graphics.vertex_instructions.BorderImage)
graphics instruction. Used for the `background_normal` and the
`background_down` properties. Can be used when using custom
backgrounds.
It must be a list of four values: (bottom, right, top, left). Read the
BorderImage instructions for more information about how to use it.
[`border`](https://kivy.org/doc/stable/#kivy.uix.modalview.ModalView.border) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) and defaults to
(16, 16, 16, 16).

**kivy.uix.modalview.ModalView.dismiss**

Close the view if it is open.
If you really want to close the view, whatever the on_dismiss
event returns, you can use the *force* keyword argument:

When the view is dismissed, it will be faded out before being
removed from the parent. If you don’t want this animation, use:

**kivy.uix.modalview.ModalView.on__anim_alpha**

animation progress callback.

**kivy.uix.modalview.ModalView.on_dismiss**

default dismiss event handler.

**kivy.uix.modalview.ModalView.on_motion**

Called when a motion event is received.

New in version 2.1.0.

**kivy.uix.modalview.ModalView.on_open**

default open event handler.

**kivy.uix.modalview.ModalView.on_pre_dismiss**

default pre-dismiss event handler.

**kivy.uix.modalview.ModalView.on_pre_open**

default pre-open event handler.

**kivy.uix.modalview.ModalView.on_touch_down**

touch down event handler.

**kivy.uix.modalview.ModalView.on_touch_move**

touch moved event handler.

**kivy.uix.modalview.ModalView.on_touch_up**

touch up event handler.

**kivy.uix.modalview.ModalView.open**

Display the modal in the Window.
When the view is opened, it will be faded in with an animation. If you
don’t want the animation, use:

**kivy.uix.modalview.ModalView.overlay_color**

Overlay color in the format (r, g, b, a).
Used for dimming the window behind the modal view.
[`overlay_color`](https://kivy.org/doc/stable/#kivy.uix.modalview.ModalView.overlay_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty) and
defaults to [0, 0, 0, .7].
New in version 2.0.0.

---

## API - [`kivy.uix.pagelayout`](https://kivy.org/doc/stable/api-kivy.uix.pagelayout.html)

**kivy.uix.pagelayout.PageLayout**

Bases: [`kivy.uix.layout.Layout`](https://kivy.org/doc/stable/api-kivy.uix.layout.html#kivy.uix.layout.Layout)
PageLayout class. See module documentation for more information.

**kivy.uix.pagelayout.PageLayout.anim_kwargs**

The animation kwargs used to construct the animation
[`anim_kwargs`](https://kivy.org/doc/stable/#kivy.uix.pagelayout.PageLayout.anim_kwargs) is a [`DictProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.DictProperty)
and defaults to {‘d’: .5, ‘t’: ‘in_quad’}.
New in version 1.11.0.

**kivy.uix.pagelayout.PageLayout.border**

The width of the border around the current page used to display
the previous/next page swipe areas when needed.
[`border`](https://kivy.org/doc/stable/#kivy.uix.pagelayout.PageLayout.border) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 50dp.

**kivy.uix.pagelayout.PageLayout.do_layout**

This function is called when a layout is called by a trigger.
If you are writing a new Layout subclass, don’t call this function
directly but use `_trigger_layout()` instead.
The function is by default called *before* the next frame, therefore
the layout isn’t updated immediately. Anything depending on the
positions of e.g. children should be scheduled for the next frame.
New in version 1.0.8.

**kivy.uix.pagelayout.PageLayout.on_touch_down**

Receive a touch down event.

**kivy.uix.pagelayout.PageLayout.on_touch_move**

Receive a touch move event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivy.org/doc/stable/#kivy.uix.pagelayout.PageLayout.on_touch_down) for more information.

**kivy.uix.pagelayout.PageLayout.on_touch_up**

Receive a touch up event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivy.org/doc/stable/#kivy.uix.pagelayout.PageLayout.on_touch_down) for more information.

**kivy.uix.pagelayout.PageLayout.page**

The currently displayed page.
[`page`](https://kivy.org/doc/stable/#kivy.uix.pagelayout.PageLayout.page) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and defaults
to 0.

**kivy.uix.pagelayout.PageLayout.swipe_threshold**

The threshold used to trigger swipes as ratio of the widget
size.
[`swipe_threshold`](https://kivy.org/doc/stable/#kivy.uix.pagelayout.PageLayout.swipe_threshold) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to .5.

---

## API - [`kivy.uix.popup`](https://kivy.org/doc/stable/api-kivy.uix.popup.html)

**kivy.uix.popup.Popup**

Bases: [`kivy.uix.modalview.ModalView`](https://kivy.org/doc/stable/api-kivy.uix.modalview.html#kivy.uix.modalview.ModalView)
Popup class. See module documentation for more information.

**kivy.uix.popup.Popup.add_widget**

Add a new widget as a child of this widget.

**kivy.uix.popup.Popup.content**

Content of the popup that is displayed just under the title.
[`content`](https://kivy.org/doc/stable/#kivy.uix.popup.Popup.content) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and defaults
to None.

**kivy.uix.popup.Popup.on_touch_down**

touch down event handler.

**kivy.uix.popup.Popup.separator_color**

Color used by the separator between title and content.
New in version 1.1.0.
[`separator_color`](https://kivy.org/doc/stable/#kivy.uix.popup.Popup.separator_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty) and
defaults to [47 / 255., 167 / 255., 212 / 255., 1.].
Changed in version 2.0.0:Changed from [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) to
[`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty).

**kivy.uix.popup.Popup.separator_height**

Height of the separator.
New in version 1.1.0.
[`separator_height`](https://kivy.org/doc/stable/#kivy.uix.popup.Popup.separator_height) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 2dp.

**kivy.uix.popup.Popup.title**

String that represents the title of the popup.
[`title`](https://kivy.org/doc/stable/#kivy.uix.popup.Popup.title) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults to
‘No title’.

**kivy.uix.popup.Popup.title_align**

Horizontal alignment of the title.
New in version 1.9.0.
[`title_align`](https://kivy.org/doc/stable/#kivy.uix.popup.Popup.title_align) is a [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty) and
defaults to ‘left’. Available options are left, center, right and justify.

**kivy.uix.popup.Popup.title_color**

Color used by the Title.
New in version 1.8.0.
[`title_color`](https://kivy.org/doc/stable/#kivy.uix.popup.Popup.title_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty) and
defaults to [1, 1, 1, 1].
Changed in version 2.0.0:Changed from [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) to
[`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty).

**kivy.uix.popup.Popup.title_font**

Font used to render the title text.
New in version 1.9.0.
[`title_font`](https://kivy.org/doc/stable/#kivy.uix.popup.Popup.title_font) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to ‘Roboto’. This value is taken
from [`Config`](https://kivy.org/doc/stable/api-kivy.config.html#kivy.config.Config).

**kivy.uix.popup.Popup.title_size**

Represents the font size of the popup title.
New in version 1.6.0.
[`title_size`](https://kivy.org/doc/stable/#kivy.uix.popup.Popup.title_size) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to ’14sp’.

**kivy.uix.popup.PopupException**

Bases: `Exception`
Popup exception, fired when multiple content widgets are added to the
popup.
New in version 1.4.0.

---

## API - [`kivy.uix.progressbar`](https://kivy.org/doc/stable/api-kivy.uix.progressbar.html)

**kivy.uix.progressbar.ProgressBar**

Bases: [`kivy.uix.widget.Widget`](https://kivy.org/doc/stable/api-kivy.uix.widget.html#kivy.uix.widget.Widget)
Class for creating a progress bar widget.
See module documentation for more details.

**kivy.uix.progressbar.ProgressBar.max**

Maximum value allowed for [`value`](https://kivy.org/doc/stable/#kivy.uix.progressbar.ProgressBar.value).
[`max`](https://kivy.org/doc/stable/#kivy.uix.progressbar.ProgressBar.max) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and defaults to
100.

**kivy.uix.progressbar.ProgressBar.value**

Current value used for the slider.
[`value`](https://kivy.org/doc/stable/#kivy.uix.progressbar.ProgressBar.value) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) that
returns the value of the progress bar. If the value is < 0 or >
[`max`](https://kivy.org/doc/stable/#kivy.uix.progressbar.ProgressBar.max), it will be normalized to those boundaries.
Changed in version 1.6.0:The value is now limited to between 0 and [`max`](https://kivy.org/doc/stable/#kivy.uix.progressbar.ProgressBar.max).

**kivy.uix.progressbar.ProgressBar.value_normalized**

Normalized value inside the range 0-1:

[`value_normalized`](https://kivy.org/doc/stable/#kivy.uix.progressbar.ProgressBar.value_normalized) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty).

---

## API - [`kivy.uix.recycleboxlayout`](https://kivy.org/doc/stable/api-kivy.uix.recycleboxlayout.html)

**kivy.uix.recycleboxlayout.RecycleBoxLayout**

Bases: [`kivy.uix.recyclelayout.RecycleLayout`](https://kivy.org/doc/stable/api-kivy.uix.recyclelayout.html#kivy.uix.recyclelayout.RecycleLayout), [`kivy.uix.boxlayout.BoxLayout`](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html#kivy.uix.boxlayout.BoxLayout)

**kivy.uix.recycleboxlayout.RecycleBoxLayout.compute_visible_views**

viewport is in coordinates of the layout manager.

**kivy.uix.recycleboxlayout.RecycleBoxLayout.get_view_index_at**

Return the view index on which position, pos, falls.
pos is in coordinates of the layout manager.

---

## API - [`kivy.uix.recyclegridlayout`](https://kivy.org/doc/stable/api-kivy.uix.recyclegridlayout.html)

**kivy.uix.recyclegridlayout.RecycleGridLayout**

Bases: [`kivy.uix.recyclelayout.RecycleLayout`](https://kivy.org/doc/stable/api-kivy.uix.recyclelayout.html#kivy.uix.recyclelayout.RecycleLayout), [`kivy.uix.gridlayout.GridLayout`](https://kivy.org/doc/stable/api-kivy.uix.gridlayout.html#kivy.uix.gridlayout.GridLayout)

**kivy.uix.recyclegridlayout.RecycleGridLayout.compute_visible_views**

viewport is in coordinates of the layout manager.

**kivy.uix.recyclegridlayout.RecycleGridLayout.get_view_index_at**

Return the view index on which position, pos, falls.
pos is in coordinates of the layout manager.

---

## API - [`kivy.uix.recyclelayout`](https://kivy.org/doc/stable/api-kivy.uix.recyclelayout.html)

**kivy.uix.recyclelayout.RecycleLayout**

Bases: [`kivy.uix.recycleview.layout.RecycleLayoutManagerBehavior`](https://kivy.org/doc/stable/api-kivy.uix.recycleview.layout.html#kivy.uix.recycleview.layout.RecycleLayoutManagerBehavior), [`kivy.uix.layout.Layout`](https://kivy.org/doc/stable/api-kivy.uix.layout.html#kivy.uix.layout.Layout)
RecycleLayout provides the default layout for RecycleViews.

**kivy.uix.recyclelayout.RecycleLayout.default_height**

Default height for items
[`default_height`](https://kivy.org/doc/stable/#kivy.uix.recyclelayout.RecycleLayout.default_height) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
default to 100.

**kivy.uix.recyclelayout.RecycleLayout.default_pos_hint**

Default pos_hint value for items
[`default_pos_hint`](https://kivy.org/doc/stable/#kivy.uix.recyclelayout.RecycleLayout.default_pos_hint) is a [`DictProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.DictProperty) and
defaults to {}.

**kivy.uix.recyclelayout.RecycleLayout.default_size**

size (width, height). Each value can be None.
[`default_size`](https://kivy.org/doc/stable/#kivy.uix.recyclelayout.RecycleLayout.default_size) is an [`ReferenceListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ReferenceListProperty)
to [[`default_width`](https://kivy.org/doc/stable/#kivy.uix.recyclelayout.RecycleLayout.default_width), [`default_height`](https://kivy.org/doc/stable/#kivy.uix.recyclelayout.RecycleLayout.default_height)].

**kivy.uix.recyclelayout.RecycleLayout.default_size_hint**

size (width, height). Each value can be None.
[`default_size_hint`](https://kivy.org/doc/stable/#kivy.uix.recyclelayout.RecycleLayout.default_size_hint) is an
[`ReferenceListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ReferenceListProperty) to
[[`default_size_hint_x`](https://kivy.org/doc/stable/#kivy.uix.recyclelayout.RecycleLayout.default_size_hint_x), [`default_size_hint_y`](https://kivy.org/doc/stable/#kivy.uix.recyclelayout.RecycleLayout.default_size_hint_y)].

**kivy.uix.recyclelayout.RecycleLayout.default_size_hint_max**

Default value for size_hint_max of items
`default_size_max` is a
[`ReferenceListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ReferenceListProperty) to
[[`default_size_hint_x_max`](https://kivy.org/doc/stable/#kivy.uix.recyclelayout.RecycleLayout.default_size_hint_x_max), [`default_size_hint_y_max`](https://kivy.org/doc/stable/#kivy.uix.recyclelayout.RecycleLayout.default_size_hint_y_max)].

**kivy.uix.recyclelayout.RecycleLayout.default_size_hint_min**

Default value for size_hint_min of items
`default_size_min` is a
[`ReferenceListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ReferenceListProperty) to
[[`default_size_hint_x_min`](https://kivy.org/doc/stable/#kivy.uix.recyclelayout.RecycleLayout.default_size_hint_x_min), [`default_size_hint_y_min`](https://kivy.org/doc/stable/#kivy.uix.recyclelayout.RecycleLayout.default_size_hint_y_min)].

**kivy.uix.recyclelayout.RecycleLayout.default_size_hint_x**

Default size_hint_x for items
[`default_size_hint_x`](https://kivy.org/doc/stable/#kivy.uix.recyclelayout.RecycleLayout.default_size_hint_x) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and default to None.

**kivy.uix.recyclelayout.RecycleLayout.default_size_hint_x_max**

Default value for size_hint_x_max of items
`default_pos_hint_x_max` is a
[`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and defaults to None.

**kivy.uix.recyclelayout.RecycleLayout.default_size_hint_x_min**

Default value for size_hint_x_min of items
`default_pos_hint_x_min` is a
[`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and defaults to None.

**kivy.uix.recyclelayout.RecycleLayout.default_size_hint_y**

Default size_hint_y for items
[`default_size_hint_y`](https://kivy.org/doc/stable/#kivy.uix.recyclelayout.RecycleLayout.default_size_hint_y) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and default to None.

**kivy.uix.recyclelayout.RecycleLayout.default_size_hint_y_max**

Default value for size_hint_y_max of items
`default_pos_hint_y_max` is a
[`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and defaults to None.

**kivy.uix.recyclelayout.RecycleLayout.default_size_hint_y_min**

Default value for size_hint_y_min of items
`default_pos_hint_y_min` is a
[`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and defaults to None.

**kivy.uix.recyclelayout.RecycleLayout.default_width**

Default width for items
[`default_width`](https://kivy.org/doc/stable/#kivy.uix.recyclelayout.RecycleLayout.default_width) is a NumericProperty and default to 100

**kivy.uix.recyclelayout.RecycleLayout.do_layout**

This function is called when a layout is called by a trigger.
If you are writing a new Layout subclass, don’t call this function
directly but use `_trigger_layout()` instead.
The function is by default called *before* the next frame, therefore
the layout isn’t updated immediately. Anything depending on the
positions of e.g. children should be scheduled for the next frame.
New in version 1.0.8.

**kivy.uix.recyclelayout.RecycleLayout.initial_height**

Initial height for the items.
[`initial_height`](https://kivy.org/doc/stable/#kivy.uix.recyclelayout.RecycleLayout.initial_height) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 100.

**kivy.uix.recyclelayout.RecycleLayout.initial_size**

Initial size of items
[`initial_size`](https://kivy.org/doc/stable/#kivy.uix.recyclelayout.RecycleLayout.initial_size) is a [`ReferenceListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ReferenceListProperty)
to [[`initial_width`](https://kivy.org/doc/stable/#kivy.uix.recyclelayout.RecycleLayout.initial_width), [`initial_height`](https://kivy.org/doc/stable/#kivy.uix.recyclelayout.RecycleLayout.initial_height)].

**kivy.uix.recyclelayout.RecycleLayout.initial_width**

Initial width for the items.
[`initial_width`](https://kivy.org/doc/stable/#kivy.uix.recyclelayout.RecycleLayout.initial_width) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 100.

**kivy.uix.recyclelayout.RecycleLayout.key_pos_hint**

If set, which key in the dict should be used to set the pos_hint of
items.
[`key_pos_hint`](https://kivy.org/doc/stable/#kivy.uix.recyclelayout.RecycleLayout.key_pos_hint) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to None.

**kivy.uix.recyclelayout.RecycleLayout.key_size**

If set, which key in the dict should be used to set the size property of
the item.
[`key_size`](https://kivy.org/doc/stable/#kivy.uix.recyclelayout.RecycleLayout.key_size) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults
to None.

**kivy.uix.recyclelayout.RecycleLayout.key_size_hint**

If set, which key in the dict should be used to set the size_hint
property of the item.
[`key_size_hint`](https://kivy.org/doc/stable/#kivy.uix.recyclelayout.RecycleLayout.key_size_hint) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to None.

**kivy.uix.recyclelayout.RecycleLayout.key_size_hint_max**

If set, which key in the dict should be used to set the size_hint_max
property of the item.
[`key_size_hint_max`](https://kivy.org/doc/stable/#kivy.uix.recyclelayout.RecycleLayout.key_size_hint_max) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to None.

**kivy.uix.recyclelayout.RecycleLayout.key_size_hint_min**

If set, which key in the dict should be used to set the size_hint_min
property of the item.
[`key_size_hint_min`](https://kivy.org/doc/stable/#kivy.uix.recyclelayout.RecycleLayout.key_size_hint_min) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to None.

**kivy.uix.recyclelayout.RecycleLayout.refresh_view_layout**

See :meth:`~kivy.uix.recycleview.views.RecycleDataAdapter.refresh_view_layout.

**kivy.uix.recyclelayout.RecycleLayout.set_visible_views**

viewport is in coordinates of the layout manager.

---

## API - [`kivy.uix.recycleview`](https://kivy.org/doc/stable/api-kivy.uix.recycleview.html)

**kivy.uix.recycleview.RecycleView**

Bases: [`kivy.uix.recycleview.RecycleViewBehavior`](https://kivy.org/doc/stable/#kivy.uix.recycleview.RecycleViewBehavior), [`kivy.uix.scrollview.ScrollView`](https://kivy.org/doc/stable/api-kivy.uix.scrollview.html#kivy.uix.scrollview.ScrollView)
RecycleView is a flexible view for providing a limited window
into a large data set.
See the module documentation for more information.

**kivy.uix.recycleview.RecycleView.add_widget**

Add a new widget as a child of this widget.

**kivy.uix.recycleview.RecycleView.data**

The data used by the current view adapter. This is a list of dicts whose
keys map to the corresponding property names of the
[`viewclass`](https://kivy.org/doc/stable/#kivy.uix.recycleview.RecycleView.viewclass).
data is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) that gets and sets the
data used to generate the views.

**kivy.uix.recycleview.RecycleView.key_viewclass**

key_viewclass is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) that gets and
sets the key viewclass for the current
`layout_manager`.

**kivy.uix.recycleview.RecycleView.remove_widget**

Remove a widget from the children of this widget.

**kivy.uix.recycleview.RecycleView.viewclass**

The viewclass used by the current layout_manager.
viewclass is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) that gets and sets
the class used to generate the individual items presented in the view.

**kivy.uix.recycleview.RecycleViewBehavior**

Bases: `builtins.object`
RecycleViewBehavior provides a behavioral model upon which the
[`RecycleView`](https://kivy.org/doc/stable/#kivy.uix.recycleview.RecycleView) is built. Together, they offer an extensible and
flexible way to produce views with limited windows over large data sets.
See the module documentation for more information.

**kivy.uix.recycleview.RecycleViewBehavior.data_model**

The Data model responsible for maintaining the data set.
data_model is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) that gets and sets
the current data model.

**kivy.uix.recycleview.RecycleViewBehavior.layout_manager**

The Layout manager responsible for positioning views within the
[`RecycleView`](https://kivy.org/doc/stable/#kivy.uix.recycleview.RecycleView).
layout_manager is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) that gets
and sets the layout_manger.

**kivy.uix.recycleview.RecycleViewBehavior.refresh_from_data**

This should be called when data changes. Data changes typically
indicate that everything should be recomputed since the source data
changed.
This method is automatically bound to the
`on_data_changed` method of the
`RecycleDataModelBehavior` class and
therefore responds to and accepts the keyword arguments of that event.
It can be called manually to trigger an update.

**kivy.uix.recycleview.RecycleViewBehavior.refresh_from_layout**

This should be called when the layout changes or needs to change. It is
typically called when a layout parameter has changed and therefore the
layout needs to be recomputed.

**kivy.uix.recycleview.RecycleViewBehavior.refresh_from_viewport**

This should be called when the viewport changes and the displayed data
must be updated. Neither the data nor the layout will be recomputed.

**kivy.uix.recycleview.RecycleViewBehavior.view_adapter**

The adapter responsible for providing views that represent items in a data
set.
view_adapter is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) that gets and
sets the current view adapter.

---

## API - [`kivy.uix.recycleview.datamodel`](https://kivy.org/doc/stable/api-kivy.uix.recycleview.datamodel.html)

**kivy.uix.recycleview.datamodel.RecycleDataModel**

Bases: [`kivy.uix.recycleview.datamodel.RecycleDataModelBehavior`](https://kivy.org/doc/stable/#kivy.uix.recycleview.datamodel.RecycleDataModelBehavior), [`kivy.event.EventDispatcher`](https://kivy.org/doc/stable/api-kivy.event.html#kivy.event.EventDispatcher)
An implementation of [`RecycleDataModelBehavior`](https://kivy.org/doc/stable/#kivy.uix.recycleview.datamodel.RecycleDataModelBehavior) that keeps the
data in a indexable list. See [`data`](https://kivy.org/doc/stable/#kivy.uix.recycleview.datamodel.RecycleDataModel.data).
When data changes this class currently dispatches on_data_changed with
one of the following additional keyword arguments.

**kivy.uix.recycleview.datamodel.RecycleDataModel.attach_recycleview**

Associates a
[`RecycleViewBehavior`](https://kivy.org/doc/stable/api-kivy.uix.recycleview.html#kivy.uix.recycleview.RecycleViewBehavior) with
this data model.

**kivy.uix.recycleview.datamodel.RecycleDataModel.data**

Stores the model’s data using a list.
The data for a item at index i can also be accessed with
[`RecycleDataModel`](https://kivy.org/doc/stable/#kivy.uix.recycleview.datamodel.RecycleDataModel) [i].

**kivy.uix.recycleview.datamodel.RecycleDataModel.detach_recycleview**

Removes the
[`RecycleViewBehavior`](https://kivy.org/doc/stable/api-kivy.uix.recycleview.html#kivy.uix.recycleview.RecycleViewBehavior)
associated with this data model.

**kivy.uix.recycleview.datamodel.RecycleDataModel.observable_dict**

A dictionary instance, which when modified will trigger a data and
consequently an on_data_changed dispatch.

**kivy.uix.recycleview.datamodel.RecycleDataModelBehavior**

Bases: `builtins.object`
[`RecycleDataModelBehavior`](https://kivy.org/doc/stable/#kivy.uix.recycleview.datamodel.RecycleDataModelBehavior) is the base class for the models
that describes and provides the data for the
[`RecycleViewBehavior`](https://kivy.org/doc/stable/api-kivy.uix.recycleview.html#kivy.uix.recycleview.RecycleViewBehavior).

**kivy.uix.recycleview.datamodel.RecycleDataModelBehavior.attach_recycleview**

Associates a
[`RecycleViewBehavior`](https://kivy.org/doc/stable/api-kivy.uix.recycleview.html#kivy.uix.recycleview.RecycleViewBehavior) with
this data model.

**kivy.uix.recycleview.datamodel.RecycleDataModelBehavior.detach_recycleview**

Removes the
[`RecycleViewBehavior`](https://kivy.org/doc/stable/api-kivy.uix.recycleview.html#kivy.uix.recycleview.RecycleViewBehavior)
associated with this data model.

**kivy.uix.recycleview.datamodel.RecycleDataModelBehavior.recycleview**

The
[`RecycleViewBehavior`](https://kivy.org/doc/stable/api-kivy.uix.recycleview.html#kivy.uix.recycleview.RecycleViewBehavior) instance
associated with this data model.

---

## API - [`kivy.uix.recycleview.layout`](https://kivy.org/doc/stable/api-kivy.uix.recycleview.layout.html)

**kivy.uix.recycleview.layout.LayoutChangeException**

Bases: `Exception`

**kivy.uix.recycleview.layout.LayoutSelectionBehavior**

Bases: [`kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.compoundselection.html#kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior)
The [`LayoutSelectionBehavior`](https://kivy.org/doc/stable/#kivy.uix.recycleview.layout.LayoutSelectionBehavior) can be combined with
[`RecycleLayoutManagerBehavior`](https://kivy.org/doc/stable/#kivy.uix.recycleview.layout.RecycleLayoutManagerBehavior) to allow its derived classes
selection behaviors similarly to how
[`CompoundSelectionBehavior`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.compoundselection.html#kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior)
can be used to add selection behaviors to normal layout.
[`RecycleLayoutManagerBehavior`](https://kivy.org/doc/stable/#kivy.uix.recycleview.layout.RecycleLayoutManagerBehavior) manages its children
differently than normal layouts or widgets so this class adapts
[`CompoundSelectionBehavior`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.compoundselection.html#kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior)
based selection to work with [`RecycleLayoutManagerBehavior`](https://kivy.org/doc/stable/#kivy.uix.recycleview.layout.RecycleLayoutManagerBehavior) as well.
Similarly to
[`CompoundSelectionBehavior`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.compoundselection.html#kivy.uix.behaviors.compoundselection.CompoundSelectionBehavior),
one can select using the keyboard or touch, which calls [`select_node()`](https://kivy.org/doc/stable/#kivy.uix.recycleview.layout.LayoutSelectionBehavior.select_node)
or [`deselect_node()`](https://kivy.org/doc/stable/#kivy.uix.recycleview.layout.LayoutSelectionBehavior.deselect_node), or one can call these methods directly. When a
item is selected or deselected [`apply_selection()`](https://kivy.org/doc/stable/#kivy.uix.recycleview.layout.LayoutSelectionBehavior.apply_selection) is called. See
[`apply_selection()`](https://kivy.org/doc/stable/#kivy.uix.recycleview.layout.LayoutSelectionBehavior.apply_selection).

**kivy.uix.recycleview.layout.LayoutSelectionBehavior.apply_selection**

Applies the selection to the view. This is called internally when
a view is displayed and it needs to be shown as selected or as not
selected.
It is called when [`select_node()`](https://kivy.org/doc/stable/#kivy.uix.recycleview.layout.LayoutSelectionBehavior.select_node) or [`deselect_node()`](https://kivy.org/doc/stable/#kivy.uix.recycleview.layout.LayoutSelectionBehavior.deselect_node) is
called or when a view needs to be refreshed. Its function is purely to
update the view to reflect the selection state. So the function may be
called multiple times even if the selection state may not have changed.
If the view is a instance of
[`RecycleDataViewBehavior`](https://kivy.org/doc/stable/api-kivy.uix.recycleview.views.html#kivy.uix.recycleview.views.RecycleDataViewBehavior), its
`apply_selection()` method will be called every time the view needs to refresh
the selection state. Otherwise, the this method is responsible
for applying the selection.

**kivy.uix.recycleview.layout.LayoutSelectionBehavior.deselect_node**

Deselects a possibly selected node.
It is called by the controller when it deselects a node and can also
be called from the outside to deselect a node directly. The derived
widget should overwrite this method and change the node to its
unselected state when this is called

**kivy.uix.recycleview.layout.LayoutSelectionBehavior.get_index_of_node**

(internal) Returns the index of the node within the
selectable_nodes returned by [`get_selectable_nodes()`](https://kivy.org/doc/stable/#kivy.uix.recycleview.layout.LayoutSelectionBehavior.get_selectable_nodes).

**kivy.uix.recycleview.layout.LayoutSelectionBehavior.get_selectable_nodes**

(internal) Returns a list of the nodes that can be selected. It can
be overwritten by the derived widget to return the correct list.
This list is used to determine which nodes to select with group
selection. E.g. the last element in the list will be selected when
home is pressed, pagedown will move (or add to, if shift is held) the
selection from the current position by negative `page_count`
nodes starting from the position of the currently selected node in
this list and so on. Still, nodes can be selected even if they are not
in this list.

Defaults to returning [`children`](https://kivy.org/doc/stable/api-kivy.uix.widget.html#kivy.uix.widget.Widget.children).

**kivy.uix.recycleview.layout.LayoutSelectionBehavior.goto_node**

(internal) Used by the controller to get the node at the position
indicated by key. The key can be keyboard inputs, e.g. pageup,
or scroll inputs from the mouse scroll wheel, e.g. scrollup.
‘last_node’ is the last node selected and is used to find the resulting
node. For example, if the key is up, the returned node is one node
up from the last node.
It can be overwritten by the derived widget.

**kivy.uix.recycleview.layout.LayoutSelectionBehavior.key_selection**

The key used to check whether a view of a data item can be selected
with touch or the keyboard.
[`key_selection`](https://kivy.org/doc/stable/#kivy.uix.recycleview.layout.LayoutSelectionBehavior.key_selection) is the key in data, which if present and `True`
will enable selection for this item from the keyboard or with a touch.
When None, the default, not item will be selectable.
[`key_selection`](https://kivy.org/doc/stable/#kivy.uix.recycleview.layout.LayoutSelectionBehavior.key_selection) is a `StringProperty` and defaults to None.

**kivy.uix.recycleview.layout.LayoutSelectionBehavior.select_node**

Selects a node.
It is called by the controller when it selects a node and can be
called from the outside to select a node directly. The derived widget
should overwrite this method and change the node state to selected
when called.

**kivy.uix.recycleview.layout.RecycleLayoutManagerBehavior**

Bases: `builtins.object`
A RecycleLayoutManagerBehavior is responsible for positioning views into
the `RecycleView.data` within a `RecycleView`. It adds new
views into the data when it becomes visible to the user, and removes them
when they leave the visible area.

**kivy.uix.recycleview.layout.RecycleLayoutManagerBehavior.compute_visible_views**

viewport is in coordinates of the layout manager.

**kivy.uix.recycleview.layout.RecycleLayoutManagerBehavior.get_view_index_at**

Return the view index on which position, pos, falls.
pos is in coordinates of the layout manager.

**kivy.uix.recycleview.layout.RecycleLayoutManagerBehavior.goto_view**

Moves the views so that the view corresponding to index is
visible.

**kivy.uix.recycleview.layout.RecycleLayoutManagerBehavior.key_viewclass**

See `RecyclerView.key_viewclass`.

**kivy.uix.recycleview.layout.RecycleLayoutManagerBehavior.refresh_view_layout**

See :meth:`~kivy.uix.recycleview.views.RecycleDataAdapter.refresh_view_layout.

**kivy.uix.recycleview.layout.RecycleLayoutManagerBehavior.set_visible_views**

viewport is in coordinates of the layout manager.

**kivy.uix.recycleview.layout.RecycleLayoutManagerBehavior.viewclass**

See `RecyclerView.viewclass`.

---

## API - [`kivy.uix.recycleview.views`](https://kivy.org/doc/stable/api-kivy.uix.recycleview.views.html)

**kivy.uix.recycleview.views.RecycleDataAdapter**

Bases: [`kivy.event.EventDispatcher`](https://kivy.org/doc/stable/api-kivy.event.html#kivy.event.EventDispatcher)
The class that converts data to a view.
— Internal details —
A view can have 3 states.
It can be completely in sync with the data, which
occurs when the view is displayed. These are stored in `views`.
It can be dirty, which occurs when the view is in sync with the data,
except for the size/pos parameters which is controlled by the layout.
This occurs when the view is not currently displayed but the data has
not changed. These views are stored in `dirty_views`.
Finally the view can be dead which occurs when the data changes and
the view was not updated or when a view is just created. Such views
are typically added to the internal cache.
Typically what happens is that the layout manager lays out the data
and then asks for views, using [`set_visible_views()`](https://kivy.org/doc/stable/#kivy.uix.recycleview.views.RecycleDataAdapter.set_visible_views), for some specific
data items that it displays.
These views are gotten from the current views, dirty or global cache. Then
depending on the view state [`refresh_view_attrs()`](https://kivy.org/doc/stable/#kivy.uix.recycleview.views.RecycleDataAdapter.refresh_view_attrs) is called to bring
the view up to date with the data (except for sizing parameters). Finally,
the layout manager gets these views, updates their size and displays them.

**kivy.uix.recycleview.views.RecycleDataAdapter.attach_recycleview**

Associates a [`RecycleViewBehavior`](https://kivy.org/doc/stable/api-kivy.uix.recycleview.html#kivy.uix.recycleview.RecycleViewBehavior)
with this instance. It is stored in [`recycleview`](https://kivy.org/doc/stable/#kivy.uix.recycleview.views.RecycleDataAdapter.recycleview).

**kivy.uix.recycleview.views.RecycleDataAdapter.create_view**

(internal) Creates and initializes the view for the data at index.
The returned view is synced with the data, except for the pos/size
information.

**kivy.uix.recycleview.views.RecycleDataAdapter.detach_recycleview**

Removes the [`RecycleViewBehavior`](https://kivy.org/doc/stable/api-kivy.uix.recycleview.html#kivy.uix.recycleview.RecycleViewBehavior)
associated with this instance and clears [`recycleview`](https://kivy.org/doc/stable/#kivy.uix.recycleview.views.RecycleDataAdapter.recycleview).

**kivy.uix.recycleview.views.RecycleDataAdapter.get_view**

(internal) Returns a view instance for the data at index
It looks through the various caches and finally creates a view if it
doesn’t exist. The returned view is synced with the data, except for
the pos/size information.
If found in the cache it’s removed from the source
before returning. It doesn’t check the current views.

**kivy.uix.recycleview.views.RecycleDataAdapter.get_visible_view**

Returns the currently visible view associated with `index`.
If no view is currently displayed for `index` it returns `None`.

**kivy.uix.recycleview.views.RecycleDataAdapter.invalidate**

Moves all the current views into the global cache.
As opposed to making a view dirty where the view is in sync with the
data except for sizing information, this will completely disconnect the
view from the data, as it is assumed the data has gone out of sync with
the view.
This is typically called when the data changes.

**kivy.uix.recycleview.views.RecycleDataAdapter.make_view_dirty**

(internal) Used to flag this view as dirty, ready to be used for
others. See [`make_views_dirty()`](https://kivy.org/doc/stable/#kivy.uix.recycleview.views.RecycleDataAdapter.make_views_dirty).

**kivy.uix.recycleview.views.RecycleDataAdapter.make_views_dirty**

Makes all the current views dirty.
Dirty views are still in sync with the corresponding data. However, the
size information may go out of sync. Therefore a dirty view can be
reused by the same index by just updating the sizing information.
Once the underlying data of this index changes, the view should be
removed from the dirty views and moved to the global cache with
[`invalidate()`](https://kivy.org/doc/stable/#kivy.uix.recycleview.views.RecycleDataAdapter.invalidate).
This is typically called when the layout manager needs to re-layout all
the data.

**kivy.uix.recycleview.views.RecycleDataAdapter.recycleview**

The [`RecycleViewBehavior`](https://kivy.org/doc/stable/api-kivy.uix.recycleview.html#kivy.uix.recycleview.RecycleViewBehavior) associated
with this instance.

**kivy.uix.recycleview.views.RecycleDataAdapter.refresh_view_attrs**

(internal) Syncs the view and brings it up to date with the data.
This method calls [`RecycleDataViewBehavior.refresh_view_attrs()`](https://kivy.org/doc/stable/#kivy.uix.recycleview.views.RecycleDataViewBehavior.refresh_view_attrs)
if the view inherits from [`RecycleDataViewBehavior`](https://kivy.org/doc/stable/#kivy.uix.recycleview.views.RecycleDataViewBehavior). See that
method for more details.

**kivy.uix.recycleview.views.RecycleDataAdapter.refresh_view_layout**

Updates the sizing information of the view.
viewport is in coordinates of the layout manager.
This method calls [`RecycleDataViewBehavior.refresh_view_attrs()`](https://kivy.org/doc/stable/#kivy.uix.recycleview.views.RecycleDataViewBehavior.refresh_view_attrs)
if the view inherits from [`RecycleDataViewBehavior`](https://kivy.org/doc/stable/#kivy.uix.recycleview.views.RecycleDataViewBehavior). See that
method for more details.

**kivy.uix.recycleview.views.RecycleDataAdapter.set_visible_views**

Gets a 3-tuple of the new, remaining, and old views for the current
viewport.
The new views are synced to the data except for the size/pos
properties.
The old views need to be removed from the layout, and the new views
added.
The new views are not necessarily *new*, but are all the currently
visible views.

**kivy.uix.recycleview.views.RecycleDataViewBehavior**

Bases: `builtins.object`
A optional base class for data views (`RecycleView`.viewclass).
If a view inherits from this class, the class’s functions will be called
when the view needs to be updated due to a data change or layout update.

**kivy.uix.recycleview.views.RecycleDataViewBehavior.refresh_view_attrs**

Called by the `RecycleAdapter` when the view is initially
populated with the values from the data dictionary for this item.
Any pos or size info should be removed because they are set
subsequently with [`refresh_view_layout`](https://kivy.org/doc/stable/#kivy.uix.recycleview.views.RecycleDataViewBehavior.refresh_view_layout).

**kivy.uix.recycleview.views.RecycleDataViewBehavior.refresh_view_layout**

Called when the view’s size is updated by the layout manager,
`RecycleLayoutManagerBehavior`.

**kivy.uix.recycleview.views.RecycleKVIDsDataViewBehavior**

Bases: [`kivy.uix.recycleview.views.RecycleDataViewBehavior`](https://kivy.org/doc/stable/#kivy.uix.recycleview.views.RecycleDataViewBehavior)
Similar to [`RecycleDataViewBehavior`](https://kivy.org/doc/stable/#kivy.uix.recycleview.views.RecycleDataViewBehavior), except that the data keys
can signify properties of an object named with an id in the root KV rule.
E.g. given a KV rule:

Then setting the data list with
`rv.data = [{'name.text': 'Kivy user', 'value.text': '12'}]` would
automatically set the corresponding labels.
So, if the key doesn’t have a period, the named property of the root widget
will be set to the corresponding value. If there is a period, the named
property of the widget with the id listed before the period will be set to
the corresponding value.
New in version 2.0.0.

**kivy.uix.recycleview.views.RecycleKVIDsDataViewBehavior.refresh_view_attrs**

Called by the `RecycleAdapter` when the view is initially
populated with the values from the data dictionary for this item.
Any pos or size info should be removed because they are set
subsequently with `refresh_view_layout`.

---

## API - [`kivy.uix.relativelayout`](https://kivy.org/doc/stable/api-kivy.uix.relativelayout.html)

**kivy.uix.relativelayout.RelativeLayout**

Bases: [`kivy.uix.floatlayout.FloatLayout`](https://kivy.org/doc/stable/api-kivy.uix.floatlayout.html#kivy.uix.floatlayout.FloatLayout)
RelativeLayout class, see module documentation for more information.

**kivy.uix.relativelayout.RelativeLayout.do_layout**

This function is called when a layout is called by a trigger.
If you are writing a new Layout subclass, don’t call this function
directly but use `_trigger_layout()` instead.
The function is by default called *before* the next frame, therefore
the layout isn’t updated immediately. Anything depending on the
positions of e.g. children should be scheduled for the next frame.
New in version 1.0.8.

**kivy.uix.relativelayout.RelativeLayout.on_motion**

Called when a motion event is received.

New in version 2.1.0.

**kivy.uix.relativelayout.RelativeLayout.on_touch_down**

Receive a touch down event.

**kivy.uix.relativelayout.RelativeLayout.on_touch_move**

Receive a touch move event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivy.org/doc/stable/#kivy.uix.relativelayout.RelativeLayout.on_touch_down) for more information.

**kivy.uix.relativelayout.RelativeLayout.on_touch_up**

Receive a touch up event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivy.org/doc/stable/#kivy.uix.relativelayout.RelativeLayout.on_touch_down) for more information.

**kivy.uix.relativelayout.RelativeLayout.to_local**

Transform parent coordinates to local (current widget) coordinates.
See [`relativelayout`](https://kivy.org/doc/stable/#module-kivy.uix.relativelayout) for details on the coordinate
systems.

**kivy.uix.relativelayout.RelativeLayout.to_parent**

Transform local (current widget) coordinates to parent coordinates.
See [`relativelayout`](https://kivy.org/doc/stable/#module-kivy.uix.relativelayout) for details on the coordinate
systems.

---

## API - [`kivy.uix.rst`](https://kivy.org/doc/stable/api-kivy.uix.rst.html)

**kivy.uix.rst.RstDocument**

Bases: [`kivy.uix.scrollview.ScrollView`](https://kivy.org/doc/stable/api-kivy.uix.scrollview.html#kivy.uix.scrollview.ScrollView)
Base widget used to store an Rst document. See module documentation for
more information.

**kivy.uix.rst.RstDocument.background_color**

Specifies the background_color to be used for the RstDocument.
New in version 1.8.0.
[`background_color`](https://kivy.org/doc/stable/#kivy.uix.rst.RstDocument.background_color) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty)
for colors[‘background’].

**kivy.uix.rst.RstDocument.base_font_size**

Font size for the biggest title, 31 by default. All other font sizes are
derived from this.
New in version 1.8.0.

**kivy.uix.rst.RstDocument.colors**

Dictionary of all the colors used in the RST rendering.

[`colors`](https://kivy.org/doc/stable/#kivy.uix.rst.RstDocument.colors) is a [`DictProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.DictProperty).

**kivy.uix.rst.RstDocument.document_root**

Root path where :doc: will search for rst documents. If no path is
given, it will use the directory of the first loaded source file.
[`document_root`](https://kivy.org/doc/stable/#kivy.uix.rst.RstDocument.document_root) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to None.

**kivy.uix.rst.RstDocument.goto**

Scroll to the reference. If it’s not found, nothing will be done.
For this text:

You can do:

New in version 1.3.0.

**kivy.uix.rst.RstDocument.preload**

Preload a rst file to get its toctree and its title.
The result will be stored in [`toctrees`](https://kivy.org/doc/stable/#kivy.uix.rst.RstDocument.toctrees) with the `filename` as
key.

**kivy.uix.rst.RstDocument.render**

Force document rendering.

**kivy.uix.rst.RstDocument.resolve_path**

Get the path for this filename. If the filename doesn’t exist,
it returns the document_root + filename.

**kivy.uix.rst.RstDocument.show_errors**

Indicate whether RST parsers errors should be shown on the screen
or not.
[`show_errors`](https://kivy.org/doc/stable/#kivy.uix.rst.RstDocument.show_errors) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to False.

**kivy.uix.rst.RstDocument.source**

Filename of the RST document.
[`source`](https://kivy.org/doc/stable/#kivy.uix.rst.RstDocument.source) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to None.

**kivy.uix.rst.RstDocument.source_encoding**

Encoding to be used for the [`source`](https://kivy.org/doc/stable/#kivy.uix.rst.RstDocument.source) file.
[`source_encoding`](https://kivy.org/doc/stable/#kivy.uix.rst.RstDocument.source_encoding) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to utf-8.

**kivy.uix.rst.RstDocument.source_error**

Error handling to be used while encoding the [`source`](https://kivy.org/doc/stable/#kivy.uix.rst.RstDocument.source) file.
[`source_error`](https://kivy.org/doc/stable/#kivy.uix.rst.RstDocument.source_error) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty) and
defaults to strict. Can be one of ‘strict’, ‘ignore’, ‘replace’,
‘xmlcharrefreplace’ or ‘backslashreplac’.

**kivy.uix.rst.RstDocument.text**

RST markup text of the document.
[`text`](https://kivy.org/doc/stable/#kivy.uix.rst.RstDocument.text) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults to
None.

**kivy.uix.rst.RstDocument.title**

Title of the current document.
[`title`](https://kivy.org/doc/stable/#kivy.uix.rst.RstDocument.title) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults to
‘’. It is read-only.

**kivy.uix.rst.RstDocument.toctrees**

Toctree of all loaded or preloaded documents. This dictionary is filled
when a rst document is explicitly loaded or where [`preload()`](https://kivy.org/doc/stable/#kivy.uix.rst.RstDocument.preload) has been
called.
If the document has no filename, e.g. when the document is loaded from a
text file, the key will be ‘’.
[`toctrees`](https://kivy.org/doc/stable/#kivy.uix.rst.RstDocument.toctrees) is a [`DictProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.DictProperty) and defaults
to {}.

**kivy.uix.rst.RstDocument.underline_color**

underline color of the titles, expressed in html color notation
[`underline_color`](https://kivy.org/doc/stable/#kivy.uix.rst.RstDocument.underline_color) is a
[`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults to ‘204a9699’.

---

## API - [`kivy.uix.sandbox`](https://kivy.org/doc/stable/api-kivy.uix.sandbox.html)

**kivy.uix.sandbox.Sandbox**

Bases: [`kivy.uix.floatlayout.FloatLayout`](https://kivy.org/doc/stable/api-kivy.uix.floatlayout.html#kivy.uix.floatlayout.FloatLayout)
Sandbox widget, used to trap all the exceptions raised by child
widgets.

**kivy.uix.sandbox.Sandbox.add_widget**

Add a new widget as a child of this widget.

**kivy.uix.sandbox.Sandbox.clear_widgets**

Remove all (or the specified) `children` of this widget.
If the ‘children’ argument is specified, it should be a list (or
filtered list) of children of the current widget.
Changed in version 1.8.0:The children argument can be used to specify the children you
want to remove.
Changed in version 2.1.0:Specifying an empty `children` list leaves the widgets unchanged.
Previously it was treated like `None` and all children were
removed.

**kivy.uix.sandbox.Sandbox.on_context_created**

Override this method in order to load your kv file or do anything
else with the newly created context.

**kivy.uix.sandbox.Sandbox.on_exception**

Override this method in order to catch all the exceptions from
children.
If you return True, it will not reraise the exception.
If you return False, the exception will be raised to the parent.

**kivy.uix.sandbox.Sandbox.on_motion**

Called when a motion event is received.

New in version 2.1.0.

**kivy.uix.sandbox.Sandbox.on_touch_down**

Receive a touch down event.

**kivy.uix.sandbox.Sandbox.on_touch_move**

Receive a touch move event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivy.org/doc/stable/#kivy.uix.sandbox.Sandbox.on_touch_down) for more information.

**kivy.uix.sandbox.Sandbox.on_touch_up**

Receive a touch up event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivy.org/doc/stable/#kivy.uix.sandbox.Sandbox.on_touch_down) for more information.

**kivy.uix.sandbox.Sandbox.remove_widget**

Remove a widget from the children of this widget.

---

## API - [`kivy.uix.scatter`](https://kivy.org/doc/stable/api-kivy.uix.scatter.html)

**kivy.uix.scatter.Scatter**

Bases: [`kivy.uix.widget.Widget`](https://kivy.org/doc/stable/api-kivy.uix.widget.html#kivy.uix.widget.Widget)
Scatter class. See module documentation for more information.

Changed in version 1.9.0:Event on_bring_to_front added.
Changed in version 1.8.0:Event on_transform_with_touch added.

**kivy.uix.scatter.Scatter.apply_transform**

Transforms the scatter by applying the “trans” transformation
matrix (on top of its current transformation state). The resultant
matrix can be found in the [`transform`](https://kivy.org/doc/stable/#kivy.uix.scatter.Scatter.transform) property.

Usage example:

**kivy.uix.scatter.Scatter.auto_bring_to_front**

If True, the widget will be automatically pushed on the top of parent
widget list for drawing.
[`auto_bring_to_front`](https://kivy.org/doc/stable/#kivy.uix.scatter.Scatter.auto_bring_to_front) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to True.

**kivy.uix.scatter.Scatter.bbox**

Bounding box of the widget in parent space:

[`bbox`](https://kivy.org/doc/stable/#kivy.uix.scatter.Scatter.bbox) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty).

**kivy.uix.scatter.Scatter.center**

Center position of the widget.
[`center`](https://kivy.org/doc/stable/#kivy.uix.scatter.Scatter.center) is a [`ReferenceListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ReferenceListProperty) of
([`center_x`](https://kivy.org/doc/stable/#kivy.uix.scatter.Scatter.center_x), [`center_y`](https://kivy.org/doc/stable/#kivy.uix.scatter.Scatter.center_y)) properties.

**kivy.uix.scatter.Scatter.center_x**

X center position of the widget.
[`center_x`](https://kivy.org/doc/stable/#kivy.uix.scatter.Scatter.center_x) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) of
([`x`](https://kivy.org/doc/stable/#kivy.uix.scatter.Scatter.x) + `width` / 2.).

**kivy.uix.scatter.Scatter.center_y**

Y center position of the widget.
[`center_y`](https://kivy.org/doc/stable/#kivy.uix.scatter.Scatter.center_y) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) of
([`y`](https://kivy.org/doc/stable/#kivy.uix.scatter.Scatter.y) + `height` / 2.).

**kivy.uix.scatter.Scatter.collide_point**

Check if a point (x, y) is inside the widget’s axis aligned bounding
box.

**kivy.uix.scatter.Scatter.do_collide_after_children**

If True, the collision detection for limiting the touch inside the
scatter will be done after dispaching the touch to the children.
You can put children outside the bounding box of the scatter and still be
able to touch them.
[`do_collide_after_children`](https://kivy.org/doc/stable/#kivy.uix.scatter.Scatter.do_collide_after_children) is a
[`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and defaults to False.
New in version 1.3.0.

**kivy.uix.scatter.Scatter.do_rotation**

Allow rotation.
[`do_rotation`](https://kivy.org/doc/stable/#kivy.uix.scatter.Scatter.do_rotation) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to True.

**kivy.uix.scatter.Scatter.do_scale**

Allow scaling.
[`do_scale`](https://kivy.org/doc/stable/#kivy.uix.scatter.Scatter.do_scale) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to True.

**kivy.uix.scatter.Scatter.do_translation**

Allow translation on the X or Y axis.
[`do_translation`](https://kivy.org/doc/stable/#kivy.uix.scatter.Scatter.do_translation) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) of
([`do_translation_x`](https://kivy.org/doc/stable/#kivy.uix.scatter.Scatter.do_translation_x) + [`do_translation_y`](https://kivy.org/doc/stable/#kivy.uix.scatter.Scatter.do_translation_y))

**kivy.uix.scatter.Scatter.do_translation_x**

Allow translation on the X axis.
[`do_translation_x`](https://kivy.org/doc/stable/#kivy.uix.scatter.Scatter.do_translation_x) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to True.

**kivy.uix.scatter.Scatter.do_translation_y**

Allow translation on Y axis.
[`do_translation_y`](https://kivy.org/doc/stable/#kivy.uix.scatter.Scatter.do_translation_y) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to True.

**kivy.uix.scatter.Scatter.on_bring_to_front**

Called when a touch event causes the scatter to be brought to the
front of the parent (only if [`auto_bring_to_front`](https://kivy.org/doc/stable/#kivy.uix.scatter.Scatter.auto_bring_to_front) is True)

New in version 1.9.0.

**kivy.uix.scatter.Scatter.on_motion**

Called when a motion event is received.

New in version 2.1.0.

**kivy.uix.scatter.Scatter.on_touch_down**

Receive a touch down event.

**kivy.uix.scatter.Scatter.on_touch_move**

Receive a touch move event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivy.org/doc/stable/#kivy.uix.scatter.Scatter.on_touch_down) for more information.

**kivy.uix.scatter.Scatter.on_touch_up**

Receive a touch up event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivy.org/doc/stable/#kivy.uix.scatter.Scatter.on_touch_down) for more information.

**kivy.uix.scatter.Scatter.on_transform_with_touch**

Called when a touch event has transformed the scatter widget.
By default this does nothing, but can be overridden by derived
classes that need to react to transformations caused by user
input.

New in version 1.8.0.

**kivy.uix.scatter.Scatter.pos**

Position of the widget.
[`pos`](https://kivy.org/doc/stable/#kivy.uix.scatter.Scatter.pos) is a [`ReferenceListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ReferenceListProperty) of
([`x`](https://kivy.org/doc/stable/#kivy.uix.scatter.Scatter.x), [`y`](https://kivy.org/doc/stable/#kivy.uix.scatter.Scatter.y)) properties.

**kivy.uix.scatter.Scatter.right**

Right position of the widget.
[`right`](https://kivy.org/doc/stable/#kivy.uix.scatter.Scatter.right) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) of
([`x`](https://kivy.org/doc/stable/#kivy.uix.scatter.Scatter.x) + `width`).

**kivy.uix.scatter.Scatter.rotation**

Rotation value of the scatter in degrees moving in a counterclockwise
direction.
[`rotation`](https://kivy.org/doc/stable/#kivy.uix.scatter.Scatter.rotation) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) and defaults
to 0.0.

**kivy.uix.scatter.Scatter.scale**

Scale value of the scatter.
[`scale`](https://kivy.org/doc/stable/#kivy.uix.scatter.Scatter.scale) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) and defaults to
1.0.

**kivy.uix.scatter.Scatter.scale_max**

Maximum scaling factor allowed.
[`scale_max`](https://kivy.org/doc/stable/#kivy.uix.scatter.Scatter.scale_max) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 1e20.

**kivy.uix.scatter.Scatter.scale_min**

Minimum scaling factor allowed.
[`scale_min`](https://kivy.org/doc/stable/#kivy.uix.scatter.Scatter.scale_min) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0.01.

**kivy.uix.scatter.Scatter.to_local**

Transform parent coordinates to local (current widget) coordinates.
See [`relativelayout`](https://kivy.org/doc/stable/api-kivy.uix.relativelayout.html#module-kivy.uix.relativelayout) for details on the coordinate
systems.

**kivy.uix.scatter.Scatter.to_parent**

Transform local (current widget) coordinates to parent coordinates.
See [`relativelayout`](https://kivy.org/doc/stable/api-kivy.uix.relativelayout.html#module-kivy.uix.relativelayout) for details on the coordinate
systems.

**kivy.uix.scatter.Scatter.top**

Top position of the widget.
[`top`](https://kivy.org/doc/stable/#kivy.uix.scatter.Scatter.top) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) of
([`y`](https://kivy.org/doc/stable/#kivy.uix.scatter.Scatter.y) + `height`).

**kivy.uix.scatter.Scatter.transform**

Transformation matrix.
[`transform`](https://kivy.org/doc/stable/#kivy.uix.scatter.Scatter.transform) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to the identity matrix.

**kivy.uix.scatter.Scatter.transform_inv**

Inverse of the transformation matrix.
[`transform_inv`](https://kivy.org/doc/stable/#kivy.uix.scatter.Scatter.transform_inv) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to the identity matrix.

**kivy.uix.scatter.Scatter.translation_touches**

Determine whether translation was triggered by a single or multiple
touches. This only has effect when [`do_translation`](https://kivy.org/doc/stable/#kivy.uix.scatter.Scatter.do_translation) = True.
[`translation_touches`](https://kivy.org/doc/stable/#kivy.uix.scatter.Scatter.translation_touches) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 1.
New in version 1.7.0.

**kivy.uix.scatter.Scatter.x**

X position of the widget.
[`x`](https://kivy.org/doc/stable/#kivy.uix.scatter.Scatter.x) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and defaults to 0.

**kivy.uix.scatter.Scatter.y**

Y position of the widget.
[`y`](https://kivy.org/doc/stable/#kivy.uix.scatter.Scatter.y) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and defaults to 0.

**kivy.uix.scatter.ScatterPlane**

Bases: [`kivy.uix.scatter.Scatter`](https://kivy.org/doc/stable/#kivy.uix.scatter.Scatter)
This is essentially an unbounded Scatter widget. It’s a convenience
class to make it easier to handle infinite planes.

**kivy.uix.scatter.ScatterPlane.collide_point**

Check if a point (x, y) is inside the widget’s axis aligned bounding
box.

---

## API - [`kivy.uix.scatterlayout`](https://kivy.org/doc/stable/api-kivy.uix.scatterlayout.html)

**kivy.uix.scatterlayout.ScatterLayout**

Bases: [`kivy.uix.scatter.Scatter`](https://kivy.org/doc/stable/api-kivy.uix.scatter.html#kivy.uix.scatter.Scatter)
ScatterLayout class, see module documentation for more information.

**kivy.uix.scatterlayout.ScatterLayout.add_widget**

Add a new widget as a child of this widget.

**kivy.uix.scatterlayout.ScatterLayout.clear_widgets**

Remove all (or the specified) `children` of this widget.
If the ‘children’ argument is specified, it should be a list (or
filtered list) of children of the current widget.
Changed in version 1.8.0:The children argument can be used to specify the children you
want to remove.
Changed in version 2.1.0:Specifying an empty `children` list leaves the widgets unchanged.
Previously it was treated like `None` and all children were
removed.

**kivy.uix.scatterlayout.ScatterLayout.remove_widget**

Remove a widget from the children of this widget.

**kivy.uix.scatterlayout.ScatterPlaneLayout**

Bases: [`kivy.uix.scatter.ScatterPlane`](https://kivy.org/doc/stable/api-kivy.uix.scatter.html#kivy.uix.scatter.ScatterPlane)
ScatterPlaneLayout class, see module documentation for more information.
Similar to ScatterLayout, but based on ScatterPlane - so the input is not
bounded.
New in version 1.9.0.

**kivy.uix.scatterlayout.ScatterPlaneLayout.collide_point**

Check if a point (x, y) is inside the widget’s axis aligned bounding
box.

---

## API - [`kivy.uix.screenmanager`](https://kivy.org/doc/stable/api-kivy.uix.screenmanager.html)

**kivy.uix.screenmanager.CardTransition**

Bases: [`kivy.uix.screenmanager.SlideTransition`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.SlideTransition)
Card transition that looks similar to Android 4.x application drawer
interface animation.
It supports 4 directions like SlideTransition: left, right, up and down,
and two modes, pop and push. If push mode is activated, the previous
screen does not move, and the new one slides in from the given direction.
If the pop mode is activated, the previous screen slides out, when the new
screen is already on the position of the ScreenManager.
New in version 1.10.

**kivy.uix.screenmanager.CardTransition.mode**

Indicates if the transition should push or pop
the screen on/off the ScreenManager.
‘push’ means the screen slides in in the given direction
‘pop’ means the screen slides out in the given direction
[`mode`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.CardTransition.mode) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty) and
defaults to ‘push’.

**kivy.uix.screenmanager.CardTransition.start**

(internal) Starts the transition. This is automatically
called by the [`ScreenManager`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.ScreenManager).

**kivy.uix.screenmanager.FadeTransition**

Bases: [`kivy.uix.screenmanager.ShaderTransition`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.ShaderTransition)
Fade transition, based on a fragment Shader.

**kivy.uix.screenmanager.FadeTransition.fs**

Fragment shader to use.
[`fs`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.FadeTransition.fs) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults to
None.

**kivy.uix.screenmanager.FallOutTransition**

Bases: [`kivy.uix.screenmanager.ShaderTransition`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.ShaderTransition)
Transition where the new screen ‘falls’ from the screen centre,
becoming smaller and more transparent until it disappears, and
revealing the new screen behind it. Mimics the popular/standard
Android transition.
New in version 1.8.0.

**kivy.uix.screenmanager.FallOutTransition.duration**

Duration in seconds of the transition, replacing the default of
[`TransitionBase`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.TransitionBase).
[`duration`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.FallOutTransition.duration) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to .15 (= 150ms).

**kivy.uix.screenmanager.FallOutTransition.fs**

Fragment shader to use.
[`fs`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.FallOutTransition.fs) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults to
None.

**kivy.uix.screenmanager.NoTransition**

Bases: [`kivy.uix.screenmanager.TransitionBase`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.TransitionBase)
No transition, instantly switches to the next screen with no delay or
animation.
New in version 1.8.0.

**kivy.uix.screenmanager.NoTransition.duration**

Duration in seconds of the transition.
[`duration`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.NoTransition.duration) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to .4 (= 400ms).
Changed in version 1.8.0:Default duration has been changed from 700ms to 400ms.

**kivy.uix.screenmanager.RiseInTransition**

Bases: [`kivy.uix.screenmanager.ShaderTransition`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.ShaderTransition)
Transition where the new screen rises from the screen centre,
becoming larger and changing from transparent to opaque until it
fills the screen. Mimics the popular/standard Android transition.
New in version 1.8.0.

**kivy.uix.screenmanager.RiseInTransition.duration**

Duration in seconds of the transition, replacing the default of
[`TransitionBase`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.TransitionBase).
[`duration`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.RiseInTransition.duration) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to .2 (= 200ms).

**kivy.uix.screenmanager.RiseInTransition.fs**

Fragment shader to use.
[`fs`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.RiseInTransition.fs) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults to
None.

**kivy.uix.screenmanager.Screen**

Bases: [`kivy.uix.relativelayout.RelativeLayout`](https://kivy.org/doc/stable/api-kivy.uix.relativelayout.html#kivy.uix.relativelayout.RelativeLayout)
Screen is an element intended to be used with a [`ScreenManager`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.ScreenManager).
Check module documentation for more information.

Changed in version 1.6.0:Events on_pre_enter, on_enter, on_pre_leave and on_leave were
added.

**kivy.uix.screenmanager.Screen.manager**

[`ScreenManager`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.ScreenManager) object, set when the screen is added to a
manager.
[`manager`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.Screen.manager) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to None, read-only.

**kivy.uix.screenmanager.Screen.name**

Name of the screen which must be unique within a [`ScreenManager`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.ScreenManager).
This is the name used for [`ScreenManager.current`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.ScreenManager.current).
[`name`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.Screen.name) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults to
‘’.

**kivy.uix.screenmanager.Screen.transition_progress**

Value that represents the completion of the current transition, if any
is occurring.
If a transition is in progress, whatever the mode, the value will change
from 0 to 1. If you want to know if it’s an entering or leaving animation,
check the [`transition_state`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.Screen.transition_state).
[`transition_progress`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.Screen.transition_progress) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.

**kivy.uix.screenmanager.Screen.transition_state**

Value that represents the state of the transition:
‘in’ if the transition is going to show your screen
‘out’ if the transition is going to hide your screen
After the transition is complete, the state will retain its last value (in
or out).
[`transition_state`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.Screen.transition_state) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty) and
defaults to ‘out’.

**kivy.uix.screenmanager.ScreenManager**

Bases: [`kivy.uix.floatlayout.FloatLayout`](https://kivy.org/doc/stable/api-kivy.uix.floatlayout.html#kivy.uix.floatlayout.FloatLayout)
Screen manager. This is the main class that will control your
[`Screen`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.Screen) stack and memory.
By default, the manager will show only one screen at a time.

**kivy.uix.screenmanager.ScreenManager.add_widget**

Changed in version 2.1.0:Renamed argument screen to widget.

**kivy.uix.screenmanager.ScreenManager.clear_widgets**

Changed in version 2.1.0:Renamed argument screens to children.

**kivy.uix.screenmanager.ScreenManager.current**

Name of the screen currently shown, or the screen to show.

[`current`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.ScreenManager.current) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults
to None.

**kivy.uix.screenmanager.ScreenManager.current_screen**

Contains the currently displayed screen. You must not change this
property manually, use [`current`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.ScreenManager.current) instead.
[`current_screen`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.ScreenManager.current_screen) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to None, read-only.

**kivy.uix.screenmanager.ScreenManager.get_screen**

Return the screen widget associated with the name or raise a
[`ScreenManagerException`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.ScreenManagerException) if not found.

**kivy.uix.screenmanager.ScreenManager.has_screen**

Return True if a screen with the name has been found.
New in version 1.6.0.

**kivy.uix.screenmanager.ScreenManager.next**

Return the name of the next screen from the screen list.

**kivy.uix.screenmanager.ScreenManager.on_motion**

Called when a motion event is received.

New in version 2.1.0.

**kivy.uix.screenmanager.ScreenManager.on_touch_down**

Receive a touch down event.

**kivy.uix.screenmanager.ScreenManager.on_touch_move**

Receive a touch move event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.ScreenManager.on_touch_down) for more information.

**kivy.uix.screenmanager.ScreenManager.on_touch_up**

Receive a touch up event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.ScreenManager.on_touch_down) for more information.

**kivy.uix.screenmanager.ScreenManager.previous**

Return the name of the previous screen from the screen list.

**kivy.uix.screenmanager.ScreenManager.remove_widget**

Remove a widget from the children of this widget.

**kivy.uix.screenmanager.ScreenManager.screen_names**

List of the names of all the [`Screen`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.Screen) widgets added. The list
is read only.
`screens_names` is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) and
is read-only. It is updated if the screen list changes or the name
of a screen changes.

**kivy.uix.screenmanager.ScreenManager.screens**

List of all the [`Screen`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.Screen) widgets added. You should not change
this list manually. Use the
[`add_widget`](https://kivy.org/doc/stable/api-kivy.uix.widget.html#kivy.uix.widget.Widget.add_widget) method instead.
[`screens`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.ScreenManager.screens) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) and defaults to
[], read-only.

**kivy.uix.screenmanager.ScreenManager.switch_to**

Add a new or existing screen to the ScreenManager and switch to it.
The previous screen will be “switched away” from. options are the
[`transition`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.ScreenManager.transition) options that will be changed before the animation
happens.
If no previous screens are available, the screen will be used as the
main one:

If any animation is in progress, it will be stopped and replaced by
this one: you should avoid this because the animation will just look
weird. Use either [`switch_to()`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.ScreenManager.switch_to) or [`current`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.ScreenManager.current) but not both.
The screen name will be changed if there is any conflict with the
current screen.

**kivy.uix.screenmanager.ScreenManager.transition**

Transition object to use for animating the transition from the current
screen to the next one being shown.
For example, if you want to use a [`WipeTransition`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.WipeTransition) between
slides:

[`transition`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.ScreenManager.transition) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to a [`SlideTransition`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.SlideTransition).
Changed in version 1.8.0:Default transition has been changed from [`SwapTransition`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.SwapTransition) to
[`SlideTransition`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.SlideTransition).

**kivy.uix.screenmanager.ScreenManagerException**

Bases: `Exception`
Exception for the [`ScreenManager`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.ScreenManager).

**kivy.uix.screenmanager.ShaderTransition**

Bases: [`kivy.uix.screenmanager.TransitionBase`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.TransitionBase)
Transition class that uses a Shader for animating the transition between
2 screens. By default, this class doesn’t assign any fragment/vertex
shader. If you want to create your own fragment shader for the transition,
you need to declare the header yourself and include the “t”, “tex_in” and
“tex_out” uniform:

**kivy.uix.screenmanager.ShaderTransition.add_screen**

(internal) Used to add a screen to the [`ScreenManager`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.ScreenManager).

**kivy.uix.screenmanager.ShaderTransition.clearcolor**

Sets the color of Fbo ClearColor.
New in version 1.9.0.
[`clearcolor`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.ShaderTransition.clearcolor) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to [0, 0, 0, 1].
Changed in version 2.0.0:Changed from [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) to
[`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty).

**kivy.uix.screenmanager.ShaderTransition.fs**

Fragment shader to use.
[`fs`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.ShaderTransition.fs) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults to
None.

**kivy.uix.screenmanager.ShaderTransition.remove_screen**

(internal) Used to remove a screen from the [`ScreenManager`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.ScreenManager).

**kivy.uix.screenmanager.ShaderTransition.stop**

(internal) Stops the transition. This is automatically called by the
[`ScreenManager`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.ScreenManager).

**kivy.uix.screenmanager.ShaderTransition.vs**

Vertex shader to use.
[`vs`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.ShaderTransition.vs) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults to
None.

**kivy.uix.screenmanager.SlideTransition**

Bases: [`kivy.uix.screenmanager.TransitionBase`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.TransitionBase)
Slide Transition, can be used to show a new screen from any direction:
left, right, up or down.

**kivy.uix.screenmanager.SlideTransition.direction**

Direction of the transition.
[`direction`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.SlideTransition.direction) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty) and
defaults to ‘left’. Can be one of ‘left’, ‘right’, ‘up’ or ‘down’.

**kivy.uix.screenmanager.SwapTransition**

Bases: [`kivy.uix.screenmanager.TransitionBase`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.TransitionBase)
Swap transition that looks like iOS transition when a new window
appears on the screen.

**kivy.uix.screenmanager.SwapTransition.add_screen**

(internal) Used to add a screen to the [`ScreenManager`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.ScreenManager).

**kivy.uix.screenmanager.SwapTransition.start**

(internal) Starts the transition. This is automatically
called by the [`ScreenManager`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.ScreenManager).

**kivy.uix.screenmanager.TransitionBase**

Bases: [`kivy.event.EventDispatcher`](https://kivy.org/doc/stable/api-kivy.event.html#kivy.event.EventDispatcher)
TransitionBase is used to animate 2 screens within the
[`ScreenManager`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.ScreenManager). This class acts as a base for other
implementations like the [`SlideTransition`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.SlideTransition) and
[`SwapTransition`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.SwapTransition).

**kivy.uix.screenmanager.TransitionBase.add_screen**

(internal) Used to add a screen to the [`ScreenManager`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.ScreenManager).

**kivy.uix.screenmanager.TransitionBase.duration**

Duration in seconds of the transition.
[`duration`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.TransitionBase.duration) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to .4 (= 400ms).
Changed in version 1.8.0:Default duration has been changed from 700ms to 400ms.

**kivy.uix.screenmanager.TransitionBase.is_active**

Indicate whether the transition is currently active or not.
[`is_active`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.TransitionBase.is_active) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to False, read-only.

**kivy.uix.screenmanager.TransitionBase.manager**

[`ScreenManager`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.ScreenManager) object, set when the screen is added to a
manager.
[`manager`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.TransitionBase.manager) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to None, read-only.

**kivy.uix.screenmanager.TransitionBase.remove_screen**

(internal) Used to remove a screen from the [`ScreenManager`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.ScreenManager).

**kivy.uix.screenmanager.TransitionBase.screen_in**

Property that contains the screen to show.
Automatically set by the [`ScreenManager`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.ScreenManager).
[`screen_in`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.TransitionBase.screen_in) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to None.

**kivy.uix.screenmanager.TransitionBase.screen_out**

Property that contains the screen to hide.
Automatically set by the [`ScreenManager`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.ScreenManager).
[`screen_out`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.TransitionBase.screen_out) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to None.

**kivy.uix.screenmanager.TransitionBase.start**

(internal) Starts the transition. This is automatically
called by the [`ScreenManager`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.ScreenManager).

**kivy.uix.screenmanager.TransitionBase.stop**

(internal) Stops the transition. This is automatically called by the
[`ScreenManager`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.ScreenManager).

**kivy.uix.screenmanager.WipeTransition**

Bases: [`kivy.uix.screenmanager.ShaderTransition`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.ShaderTransition)
Wipe transition, based on a fragment Shader.

**kivy.uix.screenmanager.WipeTransition.fs**

Fragment shader to use.
[`fs`](https://kivy.org/doc/stable/#kivy.uix.screenmanager.WipeTransition.fs) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults to
None.

---

## API - [`kivy.uix.scrollview`](https://kivy.org/doc/stable/api-kivy.uix.scrollview.html)

**kivy.uix.scrollview.ScrollView**

Bases: [`kivy.uix.stencilview.StencilView`](https://kivy.org/doc/stable/api-kivy.uix.stencilview.html#kivy.uix.stencilview.StencilView)
ScrollView class. See module documentation for more information.

Changed in version 1.9.0:on_scroll_start, on_scroll_move and on_scroll_stop events are
now dispatched when scrolling to handle nested ScrollViews.
Changed in version 1.7.0:auto_scroll, scroll_friction, scroll_moves, scroll_stoptime’ has
been deprecated, use :attr:`effect_cls instead.

**kivy.uix.scrollview.ScrollView.add_widget**

Add a new widget as a child of this widget.

**kivy.uix.scrollview.ScrollView.always_overscroll**

Make sure user can overscroll even if there is not enough content
to require scrolling.
This is useful if you want to trigger some action on overscroll, but
there is not always enough content to trigger it.
[`always_overscroll`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.always_overscroll) is a
[`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and defaults to True.
New in version 2.0.0.
The option was added and enabled by default, set to False to get the
previous behavior of only allowing to overscroll when there is
enough content to allow scrolling.

**kivy.uix.scrollview.ScrollView.bar_color**

Color of horizontal / vertical scroll bar, in RGBA format.
New in version 1.2.0.
[`bar_color`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.bar_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty) and defaults
to [.7, .7, .7, .9].
Changed in version 2.0.0:Changed from [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) to
[`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty).

**kivy.uix.scrollview.ScrollView.bar_inactive_color**

Color of horizontal / vertical scroll bar (in RGBA format), when no
scroll is happening.
New in version 1.9.0.
[`bar_inactive_color`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.bar_inactive_color) is a
[`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty) and defaults to [.7, .7, .7, .2].
Changed in version 2.0.0:Changed from [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) to
[`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty).

**kivy.uix.scrollview.ScrollView.bar_margin**

Margin between the bottom / right side of the scrollview when drawing
the horizontal / vertical scroll bar.
New in version 1.2.0.
[`bar_margin`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.bar_margin) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty), default
to 0

**kivy.uix.scrollview.ScrollView.bar_pos**

Which side of the scroll view to place each of the bars on.
[`bar_pos`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.bar_pos) is a [`ReferenceListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ReferenceListProperty) of
([`bar_pos_x`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.bar_pos_x), [`bar_pos_y`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.bar_pos_y))

**kivy.uix.scrollview.ScrollView.bar_pos_x**

Which side of the ScrollView the horizontal scroll bar should go
on. Possible values are ‘top’ and ‘bottom’.
New in version 1.8.0.
[`bar_pos_x`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.bar_pos_x) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty),
defaults to ‘bottom’.

**kivy.uix.scrollview.ScrollView.bar_pos_y**

Which side of the ScrollView the vertical scroll bar should go
on. Possible values are ‘left’ and ‘right’.
New in version 1.8.0.
[`bar_pos_y`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.bar_pos_y) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty) and
defaults to ‘right’.

**kivy.uix.scrollview.ScrollView.bar_width**

Width of the horizontal / vertical scroll bar. The width is interpreted
as a height for the horizontal bar.
New in version 1.2.0.
[`bar_width`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.bar_width) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 2.

**kivy.uix.scrollview.ScrollView.convert_distance_to_scroll**

Convert a distance in pixels to a scroll distance, depending on the
content size and the scrollview size.
The result will be a tuple of scroll distance that can be added to
[`scroll_x`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.scroll_x) and [`scroll_y`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.scroll_y)

**kivy.uix.scrollview.ScrollView.do_scroll**

Allow scroll on X or Y axis.
[`do_scroll`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.do_scroll) is a [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) of
([`do_scroll_x`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.do_scroll_x) + [`do_scroll_y`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.do_scroll_y))

**kivy.uix.scrollview.ScrollView.do_scroll_x**

Allow scroll on X axis.
[`do_scroll_x`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.do_scroll_x) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to True.

**kivy.uix.scrollview.ScrollView.do_scroll_y**

Allow scroll on Y axis.
[`do_scroll_y`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.do_scroll_y) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to True.

**kivy.uix.scrollview.ScrollView.effect_cls**

Class effect to instantiate for X and Y axis.
New in version 1.7.0.
[`effect_cls`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.effect_cls) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to `DampedScrollEffect`.
Changed in version 1.8.0:If you set a string, the [`Factory`](https://kivy.org/doc/stable/api-kivy.factory.html#kivy.factory.Factory) will be used to
resolve the class.

**kivy.uix.scrollview.ScrollView.effect_x**

Effect to apply for the X axis. If None is set, an instance of
[`effect_cls`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.effect_cls) will be created.
New in version 1.7.0.
[`effect_x`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.effect_x) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to None.

**kivy.uix.scrollview.ScrollView.effect_y**

Effect to apply for the Y axis. If None is set, an instance of
[`effect_cls`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.effect_cls) will be created.
New in version 1.7.0.
[`effect_y`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.effect_y) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to None, read-only.

**kivy.uix.scrollview.ScrollView.hbar**

Return a tuple of (position, size) of the horizontal scrolling bar.
New in version 1.2.0.
The position and size are normalized between 0-1, and represent a
proportion of the current scrollview height. This property is used
internally for drawing the little horizontal bar when you’re scrolling.
[`hbar`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.hbar) is a [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty), readonly.

**kivy.uix.scrollview.ScrollView.on_motion**

Called when a motion event is received.

New in version 2.1.0.

**kivy.uix.scrollview.ScrollView.on_touch_down**

Receive a touch down event.

**kivy.uix.scrollview.ScrollView.on_touch_move**

Receive a touch move event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.on_touch_down) for more information.

**kivy.uix.scrollview.ScrollView.on_touch_up**

Receive a touch up event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.on_touch_down) for more information.

**kivy.uix.scrollview.ScrollView.remove_widget**

Remove a widget from the children of this widget.

**kivy.uix.scrollview.ScrollView.scroll_distance**

Distance to move before scrolling the [`ScrollView`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView), in pixels. As
soon as the distance has been traveled, the [`ScrollView`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView) will start
to scroll, and no touch event will go to children.
It is advisable that you base this value on the dpi of your target device’s
screen.
[`scroll_distance`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.scroll_distance) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 20 (pixels), according to the default value in user
configuration.

**kivy.uix.scrollview.ScrollView.scroll_timeout**

Timeout allowed to trigger the [`scroll_distance`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.scroll_distance), in milliseconds.
If the user has not moved [`scroll_distance`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.scroll_distance) within the timeout,
the scrolling will be disabled, and the touch event will go to the
children.
[`scroll_timeout`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.scroll_timeout) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 55 (milliseconds) according to the default value in user
configuration.
Changed in version 1.5.0:Default value changed from 250 to 55.

**kivy.uix.scrollview.ScrollView.scroll_to**

Scrolls the viewport to ensure that the given widget is visible,
optionally with padding and animation. If animate is True (the
default), then the default animation parameters will be used.
Otherwise, it should be a dict containing arguments to pass to
[`Animation`](https://kivy.org/doc/stable/api-kivy.animation.html#kivy.animation.Animation) constructor.
New in version 1.9.1.

**kivy.uix.scrollview.ScrollView.scroll_type**

Sets the type of scrolling to use for the content of the scrollview.
Available options are: [‘content’], [‘bars’], [‘bars’, ‘content’].
[‘content’]
Content is scrolled by dragging or swiping the
content directly.
[‘bars’]
Content is scrolled by dragging or swiping the
scroll bars.
[‘bars’, ‘content’]
Content is scrolled by either of the above
methods.
New in version 1.8.0.
[`scroll_type`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.scroll_type) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty) and
defaults to [‘content’].

**kivy.uix.scrollview.ScrollView.scroll_wheel_distance**

Distance to move when scrolling with a mouse wheel.
It is advisable that you base this value on the dpi of your target device’s
screen.
New in version 1.8.0.
[`scroll_wheel_distance`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.scroll_wheel_distance) is a
[`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) , defaults to 20 pixels.

**kivy.uix.scrollview.ScrollView.scroll_x**

X scrolling value, between 0 and 1. If 0, the content’s left side will
touch the left side of the ScrollView. If 1, the content’s right side will
touch the right side.
This property is controlled by [`ScrollView`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView) only if
[`do_scroll_x`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.do_scroll_x) is True.
[`scroll_x`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.scroll_x) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0.

**kivy.uix.scrollview.ScrollView.scroll_y**

Y scrolling value, between 0 and 1. If 0, the content’s bottom side will
touch the bottom side of the ScrollView. If 1, the content’s top side will
touch the top side.
This property is controlled by [`ScrollView`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView) only if
[`do_scroll_y`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.do_scroll_y) is True.
[`scroll_y`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.scroll_y) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 1.

**kivy.uix.scrollview.ScrollView.smooth_scroll_end**

Whether smooth scroll end should be used when scrolling with the
mouse-wheel and the factor of transforming the scroll distance to
velocity. This option also enables velocity addition meaning if you
scroll more, you will scroll faster and further. The recommended value
is 10. The velocity is calculated as [`scroll_wheel_distance`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.scroll_wheel_distance) *
[`smooth_scroll_end`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.smooth_scroll_end).
New in version 1.11.0.
[`smooth_scroll_end`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.smooth_scroll_end) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to None.

**kivy.uix.scrollview.ScrollView.to_local**

Transform parent coordinates to local (current widget) coordinates.
See [`relativelayout`](https://kivy.org/doc/stable/api-kivy.uix.relativelayout.html#module-kivy.uix.relativelayout) for details on the coordinate
systems.

**kivy.uix.scrollview.ScrollView.to_parent**

Transform local (current widget) coordinates to parent coordinates.
See [`relativelayout`](https://kivy.org/doc/stable/api-kivy.uix.relativelayout.html#module-kivy.uix.relativelayout) for details on the coordinate
systems.

**kivy.uix.scrollview.ScrollView.update_from_scroll**

Force the reposition of the content, according to current value of
[`scroll_x`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.scroll_x) and [`scroll_y`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.scroll_y).
This method is automatically called when one of the [`scroll_x`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.scroll_x),
[`scroll_y`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.scroll_y), `pos` or `size` properties change, or
if the size of the content changes.

**kivy.uix.scrollview.ScrollView.vbar**

Return a tuple of (position, size) of the vertical scrolling bar.
New in version 1.2.0.
The position and size are normalized between 0-1, and represent a
proportion of the current scrollview height. This property is used
internally for drawing the little vertical bar when you’re scrolling.
[`vbar`](https://kivy.org/doc/stable/#kivy.uix.scrollview.ScrollView.vbar) is a [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty), readonly.

**kivy.uix.scrollview.ScrollView.viewport_size**

(internal) Size of the internal viewport. This is the size of your only
child in the scrollview.

---

## API - [`kivy.uix.settings`](https://kivy.org/doc/stable/api-kivy.uix.settings.html)

**kivy.uix.settings.ContentPanel**

Bases: [`kivy.uix.scrollview.ScrollView`](https://kivy.org/doc/stable/api-kivy.uix.scrollview.html#kivy.uix.scrollview.ScrollView)
A class for displaying settings panels. It displays a single
settings panel at a time, taking up the full size and shape of the
ContentPanel. It is used by [`InterfaceWithSidebar`](https://kivy.org/doc/stable/#kivy.uix.settings.InterfaceWithSidebar) and
`InterfaceWithSpinner` to display settings.

**kivy.uix.settings.ContentPanel.add_panel**

This method is used by Settings to add new panels for possible
display. Any replacement for ContentPanel *must* implement
this method.

**kivy.uix.settings.ContentPanel.add_widget**

Add a new widget as a child of this widget.

**kivy.uix.settings.ContentPanel.container**

(internal) A reference to the GridLayout that contains the
settings panel.
[`container`](https://kivy.org/doc/stable/#kivy.uix.settings.ContentPanel.container) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to None.

**kivy.uix.settings.ContentPanel.current_panel**

(internal) A reference to the current settings panel.
[`current_panel`](https://kivy.org/doc/stable/#kivy.uix.settings.ContentPanel.current_panel) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to None.

**kivy.uix.settings.ContentPanel.current_uid**

(internal) A reference to the uid of the current settings panel.
[`current_uid`](https://kivy.org/doc/stable/#kivy.uix.settings.ContentPanel.current_uid) is a
[`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and defaults to 0.

**kivy.uix.settings.ContentPanel.on_current_uid**

The uid of the currently displayed panel. Changing this will
automatically change the displayed panel.

**kivy.uix.settings.ContentPanel.panels**

(internal) Stores a dictionary mapping settings panels to their uids.
[`panels`](https://kivy.org/doc/stable/#kivy.uix.settings.ContentPanel.panels) is a [`DictProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.DictProperty) and
defaults to {}.

**kivy.uix.settings.ContentPanel.remove_widget**

Remove a widget from the children of this widget.

**kivy.uix.settings.InterfaceWithSidebar**

Bases: [`kivy.uix.boxlayout.BoxLayout`](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html#kivy.uix.boxlayout.BoxLayout)
The default Settings interface class. It displays a sidebar menu
with names of available settings panels, which may be used to switch
which one is currently displayed.
See [`add_panel()`](https://kivy.org/doc/stable/#kivy.uix.settings.InterfaceWithSidebar.add_panel) for information on the
method you must implement if creating your own interface.
This class also dispatches an event ‘on_close’, which is triggered
when the sidebar menu’s close button is released. If creating your
own interface widget, it should also dispatch such an event which
will automatically be caught by [`Settings`](https://kivy.org/doc/stable/#kivy.uix.settings.Settings) and used to
trigger its own ‘on_close’ event.

**kivy.uix.settings.InterfaceWithSidebar.add_panel**

This method is used by Settings to add new panels for possible
display. Any replacement for ContentPanel *must* implement
this method.

**kivy.uix.settings.InterfaceWithSidebar.content**

(internal) A reference to the panel display widget (a
[`ContentPanel`](https://kivy.org/doc/stable/#kivy.uix.settings.ContentPanel)).
[`content`](https://kivy.org/doc/stable/#kivy.uix.settings.InterfaceWithSidebar.content) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to None.

**kivy.uix.settings.InterfaceWithSidebar.menu**

(internal) A reference to the sidebar menu widget.
[`menu`](https://kivy.org/doc/stable/#kivy.uix.settings.InterfaceWithSidebar.menu) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to None.

**kivy.uix.settings.MenuSidebar**

Bases: [`kivy.uix.floatlayout.FloatLayout`](https://kivy.org/doc/stable/api-kivy.uix.floatlayout.html#kivy.uix.floatlayout.FloatLayout)
The menu used by [`InterfaceWithSidebar`](https://kivy.org/doc/stable/#kivy.uix.settings.InterfaceWithSidebar). It provides a
sidebar with an entry for each settings panel, which the user may
click to select.

**kivy.uix.settings.MenuSidebar.add_item**

This method is used to add new panels to the menu.

**kivy.uix.settings.MenuSidebar.buttons_layout**

(internal) Reference to the GridLayout that contains individual
settings panel menu buttons.
[`buttons_layout`](https://kivy.org/doc/stable/#kivy.uix.settings.MenuSidebar.buttons_layout) is an
[`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and defaults to None.

**kivy.uix.settings.MenuSidebar.close_button**

(internal) Reference to the widget’s Close button.
[`buttons_layout`](https://kivy.org/doc/stable/#kivy.uix.settings.MenuSidebar.buttons_layout) is an
[`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and defaults to None.

**kivy.uix.settings.MenuSidebar.on_selected_uid**

(internal) unselects any currently selected menu buttons, unless
they represent the current panel.

**kivy.uix.settings.MenuSidebar.selected_uid**

The uid of the currently selected panel. This may be used to switch
between displayed panels, e.g. by binding it to the
[`current_uid`](https://kivy.org/doc/stable/#kivy.uix.settings.ContentPanel.current_uid) of a [`ContentPanel`](https://kivy.org/doc/stable/#kivy.uix.settings.ContentPanel).
[`selected_uid`](https://kivy.org/doc/stable/#kivy.uix.settings.MenuSidebar.selected_uid) is a
[`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and defaults to 0.

**kivy.uix.settings.SettingBoolean**

Bases: [`kivy.uix.settings.SettingItem`](https://kivy.org/doc/stable/#kivy.uix.settings.SettingItem)
Implementation of a boolean setting on top of a [`SettingItem`](https://kivy.org/doc/stable/#kivy.uix.settings.SettingItem).
It is visualized with a [`Switch`](https://kivy.org/doc/stable/api-kivy.uix.switch.html#kivy.uix.switch.Switch) widget.
By default, 0 and 1 are used for values: you can change them by setting
[`values`](https://kivy.org/doc/stable/#kivy.uix.settings.SettingBoolean.values).

**kivy.uix.settings.SettingBoolean.values**

Values used to represent the state of the setting. If you want to use
“yes” and “no” in your ConfigParser instance:

[`values`](https://kivy.org/doc/stable/#kivy.uix.settings.SettingBoolean.values) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) and defaults to
[‘0’, ‘1’]

**kivy.uix.settings.SettingItem**

Bases: [`kivy.uix.floatlayout.FloatLayout`](https://kivy.org/doc/stable/api-kivy.uix.floatlayout.html#kivy.uix.floatlayout.FloatLayout)
Base class for individual settings (within a panel). This class cannot
be used directly; it is used for implementing the other setting classes.
It builds a row with a title/description (left) and a setting control
(right).
Look at [`SettingBoolean`](https://kivy.org/doc/stable/#kivy.uix.settings.SettingBoolean), [`SettingNumeric`](https://kivy.org/doc/stable/#kivy.uix.settings.SettingNumeric) and
[`SettingOptions`](https://kivy.org/doc/stable/#kivy.uix.settings.SettingOptions) for usage examples.

**kivy.uix.settings.SettingItem.add_widget**

Add a new widget as a child of this widget.

**kivy.uix.settings.SettingItem.content**

(internal) Reference to the widget that contains the real setting.
As soon as the content object is set, any further call to add_widget will
call the content.add_widget. This is automatically set.
[`content`](https://kivy.org/doc/stable/#kivy.uix.settings.SettingItem.content) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to None.

**kivy.uix.settings.SettingItem.desc**

Description of the setting, rendered on the line below the title.
[`desc`](https://kivy.org/doc/stable/#kivy.uix.settings.SettingItem.desc) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults to
None.

**kivy.uix.settings.SettingItem.disabled**

Indicate if this setting is disabled. If True, all touches on the
setting item will be discarded.
[`disabled`](https://kivy.org/doc/stable/#kivy.uix.settings.SettingItem.disabled) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to False.

**kivy.uix.settings.SettingItem.key**

Key of the token inside the [`section`](https://kivy.org/doc/stable/#kivy.uix.settings.SettingItem.section) in the
[`ConfigParser`](https://kivy.org/doc/stable/api-kivy.config.html#kivy.config.ConfigParser) instance.
[`key`](https://kivy.org/doc/stable/#kivy.uix.settings.SettingItem.key) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults to
None.

**kivy.uix.settings.SettingItem.on_touch_down**

Receive a touch down event.

**kivy.uix.settings.SettingItem.on_touch_up**

Receive a touch up event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivy.org/doc/stable/#kivy.uix.settings.SettingItem.on_touch_down) for more information.

**kivy.uix.settings.SettingItem.panel**

(internal) Reference to the SettingsPanel for this setting. You don’t
need to use it.
[`panel`](https://kivy.org/doc/stable/#kivy.uix.settings.SettingItem.panel) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and defaults
to None.

**kivy.uix.settings.SettingItem.section**

Section of the token inside the [`ConfigParser`](https://kivy.org/doc/stable/api-kivy.config.html#kivy.config.ConfigParser)
instance.
[`section`](https://kivy.org/doc/stable/#kivy.uix.settings.SettingItem.section) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults
to None.

**kivy.uix.settings.SettingItem.selected_alpha**

(internal) Float value from 0 to 1, used to animate the background when
the user touches the item.
[`selected_alpha`](https://kivy.org/doc/stable/#kivy.uix.settings.SettingItem.selected_alpha) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0.

**kivy.uix.settings.SettingItem.title**

Title of the setting, defaults to ‘<No title set>’.
[`title`](https://kivy.org/doc/stable/#kivy.uix.settings.SettingItem.title) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults
to ‘<No title set>’.

**kivy.uix.settings.SettingItem.value**

Value of the token according to the [`ConfigParser`](https://kivy.org/doc/stable/api-kivy.config.html#kivy.config.ConfigParser)
instance. Any change to this value will trigger a
`Settings.on_config_change()` event.
[`value`](https://kivy.org/doc/stable/#kivy.uix.settings.SettingItem.value) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and defaults
to None.

**kivy.uix.settings.SettingNumeric**

Bases: [`kivy.uix.settings.SettingString`](https://kivy.org/doc/stable/#kivy.uix.settings.SettingString)
Implementation of a numeric setting on top of a [`SettingString`](https://kivy.org/doc/stable/#kivy.uix.settings.SettingString).
It is visualized with a [`Label`](https://kivy.org/doc/stable/api-kivy.uix.label.html#kivy.uix.label.Label) widget that, when
clicked, will open a [`Popup`](https://kivy.org/doc/stable/api-kivy.uix.popup.html#kivy.uix.popup.Popup) with a
`Textinput` so the user can enter a custom
value.

**kivy.uix.settings.SettingOptions**

Bases: [`kivy.uix.settings.SettingItem`](https://kivy.org/doc/stable/#kivy.uix.settings.SettingItem)
Implementation of an option list on top of a [`SettingItem`](https://kivy.org/doc/stable/#kivy.uix.settings.SettingItem).
It is visualized with a [`Label`](https://kivy.org/doc/stable/api-kivy.uix.label.html#kivy.uix.label.Label) widget that, when
clicked, will open a [`Popup`](https://kivy.org/doc/stable/api-kivy.uix.popup.html#kivy.uix.popup.Popup) with a
list of options from which the user can select.

**kivy.uix.settings.SettingOptions.options**

List of all availables options. This must be a list of “string” items.
Otherwise, it will crash. :)
[`options`](https://kivy.org/doc/stable/#kivy.uix.settings.SettingOptions.options) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) and defaults
to [].

**kivy.uix.settings.SettingOptions.popup**

(internal) Used to store the current popup when it is shown.
[`popup`](https://kivy.org/doc/stable/#kivy.uix.settings.SettingOptions.popup) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and defaults
to None.

**kivy.uix.settings.SettingPath**

Bases: [`kivy.uix.settings.SettingItem`](https://kivy.org/doc/stable/#kivy.uix.settings.SettingItem)
Implementation of a Path setting on top of a [`SettingItem`](https://kivy.org/doc/stable/#kivy.uix.settings.SettingItem).
It is visualized with a [`Label`](https://kivy.org/doc/stable/api-kivy.uix.label.html#kivy.uix.label.Label) widget that, when
clicked, will open a [`Popup`](https://kivy.org/doc/stable/api-kivy.uix.popup.html#kivy.uix.popup.Popup) with a
[`FileChooserListView`](https://kivy.org/doc/stable/api-kivy.uix.filechooser.html#kivy.uix.filechooser.FileChooserListView) so the user can enter
a custom value.
New in version 1.1.0.

**kivy.uix.settings.SettingPath.dirselect**

Whether to allow selection of directories.
[`dirselect`](https://kivy.org/doc/stable/#kivy.uix.settings.SettingPath.dirselect) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to True.
New in version 1.10.0.

**kivy.uix.settings.SettingPath.popup**

(internal) Used to store the current popup when it is shown.
[`popup`](https://kivy.org/doc/stable/#kivy.uix.settings.SettingPath.popup) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and defaults
to None.

**kivy.uix.settings.SettingPath.show_hidden**

Whether to show ‘hidden’ filenames. What that means is
operating-system-dependent.
[`show_hidden`](https://kivy.org/doc/stable/#kivy.uix.settings.SettingPath.show_hidden) is an [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to False.
New in version 1.10.0.

**kivy.uix.settings.SettingPath.textinput**

(internal) Used to store the current textinput from the popup and
to listen for changes.
[`textinput`](https://kivy.org/doc/stable/#kivy.uix.settings.SettingPath.textinput) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to None.

**kivy.uix.settings.SettingString**

Bases: [`kivy.uix.settings.SettingItem`](https://kivy.org/doc/stable/#kivy.uix.settings.SettingItem)
Implementation of a string setting on top of a [`SettingItem`](https://kivy.org/doc/stable/#kivy.uix.settings.SettingItem).
It is visualized with a [`Label`](https://kivy.org/doc/stable/api-kivy.uix.label.html#kivy.uix.label.Label) widget that, when
clicked, will open a [`Popup`](https://kivy.org/doc/stable/api-kivy.uix.popup.html#kivy.uix.popup.Popup) with a
`Textinput` so the user can enter a custom
value.

**kivy.uix.settings.SettingString.popup**

(internal) Used to store the current popup when it’s shown.
[`popup`](https://kivy.org/doc/stable/#kivy.uix.settings.SettingString.popup) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and defaults
to None.

**kivy.uix.settings.SettingString.textinput**

(internal) Used to store the current textinput from the popup and
to listen for changes.
[`textinput`](https://kivy.org/doc/stable/#kivy.uix.settings.SettingString.textinput) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to None.

**kivy.uix.settings.SettingTitle**

Bases: [`kivy.uix.label.Label`](https://kivy.org/doc/stable/api-kivy.uix.label.html#kivy.uix.label.Label)
A simple title label, used to organize the settings in sections.

**kivy.uix.settings.Settings**

Bases: [`kivy.uix.boxlayout.BoxLayout`](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html#kivy.uix.boxlayout.BoxLayout)
Settings UI. Check module documentation for more information on how
to use this class.

**kivy.uix.settings.Settings.add_interface**

(Internal) creates an instance of [`Settings.interface_cls`](https://kivy.org/doc/stable/#kivy.uix.settings.Settings.interface_cls),
and sets it to [`interface`](https://kivy.org/doc/stable/#kivy.uix.settings.Settings.interface). When json panels are
created, they will be added to this interface which will display them
to the user.

**kivy.uix.settings.Settings.add_json_panel**

Create and add a new [`SettingsPanel`](https://kivy.org/doc/stable/#kivy.uix.settings.SettingsPanel) using the configuration
config with the JSON definition filename. If filename is not set,
then the JSON definition is read from the data parameter instead.
Check the [Create a panel from JSON](https://kivy.org/doc/stable/#settings-json) section in the documentation for more
information about JSON format and the usage of this function.

**kivy.uix.settings.Settings.add_kivy_panel**

Add a panel for configuring Kivy. This panel acts directly on the
kivy configuration. Feel free to include or exclude it in your
configuration.
See [`use_kivy_settings()`](https://kivy.org/doc/stable/api-kivy.app.html#kivy.app.App.use_kivy_settings) for information on
enabling/disabling the automatic kivy panel.

**kivy.uix.settings.Settings.create_json_panel**

Create new [`SettingsPanel`](https://kivy.org/doc/stable/#kivy.uix.settings.SettingsPanel).
New in version 1.5.0.
Check the documentation of [`add_json_panel()`](https://kivy.org/doc/stable/#kivy.uix.settings.Settings.add_json_panel) for more information.

**kivy.uix.settings.Settings.interface**

(internal) Reference to the widget that will contain, organise and
display the panel configuration panel widgets.
[`interface`](https://kivy.org/doc/stable/#kivy.uix.settings.Settings.interface) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to None.

**kivy.uix.settings.Settings.interface_cls**

The widget class that will be used to display the graphical
interface for the settings panel. By default, it displays one Settings
panel at a time with a sidebar to switch between them.
[`interface_cls`](https://kivy.org/doc/stable/#kivy.uix.settings.Settings.interface_cls) is an
[`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and defaults to
[`InterfaceWithSidebar`](https://kivy.org/doc/stable/#kivy.uix.settings.InterfaceWithSidebar).
Changed in version 1.8.0:If you set a string, the [`Factory`](https://kivy.org/doc/stable/api-kivy.factory.html#kivy.factory.Factory) will be used to
resolve the class.

**kivy.uix.settings.Settings.on_touch_down**

Receive a touch down event.

**kivy.uix.settings.Settings.register_type**

Register a new type that can be used in the JSON definition.

**kivy.uix.settings.SettingsPanel**

Bases: [`kivy.uix.gridlayout.GridLayout`](https://kivy.org/doc/stable/api-kivy.uix.gridlayout.html#kivy.uix.gridlayout.GridLayout)
This class is used to construct panel settings, for use with a
[`Settings`](https://kivy.org/doc/stable/#kivy.uix.settings.Settings) instance or subclass.

**kivy.uix.settings.SettingsPanel.config**

A [`kivy.config.ConfigParser`](https://kivy.org/doc/stable/api-kivy.config.html#kivy.config.ConfigParser) instance. See module documentation
for more information.

**kivy.uix.settings.SettingsPanel.get_value**

Return the value of the section/key from the [`config`](https://kivy.org/doc/stable/#kivy.uix.settings.SettingsPanel.config)
ConfigParser instance. This function is used by [`SettingItem`](https://kivy.org/doc/stable/#kivy.uix.settings.SettingItem) to
get the value for a given section/key.
If you don’t want to use a ConfigParser instance, you might want to
override this function.

**kivy.uix.settings.SettingsPanel.settings**

A [`Settings`](https://kivy.org/doc/stable/#kivy.uix.settings.Settings) instance that will be used to fire the
on_config_change event.

**kivy.uix.settings.SettingsPanel.title**

Title of the panel. The title will be reused by the [`Settings`](https://kivy.org/doc/stable/#kivy.uix.settings.Settings) in
the sidebar.

**kivy.uix.settings.SettingsWithNoMenu**

Bases: [`kivy.uix.settings.Settings`](https://kivy.org/doc/stable/#kivy.uix.settings.Settings)
A settings widget that displays a single settings panel with *no*
Close button. It will not accept more than one Settings panel. It
is intended for use in programs with few enough settings that a
full panel switcher is not useful.

**kivy.uix.settings.SettingsWithSidebar**

Bases: [`kivy.uix.settings.Settings`](https://kivy.org/doc/stable/#kivy.uix.settings.Settings)
A settings widget that displays settings panels with a sidebar to
switch between them. This is the default behavior of
[`Settings`](https://kivy.org/doc/stable/#kivy.uix.settings.Settings), and this widget is a trivial wrapper subclass.

**kivy.uix.settings.SettingsWithSpinner**

Bases: [`kivy.uix.settings.Settings`](https://kivy.org/doc/stable/#kivy.uix.settings.Settings)
A settings widget that displays one settings panel at a time with a
spinner at the top to switch between them.

**kivy.uix.settings.SettingsWithTabbedPanel**

Bases: [`kivy.uix.settings.Settings`](https://kivy.org/doc/stable/#kivy.uix.settings.Settings)
A settings widget that displays settings panels as pages in a
[`TabbedPanel`](https://kivy.org/doc/stable/api-kivy.uix.tabbedpanel.html#kivy.uix.tabbedpanel.TabbedPanel).

---

## API - [`kivy.uix.slider`](https://kivy.org/doc/stable/api-kivy.uix.slider.html)

**kivy.uix.slider.Slider**

Bases: [`kivy.uix.widget.Widget`](https://kivy.org/doc/stable/api-kivy.uix.widget.html#kivy.uix.widget.Widget)
Class for creating a Slider widget.
Check module documentation for more details.

**kivy.uix.slider.Slider.background_disabled_horizontal**

Background of the disabled slider used in the horizontal orientation.
New in version 1.10.0.
[`background_disabled_horizontal`](https://kivy.org/doc/stable/#kivy.uix.slider.Slider.background_disabled_horizontal) is a
[`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults to
atlas://data/images/defaulttheme/sliderh_background_disabled.

**kivy.uix.slider.Slider.background_disabled_vertical**

Background of the disabled slider used in the vertical orientation.
New in version 1.10.0.
[`background_disabled_vertical`](https://kivy.org/doc/stable/#kivy.uix.slider.Slider.background_disabled_vertical) is a
[`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults to
atlas://data/images/defaulttheme/sliderv_background_disabled.

**kivy.uix.slider.Slider.background_horizontal**

Background of the slider used in the horizontal orientation.
New in version 1.10.0.
[`background_horizontal`](https://kivy.org/doc/stable/#kivy.uix.slider.Slider.background_horizontal) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to atlas://data/images/defaulttheme/sliderh_background.

**kivy.uix.slider.Slider.background_vertical**

Background of the slider used in the vertical orientation.
New in version 1.10.0.
[`background_vertical`](https://kivy.org/doc/stable/#kivy.uix.slider.Slider.background_vertical) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to atlas://data/images/defaulttheme/sliderv_background.

**kivy.uix.slider.Slider.background_width**

Slider’s background’s width (thickness), used in both horizontal
and vertical orientations.
[`background_width`](https://kivy.org/doc/stable/#kivy.uix.slider.Slider.background_width) is a
[`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and defaults to 36sp.

**kivy.uix.slider.Slider.border_horizontal**

Border used to draw the slider background in horizontal orientation.
[`border_horizontal`](https://kivy.org/doc/stable/#kivy.uix.slider.Slider.border_horizontal) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty)
and defaults to [0, 18, 0, 18].

**kivy.uix.slider.Slider.border_vertical**

Border used to draw the slider background in vertical orientation.
[`border_horizontal`](https://kivy.org/doc/stable/#kivy.uix.slider.Slider.border_horizontal) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty)
and defaults to [18, 0, 18, 0].

**kivy.uix.slider.Slider.cursor_disabled_image**

Path of the image used to draw the disabled slider cursor.
[`cursor_image`](https://kivy.org/doc/stable/#kivy.uix.slider.Slider.cursor_image) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to atlas://data/images/defaulttheme/slider_cursor_disabled.

**kivy.uix.slider.Slider.cursor_height**

Height of the cursor image.
[`cursor_height`](https://kivy.org/doc/stable/#kivy.uix.slider.Slider.cursor_height) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 32sp.

**kivy.uix.slider.Slider.cursor_image**

Path of the image used to draw the slider cursor.
[`cursor_image`](https://kivy.org/doc/stable/#kivy.uix.slider.Slider.cursor_image) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to atlas://data/images/defaulttheme/slider_cursor.

**kivy.uix.slider.Slider.cursor_size**

Size of the cursor image.
[`cursor_size`](https://kivy.org/doc/stable/#kivy.uix.slider.Slider.cursor_size) is a [`ReferenceListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ReferenceListProperty)
of ([`cursor_width`](https://kivy.org/doc/stable/#kivy.uix.slider.Slider.cursor_width), [`cursor_height`](https://kivy.org/doc/stable/#kivy.uix.slider.Slider.cursor_height)) properties.

**kivy.uix.slider.Slider.cursor_width**

Width of the cursor image.
[`cursor_width`](https://kivy.org/doc/stable/#kivy.uix.slider.Slider.cursor_width) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 32sp.

**kivy.uix.slider.Slider.max**

Maximum value allowed for [`value`](https://kivy.org/doc/stable/#kivy.uix.slider.Slider.value).
[`max`](https://kivy.org/doc/stable/#kivy.uix.slider.Slider.max) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and defaults to
100.

**kivy.uix.slider.Slider.min**

Minimum value allowed for [`value`](https://kivy.org/doc/stable/#kivy.uix.slider.Slider.value).
[`min`](https://kivy.org/doc/stable/#kivy.uix.slider.Slider.min) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and defaults to
0.

**kivy.uix.slider.Slider.on_touch_down**

Receive a touch down event.

**kivy.uix.slider.Slider.on_touch_move**

Receive a touch move event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivy.org/doc/stable/#kivy.uix.slider.Slider.on_touch_down) for more information.

**kivy.uix.slider.Slider.on_touch_up**

Receive a touch up event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivy.org/doc/stable/#kivy.uix.slider.Slider.on_touch_down) for more information.

**kivy.uix.slider.Slider.orientation**

Orientation of the slider.
[`orientation`](https://kivy.org/doc/stable/#kivy.uix.slider.Slider.orientation) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty) and
defaults to ‘horizontal’. Can take a value of ‘vertical’ or ‘horizontal’.

**kivy.uix.slider.Slider.padding**

Padding of the slider. The padding is used for graphical representation
and interaction. It prevents the cursor from going out of the bounds of the
slider bounding box.
By default, padding is 16sp. The range of the slider is reduced from
padding *2 on the screen. It allows drawing the default cursor of 32sp
width without having the cursor go out of the widget.
[`padding`](https://kivy.org/doc/stable/#kivy.uix.slider.Slider.padding) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and defaults
to 16sp.

**kivy.uix.slider.Slider.range**

Range of the slider in the format (minimum value, maximum value):

[`range`](https://kivy.org/doc/stable/#kivy.uix.slider.Slider.range) is a [`ReferenceListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ReferenceListProperty) of
([`min`](https://kivy.org/doc/stable/#kivy.uix.slider.Slider.min), [`max`](https://kivy.org/doc/stable/#kivy.uix.slider.Slider.max)) properties.

**kivy.uix.slider.Slider.sensitivity**

Whether the touch collides with the whole body of the widget
or with the slider handle part only.
New in version 1.10.1.
[`sensitivity`](https://kivy.org/doc/stable/#kivy.uix.slider.Slider.sensitivity) is a [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to ‘all’. Can take a value of ‘all’ or ‘handle’.

**kivy.uix.slider.Slider.step**

Step size of the slider.
New in version 1.4.0.
Determines the size of each interval or step the slider takes between
[`min`](https://kivy.org/doc/stable/#kivy.uix.slider.Slider.min) and [`max`](https://kivy.org/doc/stable/#kivy.uix.slider.Slider.max). If the value range can’t be evenly
divisible by step the last step will be capped by slider.max.
A zero value will result in the smallest possible intervals/steps,
calculated from the (pixel) position of the slider.
[`step`](https://kivy.org/doc/stable/#kivy.uix.slider.Slider.step) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and defaults
to 0.

**kivy.uix.slider.Slider.value**

Current value used for the slider.
[`value`](https://kivy.org/doc/stable/#kivy.uix.slider.Slider.value) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and defaults
to 0.

**kivy.uix.slider.Slider.value_normalized**

Normalized value inside the [`range`](https://kivy.org/doc/stable/#kivy.uix.slider.Slider.range) (min/max) to 0-1 range:

You can also use it for setting the real value without knowing the minimum
and maximum:

[`value_normalized`](https://kivy.org/doc/stable/#kivy.uix.slider.Slider.value_normalized) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty).

**kivy.uix.slider.Slider.value_pos**

Position of the internal cursor, based on the normalized value.
[`value_pos`](https://kivy.org/doc/stable/#kivy.uix.slider.Slider.value_pos) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty).

**kivy.uix.slider.Slider.value_track**

Decides if slider should draw the line indicating the
space between [`min`](https://kivy.org/doc/stable/#kivy.uix.slider.Slider.min) and [`value`](https://kivy.org/doc/stable/#kivy.uix.slider.Slider.value) properties values.
[`value_track`](https://kivy.org/doc/stable/#kivy.uix.slider.Slider.value_track) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivy.uix.slider.Slider.value_track_color**

Color of the `value_line` in rgba format.
[`value_track_color`](https://kivy.org/doc/stable/#kivy.uix.slider.Slider.value_track_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to [1, 1, 1, 1].
Changed in version 2.0.0:Changed from [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) to
[`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty).

**kivy.uix.slider.Slider.value_track_width**

Width of the track line.
[`value_track_width`](https://kivy.org/doc/stable/#kivy.uix.slider.Slider.value_track_width) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 3dp.

---

## API - [`kivy.uix.spinner`](https://kivy.org/doc/stable/api-kivy.uix.spinner.html)

**kivy.uix.spinner.Spinner**

Bases: [`kivy.uix.button.Button`](https://kivy.org/doc/stable/api-kivy.uix.button.html#kivy.uix.button.Button)
Spinner class, see module documentation for more information.

**kivy.uix.spinner.Spinner.dropdown_cls**

Class used to display the dropdown list when the Spinner is pressed.
[`dropdown_cls`](https://kivy.org/doc/stable/#kivy.uix.spinner.Spinner.dropdown_cls) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to [`DropDown`](https://kivy.org/doc/stable/api-kivy.uix.dropdown.html#kivy.uix.dropdown.DropDown).
Changed in version 1.8.0:If set to a string, the [`Factory`](https://kivy.org/doc/stable/api-kivy.factory.html#kivy.factory.Factory) will be used to
resolve the class name.

**kivy.uix.spinner.Spinner.is_open**

By default, the spinner is not open. Set to True to open it.
[`is_open`](https://kivy.org/doc/stable/#kivy.uix.spinner.Spinner.is_open) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to False.
New in version 1.4.0.

**kivy.uix.spinner.Spinner.option_cls**

Class used to display the options within the dropdown list displayed
under the Spinner. The text property of the class will be used to
represent the value.
The option class requires:
a text property, used to display the value.
an on_release event, used to trigger the option when pressed/touched.
a [`size_hint_y`](https://kivy.org/doc/stable/api-kivy.uix.widget.html#kivy.uix.widget.Widget.size_hint_y) of None.
the [`height`](https://kivy.org/doc/stable/api-kivy.uix.widget.html#kivy.uix.widget.Widget.height) to be set.
[`option_cls`](https://kivy.org/doc/stable/#kivy.uix.spinner.Spinner.option_cls) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to [`SpinnerOption`](https://kivy.org/doc/stable/#kivy.uix.spinner.SpinnerOption).
Changed in version 1.8.0:If you set a string, the [`Factory`](https://kivy.org/doc/stable/api-kivy.factory.html#kivy.factory.Factory) will be used to
resolve the class.

**kivy.uix.spinner.Spinner.sync_height**

Each element in a dropdown list uses a default/user-supplied height.
Set to True to propagate the Spinner’s height value to each dropdown
list element.
New in version 1.10.0.
[`sync_height`](https://kivy.org/doc/stable/#kivy.uix.spinner.Spinner.sync_height) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to False.

**kivy.uix.spinner.Spinner.text_autoupdate**

Indicates if the spinner’s `text` should be automatically
updated with the first value of the [`values`](https://kivy.org/doc/stable/#kivy.uix.spinner.Spinner.values) property.
Setting it to True will cause the spinner to update its `text`
property every time attr:values are changed.
New in version 1.10.0.
[`text_autoupdate`](https://kivy.org/doc/stable/#kivy.uix.spinner.Spinner.text_autoupdate) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to False.

**kivy.uix.spinner.Spinner.values**

Values that can be selected by the user. It must be a list of strings.
[`values`](https://kivy.org/doc/stable/#kivy.uix.spinner.Spinner.values) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) and defaults to
[].

**kivy.uix.spinner.SpinnerOption**

Bases: [`kivy.uix.button.Button`](https://kivy.org/doc/stable/api-kivy.uix.button.html#kivy.uix.button.Button)
Special button used in the [`Spinner`](https://kivy.org/doc/stable/#kivy.uix.spinner.Spinner) dropdown list. By default,
this is just a [`Button`](https://kivy.org/doc/stable/api-kivy.uix.button.html#kivy.uix.button.Button) with a size_hint_y of None
and a height of [`48dp`](https://kivy.org/doc/stable/api-kivy.metrics.html#kivy.metrics.dp).

---

## API - [`kivy.uix.splitter`](https://kivy.org/doc/stable/api-kivy.uix.splitter.html)

**kivy.uix.splitter.Splitter**

Bases: [`kivy.uix.boxlayout.BoxLayout`](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html#kivy.uix.boxlayout.BoxLayout)
See module documentation.

Changed in version 1.6.0:Added on_press and on_release events.

**kivy.uix.splitter.Splitter.add_widget**

Add a new widget as a child of this widget.

**kivy.uix.splitter.Splitter.border**

Border used for the
[`BorderImage`](https://kivy.org/doc/stable/api-kivy.graphics.vertex_instructions.html#kivy.graphics.vertex_instructions.BorderImage)
graphics instruction.
This must be a list of four values: (bottom, right, top, left).
Read the BorderImage instructions for more information about how
to use it.
[`border`](https://kivy.org/doc/stable/#kivy.uix.splitter.Splitter.border) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) and
defaults to (4, 4, 4, 4).

**kivy.uix.splitter.Splitter.clear_widgets**

Remove all (or the specified) `children` of this widget.
If the ‘children’ argument is specified, it should be a list (or
filtered list) of children of the current widget.
Changed in version 1.8.0:The children argument can be used to specify the children you
want to remove.
Changed in version 2.1.0:Specifying an empty `children` list leaves the widgets unchanged.
Previously it was treated like `None` and all children were
removed.

**kivy.uix.splitter.Splitter.keep_within_parent**

If True, will limit the splitter to stay within its parent widget.
[`keep_within_parent`](https://kivy.org/doc/stable/#kivy.uix.splitter.Splitter.keep_within_parent) is a
[`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and defaults to False.
New in version 1.9.0.

**kivy.uix.splitter.Splitter.max_size**

Specifies the maximum size beyond which the widget is not resizable.
[`max_size`](https://kivy.org/doc/stable/#kivy.uix.splitter.Splitter.max_size) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 500pt.

**kivy.uix.splitter.Splitter.min_size**

Specifies the minimum size beyond which the widget is not resizable.
[`min_size`](https://kivy.org/doc/stable/#kivy.uix.splitter.Splitter.min_size) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 100pt.

**kivy.uix.splitter.Splitter.remove_widget**

Remove a widget from the children of this widget.

**kivy.uix.splitter.Splitter.rescale_with_parent**

If True, will automatically change size to take up the same
proportion of the parent widget when it is resized, while
staying within [`min_size`](https://kivy.org/doc/stable/#kivy.uix.splitter.Splitter.min_size) and [`max_size`](https://kivy.org/doc/stable/#kivy.uix.splitter.Splitter.max_size). As long as
these attributes can be satisfied, this stops the
[`Splitter`](https://kivy.org/doc/stable/#kivy.uix.splitter.Splitter) from exceeding the parent size during rescaling.
[`rescale_with_parent`](https://kivy.org/doc/stable/#kivy.uix.splitter.Splitter.rescale_with_parent) is a
[`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and defaults to False.
New in version 1.9.0.

**kivy.uix.splitter.Splitter.sizable_from**

Specifies whether the widget is resizable. Options are:
left, right, top or bottom
[`sizable_from`](https://kivy.org/doc/stable/#kivy.uix.splitter.Splitter.sizable_from) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty)
and defaults to left.

**kivy.uix.splitter.Splitter.strip_cls**

Specifies the class of the resize Strip.
[`strip_cls`](https://kivy.org/doc/stable/#kivy.uix.splitter.Splitter.strip_cls) is an [`kivy.properties.ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to `SplitterStrip`, which is of type
[`Button`](https://kivy.org/doc/stable/api-kivy.uix.button.html#kivy.uix.button.Button).
Changed in version 1.8.0:If you set a string, the [`Factory`](https://kivy.org/doc/stable/api-kivy.factory.html#kivy.factory.Factory) will be used to
resolve the class.

**kivy.uix.splitter.Splitter.strip_size**

Specifies the size of resize strip
`strp_size` is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
defaults to 10pt

---

## API - [`kivy.uix.stacklayout`](https://kivy.org/doc/stable/api-kivy.uix.stacklayout.html)

**kivy.uix.stacklayout.StackLayout**

Bases: [`kivy.uix.layout.Layout`](https://kivy.org/doc/stable/api-kivy.uix.layout.html#kivy.uix.layout.Layout)
Stack layout class. See module documentation for more information.

**kivy.uix.stacklayout.StackLayout.do_layout**

This function is called when a layout is called by a trigger.
If you are writing a new Layout subclass, don’t call this function
directly but use `_trigger_layout()` instead.
The function is by default called *before* the next frame, therefore
the layout isn’t updated immediately. Anything depending on the
positions of e.g. children should be scheduled for the next frame.
New in version 1.0.8.

**kivy.uix.stacklayout.StackLayout.minimum_height**

Minimum height needed to contain all children. It is automatically set
by the layout.
New in version 1.0.8.
[`minimum_height`](https://kivy.org/doc/stable/#kivy.uix.stacklayout.StackLayout.minimum_height) is a [`kivy.properties.NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0.

**kivy.uix.stacklayout.StackLayout.minimum_size**

Minimum size needed to contain all children. It is automatically set
by the layout.
New in version 1.0.8.
[`minimum_size`](https://kivy.org/doc/stable/#kivy.uix.stacklayout.StackLayout.minimum_size) is a
[`ReferenceListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ReferenceListProperty) of
([`minimum_width`](https://kivy.org/doc/stable/#kivy.uix.stacklayout.StackLayout.minimum_width), [`minimum_height`](https://kivy.org/doc/stable/#kivy.uix.stacklayout.StackLayout.minimum_height)) properties.

**kivy.uix.stacklayout.StackLayout.minimum_width**

Minimum width needed to contain all children. It is automatically set
by the layout.
New in version 1.0.8.
[`minimum_width`](https://kivy.org/doc/stable/#kivy.uix.stacklayout.StackLayout.minimum_width) is a [`kivy.properties.NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0.

**kivy.uix.stacklayout.StackLayout.orientation**

Orientation of the layout.
[`orientation`](https://kivy.org/doc/stable/#kivy.uix.stacklayout.StackLayout.orientation) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty) and
defaults to ‘lr-tb’.
Valid orientations are ‘lr-tb’, ‘tb-lr’, ‘rl-tb’, ‘tb-rl’, ‘lr-bt’,
‘bt-lr’, ‘rl-bt’ and ‘bt-rl’.
Changed in version 1.5.0:[`orientation`](https://kivy.org/doc/stable/#kivy.uix.stacklayout.StackLayout.orientation) now correctly handles all valid combinations of
‘lr’,’rl’,’tb’,’bt’. Before this version only ‘lr-tb’ and
‘tb-lr’ were supported, and ‘tb-lr’ was misnamed and placed
widgets from bottom to top and from right to left (reversed compared
to what was expected).

**kivy.uix.stacklayout.StackLayout.padding**

Padding between the layout box and it’s children: [padding_left,
padding_top, padding_right, padding_bottom].
padding also accepts a two argument form [padding_horizontal,
padding_vertical] and a single argument form [padding].
Changed in version 1.7.0:Replaced the NumericProperty with a VariableListProperty.
[`padding`](https://kivy.org/doc/stable/#kivy.uix.stacklayout.StackLayout.padding) is a
[`VariableListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.VariableListProperty) and defaults to
[0, 0, 0, 0].

**kivy.uix.stacklayout.StackLayout.spacing**

Spacing between children: [spacing_horizontal, spacing_vertical].
spacing also accepts a single argument form [spacing].
[`spacing`](https://kivy.org/doc/stable/#kivy.uix.stacklayout.StackLayout.spacing) is a
[`VariableListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.VariableListProperty) and defaults to [0, 0].

---

## API - [`kivy.uix.stencilview`](https://kivy.org/doc/stable/api-kivy.uix.stencilview.html)

**kivy.uix.stencilview.StencilView**

Bases: [`kivy.uix.widget.Widget`](https://kivy.org/doc/stable/api-kivy.uix.widget.html#kivy.uix.widget.Widget)
StencilView class. See module documentation for more information.

---

## API - [`kivy.uix.switch`](https://kivy.org/doc/stable/api-kivy.uix.switch.html)

**kivy.uix.switch.Switch**

Bases: [`kivy.uix.widget.Widget`](https://kivy.org/doc/stable/api-kivy.uix.widget.html#kivy.uix.widget.Widget)
Switch class. See module documentation for more information.

**kivy.uix.switch.Switch.active**

Indicate whether the switch is active or inactive.
[`active`](https://kivy.org/doc/stable/#kivy.uix.switch.Switch.active) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and defaults
to False.

**kivy.uix.switch.Switch.active_norm_pos**

(internal) Contains the normalized position of the movable element
inside the switch, in the 0-1 range.
[`active_norm_pos`](https://kivy.org/doc/stable/#kivy.uix.switch.Switch.active_norm_pos) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.

**kivy.uix.switch.Switch.on_touch_down**

Receive a touch down event.

**kivy.uix.switch.Switch.on_touch_move**

Receive a touch move event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivy.org/doc/stable/#kivy.uix.switch.Switch.on_touch_down) for more information.

**kivy.uix.switch.Switch.on_touch_up**

Receive a touch up event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivy.org/doc/stable/#kivy.uix.switch.Switch.on_touch_down) for more information.

**kivy.uix.switch.Switch.touch_control**

(internal) Contains the touch that currently interacts with the switch.
[`touch_control`](https://kivy.org/doc/stable/#kivy.uix.switch.Switch.touch_control) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty)
and defaults to None.

**kivy.uix.switch.Switch.touch_distance**

(internal) Contains the distance between the initial position of the
touch and the current position to determine if the swipe is from the left
or right.
[`touch_distance`](https://kivy.org/doc/stable/#kivy.uix.switch.Switch.touch_distance) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty)
and defaults to 0.

---

## API - [`kivy.uix.tabbedpanel`](https://kivy.org/doc/stable/api-kivy.uix.tabbedpanel.html)

**kivy.uix.tabbedpanel.StripLayout**

Bases: [`kivy.uix.gridlayout.GridLayout`](https://kivy.org/doc/stable/api-kivy.uix.gridlayout.html#kivy.uix.gridlayout.GridLayout)
The main layout that is used to house the entire tabbedpanel strip
including the blank areas in case the tabs don’t cover the entire
width/height.
New in version 1.8.0.

**kivy.uix.tabbedpanel.StripLayout.background_image**

Background image to be used for the Strip layout of the TabbedPanel.
[`background_image`](https://kivy.org/doc/stable/#kivy.uix.tabbedpanel.StripLayout.background_image) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to a transparent image.

**kivy.uix.tabbedpanel.StripLayout.border**

Border property for the [`background_image`](https://kivy.org/doc/stable/#kivy.uix.tabbedpanel.StripLayout.background_image).
[`border`](https://kivy.org/doc/stable/#kivy.uix.tabbedpanel.StripLayout.border) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) and defaults
to [4, 4, 4, 4]

**kivy.uix.tabbedpanel.TabbedPanel**

Bases: [`kivy.uix.gridlayout.GridLayout`](https://kivy.org/doc/stable/api-kivy.uix.gridlayout.html#kivy.uix.gridlayout.GridLayout)
The TabbedPanel class. See module documentation for more information.

**kivy.uix.tabbedpanel.TabbedPanel.add_widget**

Add a new widget as a child of this widget.

**kivy.uix.tabbedpanel.TabbedPanel.background_color**

Background color, in the format (r, g, b, a).
[`background_color`](https://kivy.org/doc/stable/#kivy.uix.tabbedpanel.TabbedPanel.background_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty) and
defaults to [1, 1, 1, 1].
Changed in version 2.0.0:Changed from [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) to
[`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty).

**kivy.uix.tabbedpanel.TabbedPanel.background_disabled_image**

Background image of the main shared content object when disabled.
New in version 1.8.0.
[`background_disabled_image`](https://kivy.org/doc/stable/#kivy.uix.tabbedpanel.TabbedPanel.background_disabled_image) is a
[`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults to
‘atlas://data/images/defaulttheme/tab’.

**kivy.uix.tabbedpanel.TabbedPanel.background_image**

Background image of the main shared content object.
[`background_image`](https://kivy.org/doc/stable/#kivy.uix.tabbedpanel.TabbedPanel.background_image) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to ‘atlas://data/images/defaulttheme/tab’.

**kivy.uix.tabbedpanel.TabbedPanel.bar_width**

Width of the horizontal scroll bar. The width is interpreted
as a height for the horizontal bar.
New in version 2.2.0.
[`bar_width`](https://kivy.org/doc/stable/#kivy.uix.tabbedpanel.TabbedPanel.bar_width) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 2.

**kivy.uix.tabbedpanel.TabbedPanel.border**

Border used for [`BorderImage`](https://kivy.org/doc/stable/api-kivy.graphics.vertex_instructions.html#kivy.graphics.vertex_instructions.BorderImage)
graphics instruction, used itself for [`background_image`](https://kivy.org/doc/stable/#kivy.uix.tabbedpanel.TabbedPanel.background_image).
Can be changed for a custom background.
It must be a list of four values: (bottom, right, top, left). Read the
BorderImage instructions for more information.
[`border`](https://kivy.org/doc/stable/#kivy.uix.tabbedpanel.TabbedPanel.border) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) and
defaults to (16, 16, 16, 16)

**kivy.uix.tabbedpanel.TabbedPanel.clear_widgets**

Remove all (or the specified) `children` of this widget.
If the ‘children’ argument is specified, it should be a list (or
filtered list) of children of the current widget.
Changed in version 1.8.0:The children argument can be used to specify the children you
want to remove.
Changed in version 2.1.0:Specifying an empty `children` list leaves the widgets unchanged.
Previously it was treated like `None` and all children were
removed.

**kivy.uix.tabbedpanel.TabbedPanel.content**

This is the object holding (current_tab’s content is added to this)
the content of the current tab. To Listen to the changes in the content
of the current tab, you should bind to current_tabs content property.
[`content`](https://kivy.org/doc/stable/#kivy.uix.tabbedpanel.TabbedPanel.content) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to ‘None’.

**kivy.uix.tabbedpanel.TabbedPanel.current_tab**

Links to the currently selected or active tab.
New in version 1.4.0.
[`current_tab`](https://kivy.org/doc/stable/#kivy.uix.tabbedpanel.TabbedPanel.current_tab) is an `AliasProperty`, read-only.

**kivy.uix.tabbedpanel.TabbedPanel.default_tab**

Holds the default tab.

[`default_tab`](https://kivy.org/doc/stable/#kivy.uix.tabbedpanel.TabbedPanel.default_tab) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty).

**kivy.uix.tabbedpanel.TabbedPanel.default_tab_cls**

Specifies the class to use for the styling of the default tab.
New in version 1.4.0.

[`default_tab_cls`](https://kivy.org/doc/stable/#kivy.uix.tabbedpanel.TabbedPanel.default_tab_cls) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty)
and defaults to TabbedPanelHeader. If you set a string, the
[`Factory`](https://kivy.org/doc/stable/api-kivy.factory.html#kivy.factory.Factory) will be used to resolve the class.
Changed in version 1.8.0:The [`Factory`](https://kivy.org/doc/stable/api-kivy.factory.html#kivy.factory.Factory) will resolve the class if a string
is set.

**kivy.uix.tabbedpanel.TabbedPanel.default_tab_content**

Holds the default tab content.
[`default_tab_content`](https://kivy.org/doc/stable/#kivy.uix.tabbedpanel.TabbedPanel.default_tab_content) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty).

**kivy.uix.tabbedpanel.TabbedPanel.default_tab_text**

Specifies the text displayed on the default tab header.
[`default_tab_text`](https://kivy.org/doc/stable/#kivy.uix.tabbedpanel.TabbedPanel.default_tab_text) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to ‘default tab’.

**kivy.uix.tabbedpanel.TabbedPanel.do_default_tab**

Specifies whether a default_tab head is provided.
New in version 1.5.0.
[`do_default_tab`](https://kivy.org/doc/stable/#kivy.uix.tabbedpanel.TabbedPanel.do_default_tab) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to ‘True’.

**kivy.uix.tabbedpanel.TabbedPanel.remove_widget**

Remove a widget from the children of this widget.

**kivy.uix.tabbedpanel.TabbedPanel.scroll_type**

Sets the type of scrolling to use for the content of the scrollview.
Available options are: [‘content’], [‘bars’], [‘bars’, ‘content’].
New in version 2.2.0.
[`scroll_type`](https://kivy.org/doc/stable/#kivy.uix.tabbedpanel.TabbedPanel.scroll_type) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty) and
defaults to [‘content’].

**kivy.uix.tabbedpanel.TabbedPanel.strip_border**

Border to be used on [`strip_image`](https://kivy.org/doc/stable/#kivy.uix.tabbedpanel.TabbedPanel.strip_image).
New in version 1.8.0.
[`strip_border`](https://kivy.org/doc/stable/#kivy.uix.tabbedpanel.TabbedPanel.strip_border) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) and
defaults to [4, 4, 4, 4].

**kivy.uix.tabbedpanel.TabbedPanel.strip_image**

Background image of the tabbed strip.
New in version 1.8.0.
[`strip_image`](https://kivy.org/doc/stable/#kivy.uix.tabbedpanel.TabbedPanel.strip_image) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to a empty image.

**kivy.uix.tabbedpanel.TabbedPanel.switch_to**

Switch to a specific panel header.
Changed in version 1.10.0.
If used with do_scroll=True, it scrolls
to the header’s tab too.
[`switch_to()`](https://kivy.org/doc/stable/#kivy.uix.tabbedpanel.TabbedPanel.switch_to) cannot be called from within the
[`TabbedPanel`](https://kivy.org/doc/stable/#kivy.uix.tabbedpanel.TabbedPanel) or its subclass’ `__init__` method.
If that is required, use the `Clock` to schedule it. See [discussion](https://github.com/kivy/kivy/issues/3493#issuecomment-121567969)
for full example.

**kivy.uix.tabbedpanel.TabbedPanel.tab_height**

Specifies the height of the tab header.
[`tab_height`](https://kivy.org/doc/stable/#kivy.uix.tabbedpanel.TabbedPanel.tab_height) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 40.

**kivy.uix.tabbedpanel.TabbedPanel.tab_list**

List of all the tab headers.
[`tab_list`](https://kivy.org/doc/stable/#kivy.uix.tabbedpanel.TabbedPanel.tab_list) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) and is
read-only.

**kivy.uix.tabbedpanel.TabbedPanel.tab_pos**

Specifies the position of the tabs relative to the content.
Can be one of: left_top, left_mid, left_bottom, top_left,
top_mid, top_right, right_top, right_mid, right_bottom,
bottom_left, bottom_mid, bottom_right.
[`tab_pos`](https://kivy.org/doc/stable/#kivy.uix.tabbedpanel.TabbedPanel.tab_pos) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty) and
defaults to ‘top_left’.

**kivy.uix.tabbedpanel.TabbedPanel.tab_width**

Specifies the width of the tab header.
[`tab_width`](https://kivy.org/doc/stable/#kivy.uix.tabbedpanel.TabbedPanel.tab_width) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 100.

**kivy.uix.tabbedpanel.TabbedPanelContent**

Bases: [`kivy.uix.floatlayout.FloatLayout`](https://kivy.org/doc/stable/api-kivy.uix.floatlayout.html#kivy.uix.floatlayout.FloatLayout)
The TabbedPanelContent class.

**kivy.uix.tabbedpanel.TabbedPanelException**

Bases: `Exception`
The TabbedPanelException class.

**kivy.uix.tabbedpanel.TabbedPanelHeader**

Bases: [`kivy.uix.togglebutton.ToggleButton`](https://kivy.org/doc/stable/api-kivy.uix.togglebutton.html#kivy.uix.togglebutton.ToggleButton)
A Base for implementing a Tabbed Panel Head. A button intended to be
used as a Heading/Tab for a TabbedPanel widget.
You can use this TabbedPanelHeader widget to add a new tab to a
TabbedPanel.

**kivy.uix.tabbedpanel.TabbedPanelHeader.content**

Content to be loaded when this tab header is selected.
[`content`](https://kivy.org/doc/stable/#kivy.uix.tabbedpanel.TabbedPanelHeader.content) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and defaults
to None.

**kivy.uix.tabbedpanel.TabbedPanelHeader.on_touch_down**

Receive a touch down event.

**kivy.uix.tabbedpanel.TabbedPanelItem**

Bases: [`kivy.uix.tabbedpanel.TabbedPanelHeader`](https://kivy.org/doc/stable/#kivy.uix.tabbedpanel.TabbedPanelHeader)
This is a convenience class that provides a header of type
TabbedPanelHeader and links it with the content automatically. Thus
facilitating you to simply do the following in kv language:

New in version 1.5.0.

**kivy.uix.tabbedpanel.TabbedPanelItem.add_widget**

Add a new widget as a child of this widget.

**kivy.uix.tabbedpanel.TabbedPanelItem.remove_widget**

Remove a widget from the children of this widget.

**kivy.uix.tabbedpanel.TabbedPanelStrip**

Bases: [`kivy.uix.gridlayout.GridLayout`](https://kivy.org/doc/stable/api-kivy.uix.gridlayout.html#kivy.uix.gridlayout.GridLayout)
A strip intended to be used as background for Heading/Tab.
This does not cover the blank areas in case the tabs don’t cover
the entire width/height of the TabbedPanel(use [`StripLayout`](https://kivy.org/doc/stable/#kivy.uix.tabbedpanel.StripLayout)
for that).

**kivy.uix.tabbedpanel.TabbedPanelStrip.tabbed_panel**

Link to the panel that the tab strip is a part of.
[`tabbed_panel`](https://kivy.org/doc/stable/#kivy.uix.tabbedpanel.TabbedPanelStrip.tabbed_panel) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to None .

---

## API - [`kivy.uix.textinput`](https://kivy.org/doc/stable/api-kivy.uix.textinput.html)

**kivy.uix.textinput.TextInput**

Bases: [`kivy.uix.behaviors.focus.FocusBehavior`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.focus.html#kivy.uix.behaviors.focus.FocusBehavior), [`kivy.uix.widget.Widget`](https://kivy.org/doc/stable/api-kivy.uix.widget.html#kivy.uix.widget.Widget)
TextInput class. See module documentation for more information.

Changed in version 1.10.0:background_disabled_active has been removed.
Changed in version 1.9.0:[`TextInput`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput) now inherits from
[`FocusBehavior`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.html#kivy.uix.behaviors.FocusBehavior).
[`keyboard_mode`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.html#kivy.uix.behaviors.FocusBehavior.keyboard_mode),
[`show_keyboard()`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.html#kivy.uix.behaviors.FocusBehavior.show_keyboard),
[`hide_keyboard()`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.html#kivy.uix.behaviors.FocusBehavior.hide_keyboard),
[`focus()`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.html#kivy.uix.behaviors.FocusBehavior.focus),
and [`input_type`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.html#kivy.uix.behaviors.FocusBehavior.input_type)
have been removed since they are now inherited
from [`FocusBehavior`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.html#kivy.uix.behaviors.FocusBehavior).
Changed in version 1.7.0:on_double_tap, on_triple_tap and on_quad_touch events added.
Changed in version 2.1.0:[`keyboard_suggestions`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.html#kivy.uix.behaviors.FocusBehavior.keyboard_suggestions)
is now inherited from [`FocusBehavior`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.html#kivy.uix.behaviors.FocusBehavior).

**kivy.uix.textinput.TextInput.allow_copy**

Decides whether to allow copying the text.
New in version 1.8.0.
[`allow_copy`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.allow_copy) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to True.

**kivy.uix.textinput.TextInput.auto_indent**

Automatically indent multiline text.
New in version 1.7.0.
[`auto_indent`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.auto_indent) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to False.

**kivy.uix.textinput.TextInput.background_active**

Background image of the TextInput when it’s in focus.
New in version 1.4.1.
[`background_active`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.background_active) is a
[`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to ‘atlas://data/images/defaulttheme/textinput_active’.

**kivy.uix.textinput.TextInput.background_color**

Current color of the background, in (r, g, b, a) format.
New in version 1.2.0.
[`background_color`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.background_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to [1, 1, 1, 1] (white).
Changed in version 2.0.0:Changed from [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) to
[`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty).

**kivy.uix.textinput.TextInput.background_disabled_normal**

Background image of the TextInput when disabled.
New in version 1.8.0.
[`background_disabled_normal`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.background_disabled_normal) is a
[`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to ‘atlas://data/images/defaulttheme/textinput_disabled’.

**kivy.uix.textinput.TextInput.background_normal**

Background image of the TextInput when it’s not in focus.
New in version 1.4.1.
[`background_normal`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.background_normal) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to ‘atlas://data/images/defaulttheme/textinput’.

**kivy.uix.textinput.TextInput.base_direction**

Base direction of text, this impacts horizontal alignment when
[`halign`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.halign) is auto (the default). Available options are: None,
“ltr” (left to right), “rtl” (right to left) plus “weak_ltr” and
“weak_rtl”.

New in version 1.10.1.
[`base_direction`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.base_direction) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty) and
defaults to None (autodetect RTL if possible, otherwise LTR).

**kivy.uix.textinput.TextInput.border**

Border used for [`BorderImage`](https://kivy.org/doc/stable/api-kivy.graphics.vertex_instructions.html#kivy.graphics.vertex_instructions.BorderImage)
graphics instruction. Used with [`background_normal`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.background_normal) and
[`background_active`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.background_active). Can be used for a custom background.
New in version 1.4.1.
It must be a list of four values: (bottom, right, top, left). Read the
BorderImage instruction for more information about how to use it.
[`border`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.border) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) and defaults
to (4, 4, 4, 4).

**kivy.uix.textinput.TextInput.cancel_selection**

Cancel current selection (if any).

**kivy.uix.textinput.TextInput.copy**

Copy the value provided in argument data into current clipboard.
If data is not of type string it will be converted to string.
If no data is provided then current selection if present is copied.
New in version 1.8.0.

**kivy.uix.textinput.TextInput.cursor**

Tuple of (col, row) values indicating the current cursor position.
You can set a new (col, row) if you want to move the cursor. The scrolling
area will be automatically updated to ensure that the cursor is
visible inside the viewport.
[`cursor`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.cursor) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty).

**kivy.uix.textinput.TextInput.cursor_blink**

This property is used to set whether the graphic cursor should blink
or not.
Changed in version 1.10.1:cursor_blink has been refactored to enable switching the blinking
on/off and the previous behavior has been moved to a private
_cursor_blink property. The previous default value False has been
changed to True.
[`cursor_blink`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.cursor_blink) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to True.

**kivy.uix.textinput.TextInput.cursor_col**

Current column of the cursor.
[`cursor_col`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.cursor_col) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) to
cursor[0], read-only.

**kivy.uix.textinput.TextInput.cursor_color**

Current color of the cursor, in (r, g, b, a) format.
New in version 1.9.0.
[`cursor_color`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.cursor_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty) and
defaults to [1, 0, 0, 1].
Changed in version 2.0.0:Changed from [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) to
[`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty).

**kivy.uix.textinput.TextInput.cursor_index**

Return the cursor index in the text/value.

**kivy.uix.textinput.TextInput.cursor_offset**

Get the cursor x offset on the current line.

**kivy.uix.textinput.TextInput.cursor_pos**

Current position of the cursor, in (x, y).
[`cursor_pos`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.cursor_pos) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty),
read-only.

**kivy.uix.textinput.TextInput.cursor_row**

Current row of the cursor.
[`cursor_row`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.cursor_row) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) to
cursor[1], read-only.

**kivy.uix.textinput.TextInput.cursor_width**

Current width of the cursor.
New in version 1.10.0.
[`cursor_width`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.cursor_width) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to ‘1sp’.

**kivy.uix.textinput.TextInput.cut**

Copy current selection to clipboard then delete it from TextInput.
New in version 1.8.0.

**kivy.uix.textinput.TextInput.delete_selection**

Delete the current text selection (if any).

**kivy.uix.textinput.TextInput.disabled_foreground_color**

Current color of the foreground when disabled, in (r, g, b, a) format.
New in version 1.8.0.
[`disabled_foreground_color`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.disabled_foreground_color) is a
[`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty) and
defaults to [0, 0, 0, 5] (50% transparent black).
Changed in version 2.0.0:Changed from [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) to
[`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty).

**kivy.uix.textinput.TextInput.do_backspace**

Do backspace operation from the current cursor position.
This action might do several things:
removing the current selection if available.
removing the previous char and move the cursor back.
do nothing, if we are at the start.

**kivy.uix.textinput.TextInput.do_cursor_movement**

Move the cursor relative to its current position.
Action can be one of :
cursor_left: move the cursor to the left
cursor_right: move the cursor to the right
cursor_up: move the cursor on the previous line
cursor_down: move the cursor on the next line
cursor_home: move the cursor at the start of the current line
cursor_end: move the cursor at the end of current line
cursor_pgup: move one “page” before
cursor_pgdown: move one “page” after
In addition, the behavior of certain actions can be modified:
control + cursor_left: move the cursor one word to the left
control + cursor_right: move the cursor one word to the right
control + cursor_up: scroll up one line
control + cursor_down: scroll down one line
control + cursor_home: go to beginning of text
control + cursor_end: go to end of text
alt + cursor_up: shift line(s) up
alt + cursor_down: shift line(s) down
Changed in version 1.9.1.

**kivy.uix.textinput.TextInput.do_redo**

Do redo operation.
New in version 1.3.0.
This action re-does any command that has been un-done by
do_undo/ctrl+z. This function is automatically called when
ctrl+r keys are pressed.

**kivy.uix.textinput.TextInput.do_undo**

Do undo operation.
New in version 1.3.0.
This action un-does any edits that have been made since the last
call to reset_undo().
This function is automatically called when ctrl+z keys are pressed.

**kivy.uix.textinput.TextInput.do_wrap**

If True, and the text is multiline, then lines larger than the width of
the widget will wrap around to the next line, avoiding the need for
horizontal scrolling. Disabling this option ensure one line is always
displayed as one line.
[`do_wrap`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.do_wrap) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and defaults
to True.
versionadded:: 2.1.0

**kivy.uix.textinput.TextInput.font_context**

Font context. None means the font is used in isolation, so you are
guaranteed to be drawing with the TTF file resolved by [`font_name`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.font_name).
Specifying a value here will load the font file into a named context,
enabling fallback between all fonts in the same context. If a font
context is set, you are not guaranteed that rendering will actually use
the specified TTF file for all glyphs (Pango will pick the one it
thinks is best).
If Kivy is linked against a system-wide installation of FontConfig,
you can load the system fonts by specifying a font context starting
with the special string system://. This will load the system
fontconfig configuration, and add your application-specific fonts on
top of it (this imposes a significant risk of family name collision,
Pango may not use your custom font file, but pick one from the system)

New in version 1.10.1.
[`font_context`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.font_context) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to None.

**kivy.uix.textinput.TextInput.font_family**

Font family, this is only applicable when using [`font_context`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.font_context)
option. The specified font family will be requested, but note that it may
not be available, or there could be multiple fonts registered with the
same family. The value can be a family name (string) available in the
font context (for example a system font in a system:// context, or a
custom font file added using `kivy.core.text.FontContextManager`).
If set to None, font selection is controlled by the [`font_name`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.font_name)
setting.

New in version 1.10.1.
[`font_family`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.font_family) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to None.

**kivy.uix.textinput.TextInput.font_name**

Filename of the font to use. The path can be absolute or relative.
Relative paths are resolved by the [`resource_find()`](https://kivy.org/doc/stable/api-kivy.resources.html#kivy.resources.resource_find)
function.

[`font_name`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.font_name) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to ‘Roboto’. This value is taken
from [`Config`](https://kivy.org/doc/stable/api-kivy.config.html#kivy.config.Config).

**kivy.uix.textinput.TextInput.font_size**

Font size of the text in pixels.
[`font_size`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.font_size) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 15 [`sp`](https://kivy.org/doc/stable/api-kivy.metrics.html#kivy.metrics.sp).

**kivy.uix.textinput.TextInput.foreground_color**

Current color of the foreground, in (r, g, b, a) format.
New in version 1.2.0.
[`foreground_color`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.foreground_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to [0, 0, 0, 1] (black).
Changed in version 2.0.0:Changed from [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) to
[`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty).

**kivy.uix.textinput.TextInput.get_cursor_from_index**

Return the (col, row) of the cursor from text index.

**kivy.uix.textinput.TextInput.get_cursor_from_xy**

Return the (col, row) of the cursor from an (x, y) position.

**kivy.uix.textinput.TextInput.get_max_scroll_x**

Return how many pixels it needs to scroll to the right
to reveal the remaining content of a text that extends
beyond the visible width of a TextInput

**kivy.uix.textinput.TextInput.halign**

Horizontal alignment of the text.
[`halign`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.halign) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty) and
defaults to ‘auto’. Available options are : auto, left, center and right.
Auto will attempt to autodetect horizontal alignment for RTL text (Pango
only), otherwise it behaves like left.
New in version 1.10.1.

**kivy.uix.textinput.TextInput.handle_image_left**

Image used to display the Left handle on the TextInput for selection.
New in version 1.8.0.
[`handle_image_left`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.handle_image_left) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to ‘atlas://data/images/defaulttheme/selector_left’.

**kivy.uix.textinput.TextInput.handle_image_middle**

Image used to display the middle handle on the TextInput for cursor
positioning.
New in version 1.8.0.
[`handle_image_middle`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.handle_image_middle) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘atlas://data/images/defaulttheme/selector_middle’.

**kivy.uix.textinput.TextInput.handle_image_right**

Image used to display the Right handle on the TextInput for selection.
New in version 1.8.0.
[`handle_image_right`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.handle_image_right) is a
[`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults to
‘atlas://data/images/defaulttheme/selector_right’.

**kivy.uix.textinput.TextInput.hint_text**

Hint text of the widget, shown if text is ‘’.
New in version 1.6.0.
Changed in version 1.10.0:The property is now an AliasProperty and byte values are decoded to
strings. The hint text will stay visible when the widget is focused.
[`hint_text`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.hint_text) a [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) and defaults
to ‘’.

**kivy.uix.textinput.TextInput.hint_text_color**

Current color of the hint_text text, in (r, g, b, a) format.
New in version 1.6.0.
[`hint_text_color`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.hint_text_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty) and
defaults to [0.5, 0.5, 0.5, 1.0] (grey).
Changed in version 2.0.0:Changed from [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) to
[`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty).

**kivy.uix.textinput.TextInput.input_filter**

Filters the input according to the specified mode, if not None. If
None, no filtering is applied.
New in version 1.9.0.
[`input_filter`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.input_filter) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to None. Can be one of None, ‘int’ (string), or ‘float’
(string), or a callable. If it is ‘int’, it will only accept numbers.
If it is ‘float’ it will also accept a single period. Finally, if it is
a callable it will be called with two parameters; the string to be added
and a bool indicating whether the string is a result of undo (True). The
callable should return a new substring that will be used instead.

**kivy.uix.textinput.TextInput.insert_text**

Insert new text at the current cursor position. Override this
function in order to pre-process text for input validation.

**kivy.uix.textinput.TextInput.keyboard_on_key_down**

The method bound to the keyboard when the instance has focus.
When the instance becomes focused, this method is bound to the
keyboard and will be called for every input press. The parameters are
the same as [`kivy.core.window.WindowBase.on_key_down()`](https://kivy.org/doc/stable/api-kivy.core.window.html#kivy.core.window.WindowBase.on_key_down).
When overwriting the method in the derived widget, super should be
called to enable tab cycling. If the derived widget wishes to use tab
for its own purposes, it can call super after it has processed the
character (if it does not wish to consume the tab).
Similar to other keyboard functions, it should return True if the
key was consumed.

**kivy.uix.textinput.TextInput.keyboard_on_key_up**

The method bound to the keyboard when the instance has focus.
When the instance becomes focused, this method is bound to the
keyboard and will be called for every input release. The parameters are
the same as [`kivy.core.window.WindowBase.on_key_up()`](https://kivy.org/doc/stable/api-kivy.core.window.html#kivy.core.window.WindowBase.on_key_up).
When overwriting the method in the derived widget, super should be
called to enable de-focusing on escape. If the derived widget wishes
to use escape for its own purposes, it can call super after it has
processed the character (if it does not wish to consume the escape).
See [`keyboard_on_key_down()`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.keyboard_on_key_down)

**kivy.uix.textinput.TextInput.line_height**

Height of a line. This property is automatically computed from the
[`font_name`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.font_name), [`font_size`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.font_size). Changing the line_height will have
no impact.

[`line_height`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.line_height) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty),
read-only.

**kivy.uix.textinput.TextInput.line_spacing**

Space taken up between the lines.
New in version 1.8.0.
[`line_spacing`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.line_spacing) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0.

**kivy.uix.textinput.TextInput.lines_to_scroll**

Set how many lines will be scrolled at once when using the mouse scroll
wheel.
New in version 2.2.0.
`lines_to_scroll is a
:class:`~kivy.properties.BoundedNumericProperty` and defaults to 3, the
minimum is 1.

**kivy.uix.textinput.TextInput.minimum_height**

Minimum height of the content inside the TextInput.
New in version 1.8.0.
[`minimum_height`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.minimum_height) is a readonly
[`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty).

**kivy.uix.textinput.TextInput.multiline**

If True, the widget will be able show multiple lines of text. If False,
the “enter” keypress will defocus the textinput instead of adding a new
line.
[`multiline`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.multiline) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to True.

**kivy.uix.textinput.TextInput.on_cursor**

When the cursor is moved, reset cursor blinking to keep it showing,
and update all the graphics.

**kivy.uix.textinput.TextInput.on_cursor_blink**

trigger blink event reset to switch blinking while focused

**kivy.uix.textinput.TextInput.on_double_tap**

This event is dispatched when a double tap happens
inside TextInput. The default behavior is to select the
word around the current cursor position. Override this to provide
different behavior. Alternatively, you can bind to this
event to provide additional functionality.

**kivy.uix.textinput.TextInput.on_quad_touch**

This event is dispatched when four fingers are touching
inside TextInput. The default behavior is to select all text.
Override this to provide different behavior. Alternatively,
you can bind to this event to provide additional functionality.

**kivy.uix.textinput.TextInput.on_touch_down**

Receive a touch down event.

**kivy.uix.textinput.TextInput.on_touch_move**

Receive a touch move event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.on_touch_down) for more information.

**kivy.uix.textinput.TextInput.on_touch_up**

Receive a touch up event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.on_touch_down) for more information.

**kivy.uix.textinput.TextInput.on_triple_tap**

This event is dispatched when a triple tap happens
inside TextInput. The default behavior is to select the
line around current cursor position. Override this to provide
different behavior. Alternatively, you can bind to this
event to provide additional functionality.

**kivy.uix.textinput.TextInput.padding**

Padding of the text: [padding_left, padding_top, padding_right,
padding_bottom].
padding also accepts a two argument form [padding_horizontal,
padding_vertical] and a one argument form [padding].
Changed in version 1.7.0:Replaced AliasProperty with VariableListProperty.
[`padding`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.padding) is a [`VariableListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.VariableListProperty) and
defaults to [6, 6, 6, 6].

**kivy.uix.textinput.TextInput.padding_x**

Horizontal padding of the text: [padding_left, padding_right].
padding_x also accepts a one argument form [padding_horizontal].
[`padding_x`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.padding_x) is a [`VariableListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.VariableListProperty) and
defaults to [0, 0]. This might be changed by the current theme.
Deprecated since version 1.7.0:Use [`padding`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.padding) instead.

**kivy.uix.textinput.TextInput.padding_y**

Vertical padding of the text: [padding_top, padding_bottom].
padding_y also accepts a one argument form [padding_vertical].
[`padding_y`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.padding_y) is a [`VariableListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.VariableListProperty) and
defaults to [0, 0]. This might be changed by the current theme.
Deprecated since version 1.7.0:Use [`padding`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.padding) instead.

**kivy.uix.textinput.TextInput.password**

If True, the widget will display its characters as the character
set in [`password_mask`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.password_mask).
New in version 1.2.0.
[`password`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.password) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to False.

**kivy.uix.textinput.TextInput.password_mask**

Sets the character used to mask the text when [`password`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.password) is True.
New in version 1.10.0.
[`password_mask`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.password_mask) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to ‘*’.

**kivy.uix.textinput.TextInput.paste**

Insert text from system `Clipboard`
into the [`TextInput`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput) at current cursor
position.
New in version 1.8.0.

**kivy.uix.textinput.TextInput.pgmove_speed**

how much vertical distance hitting pg_up or pg_down will move

**kivy.uix.textinput.TextInput.readonly**

If True, the user will not be able to change the content of a textinput.
New in version 1.3.0.
[`readonly`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.readonly) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to False.

**kivy.uix.textinput.TextInput.replace_crlf**

Automatically replace CRLF with LF.
New in version 1.9.1.
[`replace_crlf`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.replace_crlf) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to True.

**kivy.uix.textinput.TextInput.reset_undo**

Reset undo and redo lists from memory.
New in version 1.3.0.

**kivy.uix.textinput.TextInput.scroll_distance**

Minimum distance to move before change from scroll to selection mode, in
pixels.
It is advisable that you base this value on the dpi of your target device’s
screen.
New in version 2.1.0.
[`scroll_distance`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.scroll_distance) is a NumericProperty and defaults to 20 pixels.

**kivy.uix.textinput.TextInput.scroll_from_swipe**

Allow to scroll the text using swipe gesture according to
[`scroll_timeout`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.scroll_timeout) and [`scroll_distance`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.scroll_distance).
New in version 2.1.0.
[`scroll_from_swipe`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.scroll_from_swipe) is a BooleanProperty and defaults to True on
mobile OS’s, False on desktop OS’s.

**kivy.uix.textinput.TextInput.scroll_timeout**

Timeout allowed to trigger the [`scroll_distance`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.scroll_distance), in milliseconds.
If the user has not moved [`scroll_distance`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.scroll_distance) within the timeout, the
scrolling will be disabled, and the selection mode will start.
New in version 2.1.0.
[`scroll_timeout`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.scroll_timeout) is a NumericProperty and defaults to 250
milliseconds.

**kivy.uix.textinput.TextInput.scroll_x**

X scrolling value of the viewport. The scrolling is automatically
updated when the cursor is moved or text changed. If there is no
user input, the scroll_x and scroll_y properties may be changed.
[`scroll_x`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.scroll_x) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0.

**kivy.uix.textinput.TextInput.scroll_y**

Y scrolling value of the viewport. See [`scroll_x`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.scroll_x) for more
information.
[`scroll_y`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.scroll_y) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0.

**kivy.uix.textinput.TextInput.select_all**

Select all of the text displayed in this TextInput.
New in version 1.4.0.

**kivy.uix.textinput.TextInput.select_text**

Select a portion of text displayed in this TextInput.
New in version 1.4.0.

**kivy.uix.textinput.TextInput.selection_color**

Current color of the selection, in (r, g, b, a) format.

[`selection_color`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.selection_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty) and
defaults to [0.1843, 0.6549, 0.8313, .5].
Changed in version 2.0.0:Changed from [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) to
[`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty).

**kivy.uix.textinput.TextInput.selection_from**

If a selection is in progress or complete, this property will represent
the cursor index where the selection started.
Changed in version 1.4.0:[`selection_from`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.selection_from) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty)
and defaults to None, readonly.

**kivy.uix.textinput.TextInput.selection_text**

Current content selection.
[`selection_text`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.selection_text) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘’, readonly.

**kivy.uix.textinput.TextInput.selection_to**

If a selection is in progress or complete, this property will represent
the cursor index where the selection started.
Changed in version 1.4.0:[`selection_to`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.selection_to) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) and
defaults to None, readonly.

**kivy.uix.textinput.TextInput.tab_width**

By default, each tab will be replaced by four spaces on the text
input widget. You can set a lower or higher value.
[`tab_width`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.tab_width) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 4.

**kivy.uix.textinput.TextInput.text**

Text of the widget.
Creation of a simple hello world:

If you want to create the widget with an unicode string, use:

[`text`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.text) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty).

**kivy.uix.textinput.TextInput.text_language**

Language of the text, if None Pango will determine it from locale.
This is an RFC-3066 format language tag (as a string), for example
“en_US”, “zh_CN”, “fr” or “ja”. This can impact font selection, metrics
and rendering. For example, the same bytes of text can look different
for ur and ar languages, though both use Arabic script.

New in version 1.10.1.
[`text_language`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.text_language) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to None.

**kivy.uix.textinput.TextInput.text_validate_unfocus**

If True, the `TextInput.on_text_validate()` event will unfocus the
widget, therefore make it stop listening to the keyboard. When disabled,
the `TextInput.on_text_validate()` event can be fired multiple times
as the result of TextInput keeping the focus enabled.
New in version 1.10.1.
[`text_validate_unfocus`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.text_validate_unfocus) is
a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and defaults to True.

**kivy.uix.textinput.TextInput.use_bubble**

Indicates whether the cut/copy/paste bubble is used.
New in version 1.7.0.
[`use_bubble`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.use_bubble) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to True on mobile OS’s, False on desktop OS’s.

**kivy.uix.textinput.TextInput.use_handles**

Indicates whether the selection handles are displayed.
New in version 1.8.0.
[`use_handles`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.use_handles) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to True on mobile OS’s, False on desktop OS’s.

**kivy.uix.textinput.TextInput.write_tab**

Whether the tab key should move focus to the next widget or if it should
enter a tab in the [`TextInput`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput). If True a tab will be written,
otherwise, focus will move to the next widget.
New in version 1.9.0.
[`write_tab`](https://kivy.org/doc/stable/#kivy.uix.textinput.TextInput.write_tab) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to True.

---

## API - [`kivy.uix.togglebutton`](https://kivy.org/doc/stable/api-kivy.uix.togglebutton.html)

**kivy.uix.togglebutton.ToggleButton**

Bases: [`kivy.uix.behaviors.togglebutton.ToggleButtonBehavior`](https://kivy.org/doc/stable/api-kivy.uix.behaviors.togglebutton.html#kivy.uix.behaviors.togglebutton.ToggleButtonBehavior), [`kivy.uix.button.Button`](https://kivy.org/doc/stable/api-kivy.uix.button.html#kivy.uix.button.Button)
Toggle button class, see module documentation for more information.

---

## API - [`kivy.uix.treeview`](https://kivy.org/doc/stable/api-kivy.uix.treeview.html)

**kivy.uix.treeview.TreeView**

Bases: [`kivy.uix.widget.Widget`](https://kivy.org/doc/stable/api-kivy.uix.widget.html#kivy.uix.widget.Widget)
TreeView class. See module documentation for more information.

**kivy.uix.treeview.TreeView.add_node**

Add a new node to the tree.

**kivy.uix.treeview.TreeView.deselect_node**

Deselect any selected node.
New in version 1.10.0.

**kivy.uix.treeview.TreeView.get_node_at_pos**

Get the node at the position (x, y).

**kivy.uix.treeview.TreeView.hide_root**

Use this property to show/hide the initial root node. If True, the root
node will be appear as a closed node.
[`hide_root`](https://kivy.org/doc/stable/#kivy.uix.treeview.TreeView.hide_root) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to False.

**kivy.uix.treeview.TreeView.indent_level**

Width used for the indentation of each level except the first level.
Computation of indent for each level of the tree is:

[`indent_level`](https://kivy.org/doc/stable/#kivy.uix.treeview.TreeView.indent_level) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 16.

**kivy.uix.treeview.TreeView.indent_start**

Indentation width of the level 0 / root node. This is mostly the initial
size to accommodate a tree icon (collapsed / expanded). See
[`indent_level`](https://kivy.org/doc/stable/#kivy.uix.treeview.TreeView.indent_level) for more information about the computation of level
indentation.
[`indent_start`](https://kivy.org/doc/stable/#kivy.uix.treeview.TreeView.indent_start) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 24.

**kivy.uix.treeview.TreeView.iterate_all_nodes**

Generator to iterate over all nodes from node and down whether
expanded or not. If node is None, the generator start with
[`root`](https://kivy.org/doc/stable/#kivy.uix.treeview.TreeView.root).

**kivy.uix.treeview.TreeView.iterate_open_nodes**

Generator to iterate over all the expended nodes starting from
node and down. If node is None, the generator start with
[`root`](https://kivy.org/doc/stable/#kivy.uix.treeview.TreeView.root).
To get all the open nodes:

**kivy.uix.treeview.TreeView.load_func**

Callback to use for asynchronous loading. If set, asynchronous loading
will be automatically done. The callback must act as a Python generator
function, using yield to send data back to the treeview.
The callback should be in the format:

[`load_func`](https://kivy.org/doc/stable/#kivy.uix.treeview.TreeView.load_func) is a [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to None.

**kivy.uix.treeview.TreeView.minimum_height**

Minimum height needed to contain all children.
New in version 1.0.9.
[`minimum_height`](https://kivy.org/doc/stable/#kivy.uix.treeview.TreeView.minimum_height) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0.

**kivy.uix.treeview.TreeView.minimum_size**

Minimum size needed to contain all children.
New in version 1.0.9.
[`minimum_size`](https://kivy.org/doc/stable/#kivy.uix.treeview.TreeView.minimum_size) is a [`ReferenceListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ReferenceListProperty)
of ([`minimum_width`](https://kivy.org/doc/stable/#kivy.uix.treeview.TreeView.minimum_width), [`minimum_height`](https://kivy.org/doc/stable/#kivy.uix.treeview.TreeView.minimum_height)) properties.

**kivy.uix.treeview.TreeView.minimum_width**

Minimum width needed to contain all children.
New in version 1.0.9.
[`minimum_width`](https://kivy.org/doc/stable/#kivy.uix.treeview.TreeView.minimum_width) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 0.

**kivy.uix.treeview.TreeView.on_touch_down**

Receive a touch down event.

**kivy.uix.treeview.TreeView.remove_node**

Removes a node from the tree.
New in version 1.0.7.

**kivy.uix.treeview.TreeView.root**

Root node.
By default, the root node widget is a [`TreeViewLabel`](https://kivy.org/doc/stable/#kivy.uix.treeview.TreeViewLabel) with text
‘Root’. If you want to change the default options passed to the widget
creation, use the [`root_options`](https://kivy.org/doc/stable/#kivy.uix.treeview.TreeView.root_options) property:

[`root_options`](https://kivy.org/doc/stable/#kivy.uix.treeview.TreeView.root_options) will change the properties of the
[`TreeViewLabel`](https://kivy.org/doc/stable/#kivy.uix.treeview.TreeViewLabel) instance. However, you cannot change the class used
for root node yet.
[`root`](https://kivy.org/doc/stable/#kivy.uix.treeview.TreeView.root) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) and defaults to
None. It is read-only. However, the content of the widget can be changed.

**kivy.uix.treeview.TreeView.root_options**

Default root options to pass for root widget. See [`root`](https://kivy.org/doc/stable/#kivy.uix.treeview.TreeView.root) property
for more information about the usage of root_options.
[`root_options`](https://kivy.org/doc/stable/#kivy.uix.treeview.TreeView.root_options) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to {}.

**kivy.uix.treeview.TreeView.select_node**

Select a node in the tree.

**kivy.uix.treeview.TreeView.selected_node**

Node selected by [`TreeView.select_node()`](https://kivy.org/doc/stable/#kivy.uix.treeview.TreeView.select_node) or by touch.
[`selected_node`](https://kivy.org/doc/stable/#kivy.uix.treeview.TreeView.selected_node) is a [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) and
defaults to None. It is read-only.

**kivy.uix.treeview.TreeView.toggle_node**

Toggle the state of the node (open/collapsed).

**kivy.uix.treeview.TreeViewException**

Bases: `Exception`
Exception for errors in the [`TreeView`](https://kivy.org/doc/stable/#kivy.uix.treeview.TreeView).

**kivy.uix.treeview.TreeViewLabel**

Bases: [`kivy.uix.label.Label`](https://kivy.org/doc/stable/api-kivy.uix.label.html#kivy.uix.label.Label), [`kivy.uix.treeview.TreeViewNode`](https://kivy.org/doc/stable/#kivy.uix.treeview.TreeViewNode)
Combines a [`Label`](https://kivy.org/doc/stable/api-kivy.uix.label.html#kivy.uix.label.Label) and a [`TreeViewNode`](https://kivy.org/doc/stable/#kivy.uix.treeview.TreeViewNode) to
create a [`TreeViewLabel`](https://kivy.org/doc/stable/#kivy.uix.treeview.TreeViewLabel) that can be used as a text node in the
tree.
See module documentation for more information.

**kivy.uix.treeview.TreeViewNode**

Bases: `builtins.object`
TreeViewNode class, used to build a node class for a TreeView object.

**kivy.uix.treeview.TreeViewNode.color_selected**

Background color of the node when the node is selected.
[`color_selected`](https://kivy.org/doc/stable/#kivy.uix.treeview.TreeViewNode.color_selected) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty) and
defaults to [.1, .1, .1, 1].
Changed in version 2.0.0:Changed from [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) to
[`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty).

**kivy.uix.treeview.TreeViewNode.even_color**

Background color of even nodes when the node is not selected.
`bg_color` is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty) and defaults
to [.5, .5, .5, .1].
Changed in version 2.0.0:Changed from [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) to
[`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty).

**kivy.uix.treeview.TreeViewNode.is_leaf**

Boolean to indicate whether this node is a leaf or not. Used to adjust
the graphical representation.
[`is_leaf`](https://kivy.org/doc/stable/#kivy.uix.treeview.TreeViewNode.is_leaf) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and defaults
to True. It is automatically set to False when child is added.

**kivy.uix.treeview.TreeViewNode.is_loaded**

Boolean to indicate whether this node is already loaded or not. This
property is used only if the [`TreeView`](https://kivy.org/doc/stable/#kivy.uix.treeview.TreeView) uses asynchronous loading.
[`is_loaded`](https://kivy.org/doc/stable/#kivy.uix.treeview.TreeViewNode.is_loaded) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to False.

**kivy.uix.treeview.TreeViewNode.is_open**

Boolean to indicate whether this node is opened or not, in case there
are child nodes. This is used to adjust the graphical representation.

[`is_open`](https://kivy.org/doc/stable/#kivy.uix.treeview.TreeViewNode.is_open) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and defaults
to False.

**kivy.uix.treeview.TreeViewNode.is_selected**

Boolean to indicate whether this node is selected or not. This is used
adjust the graphical representation.

[`is_selected`](https://kivy.org/doc/stable/#kivy.uix.treeview.TreeViewNode.is_selected) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to False.

**kivy.uix.treeview.TreeViewNode.level**

Level of the node.
[`level`](https://kivy.org/doc/stable/#kivy.uix.treeview.TreeViewNode.level) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and defaults
to -1.

**kivy.uix.treeview.TreeViewNode.no_selection**

[`no_selection`](https://kivy.org/doc/stable/#kivy.uix.treeview.TreeViewNode.no_selection) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and
defaults to False.

**kivy.uix.treeview.TreeViewNode.nodes**

List of nodes. The nodes list is different than the children list. A
node in the nodes list represents a node on the tree. An item in the
children list represents the widget associated with the node.

[`nodes`](https://kivy.org/doc/stable/#kivy.uix.treeview.TreeViewNode.nodes) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) and defaults to
[].

**kivy.uix.treeview.TreeViewNode.odd**

This property is set by the TreeView widget automatically and is read-only.
[`odd`](https://kivy.org/doc/stable/#kivy.uix.treeview.TreeViewNode.odd) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and defaults to
False.

**kivy.uix.treeview.TreeViewNode.odd_color**

Background color of odd nodes when the node is not selected.
[`odd_color`](https://kivy.org/doc/stable/#kivy.uix.treeview.TreeViewNode.odd_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty) and defaults
to [1., 1., 1., 0.].
Changed in version 2.0.0:Changed from [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) to
[`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty).

**kivy.uix.treeview.TreeViewNode.parent_node**

Parent node. This attribute is needed because the `parent` can be
None when the node is not displayed.
New in version 1.0.7.
[`parent_node`](https://kivy.org/doc/stable/#kivy.uix.treeview.TreeViewNode.parent_node) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to None.

---

## API - [`kivy.uix.video`](https://kivy.org/doc/stable/api-kivy.uix.video.html)

**kivy.uix.video.Video**

Bases: [`kivy.uix.image.Image`](https://kivy.org/doc/stable/api-kivy.uix.image.html#kivy.uix.image.Image)
Video class. See module documentation for more information.

**kivy.uix.video.Video.duration**

Duration of the video. The duration defaults to -1, and is set to a real
duration when the video is loaded.
[`duration`](https://kivy.org/doc/stable/#kivy.uix.video.Video.duration) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to -1.

**kivy.uix.video.Video.eos**

Boolean, indicates whether the video has finished playing or not
(reached the end of the stream).
[`eos`](https://kivy.org/doc/stable/#kivy.uix.video.Video.eos) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and defaults to
False.

**kivy.uix.video.Video.loaded**

Boolean, indicates whether the video is loaded and ready for playback
or not.
New in version 1.6.0.
[`loaded`](https://kivy.org/doc/stable/#kivy.uix.video.Video.loaded) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and defaults
to False.

**kivy.uix.video.Video.options**

Options to pass at Video core object creation.
New in version 1.0.4.
[`options`](https://kivy.org/doc/stable/#kivy.uix.video.Video.options) is an [`kivy.properties.ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and defaults
to {}.

**kivy.uix.video.Video.play**

Deprecated since version 1.4.0:Use [`state`](https://kivy.org/doc/stable/#kivy.uix.video.Video.state) instead.
Boolean, indicates whether the video is playing or not.
You can start/stop the video by setting this property:

[`play`](https://kivy.org/doc/stable/#kivy.uix.video.Video.play) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and defaults to
False.
Deprecated since version 1.4.0:Use [`state`](https://kivy.org/doc/stable/#kivy.uix.video.Video.state) instead.

**kivy.uix.video.Video.position**

Position of the video between 0 and [`duration`](https://kivy.org/doc/stable/#kivy.uix.video.Video.duration). The position
defaults to -1 and is set to a real position when the video is loaded.
[`position`](https://kivy.org/doc/stable/#kivy.uix.video.Video.position) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to -1.

**kivy.uix.video.Video.preview**

Filename / source of a preview image displayed before video starts.
[`preview`](https://kivy.org/doc/stable/#kivy.uix.video.Video.preview) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to None.
If set, it gets displayed until the video is loaded/started.
New in version 2.1.0.

**kivy.uix.video.Video.seek**

New in version 1.2.0.
Changed in version 1.10.1:The precise keyword argument has been added.

**kivy.uix.video.Video.state**

String, indicates whether to play, pause, or stop the video:

[`state`](https://kivy.org/doc/stable/#kivy.uix.video.Video.state) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty) and defaults
to ‘stop’.

**kivy.uix.video.Video.unload**

Unload the video. The playback will be stopped.
New in version 1.8.0.

**kivy.uix.video.Video.volume**

Volume of the video, in the range 0-1. 1 means full volume, 0
means mute.
[`volume`](https://kivy.org/doc/stable/#kivy.uix.video.Video.volume) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and defaults
to 1.

---

## API - [`kivy.uix.videoplayer`](https://kivy.org/doc/stable/api-kivy.uix.videoplayer.html)

**kivy.uix.videoplayer.VideoPlayer**

Bases: [`kivy.uix.gridlayout.GridLayout`](https://kivy.org/doc/stable/api-kivy.uix.gridlayout.html#kivy.uix.gridlayout.GridLayout)
VideoPlayer class. See module documentation for more information.

**kivy.uix.videoplayer.VideoPlayer.allow_fullscreen**

By default, you can double-tap on the video to make it fullscreen. Set
this property to False to prevent this behavior.
[`allow_fullscreen`](https://kivy.org/doc/stable/#kivy.uix.videoplayer.VideoPlayer.allow_fullscreen) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
defaults to True.

**kivy.uix.videoplayer.VideoPlayer.annotations**

If set, it will be used for reading annotations box.
[`annotations`](https://kivy.org/doc/stable/#kivy.uix.videoplayer.VideoPlayer.annotations) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘’.

**kivy.uix.videoplayer.VideoPlayer.duration**

Duration of the video. The duration defaults to -1 and is set to the
real duration when the video is loaded.
[`duration`](https://kivy.org/doc/stable/#kivy.uix.videoplayer.VideoPlayer.duration) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to -1.

**kivy.uix.videoplayer.VideoPlayer.fullscreen**

Switch to fullscreen view. This should be used with care. When
activated, the widget will remove itself from its parent, remove all
children from the window and will add itself to it. When fullscreen is
unset, all the previous children are restored and the widget is restored to
its previous parent.

[`fullscreen`](https://kivy.org/doc/stable/#kivy.uix.videoplayer.VideoPlayer.fullscreen) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty)
and defaults to False.

**kivy.uix.videoplayer.VideoPlayer.image_loading**

Image filename used when the video is loading.
[`image_loading`](https://kivy.org/doc/stable/#kivy.uix.videoplayer.VideoPlayer.image_loading) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to ‘data/images/image-loading.zip’.

**kivy.uix.videoplayer.VideoPlayer.image_overlay_play**

Image filename used to show a “play” overlay when the video has not yet
started.
[`image_overlay_play`](https://kivy.org/doc/stable/#kivy.uix.videoplayer.VideoPlayer.image_overlay_play) is a
[`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to ‘atlas://data/images/defaulttheme/player-play-overlay’.

**kivy.uix.videoplayer.VideoPlayer.image_pause**

Image filename used for the “Pause” button.
[`image_pause`](https://kivy.org/doc/stable/#kivy.uix.videoplayer.VideoPlayer.image_pause) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to ‘atlas://data/images/defaulttheme/media-playback-pause’.

**kivy.uix.videoplayer.VideoPlayer.image_play**

Image filename used for the “Play” button.
[`image_play`](https://kivy.org/doc/stable/#kivy.uix.videoplayer.VideoPlayer.image_play) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to ‘atlas://data/images/defaulttheme/media-playback-start’.

**kivy.uix.videoplayer.VideoPlayer.image_stop**

Image filename used for the “Stop” button.
[`image_stop`](https://kivy.org/doc/stable/#kivy.uix.videoplayer.VideoPlayer.image_stop) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to ‘atlas://data/images/defaulttheme/media-playback-stop’.

**kivy.uix.videoplayer.VideoPlayer.image_volumehigh**

Image filename used for the volume icon when the volume is high.
[`image_volumehigh`](https://kivy.org/doc/stable/#kivy.uix.videoplayer.VideoPlayer.image_volumehigh) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to ‘atlas://data/images/defaulttheme/audio-volume-high’.

**kivy.uix.videoplayer.VideoPlayer.image_volumelow**

Image filename used for the volume icon when the volume is low.
[`image_volumelow`](https://kivy.org/doc/stable/#kivy.uix.videoplayer.VideoPlayer.image_volumelow) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘atlas://data/images/defaulttheme/audio-volume-low’.

**kivy.uix.videoplayer.VideoPlayer.image_volumemedium**

Image filename used for the volume icon when the volume is medium.
[`image_volumemedium`](https://kivy.org/doc/stable/#kivy.uix.videoplayer.VideoPlayer.image_volumemedium) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘atlas://data/images/defaulttheme/audio-volume-medium’.

**kivy.uix.videoplayer.VideoPlayer.image_volumemuted**

Image filename used for the volume icon when the volume is muted.
[`image_volumemuted`](https://kivy.org/doc/stable/#kivy.uix.videoplayer.VideoPlayer.image_volumemuted) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to ‘atlas://data/images/defaulttheme/audio-volume-muted’.

**kivy.uix.videoplayer.VideoPlayer.on_touch_down**

Receive a touch down event.

**kivy.uix.videoplayer.VideoPlayer.options**

Optional parameters can be passed to a [`Video`](https://kivy.org/doc/stable/api-kivy.uix.video.html#kivy.uix.video.Video)
instance with this property.
[`options`](https://kivy.org/doc/stable/#kivy.uix.videoplayer.VideoPlayer.options) a [`DictProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.DictProperty) and
defaults to {}.

**kivy.uix.videoplayer.VideoPlayer.play**

Deprecated since version 1.4.0:Use [`state`](https://kivy.org/doc/stable/#kivy.uix.videoplayer.VideoPlayer.state) instead.
Boolean, indicates whether the video is playing or not. You can start/stop
the video by setting this property:

[`play`](https://kivy.org/doc/stable/#kivy.uix.videoplayer.VideoPlayer.play) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and defaults
to False.

**kivy.uix.videoplayer.VideoPlayer.position**

Position of the video between 0 and [`duration`](https://kivy.org/doc/stable/#kivy.uix.videoplayer.VideoPlayer.duration). The position
defaults to -1 and is set to the real position when the video is loaded.
[`position`](https://kivy.org/doc/stable/#kivy.uix.videoplayer.VideoPlayer.position) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to -1.

**kivy.uix.videoplayer.VideoPlayer.seek**

New in version 1.2.0.
Changed in version 1.10.1:The precise keyword argument has been added.

**kivy.uix.videoplayer.VideoPlayer.source**

Source of the video to read.
[`source`](https://kivy.org/doc/stable/#kivy.uix.videoplayer.VideoPlayer.source) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to ‘’.
Changed in version 1.4.0.

**kivy.uix.videoplayer.VideoPlayer.state**

String, indicates whether to play, pause, or stop the video:

[`state`](https://kivy.org/doc/stable/#kivy.uix.videoplayer.VideoPlayer.state) is an [`OptionProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.OptionProperty) and defaults
to ‘stop’.

**kivy.uix.videoplayer.VideoPlayer.thumbnail**

Thumbnail of the video to show. If None, VideoPlayer will try to find
the thumbnail from the [`source`](https://kivy.org/doc/stable/#kivy.uix.videoplayer.VideoPlayer.source) + ‘.png’.
[`thumbnail`](https://kivy.org/doc/stable/#kivy.uix.videoplayer.VideoPlayer.thumbnail) a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults
to ‘’.
Changed in version 1.4.0.

**kivy.uix.videoplayer.VideoPlayer.volume**

Volume of the video in the range 0-1. 1 means full volume and 0 means
mute.
[`volume`](https://kivy.org/doc/stable/#kivy.uix.videoplayer.VideoPlayer.volume) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and defaults
to 1.

**kivy.uix.videoplayer.VideoPlayerAnnotation**

Bases: [`kivy.uix.label.Label`](https://kivy.org/doc/stable/api-kivy.uix.label.html#kivy.uix.label.Label)
Annotation class used for creating annotation labels.
Additional keys are available:
bgcolor: [r, g, b, a] - background color of the text box
bgsource: ‘filename’ - background image used for the background text box
border: (n, e, s, w) - border used for the background image

**kivy.uix.videoplayer.VideoPlayerAnnotation.duration**

Duration of the annotation.
[`duration`](https://kivy.org/doc/stable/#kivy.uix.videoplayer.VideoPlayerAnnotation.duration) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 1.

**kivy.uix.videoplayer.VideoPlayerAnnotation.start**

Start time of the annotation.
[`start`](https://kivy.org/doc/stable/#kivy.uix.videoplayer.VideoPlayerAnnotation.start) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and defaults
to 0.

---

## API - [`kivy.uix.vkeyboard`](https://kivy.org/doc/stable/api-kivy.uix.vkeyboard.html)

**kivy.uix.vkeyboard.VKeyboard**

Bases: [`kivy.uix.scatter.Scatter`](https://kivy.org/doc/stable/api-kivy.uix.scatter.html#kivy.uix.scatter.Scatter)
VKeyboard is an onscreen keyboard with multitouch support.
Its layout is entirely customizable and you can switch between available
layouts using a button in the bottom right of the widget.

**kivy.uix.vkeyboard.VKeyboard.available_layouts**

Dictionary of all available layouts. Keys are the layout ID, and the
value is the JSON (translated into a Python object).
[`available_layouts`](https://kivy.org/doc/stable/#kivy.uix.vkeyboard.VKeyboard.available_layouts) is a [`DictProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.DictProperty) and
defaults to {}.

**kivy.uix.vkeyboard.VKeyboard.background**

Filename of the background image.
[`background`](https://kivy.org/doc/stable/#kivy.uix.vkeyboard.VKeyboard.background) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to `atlas://data/images/defaulttheme/vkeyboard_background`.

**kivy.uix.vkeyboard.VKeyboard.background_border**

Background image border. Used for controlling the
[`border`](https://kivy.org/doc/stable/api-kivy.graphics.vertex_instructions.html#kivy.graphics.vertex_instructions.BorderImage.border) property of
the background.
[`background_border`](https://kivy.org/doc/stable/#kivy.uix.vkeyboard.VKeyboard.background_border) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) and
defaults to [16, 16, 16, 16]

**kivy.uix.vkeyboard.VKeyboard.background_color**

Background color, in the format (r, g, b, a). If a background is
set, the color will be combined with the background texture.
[`background_color`](https://kivy.org/doc/stable/#kivy.uix.vkeyboard.VKeyboard.background_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty) and
defaults to [1, 1, 1, 1].
Changed in version 2.0.0:Changed from [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) to
[`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty).

**kivy.uix.vkeyboard.VKeyboard.background_disabled**

Filename of the background image when the vkeyboard is disabled.
New in version 1.8.0.
[`background_disabled`](https://kivy.org/doc/stable/#kivy.uix.vkeyboard.VKeyboard.background_disabled) is a
[`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults to
`atlas://data/images/defaulttheme/vkeyboard__disabled_background`.

**kivy.uix.vkeyboard.VKeyboard.callback**

Callback can be set to a function that will be called if the
VKeyboard is closed by the user.
[`target`](https://kivy.org/doc/stable/#kivy.uix.vkeyboard.VKeyboard.target) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) instance and
defaults to None.

**kivy.uix.vkeyboard.VKeyboard.collide_margin**

Do a collision test, and return True if the (x, y) is inside the
vkeyboard margin.

**kivy.uix.vkeyboard.VKeyboard.docked**

Indicate whether the VKeyboard is docked on the screen or not. If you
change it, you must manually call [`setup_mode()`](https://kivy.org/doc/stable/#kivy.uix.vkeyboard.VKeyboard.setup_mode) otherwise it will have
no impact. If the VKeyboard is created by the Window, the docked mode will
be automatically set by the configuration, using the keyboard_mode token
in [kivy] section.
[`docked`](https://kivy.org/doc/stable/#kivy.uix.vkeyboard.VKeyboard.docked) is a [`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) and defaults
to False.

**kivy.uix.vkeyboard.VKeyboard.font_size**

font_size, specifies the size of the text on the virtual keyboard keys.
It should be kept within limits to ensure the text does not extend beyond
the bounds of the key or become too small to read.
New in version 1.10.0.
[`font_size`](https://kivy.org/doc/stable/#kivy.uix.vkeyboard.VKeyboard.font_size) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 20.

**kivy.uix.vkeyboard.VKeyboard.key_background_color**

Key background color, in the format (r, g, b, a). If a key background is
set, the color will be combined with the key background texture.
[`key_background_color`](https://kivy.org/doc/stable/#kivy.uix.vkeyboard.VKeyboard.key_background_color) is a [`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty)
and defaults to [1, 1, 1, 1].
Changed in version 2.0.0:Changed from [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) to
[`ColorProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ColorProperty).

**kivy.uix.vkeyboard.VKeyboard.key_background_down**

Filename of the key background image for use when a touch is active
on the widget.
[`key_background_down`](https://kivy.org/doc/stable/#kivy.uix.vkeyboard.VKeyboard.key_background_down) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to
`atlas://data/images/defaulttheme/vkeyboard_key_down`.

**kivy.uix.vkeyboard.VKeyboard.key_background_normal**

Filename of the key background image for use when no touches are active
on the widget.
[`key_background_normal`](https://kivy.org/doc/stable/#kivy.uix.vkeyboard.VKeyboard.key_background_normal) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)
and defaults to
`atlas://data/images/defaulttheme/vkeyboard_key_normal`.

**kivy.uix.vkeyboard.VKeyboard.key_border**

Key image border. Used for controlling the
[`border`](https://kivy.org/doc/stable/api-kivy.graphics.vertex_instructions.html#kivy.graphics.vertex_instructions.BorderImage.border) property of
the key.
[`key_border`](https://kivy.org/doc/stable/#kivy.uix.vkeyboard.VKeyboard.key_border) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) and
defaults to [16, 16, 16, 16]

**kivy.uix.vkeyboard.VKeyboard.key_disabled_background_normal**

Filename of the key background image for use when no touches are active
on the widget and vkeyboard is disabled.
New in version 1.8.0.
[`key_disabled_background_normal`](https://kivy.org/doc/stable/#kivy.uix.vkeyboard.VKeyboard.key_disabled_background_normal) is a
[`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults to
`atlas://data/images/defaulttheme/vkeyboard_disabled_key_normal`.

**kivy.uix.vkeyboard.VKeyboard.key_margin**

Key margin, used to create space between keys. The margin is composed of
four values, in pixels:

[`key_margin`](https://kivy.org/doc/stable/#kivy.uix.vkeyboard.VKeyboard.key_margin) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) and defaults
to [2, 2, 2, 2]

**kivy.uix.vkeyboard.VKeyboard.layout**

Layout to use for the VKeyboard. By default, it will be the
layout set in the configuration, according to the keyboard_layout
in [kivy] section.
Changed in version 1.8.0:If layout is a .json filename, it will loaded and added to the
available_layouts.
[`layout`](https://kivy.org/doc/stable/#kivy.uix.vkeyboard.VKeyboard.layout) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and defaults
to None.

**kivy.uix.vkeyboard.VKeyboard.layout_path**

Path from which layouts are read.
[`layout`](https://kivy.org/doc/stable/#kivy.uix.vkeyboard.VKeyboard.layout) is a [`StringProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty) and
defaults to `<kivy_data_dir>/keyboards/`

**kivy.uix.vkeyboard.VKeyboard.margin_hint**

Margin hint, used as spacing between keyboard background and keys
content. The margin is composed of four values, between 0 and 1:

The margin hints will be multiplied by width and height, according to their
position.
[`margin_hint`](https://kivy.org/doc/stable/#kivy.uix.vkeyboard.VKeyboard.margin_hint) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) and
defaults to [.05, .06, .05, .06]

**kivy.uix.vkeyboard.VKeyboard.on_touch_down**

Receive a touch down event.

**kivy.uix.vkeyboard.VKeyboard.on_touch_up**

Receive a touch up event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivy.org/doc/stable/#kivy.uix.vkeyboard.VKeyboard.on_touch_down) for more information.

**kivy.uix.vkeyboard.VKeyboard.refresh**

(internal) Recreate the entire widget and graphics according to the
selected layout.

**kivy.uix.vkeyboard.VKeyboard.setup_mode**

Call this method when you want to readjust the keyboard according to
options: [`docked`](https://kivy.org/doc/stable/#kivy.uix.vkeyboard.VKeyboard.docked) or not, with attached [`target`](https://kivy.org/doc/stable/#kivy.uix.vkeyboard.VKeyboard.target) or not:
If [`docked`](https://kivy.org/doc/stable/#kivy.uix.vkeyboard.VKeyboard.docked) is True, it will call [`setup_mode_dock()`](https://kivy.org/doc/stable/#kivy.uix.vkeyboard.VKeyboard.setup_mode_dock)
If [`docked`](https://kivy.org/doc/stable/#kivy.uix.vkeyboard.VKeyboard.docked) is False, it will call [`setup_mode_free()`](https://kivy.org/doc/stable/#kivy.uix.vkeyboard.VKeyboard.setup_mode_free)
Feel free to overload these methods to create new
positioning behavior.

**kivy.uix.vkeyboard.VKeyboard.setup_mode_dock**

Setup the keyboard in docked mode.
Dock mode will reset the rotation, disable translation, rotation and
scale. Scale and position will be automatically adjusted to attach the
keyboard to the bottom of the screen.

**kivy.uix.vkeyboard.VKeyboard.setup_mode_free**

Setup the keyboard in free mode.
Free mode is designed to let the user control the position and
orientation of the keyboard. The only real usage is for a multiuser
environment, but you might found other ways to use it.
If a [`target`](https://kivy.org/doc/stable/#kivy.uix.vkeyboard.VKeyboard.target) is set, it will place the vkeyboard under the
target.

**kivy.uix.vkeyboard.VKeyboard.target**

Target widget associated with the VKeyboard. If set, it will be used to
send keyboard events. If the VKeyboard mode is “free”, it will also be used
to set the initial position.
[`target`](https://kivy.org/doc/stable/#kivy.uix.vkeyboard.VKeyboard.target) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) instance and
defaults to None.

---

## API - [`kivy.uix.widget`](https://kivy.org/doc/stable/api-kivy.uix.widget.html)

**kivy.uix.widget.Widget**

Bases: `kivy.uix.widget.WidgetBase`
Widget class. See module documentation for more information.

Changed in version 1.0.9:Everything related to event properties has been moved to the
[`EventDispatcher`](https://kivy.org/doc/stable/api-kivy.event.html#kivy.event.EventDispatcher). Event properties can now be used
when constructing a simple class without subclassing [`Widget`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget).
Changed in version 1.5.0:The constructor now accepts on_* arguments to automatically bind
callbacks to properties or events, as in the Kv language.

**kivy.uix.widget.Widget.add_widget**

Add a new widget as a child of this widget.

**kivy.uix.widget.Widget.apply_class_lang_rules**

Method that is called by kivy to apply the kv rules of this widget’s
class.

This is useful to be able to execute code before/after the class kv
rules are applied to the widget. E.g. if the kv code requires some
properties to be initialized before it is used in a binding rule.
If overwriting remember to call `super`, otherwise the kv rules will
not be applied.
In the following example,

When `OtherWidget` is instantiated with `OtherWidget()`, the
widget’s [`apply_class_lang_rules()`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.apply_class_lang_rules) is called and it applies the
kv rules of this class - `<MyWidget>` and `<OtherWidget>`.
Similarly, when the widget is instantiated from kv, e.g.

`OtherWidget`’s [`apply_class_lang_rules()`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.apply_class_lang_rules) is called and it
applies the kv rules of this class - `<MyWidget>` and
`<OtherWidget>`.

Changed in version 1.11.0.

**kivy.uix.widget.Widget.canvas**

Canvas of the widget.
The canvas is a graphics object that contains all the drawing instructions
for the graphical representation of the widget.
There are no general properties for the Widget class, such as background
color, to keep the design simple and lean. Some derived classes, such as
Button, do add such convenience properties but generally the developer is
responsible for implementing the graphics representation for a custom
widget from the ground up. See the derived widget classes for patterns to
follow and extend.
See [`Canvas`](https://kivy.org/doc/stable/api-kivy.graphics.html#kivy.graphics.Canvas) for more information about the usage.

**kivy.uix.widget.Widget.center**

Center position of the widget.
[`center`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.center) is a [`ReferenceListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ReferenceListProperty) of
([`center_x`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.center_x), [`center_y`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.center_y)) properties.

**kivy.uix.widget.Widget.center_x**

X center position of the widget.
[`center_x`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.center_x) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) of
([`x`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.x) + [`width`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.width) / 2.).

**kivy.uix.widget.Widget.center_y**

Y center position of the widget.
[`center_y`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.center_y) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) of
([`y`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.y) + [`height`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.height) / 2.).

**kivy.uix.widget.Widget.children**

List of children of this widget.
[`children`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.children) is a [`ListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ListProperty) and
defaults to an empty list.
Use [`add_widget()`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.add_widget) and [`remove_widget()`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.remove_widget) for manipulating the
children list. Don’t manipulate the children list directly unless you know
what you are doing.

**kivy.uix.widget.Widget.clear_widgets**

Remove all (or the specified) [`children`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.children) of this widget.
If the ‘children’ argument is specified, it should be a list (or
filtered list) of children of the current widget.
Changed in version 1.8.0:The children argument can be used to specify the children you
want to remove.
Changed in version 2.1.0:Specifying an empty `children` list leaves the widgets unchanged.
Previously it was treated like `None` and all children were
removed.

**kivy.uix.widget.Widget.cls**

Class of the widget, used for styling.

**kivy.uix.widget.Widget.collide_point**

Check if a point (x, y) is inside the widget’s axis aligned bounding
box.

**kivy.uix.widget.Widget.collide_widget**

Check if another widget collides with this widget. This function
performs an axis-aligned bounding box intersection test by default.

**kivy.uix.widget.Widget.disabled**

Indicates whether this widget can interact with input or not.
[`disabled`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.disabled) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) and
defaults to False.

New in version 1.8.0.
Changed in version 1.10.1:[`disabled`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.disabled) was changed from a
[`BooleanProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.BooleanProperty) to an
[`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) to allow access to its
previous state when a parent’s disabled state is changed.

**kivy.uix.widget.Widget.export_as_image**

Return an core [`Image`](https://kivy.org/doc/stable/api-kivy.core.image.html#kivy.core.image.Image) of the actual
widget.
New in version 1.11.0.

**kivy.uix.widget.Widget.export_to_png**

Saves an image of the widget and its children in png format at the
specified filename. Works by removing the widget canvas from its
parent, rendering to an [`Fbo`](https://kivy.org/doc/stable/api-kivy.graphics.fbo.html#kivy.graphics.fbo.Fbo), and calling
[`save()`](https://kivy.org/doc/stable/api-kivy.graphics.texture.html#kivy.graphics.texture.Texture.save).

New in version 1.9.0.

**kivy.uix.widget.Widget.get_parent_window**

Return the parent window.

**kivy.uix.widget.Widget.get_root_window**

Return the root window.

**kivy.uix.widget.Widget.get_window_matrix**

Calculate the transformation matrix to convert between window and
widget coordinates.

**kivy.uix.widget.Widget.height**

Height of the widget.
[`height`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.height) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and defaults
to 100.

**kivy.uix.widget.Widget.ids**

This is a dictionary of ids defined in your kv language. This will only
be populated if you use ids in your kv language code.
New in version 1.7.0.
[`ids`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.ids) is a [`DictProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.DictProperty) and defaults to an
empty dict {}.
The [`ids`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.ids) are populated for each root level widget definition. For
example:

Then, in python:

**kivy.uix.widget.Widget.motion_filter**

Holds a dict of type_id to list of child widgets registered to
receive motion events of type_id.
Don’t change the property directly but use
[`register_for_motion_event()`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.register_for_motion_event) and [`unregister_for_motion_event()`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.unregister_for_motion_event)
to register and unregister for motion events. If self is registered it
will always be the first element in the list.
New in version 2.1.0.

**kivy.uix.widget.Widget.on_motion**

Called when a motion event is received.

New in version 2.1.0.

**kivy.uix.widget.Widget.on_touch_down**

Receive a touch down event.

**kivy.uix.widget.Widget.on_touch_move**

Receive a touch move event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.on_touch_down) for more information.

**kivy.uix.widget.Widget.on_touch_up**

Receive a touch up event. The touch is in parent coordinates.
See [`on_touch_down()`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.on_touch_down) for more information.

**kivy.uix.widget.Widget.opacity**

Opacity of the widget and all its children.
New in version 1.4.1.
The opacity attribute controls the opacity of the widget and its children.
Be careful, it’s a cumulative attribute: the value is multiplied by the
current global opacity and the result is applied to the current context
color.
For example, if the parent has an opacity of 0.5 and a child has an
opacity of 0.2, the real opacity of the child will be 0.5 * 0.2 = 0.1.
Then, the opacity is applied by the shader as:

[`opacity`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.opacity) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and defaults
to 1.0.

**kivy.uix.widget.Widget.parent**

Parent of this widget. The parent of a widget is set when the widget
is added to another widget and unset when the widget is removed from its
parent.
[`parent`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.parent) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty) and
defaults to None.

**kivy.uix.widget.Widget.pos**

Position of the widget.
[`pos`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.pos) is a [`ReferenceListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ReferenceListProperty) of
([`x`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.x), [`y`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.y)) properties.

**kivy.uix.widget.Widget.pos_hint**

Position hint. This property allows you to set the position of
the widget inside its parent layout (similar to
size_hint).
For example, if you want to set the top of the widget to be at 90%
height of its parent layout, you can write:

The keys ‘x’, ‘right’ and ‘center_x’ will use the parent width.
The keys ‘y’, ‘top’ and ‘center_y’ will use the parent height.
See [Float Layout](https://kivy.org/doc/stable/api-kivy.uix.floatlayout.html) for further reference.

[`pos_hint`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.pos_hint) is an [`ObjectProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ObjectProperty)
containing a dict.

**kivy.uix.widget.Widget.proxy_ref**

Return a proxy reference to the widget, i.e. without creating a
reference to the widget. See [weakref.proxy](http://docs.python.org/2/library/weakref.html?highlight=proxy#weakref.proxy) for more information.
New in version 1.7.2.

**kivy.uix.widget.Widget.register_for_motion_event**

Register to receive motion events of type_id.
Override [`on_motion()`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.on_motion) or bind to on_motion event to handle
the incoming motion events.

New in version 2.1.0.

**kivy.uix.widget.Widget.remove_widget**

Remove a widget from the children of this widget.

**kivy.uix.widget.Widget.right**

Right position of the widget.
[`right`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.right) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) of
([`x`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.x) + [`width`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.width)).

**kivy.uix.widget.Widget.size**

Size of the widget.
[`size`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.size) is a [`ReferenceListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ReferenceListProperty) of
([`width`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.width), [`height`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.height)) properties.

**kivy.uix.widget.Widget.size_hint**

Size hint.
[`size_hint`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.size_hint) is a [`ReferenceListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ReferenceListProperty) of
([`size_hint_x`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.size_hint_x), [`size_hint_y`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.size_hint_y)) properties.
See [`size_hint_x`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.size_hint_x) for more information.

**kivy.uix.widget.Widget.size_hint_max**

Maximum size when using [`size_hint`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.size_hint).
[`size_hint_max`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.size_hint_max) is a [`ReferenceListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ReferenceListProperty)
of ([`size_hint_max_x`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.size_hint_max_x), [`size_hint_max_y`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.size_hint_max_y)) properties.
New in version 1.10.0.

**kivy.uix.widget.Widget.size_hint_max_x**

When not None, the x-direction maximum size (in pixels,
like [`width`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.width)) when [`size_hint_x`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.size_hint_x) is also not None.
Similar to [`size_hint_min_x`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.size_hint_min_x), except that it sets the maximum width.
[`size_hint_max_x`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.size_hint_max_x) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to None.
New in version 1.10.0.

**kivy.uix.widget.Widget.size_hint_max_y**

When not None, the y-direction maximum size (in pixels,
like [`height`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.height)) when [`size_hint_y`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.size_hint_y) is also not None.
Similar to [`size_hint_min_y`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.size_hint_min_y), except that it sets the maximum height.
[`size_hint_max_y`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.size_hint_max_y) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to None.
New in version 1.10.0.

**kivy.uix.widget.Widget.size_hint_min**

Minimum size when using [`size_hint`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.size_hint).
[`size_hint_min`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.size_hint_min) is a [`ReferenceListProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.ReferenceListProperty)
of ([`size_hint_min_x`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.size_hint_min_x), [`size_hint_min_y`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.size_hint_min_y)) properties.
New in version 1.10.0.

**kivy.uix.widget.Widget.size_hint_min_x**

When not None, the x-direction minimum size (in pixels,
like [`width`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.width)) when [`size_hint_x`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.size_hint_x) is also not None.
When [`size_hint_x`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.size_hint_x) is not None, it is the minimum width that the
widget will be set due to the [`size_hint_x`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.size_hint_x). I.e. when a smaller size
would be set, [`size_hint_min_x`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.size_hint_min_x) is the value used instead for the
widget width. When None, or when [`size_hint_x`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.size_hint_x) is None,
[`size_hint_min_x`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.size_hint_min_x) doesn’t do anything.
Only the [`Layout`](https://kivy.org/doc/stable/api-kivy.uix.layout.html#kivy.uix.layout.Layout) and
`Window` classes make use of the hint.
[`size_hint_min_x`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.size_hint_min_x) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to None.
New in version 1.10.0.

**kivy.uix.widget.Widget.size_hint_min_y**

When not None, the y-direction minimum size (in pixels,
like [`height`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.height)) when [`size_hint_y`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.size_hint_y) is also not None.
When [`size_hint_y`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.size_hint_y) is not None, it is the minimum height that the
widget will be set due to the [`size_hint_y`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.size_hint_y). I.e. when a smaller size
would be set, [`size_hint_min_y`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.size_hint_min_y) is the value used instead for the
widget height. When None, or when [`size_hint_y`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.size_hint_y) is None,
[`size_hint_min_y`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.size_hint_min_y) doesn’t do anything.
Only the [`Layout`](https://kivy.org/doc/stable/api-kivy.uix.layout.html#kivy.uix.layout.Layout) and
`Window` classes make use of the hint.
[`size_hint_min_y`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.size_hint_min_y) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to None.
New in version 1.10.0.

**kivy.uix.widget.Widget.size_hint_x**

x size hint. Represents how much space the widget should use in the
direction of the x axis relative to its parent’s width.
Only the [`Layout`](https://kivy.org/doc/stable/api-kivy.uix.layout.html#kivy.uix.layout.Layout) and
`Window` classes make use of the hint.
The size_hint is used by layouts for two purposes:
When the layout considers widgets on their own rather than in
relation to its other children, the size_hint_x is a direct proportion
of the parent width, normally between 0.0 and 1.0. For instance, a
widget with `size_hint_x=0.5` in
a vertical BoxLayout will take up half the BoxLayout’s width, or
a widget in a FloatLayout with `size_hint_x=0.2` will take up 20%
of the FloatLayout width. If the size_hint is greater than 1, the
widget will be wider than the parent.
When multiple widgets can share a row of a layout, such as in a
horizontal BoxLayout, their widths will be their size_hint_x as a
fraction of the sum of widget size_hints. For instance, if the
size_hint_xs are (0.5, 1.0, 0.5), the first widget will have a
width of 25% of the parent width.
[`size_hint_x`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.size_hint_x) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 1.

**kivy.uix.widget.Widget.size_hint_y**

y size hint.
[`size_hint_y`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.size_hint_y) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and
defaults to 1.
See [`size_hint_x`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.size_hint_x) for more information, but with widths and heights
swapped.

**kivy.uix.widget.Widget.to_local**

Transform parent coordinates to local (current widget) coordinates.
See [`relativelayout`](https://kivy.org/doc/stable/api-kivy.uix.relativelayout.html#module-kivy.uix.relativelayout) for details on the coordinate
systems.

**kivy.uix.widget.Widget.to_parent**

Transform local (current widget) coordinates to parent coordinates.
See [`relativelayout`](https://kivy.org/doc/stable/api-kivy.uix.relativelayout.html#module-kivy.uix.relativelayout) for details on the coordinate
systems.

**kivy.uix.widget.Widget.to_widget**

Convert the coordinate from window to local (current widget)
coordinates.
See [`relativelayout`](https://kivy.org/doc/stable/api-kivy.uix.relativelayout.html#module-kivy.uix.relativelayout) for details on the coordinate
systems.

**kivy.uix.widget.Widget.to_window**

If `initial` is True, the default, it transforms **parent**
coordinates to window coordinates. Otherwise, it transforms **local**
(current widget) coordinates to window coordinates.
See [`relativelayout`](https://kivy.org/doc/stable/api-kivy.uix.relativelayout.html#module-kivy.uix.relativelayout) for details on the coordinate
systems.

**kivy.uix.widget.Widget.top**

Top position of the widget.
[`top`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.top) is an [`AliasProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.AliasProperty) of
([`y`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.y) + [`height`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.height)).

**kivy.uix.widget.Widget.unregister_for_motion_event**

Unregister to receive motion events of type_id.

New in version 2.1.0.

**kivy.uix.widget.Widget.walk**

Iterator that walks the widget tree starting with this widget and
goes forward returning widgets in the order in which layouts display
them.

For example, given a tree with the following structure:

walking this tree:

New in version 1.9.0.

**kivy.uix.widget.Widget.walk_reverse**

Iterator that walks the widget tree backwards starting with the
widget before this, and going backwards returning widgets in the
reverse order in which layouts display them.
This walks in the opposite direction of [`walk()`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.walk), so a list of the
tree generated with [`walk()`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.walk) will be in reverse order compared
to the list generated with this, provided loopback is True.

For example, given a tree with the following structure:

walking this tree:

New in version 1.9.0.

**kivy.uix.widget.Widget.width**

Width of the widget.
[`width`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.width) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and defaults
to 100.

**kivy.uix.widget.Widget.x**

X position of the widget.
[`x`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.x) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and defaults to 0.

**kivy.uix.widget.Widget.y**

Y position of the widget.
[`y`](https://kivy.org/doc/stable/#kivy.uix.widget.Widget.y) is a [`NumericProperty`](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.NumericProperty) and defaults to 0.

**kivy.uix.widget.WidgetException**

Bases: `Exception`
Fired when the widget gets an exception.

---

## API - [`kivy.utils`](https://kivy.org/doc/stable/api-kivy.utils.html)

**kivy.utils.QueryDict**

Bases: `builtins.dict`
QueryDict is a dict() that can be queried with dot.

New in version 1.0.4.

**kivy.utils.SafeList**

Bases: `builtins.list`
List with a clear() method.

**kivy.utils.SafeList.clear**

Remove all items from list.

**kivy.utils.boundary**

Limit a value between a minvalue and maxvalue.

**kivy.utils.deprecated**

This is a decorator which can be used to mark functions
as deprecated. It will result in a warning being emitted the first time
the function is used.

**kivy.utils.difference**

Return the difference between 2 lists.

**kivy.utils.escape_markup**

Escape markup characters found in the text. Intended to be used when markup
text is activated on the Label:

New in version 1.3.0.

**kivy.utils.format_bytes_to_human**

Format a byte value to a human readable representation (B, KB, MB…).
New in version 1.0.8.

Examples:

**kivy.utils.get_color_from_hex**

Transform a hex string color to a kivy
[`Color`](https://kivy.org/doc/stable/api-kivy.graphics.html#kivy.graphics.Color).

**kivy.utils.get_hex_from_color**

Transform a kivy [`Color`](https://kivy.org/doc/stable/api-kivy.graphics.html#kivy.graphics.Color) to a hex value:

New in version 1.5.0.

**kivy.utils.get_random_color**

Returns a random color (4 tuple).

**kivy.utils.interpolate**

Interpolate between two values, by providing the
reciprocal of the proportion between two points.
Deprecated since version 2.3.0:For animations, consider using the
AnimationTransition.linear() for a similar purpose.

**kivy.utils.intersection**

Return the intersection of 2 lists.

**kivy.utils.is_color_transparent**

Return True if the alpha channel is 0.

**kivy.utils.platform**

A string identifying the current operating system. It is one
of: ‘win’, ‘linux’, ‘android’, ‘macosx’, ‘ios’ or ‘unknown’.
You can use it as follows:

New in version 1.3.0.
Changed in version 1.8.0:platform is now a variable instead of a function.

**kivy.utils.reify**

Bases: `builtins.object`
Put the result of a method which uses this (non-data) descriptor decorator
in the instance dict after the first call, effectively replacing the
decorator with an instance variable.
It acts like @property, except that the function is only ever called once;
after that, the value is cached as a regular attribute. This gives you lazy
attribute creation on objects that are meant to be immutable.
Taken from the [Pyramid project](https://pypi.python.org/pypi/pyramid/).
To use this as a decorator:

**kivy.utils.rgba**

Return a Kivy color (4 value from 0-1 range) from either a hex string or
a list of 0-255 values.
New in version 1.10.0.

**kivy.utils.strtotuple**

Convert a tuple string into a tuple
with some security checks. Designed to be used
with the eval() function:

---

## API - [`kivy.vector`](https://kivy.org/doc/stable/api-kivy.vector.html)

**kivy.vector.Vector**

Bases: `builtins.list`
Vector class. See module documentation for more information.

**kivy.vector.Vector.angle**

Computes the angle between a and b, and returns the angle in
degrees.

**kivy.vector.Vector.distance**

Returns the distance between two points.

**kivy.vector.Vector.distance2**

Returns the distance between two points squared.

**kivy.vector.Vector.dot**

Computes the dot product of a and b.

**kivy.vector.Vector.in_bbox**

Return True if point is in the bounding box defined by a
and b.

**kivy.vector.Vector.length**

Returns the length of a vector.

**kivy.vector.Vector.length2**

Returns the length of a vector squared.

**kivy.vector.Vector.line_intersection**

Finds the intersection point between the lines (1)v1->v2 and (2)v3->v4
and returns it as a vector object.

For math see: [http://en.wikipedia.org/wiki/Line-line_intersection](http://en.wikipedia.org/wiki/Line-line_intersection)

**kivy.vector.Vector.normalize**

Returns a new vector that has the same direction as vec,
but has a length of one.

**kivy.vector.Vector.rotate**

Rotate the vector with an angle in degrees.

**kivy.vector.Vector.segment_intersection**

Finds the intersection point between segments (1)v1->v2 and (2)v3->v4
and returns it as a vector object.

**kivy.vector.Vector.x**

[`x`](https://kivy.org/doc/stable/#kivy.vector.Vector.x) represents the first element in the list.

**kivy.vector.Vector.y**

[`y`](https://kivy.org/doc/stable/#kivy.vector.Vector.y) represents the second element in the list.

---

## API - [`kivy.weakmethod`](https://kivy.org/doc/stable/api-kivy.weakmethod.html)

**kivy.weakmethod.WeakMethod**

Bases: `builtins.object`
Implementation of a
[weakref](http://en.wikipedia.org/wiki/Weak_reference)
for functions and bound methods.

**kivy.weakmethod.WeakMethod.is_dead**

Returns True if the referenced callable was a bound method and
the instance no longer exists. Otherwise, return False.

---

## API - [`kivy.weakproxy`](https://kivy.org/doc/stable/api-kivy.weakproxy.html)

**kivy.weakproxy.WeakProxy**

Bases: `builtins.object`
Replacement for weakref.proxy to support comparisons

---


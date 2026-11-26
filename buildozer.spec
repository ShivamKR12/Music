[app]

# (str) Title of your application
title = Kivy Music

# (str) Package name
package.name = kivymusicapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.shivam.music

# (str) Source code where the main.py lives
source.dir = ./KivyMusicApp

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,otf,json,md

# (list) List of directory to exclude (let empty to not exclude anything)
source.exclude_dirs = tests, cache, bin, .buildozer, .git, __pycache__, .pytest_cache, docs, recipes

# (list) List of exclusions using pattern matching
source.exclude_patterns = tests/*, cache/*, bin/*, *.db, *.db-journal, *.db-wal, *.db-shm, test_tone.wav

# (str) Application versioning (method 1)
version = 0.1.4

# (list) Application requirements
# Pinned to exact system-validated versions to prevent PyPI dependency resolution conflicts
# kivymd is built via local recipe (without materialshapes/pycairo)
requirements = python3,kivy==2.3.1,kivymd,materialyoucolor,asynckivy==0.6.4,pillow==11.2.1,requests==2.32.5,urllib3==2.5.0,yt_dlp,pyjnius,openssl,sqlite3,android

# (str) The directory in which python-for-android should look for your own build recipes
p4a.local_recipes = ./recipes

# (list) Supported orientations
# Valid options are: landscape, portrait, portrait-reverse or landscape-reverse
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Application services (python-for-android background foreground media service)
services = MusicPlayback:service/main.py:foreground

# (list) Permissions
android.permissions = INTERNET, ACCESS_NETWORK_STATE, FOREGROUND_SERVICE, FOREGROUND_SERVICE_MEDIA_PLAYBACK, WAKE_LOCK, POST_NOTIFICATIONS, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, READ_MEDIA_AUDIO, VIBRATE, BLUETOOTH_CONNECT

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK / AAB will support.
android.minapi = 21

# (int) Android NDK API to use. This is the minimum API your app will support, it should usually match android.minapi.
android.ndk_api = 21

# (list) The Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a

# (bool) Allow backup
android.allow_backup = True

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

# (str) Android entry point, default is ok for Kivy-based app
#android.entrypoint = org.kivy.android.PythonActivity

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 0

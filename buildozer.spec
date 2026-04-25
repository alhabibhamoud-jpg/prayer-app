[app]
# (str) Title of your application
title = Prayer Times

# (str) Package name
package.name = prayertimes

# (str) Package domain (needed for android packaging)
package.domain = org.example

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let's include json for prayer data)
source.include_exts = py,ttf,mp3,json

# (str) Application versioning
version = 1.0

# (list) Application requirements
# Added openssl for HTTPS support and requests for API calls
requirements = python3, kivy==2.3.0, requests, certifi, openssl

# (str) Supported orientation
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 31

# (int) Minimum API your APK will support.
android.minapi = 21

# (list) The Android architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) Allow backup
android.allow_backup = True

# (list) Android meta-data messages
android.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-xxxxxxxx~xxxxxx

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = no, 1 = yes)
warn_on_root = 1

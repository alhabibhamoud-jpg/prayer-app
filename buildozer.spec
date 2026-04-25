[app]

title = Prayer Times
package.name = prayertimes
package.domain = org.example

source.dir = .
source.include_exts = py,ttf,mp3

version = 1.0

requirements = python3,kivy

orientation = portrait

fullscreen = 0

android.permissions = INTERNET

android.api = 31
android.minapi = 21

android.archs = arm64-v8a, armeabi-v7a

android.allow_backup = True

[buildozer]

log_level = 2
warn_on_root = 1

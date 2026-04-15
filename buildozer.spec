[app]

title = Subway Runner
package.name = subwayrunner
package.domain = org.subwayrunner

source.dir = .
source.include_exts = py,png,jpg,kv,json

version = 1.0

requirements = python3,kivy

orientation = portrait
fullscreen = 1

android.permissions = INTERNET

android.api = 33
android.minapi = 21

android.private_storage = True

# الأيقونة
icon.filename = icon.png

[buildozer]

log_level = 2
warn_on_root = 1

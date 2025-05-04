[app]

title = CaRT
package.name = CaRT
package.domain = org.example
source.dir = .
source.include_exts = py,json,kv,png,jpg
source.include_patterns = lang/*

version = 1.0

requirements = python3,kivy==2.3.1,kivymd==1.2.0

icon.filename = icon.png
orientation = portrait
fullscreen = 1

log_level = 2

[buildozer]
arch = arm64-v8a
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
log_level = 2
warn_on_root = 1

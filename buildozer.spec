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

# Запобігає проблемам із кодировкою та перезапуском
android.entrypoint = org.kivy.android.PythonActivity
android.minapi = 24
android.target = 34
android.sdk = 34
android.ndk = 25b
android.ndk_path = 
android.gradle_dependencies = com.android.support:appcompat-v7:28.0.0

# Права доступу
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Інші параметри
log_level = 2
warn_on_root = 1

[buildozer]
log_level = 2
warn_on_root = 1
arch = armeabi-v7a
p4a.branch = develop

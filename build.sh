#!/bin/bash

p4a apk \
  --private=. \
  --package=org.example.cart \
  --name=CaRT \
  --version=1.0 \
  --requirements=python3,kivy==2.3.1,kivymd==1.2.0 \
  --arch=armeabi-v7a \
  --permission=INTERNET \
  --permission=WRITE_EXTERNAL_STORAGE \
  --permission=READ_EXTERNAL_STORAGE \
  --icon=icon.png \
  --orientation=portrait \
  --fullscreen \
  --presplash=icon.png \
  --copy-libs \
  --sdk-dir=$HOME/Android/Sdk \
  --ndk-dir=$HOME/Android/Sdk/ndk/25.2.9519653 \
  --android-api=33

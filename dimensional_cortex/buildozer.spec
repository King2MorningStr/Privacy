
[app]
title = Dimensional Cortex Mobile
package.name = dimensionalcortex
package.domain = org.udac
source.dir = .
source.include_exts = py,kv,txt,enc
version = 1.0.0
requirements = python3,kivy,cryptography
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 23b
android.archs = armeabi-v7a, arm64-v8a
android.permissions = INTERNET

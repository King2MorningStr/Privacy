[app]
title = Dimensional Cortex Mobile
package.name = dimensionalcortex
package.domain = org.dimensionalcortex.app
source.dir = .
source.include_exts = py,kv,txt,enc,png,jpg,gif,json,xml
version = 1.0.0
# Removed Spacy to avoid build complexity (using lite engine)
requirements = python3,kivy,cryptography,numpy,networkx

orientation = portrait
fullscreen = 0

# Add Java source directory
android.add_src = android_src

# Add XML resources
android.add_resource = android_src/udac_accessibility_config.xml
android.manifest_xml = android_src/udac_manifest_additions.xml

# Permissions
android.permissions = INTERNET,SYSTEM_ALERT_WINDOW,BIND_ACCESSIBILITY_SERVICE,RECEIVE_BOOT_COMPLETED,FOREGROUND_SERVICE

# User requested to keep services line
# Note: This refers to Python services.
# UDACAccessibilityService is Java, so it's handled via manifest_xml/add_src.
# However, keeping this line as requested might be interpreted by Buildozer
# as a need to start a service. We point it to the Java class.
android.services = UDACAccessibilityService:org.dimensionalcortex.app.UDACAccessibilityService

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 23b
android.archs = armeabi-v7a, arm64-v8a

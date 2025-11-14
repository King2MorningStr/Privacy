
# Dimensional Cortex Mobile (Local Trinity, Encrypted State)

This is the full mobile build of Dimensional Cortex, running the Trinity
system locally on-device and encrypting user/IP state at rest.

## Contents

- `main.py` – Kivy entrypoint, initializes screens and loads KV.
- `dimensionalcortex.kv` – Root layout and Home navigation.
- `secure_storage.py` – Fernet-based encrypted JSON storage.
- `local_api.py` – In-process API backed by Trinity modules.
- `ui_text_system.py` – Tier descriptions, vector catalog, trade copy.
- `upgrade_screens_mobile.py` – Monetization & trade Kivy screens.
- `backend/` – Trinity core modules:
    - `dimensional_memory_constant_standalone_demo.py`
    - `dimensional_processing_system_standalone_demo.py`
    - `dimensional_energy_regulator.py`
- `buildozer.spec` – Android build config.

## Build Instructions

1. Install buildozer (Linux/WSL recommended):

   ```bash
   pip install buildozer
   ```

2. From this directory, initialize the build:

   ```bash
   buildozer android debug
   ```

3. After the first (long) toolchain setup, your APK will appear in `bin/`:

   ```bash
   bin/dimensionalcortex-1.0.0-debug.apk
   ```

4. Install it on an Android device:

   ```bash
   adb install bin/dimensionalcortex-1.0.0-debug.apk
   ```

On-device, all user tier/vector/trade data is encrypted at rest using a
key derived from a build-time secret plus a per-device ID.

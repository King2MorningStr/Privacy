# UDAC Overlay Controller
# Manages the floating overlay bubble

from jnius import autoclass, cast
from kivy.logger import Logger
from kivy.clock import Clock

class UDACOverlayController:
    def __init__(self):
        self.WindowManager = autoclass('android.view.WindowManager')
        self.PixelFormat = autoclass('android.graphics.PixelFormat')
        self.Gravity = autoclass('android.view.Gravity')
        self.LayoutInflater = autoclass('android.view.LayoutInflater')
        self.View = autoclass('android.view.View')
        self.PythonActivity = autoclass('org.kivy.android.PythonActivity')

        self.activity = self.PythonActivity.mActivity
        self.window_manager = cast(
            'android.view.WindowManager',
            self.activity.getSystemService(self.activity.WINDOW_SERVICE)
        )
        self.overlay_view = None

    def show_overlay(self):
        """Draws the overlay on the screen."""
        if self.overlay_view:
            return # Already shown

        # Run on UI thread
        self.activity.runOnUiThread(Runnable(self._create_view))

    def _create_view(self):
        try:
            # Params for the overlay window
            # TYPE_APPLICATION_OVERLAY is required for Android O+
            TYPE_APPLICATION_OVERLAY = 2038

            params = self.WindowManager.LayoutParams(
                self.WindowManager.LayoutParams.WRAP_CONTENT,
                self.WindowManager.LayoutParams.WRAP_CONTENT,
                TYPE_APPLICATION_OVERLAY,
                self.WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE,
                self.PixelFormat.TRANSLUCENT
            )

            params.gravity = self.Gravity.TOP | self.Gravity.LEFT
            params.x = 0
            params.y = 100

            # Ideally we would inflate an XML layout, but we might not have one compiled in R.
            # So we might need to create a TextView programmatically.
            # For now, let's try to create a simple button/view.

            TextView = autoclass('android.widget.TextView')
            Color = autoclass('android.graphics.Color')

            self.overlay_view = TextView(self.activity)
            self.overlay_view.setText("UDAC")
            self.overlay_view.setBackgroundColor(Color.BLUE)
            self.overlay_view.setTextColor(Color.WHITE)
            self.overlay_view.setPadding(20, 20, 20, 20)

            self.window_manager.addView(self.overlay_view, params)
            Logger.info("UDAC: Overlay shown")

        except Exception as e:
            Logger.error(f"UDAC: Error showing overlay: {e}")

    def update_text(self, text):
        if self.overlay_view:
            def _update():
                self.overlay_view.setText(text)
            self.activity.runOnUiThread(Runnable(_update))

    def hide_overlay(self):
        if self.overlay_view:
            self.activity.runOnUiThread(Runnable(self._remove_view))

    def _remove_view(self):
        if self.overlay_view:
            self.window_manager.removeView(self.overlay_view)
            self.overlay_view = None
            Logger.info("UDAC: Overlay hidden")

# Runnable helper
class Runnable(autoclass('java.lang.Runnable')):
    def __init__(self, func):
        self.func = func
    def run(self):
        self.func()

controller = UDACOverlayController()

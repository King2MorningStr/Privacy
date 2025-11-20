# UDAC Permission Orchestrator
# Handles Android permissions: Accessibility, Overlay, etc.

from jnius import autoclass
from kivy.logger import Logger
from kivy.core.window import Window

class UDACPermissionOrchestrator:
    def __init__(self):
        self.PythonActivity = autoclass('org.kivy.android.PythonActivity')
        self.Settings = autoclass('android.provider.Settings')
        self.Uri = autoclass('android.net.Uri')
        self.Intent = autoclass('android.content.Intent')
        self.Context = autoclass('android.content.Context')
        self.activity = self.PythonActivity.mActivity

    def check_overlay_permission(self):
        """Check if SYSTEM_ALERT_WINDOW permission is granted."""
        if self.Settings.canDrawOverlays(self.activity):
            Logger.info("UDAC: Overlay permission granted.")
            return True
        else:
            Logger.info("UDAC: Overlay permission NOT granted.")
            return False

    def request_overlay_permission(self):
        """Request SYSTEM_ALERT_WINDOW permission."""
        if not self.check_overlay_permission():
            intent = self.Intent(
                self.Settings.ACTION_MANAGE_OVERLAY_PERMISSION,
                self.Uri.parse("package:" + self.activity.getPackageName())
            )
            self.activity.startActivityForResult(intent, 101)

    def check_accessibility_permission(self):
        """Check if Accessibility Service is enabled."""
        accessibility_enabled = 0
        try:
            accessibility_enabled = self.Settings.Secure.getInt(
                self.activity.getContentResolver(),
                self.Settings.Secure.ACCESSIBILITY_ENABLED
            )
        except Exception as e:
            Logger.error(f"UDAC: Error checking accessibility: {e}")

        if accessibility_enabled == 1:
            # Detailed check to see if OUR service is enabled
            setting_value = self.Settings.Secure.getString(
                self.activity.getContentResolver(),
                self.Settings.Secure.ENABLED_ACCESSIBILITY_SERVICES
            )
            if setting_value and "UDACAccessibilityService" in setting_value:
                Logger.info("UDAC: Accessibility permission granted.")
                return True

        Logger.info("UDAC: Accessibility permission NOT granted.")
        return False

    def request_accessibility_permission(self):
        """Open Accessibility Settings."""
        if not self.check_accessibility_permission():
            intent = self.Intent(self.Settings.ACTION_ACCESSIBILITY_SETTINGS)
            self.activity.startActivity(intent)

orchestrator = UDACPermissionOrchestrator()

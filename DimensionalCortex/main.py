# main.py – Kivy UI Shell
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.utils import get_color_from_hex
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.utils import platform

# Import new Android modules (will only work on Android, so wrap in try/except or check platform)
try:
    if platform == 'android':
        from backend.UDACPermissionOrchestrator import orchestrator
        from backend.UDACLocalBridge import bridge
        from backend.UDACOverlayController import controller
        from backend.UDACSessionManager import session_manager

        # Use updated import path for TrinitySystem
        from backend.cortex_server import TrinitySystem
except ImportError:
    orchestrator = None
    bridge = None
    controller = None
    session_manager = None
    TrinitySystem = None

class ScreenBase(Screen):
    title = StringProperty('')

class OnboardingScreen(Screen): pass
class DashboardScreen(ScreenBase): pass
class InsightsScreen(ScreenBase): pass
class VectorsScreen(ScreenBase): pass
class TradeProgramScreen(ScreenBase): pass
class SettingsScreen(ScreenBase): pass
class AboutScreen(Screen): pass

class UDACApp(App):
    def build(self):
        # Update KV file name to main.kv which is standard
        Builder.load_file("main.kv")
        sm = ScreenManager()
        sm.background_color = get_color_from_hex("#2C3E50")
        sm.add_widget(OnboardingScreen(name="onboarding"))
        sm.add_widget(DashboardScreen(name="dashboard", title="Dashboard"))
        sm.add_widget(InsightsScreen(name="insights", title="Insights"))
        sm.add_widget(VectorsScreen(name="vectors", title="Vectors"))
        sm.add_widget(TradeProgramScreen(name="trade", title="Trade Program"))
        sm.add_widget(SettingsScreen(name="settings", title="Settings"))
        sm.add_widget(AboutScreen(name="about"))
        sm.current = "onboarding"
        return sm

    def on_start(self):
        if platform == 'android':
            self.init_android_components()

    def init_android_components(self):
        # 1. Check Permissions
        if orchestrator:
            orchestrator.request_overlay_permission()
            orchestrator.request_accessibility_permission()

        # 2. Initialize Trinity Engine
        if TrinitySystem:
            self.trinity = TrinitySystem()

            # 3. Connect Bridge
            if bridge:
                bridge.initialize_engine(self.trinity)
                bridge.start_listening()

        # 4. Show Overlay (optional on start)
        if controller:
            controller.show_overlay()

    def on_stop(self):
        if hasattr(self, 'trinity'):
            self.trinity.shutdown()
        if controller:
            controller.hide_overlay()

if __name__ == "__main__":
    UDACApp().run()

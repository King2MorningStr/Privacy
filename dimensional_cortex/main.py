# main.py – Kivy UI Shell
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.utils import get_color_from_hex
from kivy.properties import StringProperty

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

if __name__ == "__main__":
    UDACApp().run()

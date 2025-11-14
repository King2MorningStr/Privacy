# main.py – Kivy UI Shell
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

class OnboardingScreen(Screen): pass
class DashboardScreen(Screen): pass
class InsightsScreen(Screen): pass
class VectorsScreen(Screen): pass
class TradeProgramScreen(Screen): pass
class SettingsScreen(Screen): pass
class AboutScreen(Screen): pass

class UDACApp(App):
    def build(self):
        Builder.load_file("main.kv")
        sm = ScreenManager()
        sm.add_widget(OnboardingScreen(name="onboarding"))
        sm.add_widget(DashboardScreen(name="dashboard"))
        sm.add_widget(InsightsScreen(name="insights"))
        sm.add_widget(VectorsScreen(name="vectors"))
        sm.add_widget(TradeProgramScreen(name="trade"))
        sm.add_widget(SettingsScreen(name="settings"))
        sm.add_widget(AboutScreen(name="about"))
        sm.current = "onboarding"
        return sm

if __name__ == "__main__":
    UDACApp().run()

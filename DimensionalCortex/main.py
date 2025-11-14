"""
Dimensional Cortex - Kivy Mobile/Desktop App
=============================================
Universal AI Continuity Engine

Buildozer-ready app with Trinity backend integration.
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.core.window import Window
import threading
import requests
import json

# Trinity imports (backend running as subprocess)
import sys
import os

# Add backend path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# ============================================================================
# SCREENS
# ============================================================================

class WelcomeScreen(Screen):
    """Onboarding/Welcome screen"""
    def on_enter(self):
        # Auto-transition to dashboard after showing welcome
        Clock.schedule_once(lambda dt: self.check_server_status(), 2)

    def check_server_status(self):
        try:
            response = requests.get('http://localhost:5000/health', timeout=2)
            if response.status_code == 200:
                self.manager.current = 'dashboard'
            else:
                self.show_setup()
        except:
            self.show_setup()

    def show_setup(self):
        self.manager.current = 'setup'


class SetupScreen(Screen):
    """Server setup and platform selection"""
    status_text = StringProperty("Initializing Trinity System...")

    def on_enter(self):
        # Start Trinity server in background thread
        self.start_trinity_server()

    def start_trinity_server(self):
        def run_server():
            self.status_text = "Starting dimensional processing layers..."
            try:
                from backend import cortex_server
                # Server will run in this thread
                cortex_server.app.run(host='127.0.0.1', port=5000, debug=False)
            except Exception as e:
                self.status_text = f"Error: {str(e)}"

        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()

        # Wait for server to be ready
        Clock.schedule_once(lambda dt: self.check_server_ready(), 3)

    def check_server_ready(self):
        try:
            response = requests.get('http://localhost:5000/health', timeout=1)
            if response.status_code == 200:
                self.status_text = "✓ Trinity System Online"
                Clock.schedule_once(lambda dt: self.go_to_dashboard(), 1)
            else:
                Clock.schedule_once(lambda dt: self.check_server_ready(), 1)
        except:
            Clock.schedule_once(lambda dt: self.check_server_ready(), 1)

    def go_to_dashboard(self):
        self.manager.current = 'dashboard'


class DashboardScreen(Screen):
    """Main dashboard with real-time stats"""
    total_nodes = NumericProperty(0)
    total_crystals = NumericProperty(0)
    energy_presence = NumericProperty(0)
    quasi_count = NumericProperty(0)

    platform_stats = ListProperty([
        {'name': 'ChatGPT', 'percent': 0, 'count': 0, 'color': [0.06, 0.64, 0.50, 1]},
        {'name': 'Claude', 'percent': 0, 'count': 0, 'color': [0.85, 0.47, 0.02, 1]},
        {'name': 'Perplexity', 'percent': 0, 'count': 0, 'color': [0.39, 0.40, 0.95, 1]}
    ])

    insights = ListProperty([
        {'title': '🎯 Waiting for data...', 'text': 'Start conversations to see insights'}
    ])

    def on_enter(self):
        # Start auto-refresh
        self.update_stats()
        Clock.schedule_interval(lambda dt: self.update_stats(), 5)

    def update_stats(self):
        try:
            response = requests.get('http://localhost:5000/stats', timeout=2)
            if response.status_code == 200:
                data = response.json()
                self.parse_stats(data)
        except Exception as e:
            print(f"Stats fetch error: {e}")

    def parse_stats(self, data):
        # Update top cards
        self.total_nodes = data['memory']['total_nodes']
        self.total_crystals = data['crystals']['total_crystals']
        self.energy_presence = int(data['energy']['presence_scale'] * 100)
        self.quasi_count = data['crystals']['level_distribution'].get('QUASI', 0)

        # Update platform breakdown
        platform_breakdown = data['memory'].get('platform_breakdown', {})
        total = sum(platform_breakdown.values())

        if total > 0:
            self.platform_stats = [
                {
                    'name': 'ChatGPT',
                    'percent': int((platform_breakdown.get('chatgpt', 0) / total) * 100),
                    'count': platform_breakdown.get('chatgpt', 0),
                    'color': [0.06, 0.64, 0.50, 1]
                },
                {
                    'name': 'Claude',
                    'percent': int((platform_breakdown.get('claude', 0) / total) * 100),
                    'count': platform_breakdown.get('claude', 0),
                    'color': [0.85, 0.47, 0.02, 1]
                },
                {
                    'name': 'Perplexity',
                    'percent': int((platform_breakdown.get('perplexity', 0) / total) * 100),
                    'count': platform_breakdown.get('perplexity', 0),
                    'color': [0.39, 0.40, 0.95, 1]
                }
            ]

        # Generate insights
        self.generate_insights(data)

    def generate_insights(self, data):
        insights = []

        if self.quasi_count > 0:
            insights.append({
                'title': f'🧠 {self.quasi_count} Self-Governing Concepts',
                'text': f'{self.quasi_count} topics evolved to QUASI level'
            })

        active_platforms = sum(1 for p in self.platform_stats if p['count'] > 0)
        if active_platforms >= 2:
            insights.append({
                'title': '🔗 Multi-Platform Continuity Active',
                'text': f'Using {active_platforms} AI platforms seamlessly'
            })

        if self.energy_presence > 80:
            insights.append({
                'title': f'⚡ High Energy ({self.energy_presence}%)',
                'text': 'System highly engaged across knowledge lattice'
            })

        patterns = data['crystals'].get('recurring_patterns', 0)
        if patterns > 0:
            insights.append({
                'title': f'🎯 {patterns} Patterns Detected',
                'text': 'Recurring conversation patterns identified'
            })

        self.insights = insights if insights else [
            {'title': '🎯 Ready', 'text': 'Start using AI platforms to build continuity'}
        ]


class InsightsScreen(Screen):
    """Detailed cross-platform insights"""
    insights_data = ListProperty([])

    def on_enter(self):
        self.load_insights()

    def load_insights(self):
        try:
            response = requests.get('http://localhost:5000/stats', timeout=2)
            if response.status_code == 200:
                data = response.json()
                self.insights_data = self.generate_detailed_insights(data)
        except:
            pass

    def generate_detailed_insights(self, data):
        insights = []

        # Crystal evolution insights
        for level, count in data['crystals']['level_distribution'].items():
            if count > 0:
                insights.append({
                    'title': f'{level} Crystals: {count}',
                    'detail': f'{count} concepts at {level} evolution stage'
                })

        # Energy diagnostics
        temporal = data['energy'].get('temporal_diagnostics', {})
        insights.append({
            'title': f'Presence: {temporal.get("presence", 0):.2f}',
            'detail': f'Momentum: {temporal.get("presence_momentum_state", "STABLE")}'
        })

        return insights


class UpgradeScreen(Screen):
    """Subscription tiers and payment"""
    current_tier = StringProperty("Free")

    def select_tier(self, tier_name):
        if tier_name == 'free':
            self.show_message("You're on Free tier")
        else:
            # TODO: Integrate payment processor
            self.show_message(f"Upgrade to {tier_name} - Payment coming soon")

    def show_message(self, msg):
        print(msg)


class SettingsScreen(Screen):
    """App settings and configuration"""
    def toggle_capture(self, platform):
        print(f"Toggle capture for {platform}")

    def clear_data(self):
        # Confirmation dialog would go here
        print("Clear data requested")


# ============================================================================
# MAIN APP
# ============================================================================

class DimensionalCortexApp(App):
    """Main Kivy application"""

    def build(self):
        Window.clearcolor = (0.06, 0.05, 0.16, 1)  # Dark purple background

        sm = ScreenManager(transition=FadeTransition())

        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(SetupScreen(name='setup'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        sm.add_widget(InsightsScreen(name='insights'))
        sm.add_widget(UpgradeScreen(name='upgrade'))
        sm.add_widget(SettingsScreen(name='settings'))

        return sm

    def on_start(self):
        """Called when app starts"""
        print("[CORTEX] Dimensional Cortex starting...")

    def on_stop(self):
        """Called when app closes"""
        print("[CORTEX] Shutting down...")
        # Cleanup server if needed


if __name__ == '__main__':
    DimensionalCortexApp().run()

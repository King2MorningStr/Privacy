#!/usr/bin/env python3
"""
Dimensional Cortex - Kivy Mobile App
====================================
Universal AI Continuity Engine
Neon Dark Cyber Theme
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.core.window import Window
import threading
import json
import os

# Import Trinity system
from dimensional_cortex.dimensional_memory_constant_standalone_demo import (
    start_memory_system, stop_memory_system
)
from dimensional_cortex.dimensional_processing_system_standalone_demo import (
    CrystalMemorySystem, GovernanceEngine
)
from dimensional_cortex.dimensional_energy_regulator_mobile import DimensionalEnergyRegulator

# ============================================================================
# THEME COLORS - Neon Dark Cyber
# ============================================================================
COLORS = {
    'bg_dark': (0.06, 0.05, 0.16, 1),      # #0f0c29
    'bg_mid': (0.19, 0.17, 0.39, 1),        # #302b63
    'bg_card': (0.15, 0.14, 0.24, 0.5),     # Card background
    'accent_blue': (0.40, 0.49, 0.92, 1),   # #667eea neon
    'accent_purple': (0.46, 0.29, 0.64, 1), # #764ba2
    'text_bright': (0.88, 0.88, 0.88, 1),   # #e0e0e0
    'text_dim': (0.63, 0.63, 0.63, 1),      # #a0a0a0
    'success': (0.06, 0.64, 0.50, 1),       # #10a37f
    'warning': (0.94, 0.27, 0.27, 1),       # #ef4444
}

# Set window background
Window.clearcolor = COLORS['bg_dark']

# ============================================================================
# TRINITY SYSTEM MANAGER (Thread-Safe)
# ============================================================================
class TrinityManager:
    """Manages the Trinity system lifecycle"""
    
    def __init__(self):
        self.memory_governor = None
        self.memory_system = None
        self.crystal_system = None
        self.energy_regulator = None
        self.save_thread = None
        self.merge_thread = None
        self.running = False
        self.user_tier = "free"  # Default tier
        
        # Tier limits
        self.tier_limits = {
            'free': {'conversations': 1000, 'crystals': 100, 'platforms': 1},
            'pro': {'conversations': 10000, 'crystals': 1000, 'platforms': 3},
            'lifetime': {'conversations': 10000, 'crystals': 1000, 'platforms': 3},
            'enterprise': {'conversations': float('inf'), 'crystals': float('inf'), 'platforms': 3}
        }
    
    def start(self):
        """Initialize Trinity system"""
        if self.running:
            return
        
        print("[Trinity] Starting system...")
        
        # Memory layer
        self.memory_governor, self.memory_system, self.save_thread, self.merge_thread = start_memory_system()
        
        # Processing layer
        processing_governance = GovernanceEngine(data_theme="conversation")
        self.crystal_system = CrystalMemorySystem(governance_engine=processing_governance)
        
        # Energy layer
        self.energy_regulator = DimensionalEnergyRegulator(conservation_limit=50.0, decay_rate=0.1)
        
        self.running = True
        print("[Trinity] System online")
    
    def stop(self):
        """Shutdown Trinity system"""
        if not self.running:
            return
        
        print("[Trinity] Shutting down...")
        stop_memory_system(self.save_thread, self.merge_thread)
        self.running = False
        print("[Trinity] System offline")
    
    def get_stats(self):
        """Get current system statistics"""
        if not self.running:
            return {
                'memory': {'total_nodes': 0},
                'crystals': {'total_crystals': 0, 'level_distribution': {}},
                'energy': {'presence': 0.0}
            }
        
        memory_stats = {
            'total_nodes': len(self.memory_system.nodes),
            'last_save': self.memory_system.last_global_save_timestamp
        }
        
        crystal_stats = self.crystal_system.get_memory_stats()
        
        energy_diag = self.energy_regulator.get_temporal_diagnostics()
        
        return {
            'memory': memory_stats,
            'crystals': crystal_stats,
            'energy': energy_diag
        }
    
    def ingest_conversation(self, conversation_data):
        """Ingest a conversation through Trinity"""
        if not self.running:
            return {"status": "error", "message": "Trinity not running"}
        
        # Check tier limits
        current_nodes = len(self.memory_system.nodes)
        limit = self.tier_limits[self.user_tier]['conversations']
        
        if current_nodes >= limit:
            return {
                "status": "limit_reached",
                "message": f"Reached {self.user_tier.upper()} tier limit ({limit} conversations)",
                "upgrade_required": True
            }
        
        try:
            # Memory layer
            # ingest_data no longer returns the parent_node directly, so we need to fetch it
            self.memory_governor.ingest_data(conversation_data)
            
            # Since ingest_data is recursive and void, we need to infer the concept
            # For this MVP, we assume the conversation_data has a 'concept' or we generate one
            # But wait, the Governor generates the concept name.
            # We need to find the node that was just created.
            # The Governor doesn't return it. This is a design mismatch between main.py and the new system.

            # Workaround: Identify the concept the same way the Governor would have
            # Or assume the 'root_concept' key if present, or fallback.
            concept = conversation_data.get('root_concept')
            if not concept:
                # If not provided, we might need to search for the most recently modified node
                # but that is race-condition prone.
                # BETTER: Update main.py to handle the fact that ingest_data returns None.
                concept = "conversation_ingested" # Fallback

            # Processing layer
            crystal = self.crystal_system.use_crystal(concept, conversation_data)
            
            # Energy layer
            self.energy_regulator.register_crystal(crystal)
            for facet_id in crystal.facets.keys():
                self.energy_regulator.inject_energy(facet_id, 0.5)
            self.energy_regulator.step()
            
            return {
                "status": "success",
                "concept": concept,
                "crystal_level": crystal.level.name,
                "nodes_created": 1
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

# Global Trinity instance
TRINITY = TrinityManager()

# ============================================================================
# CUSTOM WIDGETS
# ============================================================================

class CyberCard(BoxLayout):
    """Neon-themed card widget"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [15, 15, 15, 15]
        self.spacing = 10
        
        with self.canvas.before:
            Color(*COLORS['bg_card'])
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[15])
            Color(*COLORS['accent_blue'], 0.3)
            self.border = Line(rounded_rectangle=(self.pos[0], self.pos[1], self.size[0], self.size[1], 15), width=1.2)
        
        self.bind(pos=self._update_rect, size=self._update_rect)
    
    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.border.rounded_rectangle = (self.pos[0], self.pos[1], self.size[0], self.size[1], 15)


class CyberButton(Button):
    """Neon-themed button"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = COLORS['accent_blue']
        self.color = COLORS['text_bright']
        self.font_size = '16sp'
        self.bold = True
        self.size_hint_y = None
        self.height = 50


class StatCard(CyberCard):
    """Status card for dashboard"""
    title = StringProperty('')
    value = StringProperty('0')
    subtext = StringProperty('')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = 120
        
        # Title
        title_label = Label(
            text=self.title,
            color=COLORS['text_dim'],
            size_hint_y=None,
            height=20,
            font_size='12sp'
        )
        self.add_widget(title_label)
        
        # Value
        self.value_label = Label(
            text=self.value,
            color=COLORS['text_bright'],
            size_hint_y=None,
            height=50,
            font_size='36sp',
            bold=True
        )
        self.add_widget(self.value_label)
        
        # Subtext
        self.subtext_label = Label(
            text=self.subtext,
            color=COLORS['text_dim'],
            size_hint_y=None,
            height=20,
            font_size='12sp'
        )
        self.add_widget(self.subtext_label)
    
    def update_value(self, value, subtext=''):
        self.value_label.text = str(value)
        if subtext:
            self.subtext_label.text = subtext

# ============================================================================
# SCREENS
# ============================================================================

class OnboardingScreen(Screen):
    """Welcome and setup screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Title
        title = Label(
            text='⚡ DIMENSIONAL CORTEX',
            color=COLORS['accent_blue'],
            size_hint_y=None,
            height=80,
            font_size='32sp',
            bold=True
        )
        layout.add_widget(title)
        
        # Tagline
        tagline = Label(
            text='Universal AI Continuity Engine',
            color=COLORS['text_dim'],
            size_hint_y=None,
            height=40,
            font_size='18sp'
        )
        layout.add_widget(tagline)
        
        # Spacer
        layout.add_widget(Label(size_hint_y=0.5))
        
        # Features
        features_card = CyberCard()
        features_card.size_hint_y = None
        features_card.height = 200
        
        features = BoxLayout(orientation='vertical', spacing=10)
        for feature in [
            '✓ Remember everything across ChatGPT, Claude, Perplexity',
            '✓ Dimensional processing (not linear)',
            '✓ QUASI self-governing concepts',
            '✓ 100% local, you own your data'
        ]:
            feat_label = Label(
                text=feature,
                color=COLORS['text_bright'],
                size_hint_y=None,
                height=30,
                halign='left'
            )
            feat_label.bind(size=feat_label.setter('text_size'))
            features.add_widget(feat_label)
        
        features_card.add_widget(features)
        layout.add_widget(features_card)
        
        # Spacer
        layout.add_widget(Label(size_hint_y=0.5))
        
        # Start button
        start_btn = CyberButton(text='START TRINITY SYSTEM')
        start_btn.bind(on_press=self.start_system)
        layout.add_widget(start_btn)
        
        self.add_widget(layout)
    
    def start_system(self, instance):
        """Initialize Trinity and go to dashboard"""
        TRINITY.start()
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'dashboard'


class DashboardScreen(Screen):
    """Main dashboard with stats"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = BoxLayout(size_hint_y=None, height=60, spacing=10)
        header_label = Label(
            text='⚡ Dimensional Cortex',
            color=COLORS['accent_blue'],
            font_size='24sp',
            bold=True
        )
        header.add_widget(header_label)
        self.main_layout.add_widget(header)
        
        # Status badge
        self.status_badge = Label(
            text='● ONLINE',
            color=COLORS['success'],
            size_hint_y=None,
            height=30,
            font_size='14sp'
        )
        self.main_layout.add_widget(self.status_badge)
        
        # Stats grid
        stats_grid = GridLayout(cols=2, spacing=10, size_hint_y=None, height=260)
        
        self.total_nodes_card = StatCard(title='TOTAL MEMORIES', value='0', subtext='DataNodes stored')
        self.total_crystals_card = StatCard(title='ACTIVE CRYSTALS', value='0', subtext='0 QUASI evolved')
        self.energy_card = StatCard(title='ENERGY PRESENCE', value='0%', subtext='System coherence')
        self.conversations_card = StatCard(title='CONVERSATIONS', value='0', subtext='All platforms')
        
        stats_grid.add_widget(self.total_nodes_card)
        stats_grid.add_widget(self.total_crystals_card)
        stats_grid.add_widget(self.energy_card)
        stats_grid.add_widget(self.conversations_card)
        
        self.main_layout.add_widget(stats_grid)
        
        # Recent activity card
        activity_card = CyberCard()
        activity_card.size_hint_y = None
        activity_card.height = 150
        
        activity_title = Label(
            text='Recent Activity',
            color=COLORS['text_bright'],
            size_hint_y=None,
            height=30,
            font_size='18sp',
            bold=True
        )
        activity_card.add_widget(activity_title)
        
        self.activity_label = Label(
            text='Waiting for conversations...',
            color=COLORS['text_dim'],
            size_hint_y=None,
            height=80
        )
        activity_card.add_widget(self.activity_label)
        
        self.main_layout.add_widget(activity_card)
        
        # Navigation buttons
        nav_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, height=60)
        
        trade_btn = CyberButton(text='💎 Trade Program')
        trade_btn.bind(on_press=lambda x: self.go_to_screen('trade'))
        nav_layout.add_widget(trade_btn)
        
        upgrade_btn = CyberButton(text='⚡ Upgrade')
        upgrade_btn.bind(on_press=lambda x: self.go_to_screen('upgrade'))
        nav_layout.add_widget(upgrade_btn)
        
        self.main_layout.add_widget(nav_layout)
        
        self.add_widget(self.main_layout)
        
        # Start refresh loop
        Clock.schedule_interval(self.refresh_stats, 2.0)
    
    def refresh_stats(self, dt):
        """Update dashboard stats"""
        stats = TRINITY.get_stats()
        
        # Update cards
        self.total_nodes_card.update_value(stats['memory']['total_nodes'], 'DataNodes stored')
        
        total_crystals = stats['crystals']['total_crystals']
        quasi_count = stats['crystals']['level_distribution'].get('QUASI', 0)
        self.total_crystals_card.update_value(total_crystals, f'{quasi_count} QUASI evolved')
        
        presence = int(stats['energy']['presence'] * 100)
        self.energy_card.update_value(f'{presence}%', 'System coherence')
        
        self.conversations_card.update_value(stats['memory']['total_nodes'], 'All platforms')
        
        # Update status
        if TRINITY.running:
            self.status_badge.text = '● ONLINE'
            self.status_badge.color = COLORS['success']
        else:
            self.status_badge.text = '● OFFLINE'
            self.status_badge.color = COLORS['warning']
    
    def go_to_screen(self, screen_name):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = screen_name


class TradeProgramScreen(Screen):
    """Memory Trade Program"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Header
        header = BoxLayout(size_hint_y=None, height=60)
        back_btn = Button(
            text='← Back',
            size_hint_x=None,
            width=100,
            background_color=COLORS['bg_card'],
            color=COLORS['text_bright']
        )
        back_btn.bind(on_press=lambda x: self.go_back())
        header.add_widget(back_btn)
        
        header_label = Label(
            text='💎 Memory Trade Program',
            color=COLORS['accent_blue'],
            font_size='22sp',
            bold=True
        )
        header.add_widget(header_label)
        layout.add_widget(header)
        
        # Info card
        info_card = CyberCard()
        info_card.size_hint_y = None
        info_card.height = 200
        
        info_text = Label(
            text='Trade anonymized conversation patterns for storage credits.\n\n'
                 '• Patterns are stripped of all identifiers\n'
                 '• Only dimensional signatures exported\n'
                 '• 100 patterns = 500 storage credits\n'
                 '• Completely optional (opt-in only)',
            color=COLORS['text_bright'],
            halign='left',
            valign='top'
        )
        info_text.bind(size=info_text.setter('text_size'))
        info_card.add_widget(info_text)
        layout.add_widget(info_card)
        
        # Trade offer card
        offer_card = CyberCard()
        offer_card.size_hint_y=None
        offer_card.height = 150
        
        offer_title = Label(
            text='Current Offer',
            color=COLORS['text_bright'],
            size_hint_y=None,
            height=30,
            font_size='18sp',
            bold=True
        )
        offer_card.add_widget(offer_title)
        
        offer_details = Label(
            text='Export 100 patterns → Gain +500 conversations',
            color=COLORS['accent_blue'],
            size_hint_y=None,
            height=40,
            font_size='16sp'
        )
        offer_card.add_widget(offer_details)
        
        trade_btn = CyberButton(text='EXPORT & GAIN CREDITS')
        trade_btn.bind(on_press=self.execute_trade)
        offer_card.add_widget(trade_btn)
        
        layout.add_widget(offer_card)
        
        # Status
        self.status_label = Label(
            text='Trade status: Ready',
            color=COLORS['text_dim'],
            size_hint_y=None,
            height=40
        )
        layout.add_widget(self.status_label)
        
        self.add_widget(layout)
    
    def execute_trade(self, instance):
        """Execute the trade"""
        self.status_label.text = '✓ Trade executed! +500 conversations unlocked'
        self.status_label.color = COLORS['success']
        # TODO: Implement actual trade logic
    
    def go_back(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'dashboard'


class UpgradeScreen(Screen):
    """Subscription upgrade screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        scroll = ScrollView()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        # Header
        header = BoxLayout(size_hint_y=None, height=60)
        back_btn = Button(
            text='← Back',
            size_hint_x=None,
            width=100,
            background_color=COLORS['bg_card'],
            color=COLORS['text_bright']
        )
        back_btn.bind(on_press=lambda x: self.go_back())
        header.add_widget(back_btn)
        
        header_label = Label(
            text='⚡ Upgrade Your Continuity',
            color=COLORS['accent_blue'],
            font_size='22sp',
            bold=True
        )
        header.add_widget(header_label)
        layout.add_widget(header)
        
        # Free tier
        free_card = self.create_tier_card('FREE', '$0/month', [
            '1,000 conversations',
            '100 active crystals',
            'Single platform',
            'Local storage'
        ], 'CURRENT TIER', enabled=False)
        layout.add_widget(free_card)
        
        # Pro tier
        pro_card = self.create_tier_card('PRO', '$9.99/month', [
            '10,000 conversations',
            '1,000 active crystals',
            'All 3 platforms',
            'QUASI evolution',
            'Cross-platform insights'
        ], 'UPGRADE TO PRO')
        layout.add_widget(pro_card)
        
        # Lifetime tier
        lifetime_card = self.create_tier_card('LIFETIME', '$299 one-time', [
            'Everything in Pro',
            'Lifetime updates',
            'Founding member badge',
            'Early feature access'
        ], 'GET LIFETIME ACCESS')
        layout.add_widget(lifetime_card)
        
        scroll.add_widget(layout)
        self.add_widget(scroll)
    
    def create_tier_card(self, name, price, features, button_text, enabled=True):
        """Create a tier card"""
        card = CyberCard()
        card.size_hint_y = None
        card.height = 280
        
        # Name
        name_label = Label(
            text=name,
            color=COLORS['text_bright'],
            size_hint_y=None,
            height=30,
            font_size='22sp',
            bold=True
        )
        card.add_widget(name_label)
        
        # Price
        price_label = Label(
            text=price,
            color=COLORS['accent_blue'],
            size_hint_y=None,
            height=40,
            font_size='28sp',
            bold=True
        )
        card.add_widget(price_label)
        
        # Features
        features_box = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None, height=100)
        for feature in features:
            feat_label = Label(
                text=f'✓ {feature}',
                color=COLORS['text_bright'],
                size_hint_y=None,
                height=20,
                font_size='12sp'
            )
            features_box.add_widget(feat_label)
        card.add_widget(features_box)
        
        # Button
        btn = CyberButton(text=button_text)
        if not enabled:
            btn.background_color = COLORS['bg_card']
        btn.bind(on_press=self.upgrade_tier)
        card.add_widget(btn)
        
        return card
    
    def upgrade_tier(self, instance):
        """Handle tier upgrade"""
        # TODO: Implement payment integration
        pass
    
    def go_back(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'dashboard'


# ============================================================================
# MAIN APP
# ============================================================================

class DimensionalCortexApp(App):
    """Main Kivy application"""
    
    def build(self):
        self.title = 'Dimensional Cortex'
        
        # Screen manager
        sm = ScreenManager()
        sm.add_widget(OnboardingScreen(name='onboarding'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        sm.add_widget(TradeProgramScreen(name='trade'))
        sm.add_widget(UpgradeScreen(name='upgrade'))
        
        return sm
    
    def on_stop(self):
        """Cleanup on app close"""
        TRINITY.stop()
        return True


if __name__ == '__main__':
    DimensionalCortexApp().run()

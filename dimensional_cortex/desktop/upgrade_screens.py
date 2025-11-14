# upgrade_screens.py - Advanced monetization screens for UDAC
"""
Complete tier comparison, vector marketplace, and trade program UI
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from kivy.uix.progressbar import ProgressBar
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, DictProperty
from kivy.clock import Clock
import requests

# Import UI text
from ui_text_system import *


class TierComparisonScreen(Screen):
    """Full tier comparison with feature breakdown"""
    
    current_tier = StringProperty("free")
    
    def on_enter(self):
        self.load_current_tier()
    
    def load_current_tier(self):
        try:
            response = requests.get('http://localhost:5000/user/tier', timeout=2)
            if response.status_code == 200:
                self.current_tier = response.json().get('tier', 'free')
        except:
            self.current_tier = 'free'
    
    def upgrade_to_tier(self, tier_name):
        if tier_name == 'pro':
            # TODO: Stripe integration
            print("Upgrading to Pro...")
        elif tier_name == 'lifetime':
            print("Purchasing Lifetime...")
        
        # Show success message
        self.show_success(tier_name)
    
    def show_success(self, tier_name):
        if tier_name == 'pro':
            message = SUCCESS_UPGRADED_TO_PRO
        elif tier_name == 'lifetime':
            message = SUCCESS_LIFETIME_PURCHASED
        
        # TODO: Show modal with success message
        print(message)


class VectorStoreScreen(Screen):
    """À la carte vector marketplace"""
    
    owned_vectors = DictProperty({})
    user_tier = StringProperty("free")
    
    def on_enter(self):
        self.load_owned_vectors()
        self.load_user_tier()
    
    def load_owned_vectors(self):
        try:
            response = requests.get('http://localhost:5000/user/vectors', timeout=2)
            if response.status_code == 200:
                self.owned_vectors = response.json().get('vectors', {})
        except:
            self.owned_vectors = {}
    
    def load_user_tier(self):
        try:
            response = requests.get('http://localhost:5000/user/tier', timeout=2)
            if response.status_code == 200:
                self.user_tier = response.json().get('tier', 'free')
        except:
            self.user_tier = 'free'
    
    def is_vector_owned(self, vector_id):
        """Check if user owns this vector"""
        # Pro users get all Pro vectors for free
        if self.user_tier == 'pro' or self.user_tier == 'lifetime':
            vector_info = VECTORS_AVAILABLE.get(vector_id, {})
            if vector_info.get('tier_included') == 'Pro':
                return True
        
        # Check direct ownership
        return self.owned_vectors.get(vector_id, False)
    
    def purchase_vector(self, vector_id):
        vector_info = VECTORS_AVAILABLE[vector_id]
        
        if self.is_vector_owned(vector_id):
            print(f"{vector_info['name']} already owned")
            return
        
        # TODO: Payment processing
        print(f"Purchasing {vector_info['name']} for {vector_info['price']}")
        
        # On success
        success_msg = SUCCESS_VECTOR_PURCHASED.format(
            vector_name=vector_info['name'],
            benefit_description=vector_info['description']
        )
        print(success_msg)
        
        # Reload owned vectors
        self.load_owned_vectors()


class TradeManagerScreen(Screen):
    """Data-for-Memory Trade Program dashboard"""
    
    trade_active = BooleanProperty(False)
    credits_this_month = NumericProperty(0.0)
    total_lifetime_credits = NumericProperty(0.0)
    conversations_shared = NumericProperty(0)
    next_payout_days = NumericProperty(0)
    
    def on_enter(self):
        self.load_trade_status()
        # Auto-refresh every 10 seconds
        Clock.schedule_interval(lambda dt: self.load_trade_status(), 10)
    
    def load_trade_status(self):
        try:
            response = requests.get('http://localhost:5000/trade/status', timeout=2)
            if response.status_code == 200:
                data = response.json()
                self.trade_active = data.get('active', False)
                self.credits_this_month = data.get('credits_this_month', 0.0)
                self.total_lifetime_credits = data.get('total_credits', 0.0)
                self.conversations_shared = data.get('conversations_shared', 0)
                self.next_payout_days = data.get('days_until_payout', 0)
        except:
            pass
    
    def toggle_trade_program(self, active):
        """Enable or disable trade program"""
        try:
            response = requests.post(
                'http://localhost:5000/trade/toggle',
                json={'active': active},
                timeout=2
            )
            if response.status_code == 200:
                self.trade_active = active
                
                if active:
                    print(SUCCESS_TRADE_ENABLED)
                else:
                    print("Trade Program disabled. Your earned credits remain.")
        except:
            print("Failed to toggle trade program")
    
    def show_onboarding(self):
        """Show trade program onboarding flow"""
        # TODO: Modal with TRADE_ONBOARDING_SCREENS
        print("Showing onboarding...")


class TradeOnboardingScreen(Screen):
    """Multi-step onboarding for Trade Program"""
    
    current_step = NumericProperty(0)
    
    def on_enter(self):
        self.current_step = 0
        self.show_step(0)
    
    def show_step(self, step_index):
        if step_index < len(TRADE_ONBOARDING_SCREENS):
            step_data = TRADE_ONBOARDING_SCREENS[step_index]
            # TODO: Update UI with step_data
            self.current_step = step_index
    
    def next_step(self):
        if self.current_step < len(TRADE_ONBOARDING_SCREENS) - 1:
            self.show_step(self.current_step + 1)
        else:
            # Onboarding complete, enable trade program
            self.complete_onboarding()
    
    def complete_onboarding(self):
        try:
            response = requests.post(
                'http://localhost:5000/trade/toggle',
                json={'active': True},
                timeout=2
            )
            if response.status_code == 200:
                print(SUCCESS_TRADE_ENABLED)
                self.manager.current = 'trade_manager'
        except:
            print("Failed to enable trade program")


class UpgradeLimitPromptScreen(Screen):
    """Modal shown when user hits memory limit"""
    
    limit_type = StringProperty("memory")  # or "vector"
    vector_id = StringProperty("")
    
    def on_enter(self):
        if self.limit_type == "memory":
            self.show_memory_limit_prompt()
        elif self.limit_type == "vector":
            self.show_vector_locked_prompt()
    
    def show_memory_limit_prompt(self):
        # Display UPGRADE_PROMPT_MEMORY_LIMIT
        pass
    
    def show_vector_locked_prompt(self):
        # Display UPGRADE_PROMPT_VECTOR_LOCKED with vector details
        vector_info = VECTORS_AVAILABLE.get(self.vector_id, {})
        # TODO: Format and display prompt
        pass
    
    def action_upgrade_pro(self):
        self.manager.current = 'tier_comparison'
    
    def action_enable_trade(self):
        self.manager.current = 'trade_onboarding'
    
    def action_browse_vectors(self):
        self.manager.current = 'vector_store'


# ============================================================================
# HELPER FUNCTIONS FOR SERVER INTEGRATION
# ============================================================================

def check_memory_limit(current_gb, tier):
    """Returns True if user has hit their tier limit"""
    limits = {
        'free': 10,
        'pro': 50,
        'lifetime': 50
    }
    return current_gb >= limits.get(tier, 10)


def calculate_trade_credits(platforms_used, conversation_count, pattern_diversity):
    """Calculates monthly trade credits"""
    # Formula from TRADE_PROGRAM_CREDIT_FORMULA
    credits = (platforms_used * conversation_count * pattern_diversity) / 1000
    return round(credits, 2)


def get_vector_benefit_text(vector_id):
    """Returns user-friendly benefit text for a vector"""
    vector_info = VECTORS_AVAILABLE.get(vector_id, {})
    return vector_info.get('description', '')

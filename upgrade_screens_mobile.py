
"""Mobile-adapted monetization and trade screens for Kivy.

These talk directly to local_api instead of HTTP.
"""

from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, DictProperty
from kivy.clock import Clock

from ui_text_system import (
    VECTORS_AVAILABLE,
    SUCCESS_UPGRADED_TO_PRO,
    SUCCESS_LIFETIME_PURCHASED,
    SUCCESS_VECTOR_PURCHASED,
    SUCCESS_TRADE_ENABLED,
    TRADE_ONBOARDING_SCREENS,
    UPGRADE_PROMPT_MEMORY_LIMIT,
    UPGRADE_PROMPT_VECTOR_LOCKED,
)
import local_api


class TierComparisonScreen(Screen):
    current_tier = StringProperty("free")
    memory_limit_gb = NumericProperty(0.0)
    current_usage_gb = NumericProperty(0.0)

    def on_enter(self):
        self.load_current_tier()

    def load_current_tier(self):
        data = local_api.get_user_tier()
        self.current_tier = data.get("tier", "free")
        self.memory_limit_gb = data.get("memory_limit_gb", 0.0)
        self.current_usage_gb = data.get("current_usage_gb", 0.0)

    def upgrade_to_tier(self, tier_name):
        result = local_api.upgrade_tier(tier_name)
        if result.get("status") == "success":
            self.current_tier = result.get("new_tier", self.current_tier)
            self.load_current_tier()
            self.show_success(tier_name)
        else:
            print("Upgrade failed:", result.get("message"))

    def show_success(self, tier_name):
        if tier_name == "pro":
            message = SUCCESS_UPGRADED_TO_PRO
        elif tier_name == "lifetime":
            message = SUCCESS_LIFETIME_PURCHASED
        else:
            message = "Tier updated."
        print(message)


class VectorStoreScreen(Screen):
    owned_vectors = DictProperty({})
    user_tier = StringProperty("free")

    def on_enter(self):
        self.refresh_state()

    def refresh_state(self):
        data = local_api.get_user_vectors()
        self.owned_vectors = data.get("vectors", {})
        self.user_tier = data.get("tier", "free")

    def is_vector_owned(self, vector_id):
        if self.user_tier in ("pro", "lifetime"):
            info = VECTORS_AVAILABLE.get(vector_id, {})
            if info.get("tier_included") == "Pro":
                return True
        return self.owned_vectors.get(vector_id, False)

    def purchase_vector(self, vector_id):
        vector_info = VECTORS_AVAILABLE.get(vector_id, {})
        if self.is_vector_owned(vector_id):
            print(f"{vector_info.get('name', vector_id)} already owned")
            return

        result = local_api.purchase_vector(vector_id)
        if result.get("status") == "success":
            success_msg = SUCCESS_VECTOR_PURCHASED.format(
                vector_name=vector_info.get("name", vector_id),
                benefit_description=vector_info.get("description", ""),
            )
            print(success_msg)
            self.refresh_state()
        else:
            print("Purchase failed:", result.get("message"))


class TradeManagerScreen(Screen):
    trade_active = BooleanProperty(False)
    credits_this_month = NumericProperty(0.0)
    total_lifetime_credits = NumericProperty(0.0)
    conversations_shared = NumericProperty(0)
    next_payout_days = NumericProperty(0)

    def on_enter(self):
        self.load_trade_status()
        Clock.schedule_interval(lambda dt: self.load_trade_status(), 10)

    def load_trade_status(self):
        data = local_api.get_trade_status()
        self.trade_active = data.get("active", False)
        self.credits_this_month = data.get("credits_this_month", 0.0)
        self.total_lifetime_credits = data.get("total_credits", 0.0)
        self.conversations_shared = data.get("conversations_shared", 0)
        self.next_payout_days = data.get("days_until_payout", 0)

    def toggle_trade_program(self, active):
        result = local_api.toggle_trade_program(active)
        if result.get("status") == "success":
            self.trade_active = result.get("active", self.trade_active)
            if self.trade_active:
                print(SUCCESS_TRADE_ENABLED)
            else:
                print("Trade Program disabled. Earned credits remain.")
        else:
            print("Failed to update Trade Program state")

    def calculate_credits_now(self):
        result = local_api.calculate_trade_credits()
        print("Trade credits recalculated:", result)
        self.load_trade_status()

    def show_onboarding(self):
        if self.manager:
            self.manager.current = "trade_onboarding"


class TradeOnboardingScreen(Screen):
    current_step = NumericProperty(0)

    def on_enter(self):
        self.current_step = 0
        self.show_step(0)

    def show_step(self, index):
        if 0 <= index < len(TRADE_ONBOARDING_SCREENS):
            step = TRADE_ONBOARDING_SCREENS[index]
            self.current_step = index
            print(f"Onboarding step {index+1}: {step['title']}")

    def next_step(self):
        if self.current_step < len(TRADE_ONBOARDING_SCREENS) - 1:
            self.show_step(self.current_step + 1)
        else:
            self.complete_onboarding()

    def complete_onboarding(self):
        result = local_api.toggle_trade_program(True)
        if result.get("status") == "success":
            print(SUCCESS_TRADE_ENABLED)
            if self.manager:
                self.manager.current = "trade_manager"


class UpgradeLimitPromptScreen(Screen):
    limit_type = StringProperty("memory")
    vector_id = StringProperty("")

    def on_enter(self):
        if self.limit_type == "memory":
            self.show_memory_limit_prompt()
        elif self.limit_type == "vector":
            self.show_vector_locked_prompt()

    def show_memory_limit_prompt(self):
        print(UPGRADE_PROMPT_MEMORY_LIMIT)

    def show_vector_locked_prompt(self):
        info = VECTORS_AVAILABLE.get(self.vector_id, {})
        message = UPGRADE_PROMPT_VECTOR_LOCKED + "\n\n" + info.get("description", "")
        print(message)

    def action_upgrade_pro(self):
        if self.manager:
            self.manager.current = "tier_comparison"

    def action_enable_trade(self):
        if self.manager:
            self.manager.current = "trade_onboarding"

    def action_browse_vectors(self):
        if self.manager:
            self.manager.current = "vector_store"

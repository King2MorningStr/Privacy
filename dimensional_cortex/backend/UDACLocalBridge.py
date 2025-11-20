# UDAC Local Bridge - Replaces Flask
# Connects Android Accessibility Events to Dimensional Engine

from jnius import autoclass, cast, PythonJavaClass, java_method
from kivy.logger import Logger
from kivy.clock import Clock
import json
import threading

# Import the engine and components
# Note: Since we are running from main.py, backend is a top-level package in dimensional_cortex
try:
    from backend.dimensional_conversation_engine import DimensionalConversationEngine
    from backend.UDACOverlayController import controller as overlay_controller
    from backend.ContinuityTagger import tagger
except ImportError:
    # Fallback if running in a different context
    from ..backend.dimensional_conversation_engine import DimensionalConversationEngine
    from ..backend.UDACOverlayController import controller as overlay_controller
    from ..backend.ContinuityTagger import tagger

class UDACLocalBridge:
    def __init__(self):
        self.engine = None
        self.is_listening = False
        self.PythonActivity = autoclass('org.kivy.android.PythonActivity')
        self.Context = autoclass('android.content.Context')
        self.Intent = autoclass('android.content.Intent')
        self.IntentFilter = autoclass('android.content.IntentFilter')

        self.receiver = None

    def initialize_engine(self, engine_instance):
        self.engine = engine_instance
        Logger.info("UDAC: Local Bridge Engine Connected")

    def start_listening(self):
        if self.is_listening:
            return

        Logger.info("UDAC: Starting Local Bridge Listener")

        # Define the callback for the BroadcastReceiver
        # Must use PythonJavaClass to override Java methods
        class UDACReceiver(PythonJavaClass):
            __javainterfaces__ = ['android/content/BroadcastReceiver']
            __javabase__ = 'android/content/BroadcastReceiver'

            def __init__(self, callback):
                super().__init__()
                self.callback = callback

            @java_method('(Landroid/content/Context;Landroid/content/Intent;)V')
            def onReceive(self, context, intent):
                try:
                    action = intent.getAction()
                    if action == "org.dimensionalcortex.app.ACCESSIBILITY_EVENT":
                        pkg = intent.getStringExtra("package_name")
                        text = intent.getStringExtra("text")
                        event_type = intent.getIntExtra("event_type", 0)
                        is_editable = intent.getBooleanExtra("is_editable", False)

                        if text:
                            self.callback(pkg, text, event_type, is_editable)
                except Exception as e:
                    Logger.error(f"UDAC: Error in onReceive: {e}")

        self.callback_wrapper = UDACReceiver(self.handle_event)

        activity = self.PythonActivity.mActivity
        intent_filter = self.IntentFilter("org.dimensionalcortex.app.ACCESSIBILITY_EVENT")

        # Register receiver
        activity.registerReceiver(self.callback_wrapper, intent_filter)
        self.is_listening = True

    def handle_event(self, package_name, text, event_type, is_editable):
        Logger.info(f"UDAC: Received event from {package_name} (Editable: {is_editable}): {text[:50]}...")

        if not text:
            return

        if self.engine:
            # Run in a separate thread to not block UI
            threading.Thread(target=self._process_in_engine, args=(text, is_editable)).start()

    def _process_in_engine(self, text, is_editable):
        try:
            # 1. Process with Engine
            response = self.engine.handle_interaction(text)
            Logger.info(f"UDAC: Engine response: {response[:50]}...")

            # 2. Tag/Format Response
            tagged_data = tagger.apply(response, {"is_editable": is_editable})

            # 3. Update Overlay
            if tagged_data and overlay_controller:
                overlay_controller.update_text(tagged_data["display_text"])

        except Exception as e:
            Logger.error(f"UDAC: Engine error: {e}")

bridge = UDACLocalBridge()

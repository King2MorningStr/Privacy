# UDAC Local Bridge - Replaces Flask
# Connects Android Accessibility Events to Dimensional Engine

from jnius import autoclass, cast, PythonJavaClass, java_method
from kivy.logger import Logger
from kivy.clock import Clock
import json
import threading

# Import the engine
from .dimensional_conversation_engine import DimensionalConversationEngine

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

                        if text:
                            self.callback(pkg, text, event_type)
                except Exception as e:
                    Logger.error(f"UDAC: Error in onReceive: {e}")

        self.callback_wrapper = UDACReceiver(self.handle_event)

        activity = self.PythonActivity.mActivity
        intent_filter = self.IntentFilter("org.dimensionalcortex.app.ACCESSIBILITY_EVENT")

        # Register receiver
        activity.registerReceiver(self.callback_wrapper, intent_filter)
        self.is_listening = True

    def handle_event(self, package_name, text, event_type):
        Logger.info(f"UDAC: Received event from {package_name}: {text[:50]}...")

        if not text:
            return

        if self.engine:
            # Run in a separate thread to not block UI
            threading.Thread(target=self._process_in_engine, args=(text,)).start()

    def _process_in_engine(self, text):
        try:
            response = self.engine.handle_interaction(text)
            Logger.info(f"UDAC: Engine response: {response[:50]}...")
            # Here we would send the response back to OverlayController to display
        except Exception as e:
            Logger.error(f"UDAC: Engine error: {e}")

bridge = UDACLocalBridge()

# UDAC Session Manager
# Tracks active AI platform and continuity sessions

class UDACSessionManager:
    def __init__(self):
        self.current_platform = None
        self.current_session_id = None
        self.platform_map = {
            "com.openai.chatgpt": "ChatGPT",
            "com.google.android.apps.bard": "Gemini",
            "com.anthropic.claude": "Claude",
            "com.quora.poe": "Poe"
        }

    def update_context(self, package_name):
        platform = self.identify_platform(package_name)
        if platform != self.current_platform:
            self.current_platform = platform
            self.current_session_id = self._generate_session_id()
            print(f"UDAC: Switched to platform {platform} (Session: {self.current_session_id})")

    def identify_platform(self, package_name):
        # Simple mapping, check if package contains known strings
        if not package_name: return "Unknown"

        for key, name in self.platform_map.items():
            if key in package_name:
                return name

        return "Unknown"

    def _generate_session_id(self):
        import uuid
        return f"sess_{uuid.uuid4().hex[:8]}"

session_manager = UDACSessionManager()


import json
import os
import base64
import hashlib
from cryptography.fernet import Fernet

class SecureStorage:
    """Encrypted JSON storage using Fernet.

    Key is derived from:
    - a build-time app_secret
    - a per-device device_id

    This protects high-level IP/state at rest on the device.
    """

    def __init__(self, app_secret: str, device_id: str):
        key_material = (app_secret + device_id).encode("utf-8")
        digest = hashlib.sha256(key_material).digest()
        key = base64.urlsafe_b64encode(digest)
        self.fernet = Fernet(key)

    def save_json_encrypted(self, path: str, data: dict) -> None:
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        raw = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        token = self.fernet.encrypt(raw)
        with open(path, "wb") as f:
            f.write(token)

    def load_json_encrypted(self, path: str, default=None):
        try:
            with open(path, "rb") as f:
                token = f.read()
            raw = self.fernet.decrypt(token)
            return json.loads(raw.decode("utf-8"))
        except FileNotFoundError:
            return default
        except Exception:
            # corrupted or wrong key -> treat as no data
            return default

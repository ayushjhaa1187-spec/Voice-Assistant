import os
from cryptography.fernet import Fernet
import json

class KeyVault:
    def __init__(self):
        self.key_file = ".june_keys.enc"
        self.master_key = self._get_or_create_master_key()
        self.fernet = Fernet(self.master_key)
        self.keys = self._load_keys()

    def _get_or_create_master_key(self):
        key_path = ".june_master.key"
        if os.path.exists(key_path):
            with open(key_path, 'rb') as f:
                return f.read()
        key = Fernet.generate_key()
        with open(key_path, 'wb') as f:
            f.write(key)
        return key

    def _load_keys(self) -> dict:
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                encrypted = f.read()
            decrypted = self.fernet.decrypt(encrypted)
            return json.loads(decrypted)

        # First time: load from .env
        from dotenv import load_dotenv
        load_dotenv()
        keys = {
            "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY", ""),
            "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
            "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY", ""),
            "PERPLEXITY_API_KEY": os.getenv("PERPLEXITY_API_KEY", ""),
            "TWILIO_ACCOUNT_SID": os.getenv("TWILIO_ACCOUNT_SID", ""),
            "TWILIO_AUTH_TOKEN": os.getenv("TWILIO_AUTH_TOKEN", ""),
            "TWILIO_WHATSAPP_FROM": os.getenv("TWILIO_WHATSAPP_FROM", ""),
        }
        self._save_keys(keys)
        return keys

    def _save_keys(self, keys: dict):
        encrypted = self.fernet.encrypt(json.dumps(keys).encode())
        with open(self.key_file, 'wb') as f:
            f.write(encrypted)

    def get(self, key_name: str) -> str:
        return self.keys.get(key_name, "")

    def set(self, key_name: str, value: str):
        self.keys[key_name] = value
        self._save_keys(self.keys)

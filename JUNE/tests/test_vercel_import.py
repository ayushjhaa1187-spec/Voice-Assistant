import unittest
import sys
import os
from unittest.mock import MagicMock, patch

# Add JUNE to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock Core Dependencies (FastAPI, etc) as existing
sys.modules['fastapi'] = MagicMock()
sys.modules['fastapi.staticfiles'] = MagicMock()
sys.modules['fastapi.responses'] = MagicMock()
sys.modules['pydantic'] = MagicMock()
sys.modules['uvicorn'] = MagicMock()
sys.modules['anthropic'] = MagicMock()
sys.modules['openai'] = MagicMock()
sys.modules['google'] = MagicMock()
sys.modules['google.oauth2'] = MagicMock()
sys.modules['google.oauth2.credentials'] = MagicMock()
sys.modules['googleapiclient'] = MagicMock()
sys.modules['googleapiclient.discovery'] = MagicMock()
sys.modules['httpx'] = MagicMock()
sys.modules['chromadb'] = MagicMock()
sys.modules['dotenv'] = MagicMock()
sys.modules['rich'] = MagicMock()

# Mock cryptography to return bytes
cryptography_mock = MagicMock()
fernet_mock = MagicMock()
fernet_mock.generate_key.return_value = b'key'
fernet_mock.return_value.encrypt.return_value = b'data'
# The KeyVault logic decrypts what it reads from the file.
# If we mock open() to return b'some_bytes', then decrypt(b'some_bytes') must return valid JSON bytes.
fernet_mock.return_value.decrypt.return_value = b'{"api_key": "123"}'
cryptography_mock.fernet.Fernet = fernet_mock
sys.modules['cryptography'] = cryptography_mock
sys.modules['cryptography.fernet'] = cryptography_mock.fernet

# Mock Local-Only Dependencies
sys.modules['playwright'] = MagicMock()
sys.modules['playwright.async_api'] = MagicMock()
sys.modules['pywhatkit'] = MagicMock()
sys.modules['twilio'] = MagicMock()
sys.modules['pyttsx3'] = MagicMock()
sys.modules['speech_recognition'] = MagicMock()
sys.modules['whisper'] = MagicMock()

class TestVercelImport(unittest.TestCase):
    def test_import_api_index(self):
        """Test that api/index.py can be imported successfully with mocked deps"""
        with patch("builtins.open", new_callable=MagicMock) as mock_open:
            handle = mock_open.return_value.__enter__.return_value
            handle.read.return_value = b'some_bytes'

            try:
                import api.index
                self.assertTrue(True)
            except Exception as e:
                self.fail(f"Failed to import api.index: {e}")

if __name__ == '__main__':
    unittest.main()

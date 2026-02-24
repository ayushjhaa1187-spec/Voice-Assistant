import unittest
import sys
import os
import asyncio
from unittest.mock import MagicMock, patch

# Add JUNE to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock external dependencies
sys.modules['anthropic'] = MagicMock()
sys.modules['openai'] = MagicMock()
sys.modules['google'] = MagicMock()
sys.modules['google.oauth2'] = MagicMock()
sys.modules['google.oauth2.credentials'] = MagicMock()
sys.modules['googleapiclient'] = MagicMock()
sys.modules['googleapiclient.discovery'] = MagicMock()
sys.modules['httpx'] = MagicMock()
sys.modules['playwright'] = MagicMock()
sys.modules['playwright.async_api'] = MagicMock()
sys.modules['chromadb'] = MagicMock()
sys.modules['dotenv'] = MagicMock()
sys.modules['pywhatkit'] = MagicMock()
sys.modules['twilio'] = MagicMock()
sys.modules['twilio.rest'] = MagicMock()
sys.modules['pyttsx3'] = MagicMock()
sys.modules['speech_recognition'] = MagicMock()
sys.modules['whisper'] = MagicMock()
sys.modules['rich'] = MagicMock()
sys.modules['fastapi'] = MagicMock()
sys.modules['uvicorn'] = MagicMock()

# Mock cryptography specifically to handle bytes
cryptography_mock = MagicMock()
fernet_mock = MagicMock()
# generate_key must return bytes
fernet_mock.generate_key.return_value = b'some_random_key_bytes_32_chars_long'
# encrypt must return bytes
fernet_mock.return_value.encrypt.return_value = b'encrypted_data'
# decrypt must return bytes (valid json)
fernet_mock.return_value.decrypt.return_value = b'{"api_key": "123"}'

cryptography_mock.fernet.Fernet = fernet_mock
sys.modules['cryptography'] = cryptography_mock
sys.modules['cryptography.fernet'] = cryptography_mock.fernet

# Import Orchestrator after mocking
from core.orchestrator import Orchestrator

class TestFullStack(unittest.TestCase):
    def setUp(self):
        # We also need to mock file operations in KeyVault if we want to avoid file creation,
        # but for now let's just let it write to the temp files or mock open
        with patch("builtins.open", new_callable=MagicMock) as mock_open:
            # Setup mock file handle
            handle = mock_open.return_value.__enter__.return_value
            handle.read.return_value = b'some_bytes'

            self.orchestrator = Orchestrator()

    def test_agent_registration(self):
        expected_agents = ["email", "browser", "calendar", "whatsapp", "search", "tasks", "system", "file"]
        for agent_name in expected_agents:
            self.assertIn(agent_name, self.orchestrator.agents)

    def test_task_agent_methods(self):
        task_agent = self.orchestrator.agents["tasks"]
        self.assertTrue(hasattr(task_agent, "add_task"))
        self.assertTrue(hasattr(task_agent, "list_tasks"))

    def test_system_agent_methods(self):
        system_agent = self.orchestrator.agents["system"]
        self.assertTrue(hasattr(system_agent, "open_app"))

if __name__ == '__main__':
    unittest.main()

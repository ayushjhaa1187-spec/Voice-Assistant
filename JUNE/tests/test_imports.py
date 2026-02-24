import unittest
import sys
import os
from unittest.mock import MagicMock

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
sys.modules['cryptography'] = MagicMock()
sys.modules['cryptography.fernet'] = MagicMock()
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

class TestImports(unittest.TestCase):
    def test_orchestrator_import(self):
        try:
            from core.orchestrator import Orchestrator
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import Orchestrator: {e}")

    def test_agent_imports(self):
        try:
            from agents.email_agent import EmailAgent
            from agents.calendar_agent import CalendarAgent
            from agents.whatsapp_agent import WhatsAppAgent
            from agents.browser_agent import BrowserAgent
            from agents.search_agent import SearchAgent
            from agents.task_agent import TaskAgent
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import Agents: {e}")

    def test_llm_router_imports(self):
        try:
            from llm_router.router import LLMRouter
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import LLMRouter: {e}")

if __name__ == '__main__':
    unittest.main()

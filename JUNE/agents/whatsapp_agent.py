# Uses whatsapp-web.js via Node subprocess OR Twilio API
import subprocess
import json

class WhatsAppAgent:
    def __init__(self):
        self.mode = "web"  # "web" or "twilio"

    async def execute(self, action: str, **kwargs):
        if action == "send":
            return await self.send_message(kwargs.get("to"), kwargs.get("message"))
        elif action == "read":
            return await self.read_messages(kwargs.get("contact"))
        elif action == "reply":
            return await self.reply_message(**kwargs)
        return "Unknown action"

    async def send_message(self, to: str, message: str):
        # Using pywhatkit for simple sending
        try:
            import pywhatkit
            pywhatkit.sendwhatmsg_instantly(to, message, wait_time=10)
            return f"WhatsApp message sent to {to}"
        except ImportError:
            return "pywhatkit not installed"
        except Exception as e:
            return f"Error sending message: {e}"

    async def send_via_twilio(self, to: str, message: str):
        from twilio.rest import Client
        from api_key_manager.key_vault import KeyVault
        vault = KeyVault()

        client = Client(
            vault.get("TWILIO_ACCOUNT_SID"),
            vault.get("TWILIO_AUTH_TOKEN")
        )
        msg = client.messages.create(
            from_=f"whatsapp:{vault.get('TWILIO_WHATSAPP_FROM')}",
            body=message,
            to=f"whatsapp:{to}"
        )
        return f"Message sent: {msg.sid}"

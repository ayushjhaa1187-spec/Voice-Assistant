import anthropic
from api_key_manager.key_vault import KeyVault

class ClaudeClient:
    def __init__(self):
        self.vault = KeyVault()
        self.client = anthropic.Anthropic(
            api_key=self.vault.get("ANTHROPIC_API_KEY")
        )
        self.model = "claude-opus-4-6"

    async def complete(self, prompt: str, system: str = "You are JUNE, a helpful personal AI assistant.") -> str:
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=system,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        except Exception as e:
            return f"Claude error: {str(e)}"

    async def complete_with_image(self, prompt: str, image_b64: str) -> str:
        # Stub for browser control usage
        return "Stub response for image analysis"

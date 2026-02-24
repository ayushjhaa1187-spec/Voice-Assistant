import httpx
from api_key_manager.key_vault import KeyVault

class PerplexityClient:
    def __init__(self):
        self.vault = KeyVault()
        self.api_key = self.vault.get("PERPLEXITY_API_KEY")
        self.base_url = "https://api.perplexity.ai"

    async def complete(self, prompt: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": "llama-3.1-sonar-large-128k-online",
                    "messages": [{"role": "user", "content": prompt}]
                }
            )
            data = response.json()
            return data["choices"][0]["message"]["content"]

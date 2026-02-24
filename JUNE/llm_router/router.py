from llm_router.claude_client import ClaudeClient
from llm_router.gemini_client import GeminiClient
from llm_router.openai_client import OpenAIClient
from llm_router.perplexity_client import PerplexityClient
from llm_router.aggregator import ResultAggregator

class LLMRouter:
    def __init__(self):
        self.clients = {
            "claude": ClaudeClient(),
            "gemini": GeminiClient(),
            "openai": OpenAIClient(),
            "perplexity": PerplexityClient(),
        }
        self.aggregator = ResultAggregator()

        # Task → best LLM mapping
        self.task_routing = {
            "reasoning": "claude",
            "coding": "claude",
            "search": "perplexity",      # Has live web access
            "creative": "openai",
            "analysis": "gemini",
            "factual": "perplexity",
            "synthesis": "claude",       # Claude for final answers
        }

    async def query(self, prompt: str, task_type: str = "synthesis") -> str:
        llm_name = self.task_routing.get(task_type, "claude")
        client = self.clients[llm_name]
        return await client.complete(prompt)

    async def query_all(self, prompt: str) -> dict:
        """Query all LLMs and return all results"""
        import asyncio
        tasks = {
            name: client.complete(prompt)
            for name, client in self.clients.items()
        }
        results = await asyncio.gather(*tasks.values(), return_exceptions=True)
        return dict(zip(tasks.keys(), results))

    async def best_result(self, prompt: str) -> str:
        """Get best answer by querying multiple LLMs and aggregating"""
        all_results = await self.query_all(prompt)
        return await self.aggregator.pick_best(prompt, all_results)

    async def synthesize(self, original_query: str, agent_results: list, history: list) -> str:
        """Claude synthesizes everything into final response"""
        context = "\n".join([str(r) for r in agent_results])
        synthesis_prompt = f"""
You are JUNE, a personal AI assistant.
User asked: {original_query}
Agent results: {context}
History: {history[-5:] if len(history) > 5 else history}

Synthesize a clear, helpful response as JUNE.
"""
        return await self.clients["claude"].complete(synthesis_prompt)

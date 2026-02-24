class ResultAggregator:
    async def pick_best(self, prompt: str, results: dict) -> str:
        # Simple stub to pick the first result or combine them
        return "\n".join([f"{k}: {v}" for k, v in results.items()])

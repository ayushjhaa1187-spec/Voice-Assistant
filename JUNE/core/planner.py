from llm_router.claude_client import ClaudeClient
import json

class Plan:
    def __init__(self, data: dict):
        self.intent = data.get("intent", "")
        self.steps = data.get("steps", [])
        self.parallel = data.get("parallel_possible", False)

class TaskPlanner:
    def __init__(self):
        self.claude = ClaudeClient()

    async def decompose(self, user_input: str, memory_context: list) -> 'Plan':
        prompt = f"""
You are JUNE's task planner. Decompose the user request into executable steps.

User said: "{user_input}"
Memory context: {memory_context[:3]}

Available agents: email, browser, calendar, whatsapp, search, tasks

Return JSON:
{{
  "intent": "brief description",
  "steps": [
    {{
      "step": 1,
      "agent": "agent_name or llm",
      "action": "specific_action",
      "params": {{}},
      "depends_on": []
    }}
  ],
  "parallel_possible": true/false
}}

Only return valid JSON.
"""
        response = await self.claude.complete(prompt)

        try:
            plan_data = json.loads(response)
            return Plan(plan_data)
        except:
            # Fallback: simple LLM-only plan
            return Plan({
                "intent": user_input,
                "steps": [{"agent": "llm", "prompt": user_input, "params": {}}],
                "parallel_possible": False
            })

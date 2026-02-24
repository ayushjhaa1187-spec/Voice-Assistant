import asyncio
from typing import Any
from core.memory import MemoryManager
from core.context_manager import ContextManager
from core.planner import TaskPlanner
from llm_router.router import LLMRouter
from agents.email_agent import EmailAgent
from agents.browser_agent import BrowserAgent
from agents.calendar_agent import CalendarAgent
from agents.whatsapp_agent import WhatsAppAgent
from agents.search_agent import SearchAgent
from agents.task_agent import TaskAgent
from agents.system_agent import SystemAgent
from agents.file_agent import FileAgent

class Orchestrator:
    def __init__(self):
        self.memory = MemoryManager()
        self.context = ContextManager()
        self.planner = TaskPlanner()
        self.llm_router = LLMRouter()

        # Initialize all agents
        self.agents = {
            "email": EmailAgent(),
            "browser": BrowserAgent(),
            "calendar": CalendarAgent(),
            "whatsapp": WhatsAppAgent(),
            "search": SearchAgent(),
            "tasks": TaskAgent(),
            "system": SystemAgent(),
            "file": FileAgent(),
        }

    async def process(self, user_input: str) -> str:
        # 1. Add to context
        self.context.add_message("user", user_input)

        # 2. Retrieve relevant memory
        relevant_memory = self.memory.retrieve(user_input)

        # 3. Plan tasks
        plan = await self.planner.decompose(user_input, relevant_memory)

        # 4. Execute each step
        results = []
        for step in plan.steps:
            result = await self.execute_step(step)
            results.append(result)

        # 5. Synthesize final response
        final_response = await self.llm_router.synthesize(
            user_input, results, self.context.get_history()
        )

        # 6. Store to memory
        self.memory.store(user_input, final_response)
        self.context.add_message("assistant", final_response)

        return final_response

    async def execute_step(self, step: dict) -> Any:
        agent_name = step.get("agent")
        action = step.get("action")
        params = step.get("params", {})

        if agent_name in self.agents:
            try:
                agent = self.agents[agent_name]
                # Check if agent method is async (inspect or just await)
                if asyncio.iscoroutinefunction(agent.execute):
                    return await agent.execute(action, **params)
                else:
                    return agent.execute(action, **params)
            except Exception as e:
                return f"Error executing agent {agent_name}: {e}"

        # Fallback to LLM
        return await self.llm_router.query(step.get("prompt", ""))

from playwright.async_api import async_playwright
import base64
from llm_router.claude_client import ClaudeClient

class BrowserController:
    def __init__(self):
        self.claude = ClaudeClient()
        self.browser = None
        self.page = None

    async def start(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=False)
        self.page = await self.browser.new_page()

    async def navigate(self, url: str):
        await self.page.goto(url)

    async def screenshot_and_analyze(self, task: str) -> str:
        """Take screenshot, send to Claude Vision, get next action"""
        screenshot = await self.page.screenshot()
        b64_image = base64.b64encode(screenshot).decode()

        prompt = f"""
You are controlling a browser for the user.
Task: {task}
Current page: {self.page.url}

Look at this screenshot and tell me what action to take next.
Return JSON: {{"action": "click|type|scroll|navigate", "selector": "css_selector", "value": "optional_value"}}
"""
        response = await self.claude.complete_with_image(prompt, b64_image)
        return response

    async def execute_task(self, task: str):
        """Full autonomous browser task execution"""
        max_steps = 15
        for step in range(max_steps):
            action_json = await self.screenshot_and_analyze(task)

            try:
                import json
                action = json.loads(action_json)

                if action["action"] == "click":
                    await self.page.click(action["selector"])
                elif action["action"] == "type":
                    await self.page.fill(action["selector"], action["value"])
                elif action["action"] == "navigate":
                    await self.page.goto(action["value"])
                elif action["action"] == "done":
                    break

            except Exception as e:
                print(f"Browser action failed: {e}")
                break

    async def close(self):
        await self.browser.close()
        await self.playwright.stop()

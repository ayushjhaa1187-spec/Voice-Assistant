from browser_control.playwright_controller import BrowserController

class BrowserAgent:
    def __init__(self):
        self.controller = BrowserController()
        self.started = False

    async def execute(self, action: str, **kwargs):
        if not self.started:
            await self.controller.start()
            self.started = True

        try:
            if action == "navigate":
                return await self.controller.navigate(kwargs.get("url"))
            elif action == "click":
                return await self.controller.page.click(kwargs.get("selector"))
            elif action == "type":
                return await self.controller.page.fill(kwargs.get("selector"), kwargs.get("text"))
            elif action == "screenshot":
                return await self.controller.page.screenshot(path=kwargs.get("path", "screenshot.png"))
            elif action == "autonomous":
                return await self.controller.execute_task(kwargs.get("task"))
            elif action == "close":
                await self.controller.close()
                self.started = False
                return "Browser closed"
            return "Unknown action"
        except Exception as e:
            return f"Browser error: {e}"

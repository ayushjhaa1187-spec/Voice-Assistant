import asyncio

class CLI:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

    async def run(self):
        print("Type 'exit' to quit.")
        while True:
            try:
                user_input = input("You: ")
                if user_input.lower() in ["exit", "quit"]:
                    break
                response = await self.orchestrator.process(user_input)
                print(f"JUNE: {response}")
            except EOFError:
                break
            except Exception as e:
                print(f"Error: {e}")

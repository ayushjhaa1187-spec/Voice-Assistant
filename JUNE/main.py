import asyncio
from core.orchestrator import Orchestrator
from voice.stt import SpeechToText
from voice.tts import TextToSpeech
from ui.cli.interface import CLI

async def main():
    orchestrator = Orchestrator()
    # Pass orchestrator to CLI so it can process input
    cli = CLI(orchestrator)

    print("🤖 JUNE is online. How can I help?")
    await cli.run()

if __name__ == "__main__":
    asyncio.run(main())

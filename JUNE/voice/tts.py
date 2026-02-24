import pyttsx3

class TextToSpeech:
    def __init__(self):
        try:
            self.engine = pyttsx3.init()
            # Set properties _before_ adding anything to queue
            self.engine.setProperty('rate', 150)    # Speed percent (can go over 100)
            self.engine.setProperty('volume', 0.9)  # Volume 0-1
        except Exception as e:
            print(f"TTS Init Error: {e}")
            self.engine = None

    def speak(self, text: str):
        if self.engine:
            try:
                print(f"[TTS]: {text}")
                self.engine.say(text)
                self.engine.runAndWait()
            except RuntimeError:
                # pyttsx3 loop already running
                pass
            except Exception as e:
                print(f"TTS Error: {e}")
        else:
            print(f"[TTS-Fallback]: {text}")

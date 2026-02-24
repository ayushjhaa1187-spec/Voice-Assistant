import speech_recognition as sr

class SpeechToText:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen(self) -> str:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=5)

            try:
                # Use Google Speech Recognition as a default free fallback
                text = self.recognizer.recognize_google(audio)
                print(f"You said: {text}")
                return text
            except sr.UnknownValueError:
                print("Could not understand audio")
                return ""
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                return ""
        except OSError:
            print("No microphone found (running in server mode?)")
            return ""
        except Exception as e:
            print(f"STT Error: {e}")
            return ""

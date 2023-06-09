import speech_recognition


class SpeechException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class SpeechRecognitionHandler:
    def __init__(self):
        self.handler = speech_recognition.Recognizer()

    def speak(self):
        can_continue = True
        while can_continue:
            with speech_recognition.Microphone() as audio_src:
                print("\nI'm listening...")
                audio = self.handler.listen(audio_src)
            try:
                converted_text = self.handler.recognize_google(audio)
                return converted_text
            except speech_recognition.UnknownValueError:
                print("Quite not catched that. Can you repeat?")
            except speech_recognition.RequestError:
                raise SpeechException("ERROR: Speech Recognition API is not currently working")

import speech_recognition as sr
from gtts import gTTS
import os

class SpeechHandler:
    def __init__(self, language: str = 'en'):
        self.language_code = language # e.g., 'en', 'hi', 'mr'
        self.recognizer = sr.Recognizer()

    def transcribe_audio(self, audio_file_path: str) -> str:
        """
        Takes a .wav file and converts it to text using Google Web Speech API.
        """
        with sr.AudioFile(audio_file_path) as source:
            audio_data = self.recognizer.record(source)
            try:
                # Recognizes text in the self.language_code
                text = self.recognizer.recognize_google(audio_data, language=self.language_code)
                return text
            except sr.UnknownValueError:
                return "[Error: Could not understand audio]"
            except sr.RequestError as e:
                return f"[Error: Speech API Request failed; {e}]"

    def text_to_speech(self, text: str, output_path: str):
        """
        Converts text into an MP3 file using Google Text-to-Speech (gTTS).
        """
        try:
            tts = gTTS(text=text, lang=self.language_code)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            tts.save(output_path)
            return output_path
        except Exception as e:
            return f"[Error: TTS failed; {e}]"

if __name__ == "__main__":
    handler = SpeechHandler('hi')
    print("Speech Handler Ready (Requires Internet for Google API).")

"""
Voice module for speech recognition and text-to-speech functionality
"""
import speech_recognition as sr
import pygame
from gtts import gTTS
import io

class VoiceService:
    def __init__(self):
        pygame.mixer.init()
        self.recognizer = sr.Recognizer()
        
    def speak(self, text):
        """
        Convert text to speech and play it
        
        Args:
            text (str): Text to be spoken
        """
        if not text:
            print("No text to speak.")
            return
            
        print(f"🔊 Speaking: {text}")
        try:
            tts = gTTS(text=text, lang='vi')
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            pygame.mixer.music.load(fp)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except Exception as e:
            print(f"TTS or audio playback error: {e}")
    
    def recognize_speech(self):
        """
        Recognize speech from microphone
        
        Returns:
            str: Recognized text or None if recognition failed
        """
        with sr.Microphone() as source:
            print("🎤 Say your destination:")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
            
        try:
            return self.recognizer.recognize_google(audio, language="vi-VN")
        except sr.UnknownValueError:
            print("Could not recognize speech!")
        except sr.RequestError:
            print("Error connecting to speech recognition service!")
        return None
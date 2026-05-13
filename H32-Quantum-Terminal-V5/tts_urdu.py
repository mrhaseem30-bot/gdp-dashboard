from gtts import gTTS
import os

def speak_urdu(text, filename="urdu_signal.mp3"):
    try:
        tts = gTTS(text=text[:1000], lang='ur', slow=False)
        tts.save(filename)
        return filename
    except Exception as e:
        print("Voice Error:", e)
        return None

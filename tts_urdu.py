from gtts import gTTS

def speak_urdu(text, filename="urdu_signal.mp3"):
    tts = gTTS(text=text[:1000], lang='ur', slow=False)
    tts.save(filename)
    return filename

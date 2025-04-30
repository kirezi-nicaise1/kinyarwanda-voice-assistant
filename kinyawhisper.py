import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
from gtts import gTTS
import pygame

# Record audio
def record_audio(filename="my_audio.wav", duration=5, samplerate=44100):
    print("🎙️ Recording... speak now!")
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
    sd.wait()
    sf.write(filename, recording, samplerate)
    print(f"✅ Audio saved to {filename}")

# Transcribe audio using Google Speech Recognition
def transcribe_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("🎧 Listening from mic...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("🧠 Transcribing...")
        text = recognizer.recognize_google(audio, language="rw-RW")  # Kinyarwanda
        print("📝 You said:", text)
        return text.lower().strip()
    except sr.UnknownValueError:
        print("😵 Couldn’t understand what you said.")
        return ""
    except sr.RequestError:
        print("🌐 Internet error during transcription.")
        return ""

# Match question to pre-defined answer
def match_answer(text):
    qa_pairs = {
        "amakuru yawe": "Ni meza cyane, urakoze.",
        "witwa nde": "Nitwa Umufasha w'Ikoranabuhanga.",
        "urimo gukora iki": "Ndimo kugufasha!",
        "uri nde": "Ndi robot y'umunyarwanda.",
        "wakora iki": "Nshobora kukumva no kugusubiza.",
        "nitwa nde":"witwa Nicaise",
        "ijoro ryiza":"Ijoro ryiza nawe Imana ikurinde"
    }
    return qa_pairs.get(text, "Mbabarira, sinabyumvise neza.")

# Speak the answer using gTTS + pygame
def speak(text, filename="response.mp3"):
    print("🗣️ Speaking:", text)
    tts = gTTS(text=text, lang='en')
    tts.save(filename)

    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

# Main flow
if __name__ == "__main__":
    record_audio()
    user_text = transcribe_speech()
    if user_text:
        reply = match_answer(user_text)
        speak(reply)
    else:
        print("❌ No valid speech to process.")

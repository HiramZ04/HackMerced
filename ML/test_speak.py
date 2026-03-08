import sounddevice as sd
import numpy as np
import wave
import io
import os
from piper.voice import PiperVoice

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
voice = PiperVoice.load(os.path.join(BASE_DIR, "en_US-amy-medium.onnx"))

def speak(msg):
    wav_buffer = io.BytesIO()
    
    # wave.open wraps the BytesIO into a proper WAV writer
    with wave.open(wav_buffer, "wb") as wav_file:
        voice.synthesize_wav(msg, wav_file)
    
    # Read it back
    wav_buffer.seek(0)
    with wave.open(wav_buffer) as wav_file:
        audio_array = np.frombuffer(wav_file.readframes(wav_file.getnframes()), dtype=np.int16)
        samplerate = wav_file.getframerate()

    sd.play(audio_array, samplerate=samplerate)
    sd.wait()

speak(". Hey just to let you know, there is a person 5 meters in front of you  .")
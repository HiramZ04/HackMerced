import sounddevice as sd
import numpy as np
import subprocess
from faster_whisper import WhisperModel
import wave
import io
import os
from piper.voice import PiperVoice

"""
## What is this file about? ##
This file defines the 2 functions we are going to use for the voice and conversational capabilities, we use both a TTS
and a STT, which would be text to audio and audio to text, since the user requests in audio we need to convert it to text
and the text the LLM generates we have to reproduce it in audio since we are working with visually-impared individuals.
"""



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
voice = PiperVoice.load(os.path.join(BASE_DIR, "en_US-amy-medium.onnx")) # this is the voice in ONNX serialized model

# Load Whisper once — not every time we run the function for lattency purposes 
whisper_model = WhisperModel("large-v3", device="cuda")


# Define a function where we could speak the content of a text
# TTS is a text to speech, we are going to use Piper TTS
def speak(msg): 
    msg = msg + " ."  # We add a point so it talks all the way through the oration
    
    wav_buffer = io.BytesIO()
    with wave.open(wav_buffer, "wb") as wav_file:
        voice.synthesize_wav(msg, wav_file)

    wav_buffer.seek(0)
    with wave.open(wav_buffer) as wav_file:
        audio_array = np.frombuffer(wav_file.readframes(wav_file.getnframes()), dtype=np.int16)
        samplerate = wav_file.getframerate() 

    audio_array = (audio_array * 2.0).clip(-32768, 32767).astype(np.int16)  # We make it louder
    sd.play(audio_array, samplerate=samplerate)
    sd.wait()




# Define a function where we could interpret an audio and pass it to text
# STT is a speach to text, we are going to use OpenAI faster-whisper 
def listen(duration=5, samplerate=16000):
    print("Listening...")
    audio = sd.rec(
        int(duration * samplerate),
        samplerate=samplerate,
        channels=1,
        dtype="float32"
    )
    sd.wait()

    audio_np = audio.flatten()
    segments, _ = whisper_model.transcribe(
        audio_np,
        language="en",
        vad_filter=True,   
        beam_size=1        
    )

    transcription = " ".join([seg.text for seg in segments]).strip()
    print(f"User said: {transcription}")
    return transcription if transcription else None


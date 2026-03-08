# test_listen.py
from faster_whisper import WhisperModel
import sounddevice as sd

whisper_model = WhisperModel("large-v3", device="cuda")

print("Di algo...")
audio = sd.rec(int(5 * 16000), samplerate=16000, channels=1, dtype="float32")
sd.wait()

audio_np = audio.flatten()
segments, _ = whisper_model.transcribe(audio_np, language="en")
transcription = " ".join([seg.text for seg in segments])
print(f"Dijiste: {transcription}")
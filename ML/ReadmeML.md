# 🤖 Visual Assistant Robot — ML Module

> HackMerced 2026 — Assistive robot for visually impaired individuals

---

## Overview

This module handles all the AI/ML pipeline for the robot: speech recognition, text-to-speech, object context buffering, LLM inference, and the live dashboard. The robot receives object detection vectors from a Jetson Nano via TCP socket, processes them in real time, and communicates with the user through voice.

---

## File Structure

```
ML/
├── main.py          ← Orchestrates all threads, entry point
├── jetson.py        ← TCP socket connection, buffer, threads
├── llm.py           ← LLM inference (llama3.2:3b + llava:7b via Ollama)
├── alerts.py        ← Hardcoded proximity alerts (no LLM)
├── voice.py         ← STT (Whisper) + TTS (Piper)
├── server.py        ← FastAPI + WebSocket for live dashboard
├── dashboard.html   ← Live demo dashboard for judges
```

---

## Architecture

```
Jetson Nano (YOLO + LiDAR)
    ↓ TCP Socket (raw vectors every 100ms)
Backend Python
    ├── Buffer (updates every 100ms)
    ├── Hard alerts (no LLM, rules-based)
    ├── Whisper (listens to user mic)
    ├── Router → llama3.2:3b (text queries)
    │         → llava:7b (visual queries)
    └── FastAPI WebSocket → dashboard.html
```

### Thread breakdown

| Thread | Function | Description |
|--------|----------|-------------|
| T1 | `thread_vectors()` | Receives object vectors from Jetson every 100ms |
| T2 | `thread_voice_query()` | Listens for user audio, routes to LLM |
| T3 | `thread_alerts()` | Checks buffer and fires hardcoded proximity alerts |
| T4 | `thread_scene_change()` | Compares webcam frames every 10s via VLM |

---

## Models

| Model | Purpose | VRAM |
|-------|---------|------|
| `llama3.2:3b` | Text queries, buffer context | ~2GB |
| `llava:7b` | Visual queries, scene change detection | ~5GB |
| `faster-whisper large-v3` | Speech to text | ~1.5GB |
| `Piper TTS (en_US-amy-medium)` | Text to speech | CPU |

**Total: ~8.5GB VRAM APROX** (tested on RTX 4090 16GB)

---

## Interaction Modes

**Automatic (no user input needed):**
- Hard alerts fire when objects are within danger thresholds (e.g. person < 1.5m, car < 5m)
- Scene change detection notifies user when environment changes significantly

**User-triggered:**
- Text query → `llama3.2:3b` + buffer context (e.g. "Can I keep walking?")
- Visual query → `llava:7b` + webcam frame (e.g. "Where am I?", "What's in front of me?")

---

## Setup

### 1. Install dependencies

```bash
pip install faster-whisper piper-tts sounddevice numpy ollama fastapi "uvicorn[standard]" opencv-python
```

### 2. Pull Ollama models

```bash
ollama pull llama3.2:3b
ollama pull llava:7b
```

### 3. Configure Jetson IP

In `main.py`, update the Jetson Nano IP:
```python
connect_jetson(host="YOUR_JETSON_IP", port=9000)
```

### 4. Run

```bash
cd ML
python main.py
```

Dashboard available at `http://localhost:8000`

---

## Dashboard [THIS WAS NOT USED]

Live demo dashboard built with FastAPI + WebSockets + Plotly. Displays:
- 📷 Webcam feed with bounding boxes
- 🗺️ LiDAR 2D map
- 🔴 Alert history with priority colors
- 💬 LLM conversation transcription in real time

---

## Data Format

Vectors received from Jetson Nano via TCP:
```
"person,0.32,18:53:02"
```
Parsed as: `{ tipo, distancia, tiempo }`

Max buffer size: 10 vectors (sliding window)

---

## Personal Context (RAG Simulated)

User-specific information is injected directly into the system prompt for demo purposes:
- Medications and schedule
- Upcoming appointments
- Emergency contacts
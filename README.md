# 🤖 Visual Assistant Robot — HackMerced 2026

> An AI-powered assistive robot that guides visually impaired individuals in real time through voice, object detection, and environmental awareness.

🌐 **Live Demo:** https://hack-merced-4iq2.vercel.app/

---

## What is this?

A blind-assistive mobile robot that acts as the eyes of a visually impaired person. The robot detects objects and obstacles in its path (and gives alerts), understands the environment through a camera, and communicates everything to the user through natural voice conversation with LLMs.

The user can ask questions like *"Where am I?"*, *"What's in front of me?"*, or *"Can I keep walking?"* and the robot responds instantly. It also proactively warns the user of nearby dangers without being asked.

---

## How it works

```
Jetson Nano (on the robot)
    ├── YOLO object detection → identifies objects + distance
    ├── Webcam → captures environment every 10s
    └── TCP Socket → streams data to the backend

Backend (Python, on laptop/server)
    ├── Receives object vectors every 100ms → context buffer  [Better latency]
    ├── Hard-coded proximity alerts → speaks warnings instantly
    ├── Whisper STT → listens to user voice queries
    ├── Router → decides LLM or VLM based on query type
    │       ├── llama3.2:3b → answers object/context questions
    │       └── llava:7b → answers visual/environment questions
    ├── Piper TTS → speaks the response back to the user
    └── FastAPI + WebSocket → streams live data to dashboard

Frontend (SvelteKit)
    └── Landing page + project information

Dashboard (HTML + Plotly)
    └── Live demo display for judges [WAS NOT USED]
```

---

## Robot Interaction Modes

### 1. Automatic Alerts (no user input)
The robot constantly monitors the buffer and fires voice alerts based on proximity rules — no LLM involved, so latency is near zero.

| Object | Distance Threshold | Alert |
|--------|-------------------|-------|
| Person | < 1.5m | "Stop, there is a person very close" |
| Car | < 5m | "Stop! There is a car way too close!" |
| Train | < 10m | "Stop immediately! There is a train!" |
| Chair | < 1.5m | "Chair in front of you, watch out" |

Alerts have a **priority system** — a train alert cannot be interrupted by a chair alert. An **anti-spam filter** prevents the same alert from firing more than once every 5 seconds.

### 2. Scene Change Detection (automatic)
Every 10 seconds the robot compares the current webcam frame with the previous one using `llava:7b`. If the environment changed significantly, it proactively tells the user:
> *"You are now entering an open outdoor area"*

### 3. Voice Queries (user-initiated)
The user speaks naturally. The system routes the query:

- **Text query** → `llama3.2:3b` + object buffer context
  - *"Can I keep walking?"*
  - *"What's nearby?"*
  - *"What time is my appointment?"*

- **Visual query** → `llava:7b` + on-demand webcam frame
  - *"Where am I?"*
  - *"What's in front of me?"*
  - *"Describe my surroundings"*

---

## Data Flow

The Jetson Nano sends object detection results as lightweight vectors over TCP every 100ms:

```
"person,0.32,18:53:02"
 ↑       ↑       ↑
type  distance  time
```

This keeps WiFi bandwidth minimal — no images are streamed continuously, only small text vectors. Images are only requested on-demand when the user asks a visual question.

---

## Models & Hardware

| Component | Model/Tool | Notes |
|-----------|-----------|-------|
| Object Detection | YOLO (Jetson Nano) | Runs on edge device |
| Speech to Text | faster-whisper large-v3 | ~1.5GB VRAM |
| Text LLM | llama3.2:3b via Ollama | ~2GB VRAM, always active |
| Vision LLM | llava:7b via Ollama | ~5GB VRAM, on-demand |
| Text to Speech | Piper TTS (en_US-amy-medium) | Runs on CPU |

This was tested in a (RTX 4090 16GB VRAM)

---

## Simulated RAG [FUTURE FEATURES]

User-specific personal context is injected into the system prompt to simulate a RAG system:
- Medications and schedule
- Upcoming appointments
- Emergency contacts

This allows the robot to answer personal questions like *"What medications do I take?"* or *"When is my next appointment?"* without a full RAG implementation.

---

## Project Structure

```
HackMerced/
├── ML/                  ← AI/ML pipeline (Python)
│   ├── main.py          ← Entry point, thread orchestration
│   ├── jetson.py        ← TCP socket, buffer, threads
│   ├── llm.py           ← LLM inference + routing
│   ├── alerts.py        ← Hardcoded proximity alerts
│   ├── voice.py         ← Whisper STT + Piper TTS
│   ├── server.py        ← FastAPI + WebSocket dashboard
│   └── dashboard.html   ← Live demo dashboard
└── Landing-Page/        ← SvelteKit frontend
```

---

## Team

Built at HackMerced 2026.

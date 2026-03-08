import asyncio
import base64
import time
import threading
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from jetson import get_buffer_text, get_buffer_images

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Shared state pushed to dashboard ────────────────────────────────────────

dashboard_state = {
    "alerts":        [],   # last 10 alerts [{time, tipo, distancia, level}]
    "transcription": [],   # last exchanges [{role, text}]
    "fps":           0,
    "latency_ms":    0,
    "mode":          "IDLE",  # CONVERSATION | ALERT | IDLE
    "jetson_ok":     False,
    "last_image_b64": None,   # base64 webcam frame
    "lidar_points":  [],       # [{x, y}] points for 2D map
}

state_lock = threading.Lock()


# ── Helper functions called from other modules ───────────────────────────────

def push_alert(tipo, distancia, level="red"):
    """Call this from alerts.py when an alert fires"""
    with state_lock:
        dashboard_state["alerts"].insert(0, {
            "time":      time.strftime("%H:%M:%S"),
            "tipo":      tipo,
            "distancia": distancia,
            "level":     level   # red | yellow | green
        })
        if len(dashboard_state["alerts"]) > 10:
            dashboard_state["alerts"].pop()

def push_transcription(role, text):
    """Call this from llm.py after each inference"""
    with state_lock:
        dashboard_state["transcription"].insert(0, {"role": role, "text": text})
        if len(dashboard_state["transcription"]) > 6:
            dashboard_state["transcription"].pop()

def push_image(img_bytes):
    """Call this from jetson.py when new frame arrives"""
    b64 = base64.b64encode(img_bytes).decode("utf-8")
    with state_lock:
        dashboard_state["last_image_b64"] = b64

def push_lidar(points):
    """Call this from jetson.py with [{x, y}] list"""
    with state_lock:
        dashboard_state["lidar_points"] = points

def set_mode(mode):
    with state_lock:
        dashboard_state["mode"] = mode

def set_jetson_ok(ok):
    with state_lock:
        dashboard_state["jetson_ok"] = ok


# ── WebSocket endpoint ────────────────────────────────────────────────────────

connected_clients = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            with state_lock:
                state_snapshot = dict(dashboard_state)
                state_snapshot["vectors"] = get_buffer_text()
            await websocket.send_json(state_snapshot)
            await asyncio.sleep(0.5)  # push update every 500ms
    except WebSocketDisconnect:
        connected_clients.discard(websocket)


# ── Serve dashboard HTML ──────────────────────────────────────────────────────

@app.get("/")
async def get_dashboard():
    with open("dashboard.html", "r") as f:
        return HTMLResponse(f.read())

# ESTAS SON UNAS APIS ENDPOINTS DE PRUEBA PARA PROBAR CON HOPPSCOTCH ANTES DE QUE TENGAMOS EL ROBOT RUNNING:
@app.post("/test/alert")
def test_alert(tipo: str = "person", distancia: float = 0.5, level: str = "red"):
    push_alert(tipo, distancia, level)
    return {"ok": True}

@app.post("/test/transcript")
def test_transcript(role: str = "user", text: str = "Where am I?"):
    push_transcription(role, text)
    return {"ok": True}

@app.post("/test/lidar")
def test_lidar():
    import random, math
    points = [{"x": math.cos(i)*random.uniform(1,4), "y": math.sin(i)*random.uniform(1,4)} for i in range(30)]
    push_lidar(points)
    return {"ok": True}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
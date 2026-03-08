import threading
import time
from jetson import connect_jetson, thread_vectors, thread_scene_change, get_last_text, thread_voice_query
from alerts import alerts_constant
from voice import speak
import uvicorn

"""
## What is this file about? ##
This file is the responsible to orchestrate all the threads and functions, first, we connect to the Jetson Nano,
then, we run thread 1 every 100 ms (vectors in buffer), we run thread 3 every 10s (environment comparition using images) 
and we wait for the listen() function to check for user audio prompts, run the hard-coded alerts every time we receive 
the vector of information from the Jetson Nano.
"""


def thread_alerts():
    while True:
        last = get_last_text()
        if last:
            alerts_constant(last["tipo"], last["distancia"])
        time.sleep(0.1)  # checks buffer every 100ms

if __name__ == "__main__":

    # Connect to Jetson Nano first
    connect_jetson(host="192.168.1.100", port=9000)  # Function we programmed
    speak("Robot online, ready to assist.")          # Audio confirmation   

    # Define all threads
    threads = [  
        threading.Thread(target=thread_vectors,     daemon=True, name="T1-vectors"),   # Daemon in each thread means if the program dies
        threading.Thread(target=thread_voice_query, daemon=True, name="T2-voice"),     # the thread dies with it. **WHAT HAPPENS IN VEGAS STAYS IN VEGAS** 
        threading.Thread(target=thread_alerts,      daemon=True, name="T3-alerts"),
        threading.Thread(target=thread_scene_change,daemon=True, name="T4-scene"),
    ]

    # Start all threads
    for t in threads:
        t.start()
        print(f"[main] {t.name} started")  # just a simple for to check if everthing worked

    # Keep main thread alive 
    while True:
        time.sleep(1)
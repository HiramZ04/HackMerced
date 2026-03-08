import time
from voice import speak
import threading
# TO DO 
# [] Cuando tengamos la funcion speak( ) vamos a utilizarla para hablar la alerta 
# [] Agregar funcionalidad para poder no pisar alertas y hacerlo por orden de prioridad


last_time_alert = {}
global_priority = 99  # No one giving a alert

priority_lock = threading.Lock() # We need to address what happens if they both threads access the global priority variable at the same time by accident
# We need to lock who can access and that 

# This is a priority list, so the current alert does not get interrupted by a weaker alert o byseversa
PRIORITY = {
    "train":         1,
    "car":           2,
    "truck":         2,
    "bus":           2,
    "motorcycle":    3,
    "person":        4,
    "bicycle":       4,
    "traffic light": 4,
    "stop sign":     5,
    "chair":         6,
    "dining table":  6,
    "couch":         6,
}


def alerts_constant(tipo, distancia): # We pass the parameter to the function only the buffer last log type of object and the distance
    # Global variable contains what is the priority of the current alert
    global global_priority
    
    
    now = time.time() # We assign the time at the moment of the function

    if tipo in last_time_alert: # If the type of this vector was called as a last alert we check the time from the last alert
        if now - last_time_alert[tipo] < 5: # If the last alert of this type of object was less than 5 seconds ago, we exit the function
            return

    current_priority = PRIORITY.get(tipo, 99) # We get the current thread priority

    if current_priority > global_priority: #If there is a message currently running with more priority (Global priority) we let this one pass. Lesser prioirity is more in this logic
        return
    
# we initialize the msg with no value before the Ifs
    msg = None
# We define the alerts, we use elif so the conditional stops at the first true value

    if tipo == "person" and distancia < 1.5:
        msg = "Stop, there is a person very close in front of you, lets wait for the path to be clear"
    elif tipo == "car" and distancia < 5:
        msg = "Stop!!! there is a car way too close!!!"
    elif tipo == "chair" and distancia < 1.5:
        msg = "Chair in front of you, watch out"
    elif tipo == "dining table" and distancia < 1.5:
        msg = "Table ahead, slow down"
    elif tipo == "couch" and distancia < 1.0:
        msg = "Couch ahead"
    elif tipo == "stop sign" and distancia < 4:
        msg = "Let's make a stop here, there is a stop sign!, lets make sure there is no danger"
    elif tipo == "bus" and distancia < 10:
        msg = "Stop! there is a bus ahead, is dangerous!"
    elif tipo == "train" and distancia < 10:
        msg = "Stop immediately!, there is a train in front of you!"
    elif tipo == "truck" and distancia < 10:
        msg = "Stop!! There is a truck ahead"
    elif tipo == "traffic light" and distancia < 10:
        msg = "Traffic light ahead, stop and wait"
  #Without else because msg is already None

# If this log completes the full set of ifs WITH NO MATCH, then the human was not alerted so we put alerted value at False

    if msg:
        with priority_lock:
            if current_priority > global_priority: # Another litte check
                return
            global_priority = current_priority  # Since there is no higher priority task at the moment we take the global priority with our current thread
        # so no task with lower priority can block us
        speak(msg)                          # speak() from voice.py speaks the message 
        with priority_lock:
            global_priority = 99               # Reset after speaking ONLY AFTER SPEAKING, another thread can be running in the back while this one is running
        last_time_alert[tipo] = now         # lAST ALERT FOR THIS TYPE OF OBJECT WAS AT THIS TIME (we save it)
   
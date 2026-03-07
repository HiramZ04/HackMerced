import time
# TO DO 
# [] Cuando tengamos la funcion speak( ) vamos a utilizarla para hablar la alerta 
# [] Agregar funcionalidad para poder no pisar alertas y hacerlo por orden de prioridad


last_time_alert = {}

def alerts_constant(tipo, distancia): # We pass the parameter to the function only the buffer last log type of object and the distance

    now = time.now()

    if tipo in last_time_alert:
        if last_time_alert - now < 5:
            return

# If the time from the last alert was less then 5 seconds then we just exit the function and put alerted value at False
    alerted = True

# We define the alerts, we use elif so the conditional stops at the first true value

    if tipo == "person" and distancia < 1.5:
        print("Stop, there is a person 3 meters in front of you, lets wait for the path to be clear")
    elif tipo == "car" and distancia < 5:
        print("Stop!!! there is a car way to close!!!")
    elif tipo == "chair" and distancia < 1.5:
        print("Chair in front of you, watch out")
    elif tipo == "dining table" and distancia < 1.5:
        print("Table ahead, slow down")
    elif tipo == "couch" and distancia < 1.0:
        print("Couch ahead")
    elif tipo == "stop sign" and distancia < 4:
        print("Let's make a stop here, there is a stop sign!, lets make sure there is no danger")
    elif tipo == "bus" and distancia < 10:
        print("Stop! there is a bus 10 meters at ahead, is dangerous!")
    elif tipo == "train" and distancia < 10:
        print("Stop inmedeatly!, there is a train 10 meters in front of you!")
    elif tipo == "truck" and distancia < 10:
        print("Stop!! There is a truck 10 meters away in front you")
    elif tipo == "traffic light" and distancia < 10:
        print("Traffic light ahead, stop and wait")
    else:
        alerted = False
# If this log completes the full set of ifs, then the human was not alerted so we put alerted value at False

    if alerted:
        last_time_alert[tipo] = now

# Cuando tengamos la funcion speak( ) vamos a utilizarla para hablar la alerta 
def alerts_constant(tipo, distancia): # We pass the parameter to the function only the buffer last log type of object and the distance
    if tipo == "person" and distancia < 3:
        print("Stop, there is a person 3 meters in front of you, lets wait for the path to be clear")
    if tipo == "car" and distancia < 5:
        print("Stop!!!1 there is a car way to close!!!")
    if tipo == "stop sign" and distancia < 4:
        print("Let's make a stop here, there is a stop sign!, lets make sure there is no danger")
    if tipo == "bus" and distancia < 10:
        print("Stop! there is a bus 10 meters at north, is dangerous!")
    if tipo == "train" and distancia < 10:
        print("Stop inmedeatly!, there is a train 10 meters in front of you!")
    if tipo == "truck" and distancia < 10:
        print("Stop!! There is a truck 10 meters away in front you")
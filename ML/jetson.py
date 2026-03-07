import numpy as np
import socket # For the JetsonNano communication

# Define the buffer with the current context, the buffer is going to be fed every 100ms with a new vector of information from the Jetson Nano 
# Trough TCP Socket which is great for low latency, buffer is a RAM memory variable which gets deleted. 
buffer = {
    "vectors": [],        # Objects is a json array with the type of object at sight, the distance and the timestamp (this is the vector of information) 
    "images": []          # This would be the last image sent by the Jetson Nano periodically (10s)
}

# We define the function we call in the Main.py to add new vectors to the buffer
def add_buffer_text(raw_string):
# We parse the raw string we get from the JetNano

    parse = raw_string.split(",") # we split it by commas, this is how we get the info from the JetNano
    object_type1 = parse[0] 
    distance = float(parse[1])
    timestamp = parse[2]


    buffer["vectors"].append({
        "tipo": object_type1,
        "distancia": distance,
        "tiempo": timestamp
    })
# We do a security checkup, and keep the buffer at len 10, if we have more objects than that we pop the last one. 
    if len(buffer["vectors"]) > 10:
        buffer["vectors"].pop(0) 



def add_buffer_img(img):
# We append the image as it comes from the Jetson Nano to the buffer
    buffer["images"].append(img, axis=0)

# We should not have more than 2 images in the buffer, the new one and the old one to compare.
    if len(buffer["images"]) > 2:
        buffer["images"].pop(0)

# We define a function to read the buffer text 
def get_buffer_text():
    return buffer["vectors"]

# We define a function to get the images from the buffer
def get_buffer_images():
    return buffer["images"]

def get_last_text():
    return buffer["vectors"][-1]

def compare_2_images():
    return buffer["images"][0], buffer["images"][1]




# DEFINE JetsonNano Connection
"""
Para esta funcion vamos a definir la conexion con TCP socket para poder pasar los datos del Jetson Nano para.S
"""



# DEFINE JetsonNano thread 1
"""
Definir el thread 1 donde vamos a poner el thread constante que seria recibir cada 100ms los vectores nuevos y actualizar al buffer
"""


# DEFINE JetsonNano thread 2
"""
Para el thread 2 va a ser que el usuario meta un query por medio de audio a el LLM y el thread 2 sera escuchar el query y poder 
pasarselo al LLM con todo y la pregunta, el contexto  
"""

# DEFINE JetsonNano thread 3
"""
Para el thread 3 va a ser que el usuario pregunta "En donde estoy?" y el vamos a pedirle una imagen a la Nano por medio del tcp socket y 
despues pasarle esta imagen al LLM junto con el contexto del buffer, la pregunta y la imagen actualizada 
"""

# DEFINE JetsonNano thread 4
"""
Para el thread 4 vamos a hacer que cuando llegue una imagen nueva al buffer, va a compararala con la imagen vieja, el LLM de vision y 
si si hay muchos cambios como para describirlos o no
"""

import numpy as np
import socket # For the JetsonNano communication
import threading
import time
import json

# Define the buffer with the current context, the buffer is going to be fed every 100ms with a new vector of information from the Jetson Nano 
# Trough TCP Socket which is great for low latency, buffer is a RAM memory variable which gets deleted. 
buffer = {
    "vectors": [],        # Objects is a json array with the type of object at sight, the distance and the timestamp (this is the vector of information) 
    "images": []          # This would be the last image sent by the Jetson Nano periodically (10s)
}

buffer_lock = threading.Lock()  # prevents race conditions between threads, you can not modify a thread being modified, thats the lock

jetson_socket = None  # Global Variable for the websocket


# We define the function we call in the Main.py to add new vectors to the buffer
def add_buffer_text(raw_string):
# We parse the raw string we get from the JetNano

    parse = raw_string.split(",") # we split it by commas, this is how we get the info from the JetNano
    object_type1 = parse[0] 
    distance = float(parse[1])
    timestamp = parse[2]

    with buffer_lock:
        buffer["vectors"].append({
            "tipo": object_type1,
            "distancia": distance,
            "tiempo": timestamp
        })
    # We do a security checkup, and keep the buffer at len 10, if we have more objects than that we pop the last one. 
        if len(buffer["vectors"]) > 10:
            buffer["vectors"].pop(0) 



def add_buffer_img(img):
    with buffer_lock:
# We append the image as it comes from the Jetson Nano to the buffer
        buffer["images"].append(img)
# We should not have more than 2 images in the buffer, the new one and the old one to compare.
        if len(buffer["images"]) > 2:
            buffer["images"].pop(0)

# We define a function to read the buffer text 
def get_buffer_text():
    with buffer_lock:
        return buffer["vectors"]

# We define a function to get the images from the buffer
def get_buffer_images():
    with buffer_lock:
        return buffer["images"]

def get_last_text():
    with buffer_lock:
        return buffer["vectors"][-1] if buffer["vectors"] else None

def compare_2_images():
    with buffer_lock:
        if len(buffer["images"]) < 2:
            return None, None
        return buffer["images"][0], buffer["images"][1]


# --------------------------------------------------------------------------------------------------------- JETSON THREADS --------

# DEFINE JetsonNano Connection
"""
Para esta funcion vamos a definir la conexion con TCP socket para poder pasar los datos del Jetson Nano para.S
"""
def connect_jetson(host="192.168.1.100", port=9000):
    global jetson_socket
    jetson_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    jetson_socket.connect((host, port))
    print(f"Connected to Jetson at {host}:{port}")


# DEFINE FUNCTION to request an image from the JetsonNano
def request_image_from_jetson():
    jetson_socket.sendall(b"GET_IMAGE\n")
    size_data = jetson_socket.recv(8)
    img_size = int.from_bytes(size_data, "big")
    img_bytes = b""
    while len(img_bytes) < img_size:
        img_bytes += jetson_socket.recv(4096)
    return np.frombuffer(img_bytes, dtype=np.uint8)

# DEFINE JetsonNano thread 1
"""
Definir el thread 1 donde vamos a poner el thread constante que seria recibir cada 100ms los vectores nuevos y actualizar al buffer
"""
def thread_vectors():
    while True:
        try:
            raw = jetson_socket.recv(1024).decode("utf-8").strip()
            if raw:
                add_buffer_text(raw)
        except Exception as e:
            print(f"[Thread1] Error: {e}")
            break
        time.sleep(0.1)

# DEFINE JetsonNano thread 2
"""
Para el thread 2 va a ser que el usuario meta un query por medio de audio a el LLM y el thread 2 sera escuchar el query y poder 
pasarselo al LLM con todo y la pregunta, el contexto  
"""
def thread_voice_query():
    from voice import listen, speak
    from llm import infer_text

    while True:
        transcription = listen()  # We listen to the user 
        if transcription:         
            response = infer_text(transcription) # We do an inference on the LLM on the transcription of the audio
            speak(response) # we SPEAK the answer of the LLM


# DEFINE JetsonNano thread 3
"""
Para el thread 3 va a ser que el usuario pregunta "En donde estoy?" y el vamos a pedirle una imagen a la Nano por medio del tcp socket y 
despues pasarle esta imagen al LLM junto con el contexto del buffer, la pregunta y la imagen actualizada 
"""
def thread_visual_query(user_query):
    from voice import speak
    from llm import infer_image
    import tempfile, cv2

    img_array = request_image_from_jetson()
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    # Save temp image so llava can read it
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
        cv2.imwrite(f.name, img)
        response = infer_image(user_query, f.name)

    speak(response)


# DEFINE JetsonNano thread 4
"""
Para el thread 4 vamos a hacer que cuando llegue una imagen nueva al buffer, va a compararala con la imagen vieja, el LLM de vision y 
si si hay muchos cambios como para describirlos o no
"""
def thread_scene_change():
    from voice import speak
    from llm import infer_image
    import tempfile, cv2

    while True:
        time.sleep(10)  # wait for new image to arrive

        old_img, new_img = compare_2_images()
        if old_img is None or new_img is None:
            continue

        # Save both to temp files for llava
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f1, \
             tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f2:

            cv2.imwrite(f1.name, cv2.imdecode(old_img, cv2.IMREAD_COLOR))
            cv2.imwrite(f2.name, cv2.imdecode(new_img, cv2.IMREAD_COLOR))

            response = infer_image(
                "Compare these two images. If the scene changed significantly, describe in one sentence where the person is now. If nothing important changed, respond only with: NO_CHANGE",
                f2.name  # llava solo acepta 1 imagen, le damos la nueva
            )

        if "NO_CHANGE" not in response:
            speak(response)
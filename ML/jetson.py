import numpy as np

# Define the buffer with the current context, the buffer is going to be fed every 100ms with a new vector of information from the Jetson Nano 
# Trough TCP Socket which is great for low latency, buffer is a RAM memory variable which gets deleted. 
buffer = {
    "objetos": [],        # Objects is a json array with the type of object at sight, the distance and the timestamp (this is the vector of information) 
    "images": np.array # This would be the last image sent by the Jetson Nano periodically (10s)
}

# We define the function we call in the Main.py to add new vectors to the buffer
def add_buffer_text(raw_string):
# We parse the raw string we get from the JetNano

    parse = raw_string.split(",") # we split it by commas, this is how we get the info from the JetNano
    type = parse[0] 
    distance = float(parse[1])
    time = parse[2]


    buffer["objetos"].append({
        "tipo": type,
        "distancia": distance,
        "tiempo": time
    })
# We do a security checkup, and keep the buffer at len 10, if we have more objects than that we pop the last one. 
    if len(buffer["objetos"]) > 10:
        buffer["objetos"].pop(0) 

def add_buffer_img(img):
# We append the image as it comes from the Jetson Nano to the buffer
    buffer["images"].np.append(img, axis=0)

# We should not have more than 2 images in the buffer, the new one and the old one to compare.
    if len(buffer["images"]) > 2:
        buffer["images"].pop(0)

def get_buffer_text():
    return buffer["objetos"]

def get_buffer_images():
    return buffer["images"]




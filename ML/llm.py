from ollama import chat
from ollama import ChatResponse
from jetson import get_buffer_text

"""
## What is this file about? ##
This file defines the LLMs we are using, the System prompt so it can answer as we want it for the visually-impaired individuals
It also has a routing function with some keywords so we can route the user query to the VLM or the LLM depending on the request
the user is making.
"""



# This system prompt is really important since it would actually help the model understand what is his function and not exceed certain word limits,
# Setup the alerts that are not hardcoded without LLM and specify how to answer or give the alerts.
system_prompt = """
You are the voice assistant of a robot that guides visually impaired people.
Be concise, max 2 sentences. Never invent objects or distances.
If there is danger say STOP first.
Only use the context provided to you.
"""


# We are going to route the query of the user to the VLM or the LLM depending on what is more suitable
# we COULD use the same LLM to classify the routing but would add latency in the calls for the robot
def routing(query):
    keywords_visual = ["look like", "what am i watching", "what am i looking", 
                   "describe", "where am i", "surroundings", "around me", 
                   "in front", "what is this", "what's this"]
    if any(k in query.lower() for k in keywords_visual):
        return "visual"
    else:
        return "text"




# Deffine the function to make an inference based on text and Lidar metrics
def inference_text(query):
    context = get_buffer_text() or "No objects detected nearby."
    response = chat(model='llama3.2:3b', messages=[
        {
            'role': 'system',
            'content': system_prompt
        },
        {
            'role': 'user',
            'content': f'Here is some context of the Lidar measurements: {context}\n\n{query}'
        }
    ])
    return response['message']['content']



# Define the function to make an inference based on an image
def inference_images(img, query):
    context = get_buffer_text() or "No objects detected nearby."
    response = chat(model='llava:7b', messages=[
        {
            'role': 'system',
            'content': system_prompt
        },
        {
            'role': 'user',
            'content': f'Here is some context of the Lidar measurements: {context}\n\n{query}',
            'images': [img]
        }
    ])
    return response['message']['content']
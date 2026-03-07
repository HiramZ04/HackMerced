from ollama import chat
from ollama import ChatResponse

# This system prompt is really important since it would actually help the model understand what is his function and not exceed certain word limits,
# Setup the alerts that are not hardcoded without LLM and specify how to answer or give the alerts.
system_prompt = """
You are a senior-assistive robot


"""



response: ChatResponse = chat(model='llava:7b', messages=[
  {
    'role': 'user',
    'system': 'You are a the voice of a robot who assists, visually impaired people. The robots goes in front and you basically have to explain to the blind person what are you seeing, the images i sent you is what you have to describe, be conciseeee not more than 15 seconds per explanation',
    'content': 'What am i watching?',
    'images': ["\images\classroom.jpg"],
  }
])
print(response['message']['content'])

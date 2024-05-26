#!~/.pyenv/versions/3.12.2/envs/gpt-4/bin/python

from openai import OpenAI
import os
import json
from IPython.display import display

def show_json(obj):
    display(json.loads(obj.model_dump_json()))

client = OpenAI(
    api_key=os.environ['OPENAI_API_KEY_GPT_4_1']
)

assistant = client.beta.assistants.create(
    name="GPT-4",
    instructions="You are a Helpfull Assistant. You name is GPT-4.1. Answer questions briefly. The less words the better.",
    model="gpt-4-0125-preview"
)

# Print the assistant ID
print(f"Assistant ID: {assistant.id}")

# Create a new thread
thread = client.beta.threads.create()

# Send a message in the thread
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content='Hello, GPT-4.1!',
)

# Show the message JSON
show_json(message)
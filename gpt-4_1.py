#!~/.pyenv/versions/3.12.2/envs/gpt-4/bin/python

from openai import OpenAI
import os
import json, time
from pprint import pprint as pp
from IPython.display import display

ASSISTANT_ID = ''
# THREAD_ID = ''
# RUN_ID = ''

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
ASSISTANT_ID = assistant.id

# thread = client.beta.threads.create()

# message = client.beta.threads.messages.create(
#     thread_id=thread.id,
#     role="user",
#     content='',
# )

# run = client.beta.threads.runs.create(
#     thread_id=thread.id,
#     assistant_id=assistant.id,
# )

# def wait_on_run(run, thread):
#     while run.status == "queued" or run.status == "in_progress":
#         run = client.beta.threads.runs.retrieve(
#             thread_id=thread.id,
#             run_id=run.id,
#         )
#         time.sleep(0.5)
#     return run

# run = wait_on_run(run, thread)

# Create a message to append to our thread
# message = client.beta.threads.messages.create(
#     thread_id=thread.id, role="user", content="Could you explain this to me?"
# )

# Execute our run
# run = client.beta.threads.runs.create(
#     thread_id=thread.id,
#     assistant_id=assistant.id,
# )

# Wait for completion
# wait_on_run(run, thread)




# Retrieve all the messages added after our last user message
# messages = client.beta.threads.messages.list(
#     thread_id=thread.id, order="asc", after=message.id
# )

def submit_message(assistant_id, thread, user_message):
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )
    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )

def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc")





def create_thread_and_run(user_input):
    thread = client.beta.threads.create()
    run = submit_message(ASSISTANT_ID, thread, user_input)
    return thread, run


# # Emulating concurrent user requests
# thread1, run1 = create_thread_and_run(
#     "I need to solve the equation `3x + 11 = 14`. Can you help me?"
# )
# thread2, run2 = create_thread_and_run("Could you explain linear algebra to me?")
# thread3, run3 = create_thread_and_run("I don't like math. What can I do?")

# Now all Runs are executing...






# Pretty printing helper
def pretty_print(messages):
    print("\n" + "# Messages")
    for m in messages:
        print(f"{m.role}: {m.content[0].text.value}") 
    print()

# Pretty printing helper (v.2)
# def pretty_print(messages):
#     # print("\n" + "# Messages")
#     # for m in messages:
#     #     print(f"{m.role}: {m.content[0].text.value}")
#     print(f"{messages.role}: {messages.content[0].text.value}")
#     print()


# Waiting in a loop
def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run


# # Wait for Run 1
# run1 = wait_on_run(run1, thread1)
# pretty_print(get_response(thread1))

# # Wait for Run 2
# run2 = wait_on_run(run2, thread2)
# pretty_print(get_response(thread2))

# # Wait for Run 3
# run3 = wait_on_run(run3, thread3)
# pretty_print(get_response(thread3))

# # Thank our assistant on Thread 3 :)
# run4 = submit_message(ASSISTANT_ID, thread3, "Thank you!")
# run4 = wait_on_run(run4, thread3)
# pretty_print(get_response(thread3))




# def chat_with_gpt(prompt, model="gpt-4-0125-preview", temperature=0.7, max_tokens=150):
#     response = openai.ChatCompletion.create(
#         model=model, 
#         messages=[{"role": "user", "content": prompt}],
#         temperature=temperature,
#         max_tokens=max_tokens
#     )
#     return response.choices[0].message['content'].strip()

def main():
    print("\n" + "Let's chat with GPT-4 Turbo! Type 'quit' to exit." + "\n")
    
    user_input = input("You: ")
    thread, run = create_thread_and_run(user_input)
    run = wait_on_run(run, thread)
    pretty_print(get_response(thread))

    # thread = client.beta.threads.create()
    # message = client.beta.threads.messages.create(thread.id, "user", user_input)
    # run = client.beta.threads.runs.create(thread.id, assistant.id)

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit' or user_input.lower() == 'q':
            break
        run = submit_message(ASSISTANT_ID, thread, user_input)
        run = wait_on_run(run, thread)
        pretty_print(get_response(thread))
    
    # while True:
    #     user_input = input("You: ")
    #     if user_input.lower() == 'quit':
    #         break
        
        # response = chat_with_gpt(user_input)
        # print("GPT-4 Turbo:", response)





if __name__ == "__main__":
    main()

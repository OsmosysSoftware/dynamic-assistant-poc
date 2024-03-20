import time
from openai import OpenAI
import os;

# gets API Key from environment variable OPENAI_API_KEY
client = OpenAI(
    api_key= os.getenv("OPENAI_API_KEY"),
)

policyAssistant = client.beta.assistants.retrieve("asst_E2NTtF5sSbmxT10NvJk9WquB")
skillAssistant = client.beta.assistants.retrieve("asst_6SndT0pLTqkvJTtCcV8Sfaxd")
masterAssistant = client.beta.assistants.retrieve("asst_Zw8OIqpkGHeYpcMMttPS6jzt")

thread = client.beta.threads.create()

def runAssistant(assistant_id,thread_id,user_instructions):
    
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions=user_instructions,
    )

    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

        if run.status == "completed":
            break
        else:
            time.sleep(5)

def classify_question(user_query):

    empty_thread = client.beta.threads.create()

    client.beta.threads.messages.create(
    empty_thread.id,
    role="user",
    content=user_query,
    )
    
    run = client.beta.threads.runs.create(
    thread_id=empty_thread.id,
    assistant_id=masterAssistant.id
    )

    while True:
        run = client.beta.threads.runs.retrieve(thread_id=empty_thread.id, run_id=run.id)

        if run.status == "completed":
            messages = client.beta.threads.messages.list(thread_id=empty_thread.id)
            for message in messages.data:
                if message.role == "assistant":
                    return message.content[0].text.value
                break
        else:     
            time.sleep(2)

def handle_user_query():
    while True:
        user_query = input("Please enter your question (type 'exit' to quit): ")

        if user_query.lower() == "exit":
            break
        
        assistant_id = classify_question(user_query)
        
        if assistant_id:
            runAssistant(assistant_id, thread.id, user_query)
        else:
            print("No assistant found for the query.")

        # Show the final results
        messages = client.beta.threads.messages.list(thread_id=thread.id)

        # Save the text of the messages so that they can be printed in reverse order
        message_store = []

        for message in messages:
            assistant_name = "Policy Assistant: " if message.assistant_id == policyAssistant.id else "Skill Assistant: "
            message_store.append(assistant_name + message.content[0].text.value)

        # To make it more readable, print the messages in reversed order
        for message in reversed(message_store):
            print(message)

handle_user_query()
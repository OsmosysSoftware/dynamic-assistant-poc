import time
from openai import OpenAI
import os;

# gets API Key from environment variable OPENAI_API_KEY
client = OpenAI(
    api_key= os.getenv("OPENAI_API_KEY"),
)

policyAssistant = client.beta.assistants.retrieve("asst_E2NTtF5sSbmxT10NvJk9WquB")
skillAssistant = client.beta.assistants.retrieve("asst_6SndT0pLTqkvJTtCcV8Sfaxd")

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
            print("This run has completed!")

            break
        else:
            print("in progress...")
            time.sleep(5)

def handle_user_query():
    while True:
        user_query = input("Please enter your question (type 'exit' to quit): ")

        if user_query.lower() == "exit":
            break

        if "skill" in user_query.lower():
            runAssistant(skillAssistant.id, thread.id, user_query)
        elif "policy" in user_query.lower():
            runAssistant(policyAssistant.id, thread.id, user_query)
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





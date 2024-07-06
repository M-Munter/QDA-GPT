from django.conf import settings
import openai
import time
from openai import OpenAI
import os
import django
from django.conf import settings

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()


# Adjust these constants
model  = "gpt-3.5-turbo"
file_path = r"C:\Users\MM\PycharmProjects\QDA-GPT_project\data\Interviews.txt"



def get_openai_client():
    """
    Initialize and return an OpenAI client using the API key from Django settings.
    """
    api_key = settings.OPENAI_API_KEY
    if not api_key:
        raise ValueError("Failed to load the OPENAI_API_KEY from settings.\n\n")
    openai.api_key = api_key
    return OpenAI(api_key=api_key)


def initialize_openai_resources(file_path, model):
    client = get_openai_client()

    # Upload a file
    with open(file_path, 'rb') as file_data:
        my_file = client.files.create(
            file=file_data,
            purpose="assistants"
        )
    print(f"File uploaded successfully with ID: {my_file.id}\n")

    # Create Vector Store and upload a file there
    vector_store = client.beta.vector_stores.create(file_ids=[my_file.id])
    print(f"Vector store created successfully with ID: {vector_store.id}\n")
    print(f"File with ID {my_file.id} has been successfully attached to Vector store with ID {vector_store.id}\n")


    # Create an Assistant
    my_assistant = client.beta.assistants.create(
        instructions="Answer question regarding attached data.",
        name="QDA-GPT",
        tools=[{"type": "file_search"}],
        model=model,
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}}
    )
    print(f"Assistant created successfully with ID: {my_assistant.id}\n")

    return my_assistant, my_file, vector_store


# Create one thread
def create_thread():
    try:
        client = get_openai_client()
        thread = client.beta.threads.create()
        print(f"Thread ID: {thread.id}")
        return thread.id
    except Exception as e:
        print(f"Error creating thread: {e}")
        return None


def get_openai_response(content, assistant_id, thread_id):
    client = get_openai_client()

    try:
        # Send message to the thread
        my_thread_message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=content
        )
        print(f"Message sent successfully. Message ID: {my_thread_message.id}\n")

        if not my_thread_message or not my_thread_message.content:
            return "Message creation failed.", "Failure"
        print(f"Message sent to thread. Message ID: {my_thread_message.id}\n")

        # Just create_and_poll for get a terminal state
        print(f">>Running: {assistant_id} <> Thread:", thread_id)
        try:
            run = client.beta.threads.runs.create_and_poll(  # This method is a helper, so you dont need to use a While
                thread_id=thread_id,
                assistant_id=assistant_id,
                # instructions="instructions just for this run if you want"
            )
            print(f">>Run: {run.id}")
        except Exception as e:
            print(f"Error: {e}")

        try:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )
            print(">>Status: ", run_status.status)
        except Exception as e:
            print(f"Error with run: {e}")

        if run_status.status == 'completed':
            print("Run status: completed\n")
            reply_data = client.beta.threads.messages.list(
                thread_id=thread_id,
                run_id=run.id
            )
            # The assistants can return multiple responses in each run, with this code you can obtain multiple responses, within each response there can be different types of content, with this same logic you can obtain files, annotations, images, etc. ..
            for reply in reversed(reply_data.data):
                if reply.role == 'assistant':
                    reply_content = reply.content

                    for reply_item in reply_content:
                        type = reply_item.type
                        if type == 'text':

                            if isinstance(reply_item.text, dict):
                                texto = reply_item.text["value"]
                                print(">>>Answer: ",texto)
                            else:
                                texto = reply_item.text.value
                                print(">>>Answer: ",texto)
        elif run_status.status == 'failed':
            print(">>Failed")
        elif run_status.status == 'requires_action':
            print(">>Use tool submit actions..")

    except Exception as e:
        print(f"An error occurred: {str(e)} \n")
        return "Failed to retrieve a valid response from OpenAI.\n"


def delete_openai_resources(assistant_id, file_id, thread_id, vector_store_id):

    client = get_openai_client()
    print("OpenAI API key loaded successfully. \n")

    results = {}
    try:
        results['file'] = client.files.delete(file_id)
        print("File deleted. \n")
    except Exception as e:
        print(f"Failed to delete file: {e} \n")

    try:
        results['vector_store'] = client.beta.vector_stores.delete(vector_store_id)
        print("Vector store deleted. \n")
    except Exception as e:
        print(f"Failed to delete vector store: {e} \n")

    try:
        results['assistant'] = client.beta.assistants.delete(assistant_id)
        print("Assistant deleted. \n")
    except Exception as e:
        print(f"Failed to delete assistant: {e} \n")

    try:
        results['thread'] = client.beta.threads.delete(thread_id)
        print("Thread deleted. \n")
    except Exception as e:
        print(f"Failed to delete thread: {e} \n")

    return results



# Create a thread just one time
thread_id = create_thread()

# Initialize OpenAI resources
assistant, uploaded_file, vector_store = initialize_openai_resources(file_path, model)

# Wait for a few seconds to ensure the document is indexed
time.sleep(5)

# First question
get_openai_response("What are the first 10 words in the document?", assistant.id, thread_id)

# Second question
get_openai_response("What are the words from the 10th to the 20th in the attached document?", assistant.id, thread_id)

# Third question
get_openai_response("Summarize the content of this attachment in 5 sentences.", assistant.id, thread_id)

# Delete OpenAI resources
delete_openai_resources(assistant.id, uploaded_file.id, thread_id, vector_store.id)
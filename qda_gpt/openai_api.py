import openai
import sys  # Import sys to use sys.stdout for printing without new lines
import time
from django.conf import settings



def get_openai_client():
    """
    Initialize and return an OpenAI client using the API key from Django settings.
    """
    api_key = settings.OPENAI_API_KEY
    if not api_key:
        raise ValueError("Failed to load the OPENAI_API_KEY from settings.")
    openai.api_key = api_key
    return openai.OpenAI(api_key=api_key)




def initialize_openai_resources(file_path, model):
    """
    Initializes OpenAI client, uploads a file, creates an assistant, and initializes a thread based on predefined settings.

    Parameters:
    - file_path: Path to the file to be uploaded.
    - model: Model type for the assistant (e.g., 'gpt-3.5-turbo').

    Returns:
    - A dictionary containing the assistant and thread objects.
    """
    client = get_openai_client()
    print("OpenAI API key loaded successfully. \n\n")

    # Upload a file
    with open(file_path, 'rb') as file_data:
        my_files = client.files.create(
            file=file_data,
            purpose="assistants"
        )
    print(f"File ID: {my_files.id} \n\n")

    # Create an Assistant
    my_assistant = client.beta.assistants.create(
        model=model,
        instructions="You are a qualitative data analyst. Your task is to analyze the provided dataset of transcribed interviews.",
        name="QDA-GPT",
        tools=[{"type": "retrieval"}],
        file_ids=[my_files.id]
    )
    print(f"This is the assistant object: {my_assistant} \n\n")

    # Create a Thread
    my_thread = client.beta.threads.create()
    print(f"This is the thread object: {my_thread} \n\n")

    return {'assistant': my_assistant, 'file':my_files, 'thread': my_thread}


# Here’s how you would use these functions together in your Django project:
# Calling the function
# from .openai_api import initialize_openai_resources

# result = initialize_openai_resources(file_path="data/Interviews.txt")
# assistant = result['assistant']
# thread = result['thread']



def get_openai_response(content, assistant_id, thread_id):
    """
    Sends content to ChatGPT using an existing assistant and thread, and retrieves the response.

    Parameters:
    - content: The user's input to be sent to ChatGPT.
    - assistant_id: The ID of the initialized assistant.
    - thread_id: The ID of the initialized thread.

    Returns:
    - The response from ChatGPT as a string, or "No response." if no response is retrieved.
    """
    client = get_openai_client()
    print("OpenAI API key loaded successfully. \n\n")



    try:
        # Send message to the thread
        my_thread_message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=content
        )
        print(f"This is the message object: {my_thread_message} \n\n")

        # Run the assistant
        my_run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
        )
        print(f"This is the run object: {my_run} \n\n")

        # Retrieve the Run status
        # Periodically retrieve the Run to check on its status to see if it has moved to completed
        print("Run status: in_progress", end="")
        sys.stdout.flush()  # Ensure "in_progress" is displayed immediately
        while my_run.status in ["queued", "in_progress"]:
            keep_retrieving_run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=my_run.id
            )

            if keep_retrieving_run.status == "in_progress":
                print(".", end="")
                sys.stdout.flush()  # Print each dot immediately
                time.sleep(0.57)    # Increase/reduce this if necessary
            elif keep_retrieving_run.status == "completed":
                print("\nRun status: completed\n")

                # Retrieve the Messages added by the Assistant to the Thread
                all_messages = client.beta.threads.messages.list(
                    thread_id=thread_id
                )
                response = "Assistant: " + all_messages.data[0].content[0].text.value
                print("------------------------------------------------------------ \n\n")
                print(f"User: {my_thread_message.content[0].text.value} \n\n")
                print(f"Assistant: {all_messages.data[0].content[0].text.value} \n\n")
                return response
            else:
                print(f"\nRun status: {keep_retrieving_run.status} \n\n")
                break

        return "Failed to retrieve a valid response from OpenAI. \n\n"

    except Exception as e:
        print(f"An error occurred: {str(e)} \n\n")
        return "Failed to retrieve a valid response from OpenAI. \n\n"


# Here’s how you would use these functions together in your Django project:
# from .openai_api import initialize_openai_resources, get_chatgpt_response

# Initialize resources
# resources = initialize_openai_resources("data/Interviews.txt")
# assistant = resources['assistant']
# thread = resources['thread']

# Get a response from ChatGPT
# response = get_chatgpt_response("Can you provide thematic analysis for the attached document containing interviews?", assistant.id, thread.id)
# print(response)




def delete_openai_resources(assistant_id, file_id, thread_id):
    """
    Deletes the specified assistant, file, and thread.

    Parameters:
    - assistant_id: The ID of the assistant to delete.
    - file_id: The ID of the file to delete.
    - thread_id: The ID of the thread to delete.

    Returns:
    - A dictionary with the status of deletions for the assistant, file, and thread.
    """
    client = get_openai_client()
    print("OpenAI API key loaded successfully. \n\n")

    results = {}
    try:
        results['file'] = client.files.delete(file_id)
        print("File deleted. \n\n")
    except Exception as e:
        print(f"Failed to delete file: {e} \n\n")

    try:
        results['assistant'] = client.beta.assistants.delete(assistant_id)
        print("Assistant deleted. \n\n")
    except Exception as e:
        print(f"Failed to delete assistant: {e} \n\n")

    try:
        results['thread'] = client.beta.threads.delete(thread_id)
        print("Thread deleted. \n\n")
    except Exception as e:
        print(f"Failed to delete thread: {e} \n\n")

    return results






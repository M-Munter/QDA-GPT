import openai
import sys  # Import sys to use sys.stdout for printing without new lines
import time
from django.conf import settings
from openai import OpenAI
from qda_gpt.prompts.prompts_ta import ta_instruction
from qda_gpt.prompts.prompts_ca import ca_instruction
from qda_gpt.prompts.prompts_gt import gt_instruction

def get_openai_client():
    """
    Initialize and return an OpenAI client using the API key from Django settings.
    """
    api_key = settings.OPENAI_API_KEY
    if not api_key:
        raise ValueError("Failed to load the OPENAI_API_KEY from settings.\n\n")
    openai.api_key = api_key
    return OpenAI(api_key=api_key)



def initialize_openai_resources(file_path, model, analysis_type, user_prompt):
    """
    Initializes OpenAI client, uploads a file, creates an assistant, and initializes a thread based on predefined settings.

    Parameters:
    - file_path: Path to the file to be uploaded.
    - model: Model type for the assistant (e.g., 'gpt-3.5-turbo').

    Returns:
    - A dictionary containing the assistant and thread objects.
    """
    client = get_openai_client()
    print("OpenAI API key loaded successfully.\n")

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

    if analysis_type == 'thematic':
        instructions = ta_instruction.format(user_prompt=user_prompt)
    elif analysis_type == 'content':
        instructions = ca_instruction.format(user_prompt=user_prompt)
    elif analysis_type == 'grounded':
        instructions = gt_instruction.format(user_prompt=user_prompt)
    else:
        raise ValueError("Unsupported analysis type")

    # Create an Assistant
    my_assistant = client.beta.assistants.create(
        instructions=instructions,
        name="QDA-GPT",
        tools=[{"type": "file_search"}],
        model=model,
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}}
    )
    print(f"Assistant created successfully with ID: {my_assistant.id}\n")

    # Create a Thread
    my_thread = client.beta.threads.create()

    # Validate that everything has been initialized successfully.
    print(f"Thread created successfully with ID: {my_thread.id}\n")

    return {'assistant': my_assistant, 'file':my_file, 'thread': my_thread, 'vector_store': vector_store,}





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
    print("OpenAI API key loaded successfully. Sending content to OpenAi Assistant.\n")


    try:

        # Send message to the thread
        my_thread_message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=content
        )
        if not my_thread_message or not my_thread_message.content:
            return "Message creation failed.", "Failure"
        print(f"Message sent to thread. Message ID: {my_thread_message.id}\n")


        # Run the assistant
        my_run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
        )
        print(f"Assistant run initiated. Run ID: {my_run.id}\n")

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
                time.sleep(0.5)    # Increase/reduce this if necessary
            elif keep_retrieving_run.status == "completed":
                print("\nRun status: completed\n")

                # Retrieve the Messages added by the Assistant to the Thread
                all_messages = client.beta.threads.messages.list(
                    thread_id=thread_id
                )
                if not all_messages or not all_messages.data or not all_messages.data[0].content:
                    return "Response retrieval failed.", "Failure"

                response = all_messages.data[0].content[0].text.value

                print("------------------------------------------------------------\n")
                print("Response retrieved successfully.\n")
                print("Assistant response processed successfully.\n")
                return response
            else:
                print(f"\nRun status: {keep_retrieving_run.status}\n")
                break

        return "Failed to retrieve a valid response from OpenAI.\n"

    except Exception as e:
        print(f"An error occurred: {str(e)} \n")
        return "Failed to retrieve a valid response from OpenAI.\n"


# Here’s how you would use these functions together in your Django project:
# from .openai_api import initialize_openai_resources, get_chatgpt_response

# Initialize resources
# resources = initialize_openai_resources("data/Interviews.txt")
# assistant = resources['assistant']
# thread = resources['thread']

# Get a response from ChatGPT
# response = get_chatgpt_response("Can you provide thematic analysis for the attached document containing interviews?", assistant.id, thread.id)
# print(response)




def delete_openai_resources(assistant_id, file_id, thread_id, vector_store_id):
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



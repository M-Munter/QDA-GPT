import openai
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
        raise ValueError("Failed to load the OPENAI_API_KEY from settings.\n")
    openai.api_key = api_key
    return OpenAI(api_key=api_key)


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


def initialize_openai_resources(file_path, model, analysis_type, user_prompt):
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

    # I assume this has a specific proposal for you
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

    return {
        'assistant': my_assistant,
        'file': my_file,
        'vector_store': vector_store
    }



def get_openai_response(content, assistant_id, thread_id):
    client = get_openai_client()
    print("OpenAI API key loaded successfully. Sending message to OpenAI Assistant.\n")

    try:
        # Send message to the thread
        my_thread_message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=content
        )

        # Verification print statements for success and failure
        if not my_thread_message or not my_thread_message.content:
            print("Message creation failed.\n")
            return "Message creation failed.", "Failure"
        print(f"Message sent to thread. Message ID: {my_thread_message.id}\n")

        # Just create_and_poll for get a terminal state
        print(f"Run initiated with Assistant ID: {assistant_id} and Thread ID {thread_id}\n")
        try:
            # Checking when the run is completed.
            run = client.beta.threads.runs.create_and_poll(
                thread_id=thread_id,
                assistant_id=assistant_id,
                poll_interval_ms=5000,
                timeout=60.0
                # instructions just for this run if needed
            )
            print(f"Run ID: {run.id}\n")
        except Exception as e:
            print(f"Error: {e}")

        # Retrieve the Run status
        try:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )
            print(f"Run status: {run_status.status}\n")
        except Exception as e:
            print(f"Error with run: {e}")

        if run_status.status == 'completed':
            # Retrieve the Messages added by the Assistant to the Thread
            all_messages = client.beta.threads.messages.list(
                thread_id=thread_id,
                run_id = run.id
            )
            if not all_messages or not all_messages.data or not all_messages.data[0].content:
                return "Response retrieval failed.", "Failure"

            response = all_messages.data[0].content[0].text.value

            print("Response retrieved and processed successfully.")
            print("----------------------------------------------\n\n")
            return response

        elif run_status.status == 'failed':
            print("Failed")
        elif run_status.status == 'requires_action':
            print("Run status: requires action")

    except Exception as e:
        print(f"An error occurred in getting the response from OpenAI: {str(e)} \n")
        return "Failed to retrieve a valid response from OpenAI.\n"



def delete_openai_resources(assistant_id, thread_id, vector_store_id, file_id=None):
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
        client.files.delete(file_id)
        results['file'] = {'deleted': True}
        print("File deleted. \n")
    except Exception as e:
        results['file'] = {'deleted': False, 'error': str(e)}
        print(f"Failed to delete file: {e} \n")

    try:
        results['vector_store'] = client.beta.vector_stores.delete(vector_store_id)
        results['vector_store'] = {'deleted': True}
        print("Vector store deleted. \n")
    except Exception as e:
        results['vector_store'] = {'deleted': False, 'error': str(e)}
        print(f"Failed to delete vector store: {e} \n")

    try:
        client.beta.assistants.delete(assistant_id)
        results['assistant'] = {'deleted': True}
        print("Assistant deleted. \n")
    except Exception as e:
        print(f"Failed to delete assistant: {e} \n")
        results['assistant'] = {'deleted': False, 'error': str(e)}

    try:
        client.beta.threads.delete(thread_id)
        results['thread'] = {'deleted': True}
        print("Thread deleted. \n")
    except Exception as e:
        results['thread'] = {'deleted': False, 'error': str(e)}
        print(f"Failed to delete thread: {e} \n")

    return results



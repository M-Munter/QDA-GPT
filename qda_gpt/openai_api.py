"""
openai_api.py
#
This script provides functions to interact with the OpenAI API within a Django application.
It covers the full lifecycle of an OpenAI session:
1. Initialization: It sets up an OpenAI client, uploads necessary files, and initializes resources like thread, vector store, and assistant.
2. Message Exchange: It allows the application to send messages to an OpenAI assistant and retrieve responses.
3. Termination: It includes functions to delete all resources (such as assistants, files, threads, and vector stores) once they are no longer needed.
"""

import openai
from django.conf import settings
from openai import OpenAI
from qda_gpt.prompts.prompts_ta import ta_instruction
from qda_gpt.prompts.prompts_ca import ca_instruction
from qda_gpt.prompts.prompts_gt import gt_instruction
import logging

logger = logging.getLogger(__name__)

def get_openai_client():
    """
    Initialize and return an OpenAI client using the API key from Django settings.
    """
    api_key = settings.OPENAI_API_KEY
    if not api_key:
        raise ValueError("Failed to load the OPENAI_API_KEY from settings.\n")
    openai.api_key = api_key  # Set the API key for the OpenAI library
    return OpenAI(api_key=api_key)  # Return the initialized OpenAI client


def create_thread():
    """
    Create a new thread using the OpenAI client.
    """
    try:
        client = get_openai_client()
        thread = client.beta.threads.create()  # Create a new thread
        logger.debug(f"Thread ID: {thread.id}\n")
        return thread.id
    except Exception as e:
        logger.error(f"Error creating thread: {e}\n")
        return None


def initialize_openai_resources(file_path, model, analysis_type, user_prompt):
    """
    Initialize OpenAI resources by uploading a file, creating a vector store, and creating an assistant.

    Parameters:
    - file_path: The path to the file to upload.
    - model: The model to be used for the assistant.
    - analysis_type: The type of analysis (thematic, content, or grounded).
    - user_prompt: The prompt to be used for generating instructions.

    Returns:
    - A dictionary containing the initialized assistant, file, and vector store.
    """
    client = get_openai_client()

    # Upload a file to the OpenAI API
    with open(file_path, 'rb') as file_data:
        my_file = client.files.create(
            file=file_data,
            purpose="assistants"
        )
    logger.debug(f"File uploaded successfully with ID: {my_file.id}\n")

    # Create a vector store and associate the uploaded file with it
    vector_store = client.beta.vector_stores.create(file_ids=[my_file.id])
    print(f"Vector store created successfully with ID: {vector_store.id}\n")
    print(f"File with ID {my_file.id} has been successfully attached to Vector store with ID {vector_store.id}\n")

    # Determine the instructions based on the analysis type
    if analysis_type == 'thematic':
        instructions = ta_instruction.format(user_prompt=user_prompt)
    elif analysis_type == 'content':
        instructions = ca_instruction.format(user_prompt=user_prompt)
    elif analysis_type == 'grounded':
        instructions = gt_instruction.format(user_prompt=user_prompt)
    else:
        raise ValueError("Unsupported analysis type")

    # Create an assistant with the specified instructions and model
    my_assistant = client.beta.assistants.create(
        instructions=instructions,
        name="QDA-GPT",
        tools=[{"type": "file_search"}],
        model=model,
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}}
    )
    logger.debug(f"Assistant created successfully with ID: {my_assistant.id}\n")

    return {
        'assistant': my_assistant,
        'file': my_file,
        'vector_store': vector_store
    }



def get_openai_response(content, assistant_id, thread_id):
    """
    Send a message to the OpenAI assistant and retrieve the response.

    Parameters:
    - content: The content to send to the assistant.
    - assistant_id: The ID of the assistant to use.
    - thread_id: The ID of the thread to send the message to.

    Returns:
    - The response content from the OpenAI assistant.
    """
    client = get_openai_client()
    logger.debug("OpenAI API key loaded successfully. Sending message to OpenAI Assistant.\n")

    try:
        # Send message to the thread
        my_thread_message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=content
        )

        # Verification log statements for success and failure
        if not my_thread_message or not my_thread_message.content:
            logger.error("Message creation failed.\n")
            return "Message creation failed.", "Failure"
        logger.debug(f"Message sent to thread. Message ID: {my_thread_message.id}\n")

        # Initiate and poll a run to get a terminal state
        logger.debug(f"Run initiated with Assistant ID: {assistant_id} and Thread ID {thread_id}\n")
        try:
            # Poll the run status until completion or timeout
            run = client.beta.threads.runs.create_and_poll(
                thread_id=thread_id,
                assistant_id=assistant_id,
                poll_interval_ms=5000,
                timeout=60.0
            )
            logger.debug(f"Run ID: {run.id}\n")
        except Exception as e:
            logger.error(f"Error: {e}\n")

        # Retrieve the run status
        try:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )
            logger.debug(f"Run status: {run_status.status}\n")
        except Exception as e:
            logger.error(f"Error with run: {e}\n")

        if run_status.status == 'completed':
            # Retrieve and return the first response message
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
            logger.error("Run failed\n")
        elif run_status.status == 'requires_action':
            logger.debug("Run status: requires action\n")

    except Exception as e:
        logger.error(f"An error occurred in getting the response from OpenAI: {str(e)}\n")
        return "Failed to retrieve a valid response from OpenAI.\n"



def delete_openai_resources(assistant_id, thread_id, vector_store_id, file_id=None):
    """
    Deletes the specified assistant, file, thread, and vector store.

    Parameters:
    - assistant_id: The ID of the assistant to delete.
    - thread_id: The ID of the thread to delete.
    - vector_store_id: The ID of the vector store to delete.
    - file_id: (Optional) The ID of the file to delete.

    Returns:
    - A dictionary with the status of deletions for the assistant, file, thread, and vector store.
    """
    client = get_openai_client()
    logger.debug("OpenAI API key loaded successfully.\n")

    results = {}
    try:
        # Attempt to delete the specified file
        client.files.delete(file_id)
        results['file'] = {'deleted': True}
        logger.debug("File deleted. \n")
    except Exception as e:
        results['file'] = {'deleted': False, 'error': str(e)}
        logger.error(f"Failed to delete file: {e} \n")

    try:
        # Attempt to delete the specified vector store
        results['vector_store'] = client.beta.vector_stores.delete(vector_store_id)
        results['vector_store'] = {'deleted': True}
        logger.debug("Vector store deleted. \n")
    except Exception as e:
        results['vector_store'] = {'deleted': False, 'error': str(e)}
        logger.error(f"Failed to delete vector store: {e} \n")

    try:
        # Attempt to delete the specified assistant
        client.beta.assistants.delete(assistant_id)
        results['assistant'] = {'deleted': True}
        logger.debug("Assistant deleted. \n")
    except Exception as e:
        logger.error(f"Failed to delete assistant: {e} \n")
        results['assistant'] = {'deleted': False, 'error': str(e)}

    try:
        # Attempt to delete the specified thread
        client.beta.threads.delete(thread_id)
        results['thread'] = {'deleted': True}
        logger.debug("Thread deleted. \n")
    except Exception as e:
        results['thread'] = {'deleted': False, 'error': str(e)}
        logger.error(f"Failed to delete thread: {e} \n")

    return results



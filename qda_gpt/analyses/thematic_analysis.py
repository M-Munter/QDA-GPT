"""
thematic_analysis.py

This script handles the different phases of thematic analysis by interacting
with OpenAI's API. It formats prompts, sends them to the API, and processes
the responses. The script also manages the deletion of OpenAI elements after
the analysis is completed.
"""

from qda_gpt.prompts.prompts_ta import ta_instruction, ta_prompt1, ta_prompt2, ta_prompt3, ta_prompt4, ta_prompt5, ta_prompt6, ta_prompt7, ta_prompt8
from qda_gpt.openai_api import create_thread, initialize_openai_resources, get_openai_client, get_openai_response, create_thread, delete_openai_resources
from qda_gpt.deletion import handle_deletion
import time
import logging

logger = logging.getLogger(__name__)

def phase1(analysis_data):
    formatted_prompt1 = ta_prompt1
    assistant_id = analysis_data.get('assistant_id')
    thread_id = analysis_data.get('thread_id')
    response1_json = get_openai_response(formatted_prompt1, assistant_id, thread_id)
    return response1_json, formatted_prompt1

def phase2(analysis_data):
    formatted_prompt2 = ta_prompt2
    assistant_id = analysis_data.get('assistant_id')
    thread_id = analysis_data.get('thread_id')
    response2_json = get_openai_response(formatted_prompt2, assistant_id, thread_id)
    return response2_json, formatted_prompt2

def phase3(analysis_data):
    formatted_prompt3 = ta_prompt3
    assistant_id = analysis_data.get('assistant_id')
    thread_id = analysis_data.get('thread_id')
    response3_json = get_openai_response(formatted_prompt3, assistant_id, thread_id)
    return response3_json, formatted_prompt3



def phase4(analysis_data):
    # Retrieve existing information from the session
    file_id = analysis_data.get('file_id')
    model_choice = analysis_data.get('model_choice')
    user_prompt = analysis_data.get('user_prompt')


    # Check if necessary information is available
    if not file_id or not model_choice:
        logger.error(f"Missing necessary information: file_id={file_id}, model_choice={model_choice}\n")
        return None, "Necessary information (file, model choice) not found in session."

    logger.debug(f"Phase 4 starting with: file_id={file_id}, model_choice={model_choice}, user_prompt={user_prompt}\n")

    # Create a new thread for this phase of the analysis
    new_thread_id = create_thread()
    if not new_thread_id:
        print("Failed to create thread.")
        return None, "Failed to create thread."

    logger.debug(f"New thread created: {new_thread_id}\n")

    client = get_openai_client()

    try:
        # Create a Vector Store and upload the file specified in file_id to it
        vector_store = client.beta.vector_stores.create(file_ids=[file_id])
        new_vector_store_id = vector_store.id
        logger.debug(f"Vector store created successfully with ID: {new_vector_store_id}\n")
        logger.debug(f"File with ID {file_id} has been successfully attached to Vector store with ID {new_vector_store_id}\n")

        # Create an Assistant
        instructions = ta_instruction.format(user_prompt=user_prompt)
        my_assistant = client.beta.assistants.create(
            instructions=instructions,
            name="QDA-GPT",
            tools=[{"type": "file_search"}],
            model=model_choice,
            tool_resources={"file_search": {"vector_store_ids": [new_vector_store_id]}}
        )
        new_assistant_id = my_assistant.id
        logger.debug(f"Assistant created successfully with ID: {new_assistant_id}\n")

    except Exception as e:
        # Handle any errors that occur during the creation of the vector store or assistant
        logger.error(f"Error initializing OpenAI resources: {str(e)}\n")
        return None, f"Error initializing OpenAI resources: {str(e)}\n"

    # Pause to allow time for the vector store indexing process to complete
    print("Waiting for indexing: ", end='', flush=True)
    for i in range(5, -1, -1):
        print(f"{i} ", end='', flush=True)
        time.sleep(0.9)
        print('\rWaiting for indexing: ', end='', flush=True)  # Return to the beginning of the line and overwrite
    print("0")  # Indicate that indexing is complete
    print("Indexing complete.\n")

    # Prepare and send the fourth prompt to the Assistant
    formatted_prompt4 = ta_prompt4
    response4_json = get_openai_response(formatted_prompt4, new_assistant_id, new_thread_id)

    # Call delete_openai_resources without deleting the file
    deletion_results = delete_openai_resources(new_assistant_id, thread_id=new_thread_id, vector_store_id=new_vector_store_id)
    logger.debug(f"deletion_results: {deletion_results}\n")

    return response4_json, formatted_prompt4


def phase5(analysis_data, response4_json):
    formatted_prompt5 = ta_prompt5.format(response4_json=response4_json)
    assistant_id = analysis_data.get('assistant_id')
    thread_id = analysis_data.get('thread_id')
    response5_json = get_openai_response(formatted_prompt5, assistant_id, thread_id)
    return response5_json, formatted_prompt5

def phase6(analysis_data, response2_json):
    formatted_prompt6 = ta_prompt6.format(response2_json=response2_json)
    assistant_id = analysis_data.get('assistant_id')
    thread_id = analysis_data.get('thread_id')
    response6_json = get_openai_response(formatted_prompt6, assistant_id, thread_id)
    return response6_json, formatted_prompt6

def phase7(analysis_data, response1_json):
    formatted_prompt7 = ta_prompt7.format(response1_json=response1_json)
    assistant_id = analysis_data.get('assistant_id')
    thread_id = analysis_data.get('thread_id')
    response7_json = get_openai_response(formatted_prompt7, assistant_id, thread_id)
    return response7_json, formatted_prompt7

def phase8(analysis_data):
    formatted_prompt8 = ta_prompt8
    assistant_id = analysis_data.get('assistant_id')
    thread_id = analysis_data.get('thread_id')
    file_id = analysis_data.get('file_id')
    vector_store_id = analysis_data.get('vector_store_id')

    try:
        response8_json = get_openai_response(formatted_prompt8, assistant_id, thread_id)

        # Prepare the request object equivalent
        request_data = {
            'session': {
                'assistant_id': assistant_id,
                'thread_id': thread_id,
                'vector_store_id': vector_store_id,
                'file_id': file_id
            }
        }

        # Attempt to delete OpenAI elements
        deletion_results = handle_deletion(request_data)

        if "Deletion successful" in deletion_results:
            analysis_status = "Analysis completed successfully. All OpenAI elements deleted successfully."
        else:
            analysis_status = "Analysis completed successfully. Deletion of all OpenAI elements failed."

        return response8_json, formatted_prompt8, analysis_status, deletion_results
    except Exception as e:
        return None, formatted_prompt8, f"An error occurred: {str(e)}", ""



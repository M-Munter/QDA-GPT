from qda_gpt.prompts.prompts_ta import ta_instruction, ta_prompt1, ta_prompt2, ta_prompt3, ta_prompt4, ta_prompt5, ta_prompt6, ta_prompt7, ta_prompt8
from qda_gpt.openai_api import create_thread, initialize_openai_resources, get_openai_client, get_openai_response, create_thread, delete_openai_resources
from qda_gpt.deletion import handle_deletion
import time

def phase1(request):
    formatted_prompt1 = ta_prompt1
    response1_json = get_openai_response(formatted_prompt1, request.session['assistant_id'], request.session['thread_id'])
    print(f"response1_json: {response1_json}\n")  # Debugging print statement
    return response1_json, formatted_prompt1

def phase2(request):
    formatted_prompt2 = ta_prompt2
    response2_json = get_openai_response(formatted_prompt2, request.session['assistant_id'], request.session['thread_id'])
    print(f"response2_json: {response2_json}\n")  # Debugging print statement
    return response2_json, formatted_prompt2

def phase3(request):
    formatted_prompt3 = ta_prompt3
    response3_json = get_openai_response(formatted_prompt3, request.session['assistant_id'], request.session['thread_id'])
    print(f"response3_json: {response3_json}\n")  # Debugging print statement
    return response3_json, formatted_prompt3



def phase4(request):
    # Retrieve existing information from session
    file_id = request.session.get('file_id')
    file_name = request.session.get('file_name')
    model_choice = request.session.get('model_choice')
    user_prompt = request.session.get('user_prompt', '')

    # Check if necessary information is available
    if not file_id or not file_name or not model_choice:
        print(f"Missing necessary information: file_id={file_id}, file_name={file_name}, model_choice={model_choice}")
        return None, "Necessary information (file, model choice) not found in session."

    print(f"Phase 4 starting with: file_id={file_id}, file_name={file_name}, model_choice={model_choice}, user_prompt={user_prompt}")

    # Create new thread and initialize new assistant for phase 4
    new_thread_id = create_thread()
    if not new_thread_id:
        print("Failed to create thread.")
        return None, "Failed to create thread."

    print(f"New thread created: {new_thread_id}")

    client = get_openai_client()

    try:
        # Create Vector Store and upload a file there
        vector_store = client.beta.vector_stores.create(file_ids=[file_id])
        new_vector_store_id = vector_store.id
        print(f"Vector store created successfully with ID: {new_vector_store_id}")
        print(f"File with ID {file_id} has been successfully attached to Vector store with ID {new_vector_store_id}")

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
        print(f"Assistant created successfully with ID: {new_assistant_id}")

    except Exception as e:
        print(f"Error initializing OpenAI resources: {str(e)}")
        return None, f"Error initializing OpenAI resources: {str(e)}"

    print("Waiting for indexing: ", end='', flush=True)
    for i in range(5, -1, -1):  # Adjusted range to include 0
        print(f"{i} ", end='', flush=True)  # Print the countdown number with a space
        time.sleep(0.9)
        print('\rWaiting for indexing: ', end='', flush=True)  # Return to the beginning of the line and overwrite
    print("0")
    print("Indexing complete.")

    formatted_prompt4 = ta_prompt4
    response4_json = get_openai_response(formatted_prompt4, new_assistant_id, new_thread_id)
    print(f"response4_json: {response4_json}\n")  # Debugging print statement

    # Call delete_openai_resources without deleting the file
    deletion_results = delete_openai_resources(new_assistant_id, thread_id=new_thread_id, vector_store_id=new_vector_store_id)
    print(f"deletion_results: {deletion_results}\n")  # Debugging print statement

    return response4_json, formatted_prompt4


def phase5(request, response4_json):
    formatted_prompt5 = ta_prompt5.format(response4_json=response4_json)
    response5_json = get_openai_response(formatted_prompt5, request.session['assistant_id'], request.session['thread_id'])
    print(f"response5_json: {response5_json}\n")  # Debugging print statement
    return response5_json, formatted_prompt5

def phase6(request, response2_json):
    formatted_prompt6 = ta_prompt6.format(response2_json=response2_json)
    response6_json = get_openai_response(formatted_prompt6, request.session['assistant_id'], request.session['thread_id'])
    print(f"response6_json: {response6_json}\n")  # Debugging print statement
    return response6_json, formatted_prompt6

def phase7(request, response1_json):
    formatted_prompt7 = ta_prompt7.format(response1_json=response1_json)
    response7_json = get_openai_response(formatted_prompt7, request.session['assistant_id'], request.session['thread_id'])
    print(f"response7_json: {response7_json}\n")  # Debugging print statement
    return response7_json, formatted_prompt7

def phase8(request):
    formatted_prompt8 = ta_prompt8
    if request.session.get('initialized', False):
        try:
            response8_json = get_openai_response(formatted_prompt8, request.session['assistant_id'], request.session['thread_id'])
            request.session['eighth_response'] = response8_json
            deletion_results = handle_deletion(request)
            request.session['deletion_results'] = deletion_results

            if "Deletion successful" in deletion_results:
                analysis_status = "Analysis completed. All OpenAI elements deleted successfully."
            else:
                analysis_status = "Analysis completed successfully. Deletion of all OpenAI elements failed."

            print(f"response8_json: {response8_json}\n")  # Debugging print statement
            request.session['analysis_status'] = analysis_status
            return response8_json, formatted_prompt8, analysis_status, deletion_results
        except Exception as e:
            request.session['analysis_status'] = f"An error occurred: {str(e)}"
            return None, formatted_prompt8, f"An error occurred: {str(e)}", ""
    return None, formatted_prompt8, "No analysis performed.", ""

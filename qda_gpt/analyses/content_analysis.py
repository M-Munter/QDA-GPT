from qda_gpt.prompts.prompts_ca import ca_prompt1, ca_prompt2, ca_prompt3, ca_prompt4, ca_prompt5, ca_prompt6, ca_prompt7, ca_prompt8
from qda_gpt.openai_api import get_openai_response
from qda_gpt.deletion import handle_deletion

def phase1(analysis_data):
    formatted_prompt1 = ca_prompt1
    assistant_id = analysis_data.get('assistant_id')
    thread_id = analysis_data.get('thread_id')
    response1_json = get_openai_response(formatted_prompt1, assistant_id, thread_id)
    print("response1_json:", response1_json)  # Debugging print statement
    return response1_json, formatted_prompt1

def phase2(analysis_data):
    formatted_prompt2 = ca_prompt2
    assistant_id = analysis_data.get('assistant_id')
    thread_id = analysis_data.get('thread_id')
    response2_json = get_openai_response(formatted_prompt2, assistant_id, thread_id)
    return response2_json, formatted_prompt2

def phase3(analysis_data):
    formatted_prompt3 = ca_prompt3
    assistant_id = analysis_data.get('assistant_id')
    thread_id = analysis_data.get('thread_id')
    response3_json = get_openai_response(formatted_prompt3, assistant_id, thread_id)
    return response3_json, formatted_prompt3

def phase4(analysis_data):
    formatted_prompt4 = ca_prompt4
    assistant_id = analysis_data.get('assistant_id')
    thread_id = analysis_data.get('thread_id')
    response4_json = get_openai_response(formatted_prompt4, assistant_id, thread_id)
    return response4_json, formatted_prompt4

def phase5(analysis_data, response1_json):
    formatted_prompt5 = ca_prompt5.format(response1_json=response1_json)
    assistant_id = analysis_data.get('assistant_id')
    thread_id = analysis_data.get('thread_id')
    response5_json = get_openai_response(formatted_prompt5, assistant_id, thread_id)
    print(f"[DEBUG] Response number 5: {response5_json}\n")  # Debugging print statement
    return response5_json, formatted_prompt5

def phase6(analysis_data):
    formatted_prompt6 = ca_prompt6
    assistant_id = analysis_data.get('assistant_id')
    thread_id = analysis_data.get('thread_id')
    response6_json = get_openai_response(formatted_prompt6, assistant_id, thread_id)
    return response6_json, formatted_prompt6

def phase7(analysis_data):
    formatted_prompt7 = ca_prompt7
    assistant_id = analysis_data.get('assistant_id')
    thread_id = analysis_data.get('thread_id')
    response7_json = get_openai_response(formatted_prompt7, assistant_id, thread_id)
    return response7_json, formatted_prompt7

def phase8(analysis_data):
    formatted_prompt8 = ca_prompt8
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

        deletion_results = handle_deletion(request_data)

        if "Deletion successful" in deletion_results:
            analysis_status = "Analysis completed. All OpenAI elements deleted successfully."
        else:
            analysis_status = "Analysis completed successfully. Deletion of all OpenAI elements failed."

        print("response8_json:", response8_json)  # Debugging print statement
        return response8_json, formatted_prompt8, analysis_status, deletion_results
    except Exception as e:
        return None, formatted_prompt8, f"An error occurred: {str(e)}", ""


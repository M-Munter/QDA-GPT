from qda_gpt.prompts.prompts_gt import gt_prompt1, gt_prompt2, gt_prompt3, gt_prompt4, gt_prompt5, gt_prompt6, gt_prompt7
from qda_gpt.openai_api import get_openai_response
from qda_gpt.deletion import handle_deletion
import logging

logger = logging.getLogger(__name__)

def phase1(analysis_data):
    formatted_prompt1 = gt_prompt1
    assistant_id = analysis_data.get('assistant_id')
    thread_id = analysis_data.get('thread_id')
    response1_json = get_openai_response(formatted_prompt1, assistant_id, thread_id)
    return response1_json, formatted_prompt1

def phase2(analysis_data):
    formatted_prompt2 = gt_prompt2
    assistant_id = analysis_data.get('assistant_id')
    thread_id = analysis_data.get('thread_id')
    response2_json = get_openai_response(formatted_prompt2, assistant_id, thread_id)
    return response2_json, formatted_prompt2

def phase3(analysis_data):
    formatted_prompt3 = gt_prompt3
    assistant_id = analysis_data.get('assistant_id')
    thread_id = analysis_data.get('thread_id')
    response3_json = get_openai_response(formatted_prompt3, assistant_id, thread_id)
    return response3_json, formatted_prompt3

def phase4(analysis_data):
    formatted_prompt4 = gt_prompt4
    assistant_id = analysis_data.get('assistant_id')
    thread_id = analysis_data.get('thread_id')
    response4_json = get_openai_response(formatted_prompt4, assistant_id, thread_id)
    return response4_json, formatted_prompt4

def phase5(analysis_data):
    formatted_prompt5 = gt_prompt5
    assistant_id = analysis_data.get('assistant_id')
    thread_id = analysis_data.get('thread_id')
    response5_json = get_openai_response(formatted_prompt5, assistant_id, thread_id)
    logger.debug(f"response5_json: {response5_json}")  # Debugging print statement
    return response5_json, formatted_prompt5

def phase6(analysis_data):
    formatted_prompt6 = gt_prompt6
    assistant_id = analysis_data.get('assistant_id')
    thread_id = analysis_data.get('thread_id')
    response6_json = get_openai_response(formatted_prompt6, assistant_id, thread_id)
    return response6_json, formatted_prompt6

def phase7(analysis_data):
    logger.debug(f"Phase7 called")  # Debugging print statement
    formatted_prompt7 = gt_prompt7
    assistant_id = analysis_data.get('assistant_id')
    thread_id = analysis_data.get('thread_id')
    file_id = analysis_data.get('file_id')
    vector_store_id = analysis_data.get('vector_store_id')
    logger.debug(f"Phase7 setup successful")  # Debugging print statement

    try:
        logger.debug(f"Before get_openai_response phase7")
        response7_json = get_openai_response(formatted_prompt7, assistant_id, thread_id)
        logger.debug(f"response7_json: {response7_json}")  # Debugging print statement
        print()

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

        return response7_json, formatted_prompt7, analysis_status, deletion_results
    except Exception as e:
        return None, formatted_prompt7, f"An error occurred: {str(e)}", ""


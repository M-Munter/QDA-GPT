# qda_gpt/analyses/thematic_analysis.py
from qda_gpt.prompts.prompts_ta import ta_prompt1, ta_prompt2, ta_prompt3, ta_prompt4
from qda_gpt.openai_api import get_openai_response
from qda_gpt.deletion import handle_deletion  # Ensure correct import

def handle_analysis(request, user_prompt):
    formatted_ta_prompt1 = ta_prompt1.format()
    request.session['formatted_ta_prompt1'] = formatted_ta_prompt1
    if request.session.get('initialized', False) and user_prompt:
        try:
            response_json = get_openai_response(formatted_ta_prompt1, request.session['assistant_id'], request.session['thread_id'])
            print(f"Response: {response_json[:50]}...\n")  # Print first 50 characters
            request.session['response'] = response_json
            return response_json, formatted_ta_prompt1
        except Exception as e:
            return None, f"An error occurred: {str(e)}"
    return None, "No analysis performed."

def handle_second_prompt_analysis(request, response_json):
    formatted_ta_prompt2 = ta_prompt2.format(response_json=response_json)
    if request.session.get('initialized', False):
        try:
            response2_json = get_openai_response(formatted_ta_prompt2, request.session['assistant_id'], request.session['thread_id'])
            request.session['second_response'] = response2_json
            return response2_json, formatted_ta_prompt2
        except Exception as e:
            request.session['analysis_status'] = f"An error occurred: {str(e)}"
            return None, f"An error occurred: {str(e)}"
    return None, "No analysis performed as assistant has not been initialized."

def handle_ta_phase4(request, response_json):
    formatted_ta_prompt3 = ta_prompt3.format(response_json=response_json)
    if request.session.get('initialized', False):
        try:
            response3_json = get_openai_response(formatted_ta_prompt3, request.session['assistant_id'], request.session['thread_id'])
            request.session['third_response'] = response3_json
            return response3_json, formatted_ta_prompt3
        except Exception as e:
            request.session['analysis_status'] = f"An error occurred: {str(e)}"
            return f"An error occurred: {str(e)}"
    return "No analysis performed as assistant not initialized."

def handle_ta_phase5(request, response2_json, response3_json):
    formatted_ta_prompt4 = ta_prompt4.format(response2_json=response2_json, response3_json=response3_json)
    if request.session.get('initialized', False):
        try:
            response4_json = get_openai_response(formatted_ta_prompt4, request.session['assistant_id'], request.session['thread_id'])
            request.session['third_response'] = response4_json

            deletion_results = handle_deletion(request)  # Ensure deletion_results are fetched from the correct place
            request.session['deletion_results'] = deletion_results

            if "Not all OpenAI elements were deleted successfully" in deletion_results:
                request.session['analysis_status'] = "Analysis completed, but not all OpenAI elements were deleted successfully."
            else:
                request.session['analysis_status'] = "Analysis completed successfully. All OpenAI elements deleted successfully."

            return response4_json, formatted_ta_prompt4, "Analysis completed successfully.", deletion_results
        except Exception as e:
            request.session['analysis_status'] = f"An error occurred: {str(e)}"
            return None, formatted_ta_prompt4, f"An error occurred: {str(e)}", ""
    return None, formatted_ta_prompt4, "No analysis performed as assistant not initialized.", ""

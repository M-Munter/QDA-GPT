from qda_gpt.prompts.prompts_ta import ta_prompt1, ta_prompt2, ta_prompt3, ta_prompt4
from qda_gpt.openai_api import get_openai_response
from qda_gpt.deletion import handle_deletion

def handle_analysis(request):
    formatted_ta_prompt1 = ta_prompt1.format()
    response_json = get_openai_response(formatted_ta_prompt1, request.session['assistant_id'], request.session['thread_id'])
    return response_json, formatted_ta_prompt1

def handle_second_prompt_analysis(request, response_json):
    formatted_ta_prompt2 = ta_prompt2.format(response_json=response_json)
    response2_json = get_openai_response(formatted_ta_prompt2, request.session['assistant_id'], request.session['thread_id'])
    return response2_json, formatted_ta_prompt2

def handle_ta_phase3(request, response_json):
    formatted_ta_prompt3 = ta_prompt3.format(response_json=response_json)
    response3_json = get_openai_response(formatted_ta_prompt3, request.session['assistant_id'], request.session['thread_id'])
    return response3_json, formatted_ta_prompt3

def handle_ta_phase4(request, response2_json, response3_json):
    formatted_ta_prompt4 = ta_prompt4.format(response2_json=response2_json, response3_json=response3_json)
    if request.session.get('initialized', False):
        try:
            response4_json = get_openai_response(formatted_ta_prompt4, request.session['assistant_id'], request.session['thread_id'])
            request.session['fourth_response'] = response4_json
            deletion_results = handle_deletion(request)
            request.session['deletion_results'] = deletion_results

            analysis_status = "Analysis completed successfully."
            if "Deletion successful" in deletion_results:
                analysis_status = "Analysis completed and all OpenAI elements deleted successfully."
            else:
                analysis_status = "Analysis completed successfully, but deletion of all OpenAI elements failed."

            request.session['analysis_status'] = analysis_status
            return response4_json, formatted_ta_prompt4, analysis_status, deletion_results
        except Exception as e:
            request.session['analysis_status'] = f"An error occurred: {str(e)}"
            return None, formatted_ta_prompt4, f"An error occurred: {str(e)}", ""
    return None, formatted_ta_prompt4, "No analysis performed.", ""

from qda_gpt.prompts.prompts_ca import ca_prompt1, ca_prompt2, ca_prompt3, ca_prompt4, ca_prompt5, ca_prompt6
from qda_gpt.openai_api import get_openai_response
from qda_gpt.deletion import handle_deletion

def handle_analysis(request):
    formatted_ca_prompt1 = ca_prompt1
    response_json = get_openai_response(formatted_ca_prompt1, request.session['assistant_id'], request.session['thread_id'])
    return response_json, formatted_ca_prompt1

def handle_second_prompt_analysis(request, response_json):
    formatted_ca_prompt2 = ca_prompt2.format(response_json=response_json)
    response2_json = get_openai_response(formatted_ca_prompt2, request.session['assistant_id'], request.session['thread_id'])
    return response2_json, formatted_ca_prompt2

def handle_ca_phase3(request, response2_json):
    formatted_ca_prompt3 = ca_prompt3.format(response2_json=response2_json)
    response3_json = get_openai_response(formatted_ca_prompt3, request.session['assistant_id'], request.session['thread_id'])
    return response3_json, formatted_ca_prompt3

def handle_ca_phase4(request, response3_json):
    formatted_ca_prompt4 = ca_prompt4.format(response3_json=response3_json)
    response4_json = get_openai_response(formatted_ca_prompt4, request.session['assistant_id'], request.session['thread_id'])
    return response4_json, formatted_ca_prompt4

def handle_ca_phase5(request, response4_json):
    formatted_ca_prompt5 = ca_prompt5.format(response4_json=response4_json)
    response5_json = get_openai_response(formatted_ca_prompt5, request.session['assistant_id'], request.session['thread_id'])
    return response5_json, formatted_ca_prompt5

def handle_ca_phase6(request, response5_json):
    formatted_ca_prompt6 = ca_prompt6.format(response5_json=response5_json)
    if request.session.get('initialized', False):
        try:
            response6_json = get_openai_response(formatted_ca_prompt6, request.session['assistant_id'], request.session['thread_id'])
            request.session['sixth_response'] = response6_json
            deletion_results = handle_deletion(request)
            request.session['deletion_results'] = deletion_results

            print(f"[DEBUG] Final response: {response6_json}\n")  # Debugging print statement

            if "Deletion successful" in deletion_results:
                analysis_status = "Analysis completed. All OpenAI elements deleted successfully."
            else:
                analysis_status = "Analysis completed successfully. Deletion of all OpenAI elements failed."

            request.session['analysis_status'] = analysis_status
            return response6_json, formatted_ca_prompt6, analysis_status, deletion_results
        except Exception as e:
            request.session['analysis_status'] = f"An error occurred: {str(e)}"
            return None, formatted_ca_prompt6, f"An error occurred: {str(e)}", ""
    return None, formatted_ca_prompt6, "No analysis performed.", ""

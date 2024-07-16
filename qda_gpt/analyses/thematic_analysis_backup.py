from qda_gpt.prompts.prompts_ta import ta_prompt1, ta_prompt2, ta_prompt3, ta_prompt4
from qda_gpt.openai_api import get_openai_response
from qda_gpt.deletion import handle_deletion

def phase1(request):
    formatted_prompt1 = ta_prompt1.format()
    response_json = get_openai_response(formatted_prompt1, request.session['assistant_id'], request.session['thread_id'])
    print("response_json:", response_json)  # Debugging print statement
    return response_json, formatted_prompt1

def phase2(request, response_json):
    formatted_prompt2 = ta_prompt2.format(response_json=response_json)
    response2_json = get_openai_response(formatted_prompt2, request.session['assistant_id'], request.session['thread_id'])
    print("response2_json:", response2_json)  # Debugging print statement
    return response2_json, formatted_prompt2

def phase3(request, response2_json):
    formatted_prompt3 = ta_prompt3.format(response2_json=response2_json)
    response3_json = get_openai_response(formatted_prompt3, request.session['assistant_id'], request.session['thread_id'])
    print("response3_json:", response3_json)  # Debugging print statement
    return response3_json, formatted_prompt3

def phase_deductive(request):
    ta_prompt_deductive = ta_prompt_deductive
    response4_json = get_openai_response(formatted_prompt4, request.session['assistant_id'], request.session['thread_id'])
    print("response4_json:", response4_json)  # Debugging print statement
    return response4_json, formatted_prompt4
def phase4(request, response_deductive_json):
    formatted_prompt4 = ta_prompt4.format(response_deductive_json=response_deductive_json)
    response4_json = get_openai_response(formatted_prompt4, request.session['assistant_id'], request.session['thread_id'])
    print("response4_json:", response4_json)  # Debugging print statement
    return response4_json, formatted_prompt4

def phase5(request, response2_json):
    formatted_prompt5 = ta_prompt5.format(response2_json=response2_json)
    response5_json = get_openai_response(formatted_prompt5, request.session['assistant_id'], request.session['thread_id'])
    print("response5_json:", response5_json)  # Debugging print statement
    return response5_json, formatted_prompt5

def phase6(request, response1_json):
    formatted_prompt3 = ta_prompt3.format(response1_json=response1_json)
    response6_json = get_openai_response(formatted_prompt6, request.session['assistant_id'], request.session['thread_id'])
    print("response6_json:", response6_json)  # Debugging print statement
    return response6_json, formatted_prompt6

def phase7(request):
    formatted_prompt7 = ta_prompt7
    if request.session.get('initialized', False):
        try:
            response7_json = get_openai_response(formatted_prompt7, request.session['assistant_id'], request.session['thread_id'])
            request.session['fourth_response'] = response7_json
            deletion_results = handle_deletion(request)
            request.session['deletion_results'] = deletion_results

            if "Deletion successful" in deletion_results:
                analysis_status = "Analysis completed. All OpenAI elements deleted successfully."
            else:
                analysis_status = "Analysis completed successfully. Deletion of all OpenAI elements failed."

            print("response7_json:", response7_json)  # Debugging print statement
            request.session['analysis_status'] = analysis_status
            return response7_json, formatted_prompt7, analysis_status, deletion_results
        except Exception as e:
            request.session['analysis_status'] = f"An error occurred: {str(e)}"
            return None, formatted_prompt7, f"An error occurred: {str(e)}", ""
    return None, formatted_prompt7, "No analysis performed.", ""

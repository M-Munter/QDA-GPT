from qda_gpt.prompts.prompts_ca import ca_prompt1, ca_prompt2, ca_prompt3, ca_prompt4, ca_prompt5, ca_prompt6, ca_prompt7, ca_prompt8
from qda_gpt.openai_api import get_openai_response
from qda_gpt.deletion import handle_deletion

def phase1(request):
    formatted_prompt1 = ca_prompt1
    response1_json = get_openai_response(formatted_prompt1, request.session['assistant_id'], request.session['thread_id'])
    print("response1_json:", response1_json)  # Debugging print statement
    return response1_json, formatted_prompt1

def phase2(request, response1_json=None):
    formatted_prompt2 = ca_prompt2
    response2_json = get_openai_response(formatted_prompt2, request.session['assistant_id'], request.session['thread_id'])
    print("response2_json:", response2_json)  # Debugging print statement
    return response2_json, formatted_prompt2

def phase3(request):
    formatted_prompt3 = ca_prompt3
    response3_json = get_openai_response(formatted_prompt3, request.session['assistant_id'], request.session['thread_id'])
    print("response3_json:", response3_json)  # Debugging print statement
    return response3_json, formatted_prompt3

def phase4(request):
    formatted_prompt4 = ca_prompt4
    response4_json = get_openai_response(formatted_prompt4, request.session['assistant_id'], request.session['thread_id'])
    print("response4_json:", response4_json)  # Debugging print statement
    return response4_json, formatted_prompt4

def phase5(request, response1_json):
    formatted_prompt5 = ca_prompt5.format(response1_json=response1_json)
    response5_json = get_openai_response(formatted_prompt5, request.session['assistant_id'], request.session['thread_id'])
    print(f"[DEBUG] Response number 5: {response5_json}\n")  # Debugging print statement
    return response5_json, formatted_prompt5

def phase6(request):
    formatted_prompt6 = ca_prompt6
    response6_json = get_openai_response(formatted_prompt6, request.session['assistant_id'], request.session['thread_id'])
    print(f"[DEBUG] Response number 6: {response6_json}\n")  # Debugging print statement
    return response6_json, formatted_prompt6

def phase7(request):
    formatted_prompt7 = ca_prompt7
    response7_json = get_openai_response(formatted_prompt7, request.session['assistant_id'], request.session['thread_id'])
    print(f"[DEBUG] Response number 7: {response7_json}\n")  # Debugging print statement
    return response7_json, formatted_prompt7

def phase8(request):
    formatted_prompt8 = ca_prompt8
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

            request.session['analysis_status'] = analysis_status
            print("response8_json:", response8_json)  # Debugging print statement
            return response8_json, formatted_prompt8, analysis_status, deletion_results
        except Exception as e:
            request.session['analysis_status'] = f"An error occurred: {str(e)}"
            return None, formatted_prompt8, f"An error occurred: {str(e)}", ""
    return None, formatted_prompt8, "No analysis performed.", ""

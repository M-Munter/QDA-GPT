from qda_gpt.prompts.prompts_gt import gt_prompt1, gt_prompt2, gt_prompt3, gt_prompt4, gt_prompt5, gt_prompt6, gt_prompt7
from qda_gpt.openai_api import get_openai_response
from qda_gpt.deletion import handle_deletion

def phase1(request):
    formatted_prompt1 = gt_prompt1
    response1_json = get_openai_response(formatted_prompt1, request.session['assistant_id'], request.session['thread_id'])
    return response1_json, formatted_prompt1

def phase2(request):
    formatted_prompt2 = gt_prompt2
    response2_json = get_openai_response(formatted_prompt2, request.session['assistant_id'], request.session['thread_id'])
    return response2_json, formatted_prompt2

def phase3(request):
    formatted_prompt3 = gt_prompt3
    response3_json = get_openai_response(formatted_prompt3, request.session['assistant_id'], request.session['thread_id'])
    return response3_json, formatted_prompt3

def phase4(request):
    formatted_prompt4 = gt_prompt4
    response4_json = get_openai_response(formatted_prompt4, request.session['assistant_id'], request.session['thread_id'])
    return response4_json, formatted_prompt4

def phase5(request):
    formatted_prompt5 = gt_prompt5
    response5_json = get_openai_response(formatted_prompt5, request.session['assistant_id'], request.session['thread_id'])
    return response5_json, formatted_prompt5

def phase6(request):
    formatted_prompt6 = gt_prompt6
    response6_json = get_openai_response(formatted_prompt6, request.session['assistant_id'], request.session['thread_id'])
    return response6_json, formatted_prompt6

def phase7(request):
    formatted_prompt7 = gt_prompt7
    if request.session.get('initialized', False):
        try:
            response7_json = get_openai_response(formatted_prompt7, request.session['assistant_id'], request.session['thread_id'])
            request.session['seventh_response'] = response7_json
            deletion_results = handle_deletion(request)
            request.session['deletion_results'] = deletion_results

            if "Deletion successful" in deletion_results:
                analysis_status = "Analysis completed. All OpenAI elements deleted successfully."
            else:
                analysis_status = "Analysis completed successfully. Deletion of all OpenAI elements failed."

            request.session['analysis_status'] = analysis_status
            return response7_json, formatted_prompt7, analysis_status, deletion_results
        except Exception as e:
            request.session['analysis_status'] = f"An error occurred: {str(e)}"
            return None, formatted_prompt7, f"An error occurred: {str(e)}", ""
    return None, formatted_prompt7, "No analysis performed.", ""

# views.py
from django.shortcuts import render
from django.http import JsonResponse
from .forms import SetupForm
from .openai_api import initialize_openai_resources, get_openai_response, delete_openai_resources
from .__version__ import __version__  # Import the version number
from .prompts_ta import ta_prompt1, ta_prompt2, ta_prompt3, ta_prompt4
from .utils import parse_response_to_table
import os
import time
import json

def clear_session_data(request):
    # Clears data for a session
    session_keys = ['response', 'setup_status', 'deletion_results', 'console_output', 'analysis_status',
                    'second_response', 'third_response', 'fourth_response']
    for key in session_keys:
        request.session.pop(key, None)

def handle_setup(request, setup_form):
    if setup_form.is_valid():
        file = request.FILES['file']
        model_choice = setup_form.cleaned_data['model_choice']
        file_path = handle_uploaded_file(file)
        try:
            resources = initialize_openai_resources(file_path, model_choice)
            request.session['initialized'] = True
            request.session['thread_id'] = resources['thread'].id
            request.session['assistant_id'] = resources['assistant'].id
            request.session['file_id'] = resources['file'].id
            request.session['setup_status'] = "OpenAI initialized successfully."
        except Exception as e:
            request.session['setup_status'] = str(e)
        return request.session['setup_status']

def handle_analysis(request, user_prompt):
    formatted_ta_prompt1 = ta_prompt1.format(user_prompt=user_prompt)
    request.session['formatted_ta_prompt1'] = formatted_ta_prompt1
    if request.session.get('initialized', False) and user_prompt:
        try:
            response_json = get_openai_response(formatted_ta_prompt1, request.session['assistant_id'], request.session['thread_id'])
            request.session['response'] = response_json
            return response_json, formatted_ta_prompt1
        except Exception as e:
            return None, f"An error occurred: {str(e)}", None, formatted_ta_prompt1  # Return formatted_ta_prompt1 even on error
    return None, "No analysis performed.", None, formatted_ta_prompt1  # Return formatted_ta_prompt1 even if no analysis is performed


def handle_second_prompt_analysis(request, response_json):
    formatted_ta_prompt2 = ta_prompt2.format(response_json=response_json)
    if request.session.get('initialized', False):
        try:
            # ta_prompt2_with_topics = ta_prompt2.format(topic_list=", ".join(topic_list))
            response2_json = get_openai_response(formatted_ta_prompt2, request.session['assistant_id'], request.session['thread_id'])
            request.session['second_response'] = response2_json

            return response2_json, formatted_ta_prompt2
        except Exception as e:
            request.session['analysis_status'] = f"An error occurred: {str(e)}"
            return f"An error occurred: {str(e)}"
    return "No analysis performed as assistant not initialized."

def handle_ta_phase4(request, response_json):
    formatted_ta_prompt3 = ta_prompt3.format(response_json=response_json)
    if request.session.get('initialized', False):
        try:
            # ta_prompt2_with_topics = ta_prompt2.format(topic_list=", ".join(topic_list))
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
            # ta_prompt2_with_topics = ta_prompt2.format(topic_list=", ".join(topic_list))
            response4_json = get_openai_response(formatted_ta_prompt4, request.session['assistant_id'], request.session['thread_id'])
            request.session['third_response'] = response4_json

            deletion_results = handle_deletion(request)  # Ensure deletion_results are fetched from the correct place
            request.session['deletion_results'] = deletion_results

            request.session['analysis_status'] = "Analysis completed successfully. Assistant thread deleted successfully."

            return response4_json, formatted_ta_prompt4, "Analysis completed successfully.", deletion_results
        except Exception as e:
            request.session['analysis_status'] = f"An error occurred: {str(e)}"
            return None, formatted_ta_prompt4, f"An error occurred: {str(e)}", ""
    return None, formatted_ta_prompt4, "No analysis performed as assistant not initialized.", ""

def handle_deletion(request):
    # Simulated deletion results for demonstration purposes
    deletion_results = {
        'assistant': {'deleted': True},
        'file': {'deleted': False},
        'thread': {'deleted': True}
    }

    deletion_message_parts = []
    assistant_deletion = deletion_results['assistant']
    file_deletion = deletion_results['file']
    thread_deletion = deletion_results['thread']

    if assistant_deletion['deleted']:
        deletion_message_parts.append("Assistant Deletion: Successful.")
    else:
        deletion_message_parts.append("Assistant Deletion: Failed or no data.")

    if file_deletion['deleted']:
        deletion_message_parts.append("File Deletion: Successful.")
    else:
        deletion_message_parts.append("File Deletion: Failed or no data.")

    if thread_deletion['deleted']:
        deletion_message_parts.append("Thread Deletion: Successful.")
    else:
        deletion_message_parts.append("Thread Deletion: Failed or no data.")

    deletion_message = ", ".join(deletion_message_parts)
    print(deletion_message)
    return deletion_message

def dashboard(request):
    setup_form = SetupForm(request.POST or None, request.FILES or None)
    context = {
        'setup_form': setup_form,
        'version': __version__,
        'response': request.session.get('response', ''),
        'second_response': request.session.get('second_response', ''),
        'third_response': request.session.get('third_response', ''),
        'fourth_response': request.session.get('fourth_response', ''),
        'setup_status': request.session.get('setup_status', ''),
        'analysis_status': request.session.get('analysis_status', ''),
        'deletion_results': request.session.get('deletion_results', '')
    }

    if request.method == 'GET':
        clear_session_data(request)
        print("Session cleared on GET request\n\n")

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'setup':
            context['setup_status'] = handle_setup(request, setup_form)
        elif action == 'analyze':
            user_prompt = request.POST.get('user_prompt', '')
            response_json, formatted_ta_prompt1 = handle_analysis(request, user_prompt)

            context.update({
                'response': response_json,
                'formatted_ta_prompt1': formatted_ta_prompt1
            })

            # Extracting topic list from response and passing it to handle_second_prompt_analysis
            # topic_list = extract_topic_list(response_json)

            if response_json:  # Ensuring that there is a response before proceeding to the second prompt
                response2_json, formatted_ta_prompt2 = handle_second_prompt_analysis(request, response_json)

                context.update({
                    'second_response': response2_json,
                    'formatted_ta_prompt2': formatted_ta_prompt2
                })

                if response2_json:  # Ensuring that there is a response before proceeding to the second prompt
                    response3_json, formatted_ta_prompt3 = handle_ta_phase4(request, response_json)

                    context.update({
                        'third_response': response3_json,
                        'formatted_ta_prompt3': formatted_ta_prompt3
                    })

                    if response3_json:  # Ensuring that there is a response before proceeding to the second prompt
                        response4_json, formatted_ta_prompt4, analysis_status, deletion_results = handle_ta_phase5(request, response2_json, response3_json)

                        context.update({
                            'fourth_response': response4_json,
                            'formatted_ta_prompt4': formatted_ta_prompt4,
                            'analysis_status': analysis_status,
                            # This should update the context for the analysis status
                            'deletion_results': deletion_results
                        })


            print(f"Session after POST analyze: {request.session.items()}\n\n")  # Debugging line

    context.update({
        'response': request.session.get('response', ''),
        'second_response': request.session.get('second_response', ''),
        'setup_status': request.session.get('setup_status', ''),
        'analysis_status': request.session.get('analysis_status', ''),
        'console_output': request.session.get('console_output', ''),
        'deletion_results': request.session.get('deletion_results', '')
    })
    print(f"Final context: {context}\n\n")  # Debugging line

    return render(request, 'qda_gpt/dashboard.html', context)

def handle_uploaded_file(f):
    file_path = os.path.join('uploads', f.name)
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return file_path

def extract_topic_list(response):
    try:
        if isinstance(response, str):
            json_response = json.loads(response)
        else:
            json_response = response
        topic_list = json_response.get('topics', [])
        return topic_list
    except Exception as e:
        print(f"Error extracting topic list: {str(e)}\n\n")
        return []


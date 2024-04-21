# views.py
from django.shortcuts import render
from django.http import JsonResponse
from .forms import SetupForm
from .openai_api import initialize_openai_resources, get_openai_response, delete_openai_resources
from .__version__ import __version__  # Import the version number
from .prompts_ta import ta_prompt1
import os
import time

def clear_session_data(request):
    # Clears data for a session
    session_keys = ['response', 'setup_status', 'deletion_results', 'console_output', 'analysis_status']
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
            response = get_openai_response(formatted_ta_prompt1, request.session['assistant_id'], request.session['thread_id'])
            deletion_results = handle_deletion(request)  # Ensure deletion_results are fetched from the correct place
            request.session['response'] = response
            request.session['analysis_status'] = "Analysis completed successfully."
            request.session['deletion_results'] = deletion_results
            return response, "Analysis completed successfully.", deletion_results, formatted_ta_prompt1  # Return formatted_ta_prompt1
        except Exception as e:
            request.session['analysis_status'] = f"An error occurred: {str(e)}"
            return None, f"An error occurred: {str(e)}", None, formatted_ta_prompt1  # Return formatted_ta_prompt1 even on error
    return None, "No analysis performed.", None, formatted_ta_prompt1  # Return formatted_ta_prompt1 even if no analysis is performed



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
    return deletion_message

def dashboard(request):
    setup_form = SetupForm(request.POST or None, request.FILES or None)
    context = {'setup_form': setup_form, 'version': __version__}

    if request.method == 'GET':
        clear_session_data(request)
        print("Session cleared on GET request /n/n")

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'setup':
            context['setup_status'] = handle_setup(request, setup_form)
        elif action == 'analyze':
            user_prompt = request.POST.get('user_prompt', '')
            response, analysis_status, deletion_results, formatted_ta_prompt1 = handle_analysis(request, user_prompt)
            context.update({
                'response': response,
                'analysis_status': analysis_status,
                'deletion_results': deletion_results,
                'formatted_ta_prompt1': formatted_ta_prompt1
            })
            print(f"Session after POST analyze: {request.session.items()} /n/n")  # Debugging line

    context.update({
        'response': request.session.get('response', ''),
        'setup_status': request.session.get('setup_status', ''),
        'analysis_status': request.session.get('analysis_status', ''),
        'console_output': request.session.get('console_output', ''),
        'deletion_results': request.session.get('deletion_results', '')
    })
    print(f"Final context: {context} /n/n")  # Debugging line

    return render(request, 'qda_gpt/dashboard.html', context)

def handle_uploaded_file(f):
    file_path = os.path.join('uploads', f.name)
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return file_path



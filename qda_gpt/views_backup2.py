# views.py
from django.shortcuts import render
from .forms import SetupForm
from .openai_api import initialize_openai_resources, get_openai_response
from .__version__ import __version__  # Import the version number
from qda_gpt.analyses import thematic_analysis # Import thematic analysis functions
from qda_gpt.deletion import handle_deletion  # Import the handle_deletion function
import os
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
            request.session['vector_store_id'] = resources['vector_store'].id
            request.session['assistant_id'] = resources['assistant'].id
            request.session['file_id'] = resources['file'].id
            request.session['setup_status'] = "OpenAI Assistant initialized successfully."
        except Exception as e:
            request.session['setup_status'] = f"Error initializing OpenAI resources: {str(e)}"
        return request.session['setup_status']


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
            response_json, formatted_ta_prompt1 = thematic_analysis.handle_analysis(request, user_prompt)

            context.update({
                'response': response_json,
                'formatted_ta_prompt1': formatted_ta_prompt1
            })

            # Extracting topic list from response and passing it to handle_second_prompt_analysis
            # topic_list = extract_topic_list(response_json)

            if response_json:  # Ensuring that there is a response before proceeding to the second prompt
                response2_json, formatted_ta_prompt2 = thematic_analysis.handle_second_prompt_analysis(request, response_json)

                context.update({
                    'second_response': response2_json,
                    'formatted_ta_prompt2': formatted_ta_prompt2
                })

                if response2_json:  # Ensuring that there is a response before proceeding to the second prompt
                    response3_json, formatted_ta_prompt3 = thematic_analysis.handle_ta_phase4(request, response_json)

                    context.update({
                        'third_response': response3_json,
                        'formatted_ta_prompt3': formatted_ta_prompt3
                    })

                    if response3_json:  # Ensuring that there is a response before proceeding to the second prompt
                        response4_json, formatted_ta_prompt4, analysis_status, deletion_results = thematic_analysis.handle_ta_phase5(request, response2_json, response3_json)

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
    # print(f"Final context: {context}\n\n")  # Debugging line

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


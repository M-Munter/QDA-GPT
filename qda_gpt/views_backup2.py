# views.py
from django.shortcuts import render, redirect
from .forms import SetupForm
from django.http import JsonResponse
from .openai_api import initialize_openai_resources, create_thread
from .__version__ import __version__
from qda_gpt.analyses import thematic_analysis, content_analysis, grounded_theory
import os
import time  # Import time for sleep
import sys  # Import sys to use sys.stdout for printing without new lines
import json

def clear_session_data(request):
    session_keys = [
        'response', 'setup_status', 'deletion_results', 'console_output', 'analysis_status',
        'second_response', 'third_response', 'fourth_response', 'fifth_response', 'sixth_response', 'seventh_response',
        'analysis_type', 'user_prompt', 'file_name'
    ]
    for key in session_keys:
        request.session.pop(key, None)

def clear_session(request):
    clear_session_data(request)
    return redirect('dashboard')


def get_setup_status(request):
    status = request.session.get('setup_status', '')
    print(f"[DEBUG] Current setup_status: {status}", flush=True)  # Debugging print statement
    return JsonResponse({'setup_status': status})


def handle_setup(request, setup_form):
    if setup_form.is_valid():
        file = request.FILES.get('file')
        if not file:
            return "Please select a file."
        model_choice = setup_form.cleaned_data['model_choice']
        user_prompt = request.POST.get('user_prompt', '')
        file_path = handle_uploaded_file(file)
        try:
            # Create thread and assign correct thread ID
            request.session['setup_status'] = "Initializing OpenAI Assistant."
            print(f"[DEBUG] setup_status: Initializing OpenAI resources...", flush=True)
            request.session.save()  # Explicitly save the session
            time.sleep(0.25)
            thread_id = create_thread()
            if thread_id:
                request.session['thread_id'] = thread_id
                resources = initialize_openai_resources(
                    file_path, model_choice, request.session['analysis_type'], user_prompt
                )
                request.session['setup_status'] = "OpenAI Assistant initialized successfully."
                print(f"[DEBUG] setup_status: OpenAI resources Initialized Successfully", flush=True)
                request.session.save()  # Explicitly save the session

                time.sleep(0.55)

                print("Waiting for indexing: ", end='', flush=True)
                for i in range(5, -1, -1):  # Adjusted range to include 0
                    print(f"{i} ", end='', flush=True)  # Print the countdown number with a space
                    time.sleep(0.9)
                    print('\rWaiting for indexing: ', end='',
                          flush=True)  # Return to the beginning of the line and overwrite
                print("0")
                print("Indexing complete.\n")

                request.session['initialized'] = True
                request.session['vector_store_id'] = resources['vector_store'].id
                request.session['assistant_id'] = resources['assistant'].id
                request.session['file_id'] = resources['file'].id
                request.session['file_name'] = file.name
                request.session['user_prompt'] = user_prompt  # Save user prompt to session

                return True  # Return early to immediately show the setup status. Indicate success immediately
            else:
                request.session['setup_status'] = "Failed to create thread."
                request.session.save()  # Explicitly save the session
                return False # Indicate failure immediately

        except Exception as e:
            request.session['setup_status'] = f"Error initializing OpenAI resources: {str(e)}"
            request.session.save()  # Explicitly save the session
            return False
    return False



def dashboard(request):
    setup_form = SetupForm(request.POST or None, request.FILES or None)
    analysis_type = request.POST.get('analysis_type', request.session.get('analysis_type', ''))
    user_prompt = request.POST.get('user_prompt', request.session.get('user_prompt', ''))
    file_name = request.session.get('file_name', '')

    if analysis_type:
        request.session['analysis_type'] = analysis_type

    context = {
        'setup_form': setup_form,
        'version': __version__,
        'response': request.session.get('response', ''),
        'second_response': request.session.get('second_response', ''),
        'third_response': request.session.get('third_response', ''),
        'fourth_response': request.session.get('fourth_response', ''),
        'fifth_response': request.session.get('fifth_response', ''),
        'sixth_response': request.session.get('sixth_response', ''),
        'seventh_response': request.session.get('seventh_response', ''),
        'setup_status': request.session.get('setup_status', ''),
        'analysis_status': request.session.get('analysis_status', ''),
        'deletion_results': request.session.get('deletion_results', ''),
        'analysis_type': request.session.get('analysis_type', ''),
        'user_prompt': user_prompt,
        'file_name': file_name,
    }

    if request.method == 'GET':
        clear_session_data(request)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'analyze':
            setup_success = handle_setup(request, setup_form)
            if setup_success:
                if analysis_type == 'thematic':
                    response_json, formatted_prompt1 = thematic_analysis.handle_analysis(request)
                    response2_json, formatted_prompt2 = thematic_analysis.handle_second_prompt_analysis(request,
                                                                                                        response_json)
                    response3_json, formatted_prompt3 = thematic_analysis.handle_ta_phase3(request, response_json)
                    response4_json, formatted_prompt4, analysis_status, deletion_results = thematic_analysis.handle_ta_phase4(
                        request, response2_json, response3_json)
                    context.update({
                        'response': response_json,
                        'formatted_prompt1': formatted_prompt1,
                        'second_response': response2_json,
                        'formatted_prompt2': formatted_prompt2,
                        'third_response': response3_json,
                        'formatted_prompt3': formatted_prompt3,
                        'fourth_response': response4_json,
                        'formatted_prompt4': formatted_prompt4,
                        'analysis_status': analysis_status,
                        'deletion_results': deletion_results
                    })
                elif analysis_type == 'content':
                    response_json, formatted_prompt1 = content_analysis.handle_analysis(request)
                    response2_json, formatted_prompt2 = content_analysis.handle_second_prompt_analysis(request,
                                                                                                       response_json)
                    response3_json, formatted_prompt3 = content_analysis.handle_ca_phase3(request, response2_json)
                    response4_json, formatted_prompt4 = content_analysis.handle_ca_phase4(request, response3_json)
                    response5_json, formatted_prompt5 = content_analysis.handle_ca_phase5(request, response4_json)
                    response6_json, formatted_prompt6, analysis_status, deletion_results = content_analysis.handle_ca_phase6(
                        request, response5_json)
                    context.update({
                        'response': response_json,
                        'formatted_prompt1': formatted_prompt1,
                        'second_response': response2_json,
                        'formatted_prompt2': formatted_prompt2,
                        'third_response': response3_json,
                        'formatted_prompt3': formatted_prompt3,
                        'fourth_response': response4_json,
                        'formatted_prompt4': formatted_prompt4,
                        'fifth_response': response5_json,
                        'formatted_prompt5': formatted_prompt5,
                        'sixth_response': response6_json,
                        'formatted_prompt6': formatted_prompt6,
                        'analysis_status': analysis_status,
                        'deletion_results': deletion_results
                    })
                elif analysis_type == 'grounded':
                    response_json, formatted_prompt1 = grounded_theory.handle_analysis(request)
                    response2_json, formatted_prompt2 = grounded_theory.handle_second_prompt_analysis(request,
                                                                                                      response_json)
                    response3_json, formatted_prompt3 = grounded_theory.handle_gt_phase3(request, response2_json)
                    response4_json, formatted_prompt4 = grounded_theory.handle_gt_phase4(request, response3_json)
                    response5_json, formatted_prompt5 = grounded_theory.handle_gt_phase5(request, response4_json)
                    response6_json, formatted_prompt6 = grounded_theory.handle_gt_phase6(request, response5_json)
                    response7_json, formatted_prompt7, analysis_status, deletion_results = grounded_theory.handle_gt_phase7(
                        request, response6_json)
                    context.update({
                        'response': response_json,
                        'formatted_prompt1': formatted_prompt1,
                        'second_response': response2_json,
                        'formatted_prompt2': formatted_prompt2,
                        'third_response': response3_json,
                        'formatted_prompt3': formatted_prompt3,
                        'fourth_response': response4_json,
                        'formatted_prompt4': formatted_prompt4,
                        'fifth_response': response5_json,
                        'formatted_prompt5': formatted_prompt5,
                        'sixth_response': response6_json,
                        'formatted_prompt6': formatted_prompt6,
                        'seventh_response': response7_json,
                        'formatted_prompt7': formatted_prompt7,
                        'analysis_status': analysis_status,
                        'deletion_results': deletion_results
                    })

                request.session.save()  # Explicitly save the session
            else:
                context['setup_status'] = request.session.get('setup_status', '')

    return render(request, 'qda_gpt/dashboard.html', context)

def handle_uploaded_file(f):
    file_path = os.path.join('uploads', f.name)
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return file_path

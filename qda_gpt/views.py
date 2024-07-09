# views.py
from django.shortcuts import render, redirect
from .forms import SetupForm
from django.http import JsonResponse
from .openai_api import initialize_openai_resources, create_thread
from .__version__ import __version__
from qda_gpt.analyses import thematic_analysis, content_analysis, grounded_theory
from collections import OrderedDict
import os
import time
import json

def clear_session_data(request):
    session_keys = [
        'response', 'setup_status', 'deletion_results', 'console_output', 'analysis_status',
        'second_response', 'third_response', 'fourth_response', 'fifth_response', 'sixth_response', 'seventh_response',
        'analysis_type', 'user_prompt', 'file_name', 'tables', 'prompt_table_pairs'
    ]
    for key in session_keys:
        request.session.pop(key, None)
    request.session.save()

def clear_session(request):
    clear_session_data(request)
    return redirect('dashboard')


def get_setup_status(request):
    status = request.session.get('setup_status', '')
    print(f"[DEBUG] Current setup_status: {status}\n", flush=True)  # Debugging print statement
    return JsonResponse({'setup_status': status})

def handle_uploaded_file(f):
    file_path = os.path.join('uploads', f.name)
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return file_path


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
            request.session.save()  # Explicitly save the session
            time.sleep(0.25)
            thread_id = create_thread()
            if thread_id:
                request.session['thread_id'] = thread_id
                resources = initialize_openai_resources(
                    file_path, model_choice, request.session['analysis_type'], user_prompt
                )
                request.session['setup_status'] = "OpenAI Assistant initialized successfully. Sending messages to the Assistant."
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


def generate_tables_from_response(response_text):
    try:
        start = response_text.find('{')
        end = response_text.rfind('}') + 1
        if start == -1 or end == -1:
            raise json.JSONDecodeError("Invalid JSON format", response_text, 0)
        response_text = response_text[start:end]
        response_json = json.loads(response_text, object_pairs_hook=OrderedDict)

        tables = []
        if isinstance(response_json, dict):
            for table_name, records in response_json.items():
                if isinstance(records, list):
                    flattened_data = []
                    for record in records:
                        flattened_record = flatten_dict(record)
                        flattened_data.append(flattened_record)

                    if flattened_data:
                        first_record = flattened_data[0]
                        columns = list(first_record.keys())
                        data = [[record.get(col, None) for col in columns] for record in flattened_data]
                        tables.append({
                            'table_name': table_name,
                            'columns': columns,
                            'data': data
                        })
        return tables

    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def flatten_dict(d, parent_key='', sep='_'):
    items = []
    if isinstance(d, dict):
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                if v and isinstance(v[0], dict):
                    for i, sub_v in enumerate(v):
                        items.extend(flatten_dict(sub_v, f"{new_key}{sep}{i}", sep=sep).items())
                else:
                    items.append((new_key, v))
            else:
                items.append((new_key, v))
    else:
        items.append((parent_key, d))
    return dict(items)








def handle_analysis(request, analysis_type):
    analysis_funcs = {
        'thematic': thematic_analysis,
        'content': content_analysis,
        'grounded': grounded_theory
    }
    if analysis_type in analysis_funcs:
        analysis_module = analysis_funcs[analysis_type]
        formatted_prompts = []
        prompt_table_pairs = []
        phases = [func for name, func in analysis_module.__dict__.items() if name.startswith('phase')]
        response_json = None

        for idx, phase in enumerate(phases):
            if idx == len(phases) - 1:
                if analysis_type == 'thematic':
                    response_json, formatted_prompt, analysis_status, deletion_results = phase(request, response_json)
                elif analysis_type == 'content':
                    response_json, formatted_prompt, analysis_status, deletion_results = phase(request, response_json)
                elif analysis_type == 'grounded':
                    response_json, formatted_prompt, analysis_status, deletion_results = phase(request, response_json)
                formatted_prompts.append(formatted_prompt)
                tables = generate_tables_from_response(response_json)
                prompt_table_pairs.append({'prompt': formatted_prompt, 'tables': tables})
                return {
                    'analysis_status': analysis_status,
                    'deletion_results': deletion_results,
                    'prompt_table_pairs': prompt_table_pairs
                }
            else:
                if response_json is None:
                    response_json, formatted_prompt = phase(request)
                else:
                    response_json, formatted_prompt = phase(request, response_json)
                formatted_prompts.append(formatted_prompt)
                tables = generate_tables_from_response(response_json)
                prompt_table_pairs.append({'prompt': formatted_prompt, 'tables': tables})

        return {
            'prompt_table_pairs': prompt_table_pairs
        }
    return {}

def dashboard(request):
    if request.method == 'GET':
        clear_session_data(request)
    setup_form = SetupForm(request.POST or None, request.FILES or None)
    analysis_type = request.POST.get('analysis_type', request.session.get('analysis_type', ''))
    user_prompt = request.POST.get('user_prompt', request.session.get('user_prompt', ''))
    file_name = request.session.get('file_name', '')

    if analysis_type:
        request.session['analysis_type'] = analysis_type

    context = {
        'setup_form': setup_form,
        'version': __version__,
        'setup_status': request.session.get('setup_status', ''),
        'analysis_status': request.session.get('analysis_status', ''),
        'deletion_results': request.session.get('deletion_results', ''),
        'analysis_type': request.session.get('analysis_type', ''),
        'user_prompt': user_prompt,
        'file_name': file_name,
        'tables': request.session.get('tables', []),
        'prompt_table_pairs': request.session.get('prompt_table_pairs', [])
    }

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'analyze':
            setup_success = handle_setup(request, setup_form)
            if setup_success:
                context_update = handle_analysis(request, analysis_type)
                context.update(context_update)
                request.session['prompt_table_pairs'] = context.get('prompt_table_pairs', [])
            else:
                context['setup_status'] = request.session.get('setup_status', '')

    return render(request, 'qda_gpt/dashboard.html', context)
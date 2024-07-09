# views.py
from django.shortcuts import render, redirect
from .forms import SetupForm
from django.http import JsonResponse
from .openai_api import initialize_openai_resources, create_thread
from .__version__ import __version__
from qda_gpt.analyses import thematic_analysis, content_analysis, grounded_theory
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
        response_json = json.loads(response_text)

        tables = []
        if isinstance(response_json, dict):
            for table_name, records in response_json.items():
                if isinstance(records, list):
                    flattened_data = []
                    for record in records:
                        flattened_record = flatten_dict(record)
                        flattened_data.append(flattened_record)

                    if flattened_data:
                        columns = set(flattened_data[0].keys())
                        data = [[record.get(col, None) for col in columns] for record in flattened_data]
                        tables.append({
                            'table_name': table_name,
                            'columns': list(columns),
                            'data': data
                        })
        return tables

    except json.JSONDecodeError as e:
        return []


def flatten_dict(d, parent_key='', sep='_'):
    items = []
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
    return dict(items)





def dashboard(request):
    if request.method == 'GET':
        clear_session_data(request)
        print(f"[DEBUG] GET request: setup_status after clear_session: {request.session.get('setup_status', '')}\n")

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
                formatted_prompts = []
                prompt_table_pairs = []

                print(f"[DEBUG] POST request: setup_status after handle_setup: {request.session.get('setup_status', '')}\n")
                if analysis_type == 'thematic':
                    response_json, formatted_prompt1 = thematic_analysis.phase1(request)
                    response2_json, formatted_prompt2 = thematic_analysis.phase2(request, response_json)
                    response3_json, formatted_prompt3 = thematic_analysis.phase3(request, response_json)
                    response4_json, formatted_prompt4, analysis_status, deletion_results = thematic_analysis.phase4(
                        request, response2_json, response3_json)

                    formatted_prompts.extend([formatted_prompt1, formatted_prompt2, formatted_prompt3, formatted_prompt4])
                    tables1 = generate_tables_from_response(response_json)
                    tables2 = generate_tables_from_response(response2_json)
                    tables3 = generate_tables_from_response(response3_json)
                    tables4 = generate_tables_from_response(response4_json)

                    prompt_table_pairs.append({'prompt': formatted_prompt1, 'tables': tables1})
                    prompt_table_pairs.append({'prompt': formatted_prompt2, 'tables': tables2})
                    prompt_table_pairs.append({'prompt': formatted_prompt3, 'tables': tables3})
                    prompt_table_pairs.append({'prompt': formatted_prompt4, 'tables': tables4})

                    context.update({
                        'analysis_status': analysis_status,
                        'deletion_results': deletion_results,
                        'prompt_table_pairs': prompt_table_pairs
                    })
                elif analysis_type == 'content':
                    response_json, formatted_prompt1 = content_analysis.phase1(request)
                    response2_json, formatted_prompt2 = content_analysis.phase2(request, response_json)
                    response3_json, formatted_prompt3 = content_analysis.phase3(request, response2_json)
                    response4_json, formatted_prompt4 = content_analysis.phase4(request, response3_json)
                    response5_json, formatted_prompt5 = content_analysis.phase5(request, response4_json)
                    response6_json, formatted_prompt6, analysis_status, deletion_results = content_analysis.phase6(
                        request, response5_json)

                    formatted_prompts.extend([formatted_prompt1, formatted_prompt2, formatted_prompt3, formatted_prompt4, formatted_prompt5, formatted_prompt6])
                    tables1 = generate_tables_from_response(response_json)
                    tables2 = generate_tables_from_response(response2_json)
                    tables3 = generate_tables_from_response(response3_json)
                    tables4 = generate_tables_from_response(response4_json)
                    tables5 = generate_tables_from_response(response5_json)
                    tables6 = generate_tables_from_response(response6_json)

                    prompt_table_pairs.append({'prompt': formatted_prompt1, 'tables': tables1})
                    prompt_table_pairs.append({'prompt': formatted_prompt2, 'tables': tables2})
                    prompt_table_pairs.append({'prompt': formatted_prompt3, 'tables': tables3})
                    prompt_table_pairs.append({'prompt': formatted_prompt4, 'tables': tables4})
                    prompt_table_pairs.append({'prompt': formatted_prompt5, 'tables': tables5})
                    prompt_table_pairs.append({'prompt': formatted_prompt6, 'tables': tables6})

                    context.update({
                        'analysis_status': analysis_status,
                        'deletion_results': deletion_results,
                        'prompt_table_pairs': prompt_table_pairs
                    })
                elif analysis_type == 'grounded':
                    response_json, formatted_prompt1 = grounded_theory.phase1(request)
                    response2_json, formatted_prompt2 = grounded_theory.phase2(request, response_json)
                    response3_json, formatted_prompt3 = grounded_theory.phase3(request, response2_json)
                    response4_json, formatted_prompt4 = grounded_theory.phase4(request, response3_json)
                    response5_json, formatted_prompt5 = grounded_theory.phase5(request, response4_json)
                    response6_json, formatted_prompt6 = grounded_theory.phase6(request, response5_json)
                    response7_json, formatted_prompt7, analysis_status, deletion_results = grounded_theory.phase7(
                        request, response6_json)

                    formatted_prompts.extend([formatted_prompt1, formatted_prompt2, formatted_prompt3, formatted_prompt4, formatted_prompt5, formatted_prompt6, formatted_prompt7])
                    tables1 = generate_tables_from_response(response_json)
                    tables2 = generate_tables_from_response(response2_json)
                    tables3 = generate_tables_from_response(response3_json)
                    tables4 = generate_tables_from_response(response4_json)
                    tables5 = generate_tables_from_response(response5_json)
                    tables6 = generate_tables_from_response(response6_json)
                    tables7 = generate_tables_from_response(response7_json)

                    prompt_table_pairs.append({'prompt': formatted_prompt1, 'tables': tables1})
                    prompt_table_pairs.append({'prompt': formatted_prompt2, 'tables': tables2})
                    prompt_table_pairs.append({'prompt': formatted_prompt3, 'tables': tables3})
                    prompt_table_pairs.append({'prompt': formatted_prompt4, 'tables': tables4})
                    prompt_table_pairs.append({'prompt': formatted_prompt5, 'tables': tables5})
                    prompt_table_pairs.append({'prompt': formatted_prompt6, 'tables': tables6})
                    prompt_table_pairs.append({'prompt': formatted_prompt7, 'tables': tables7})

                    context.update({
                        'analysis_status': analysis_status,
                        'deletion_results': deletion_results,
                        'prompt_table_pairs': prompt_table_pairs
                    })

                request.session['prompt_table_pairs'] = prompt_table_pairs
                print(f"[DEBUG] POST request: session saved with setup_status: {request.session.get('setup_status', '')}\n")
            else:
                context['setup_status'] = request.session.get('setup_status', '')
                print(f"[DEBUG] POST request: setup_status after failed handle_setup: {request.session.get('setup_status', '')}\n")

    return render(request, 'qda_gpt/dashboard.html', context)
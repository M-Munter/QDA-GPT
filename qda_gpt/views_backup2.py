# views.py
from django.shortcuts import render, redirect
from .forms import SetupForm
from django.http import JsonResponse, HttpResponse
from .openai_api import initialize_openai_resources, create_thread
from .__version__ import __version__
from qda_gpt.analyses import thematic_analysis, content_analysis, grounded_theory
from collections import OrderedDict
from django.core.serializers.json import DjangoJSONEncoder
from urllib.parse import quote
from qda_gpt.prompts.prompts_ca import ca_instruction
from qda_gpt.prompts.prompts_gt import gt_instruction
from qda_gpt.prompts.prompts_ta import ta_instruction
from openpyxl import Workbook
import pandas as pd
import os
import time
import json


def clear_session_data(request):
    session_keys = [
        'response', 'setup_status', 'deletion_results', 'console_output', 'analysis_status',
        'second_response', 'third_response', 'fourth_response', 'fifth_response', 'sixth_response', 'seventh_response',
        'eighth_response', 'analysis_type', 'user_prompt', 'file_name', 'tables', 'prompt_table_pairs'
    ]
    for key in session_keys:
        request.session.pop(key, None)
    request.session.save()

def clear_session(request):
    clear_session_data(request)
    return redirect('dashboard')


def get_setup_status(request):
    status = request.session.get('setup_status', '')
    analysis_status = request.session.get('analysis_status', '')
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
                    df = pd.json_normalize(records, sep='_')
                    df = explode_nested_columns(df)
                    tables.append({
                        'table_name': table_name,
                        'columns': df.columns.tolist(),
                        'data': df.values.tolist()
                    })
                elif isinstance(records, dict):
                    df = pd.json_normalize(records, sep='_')
                    df = explode_nested_columns(df)
                    if df.shape[0] == 1:
                        df = df.T.reset_index()
                        df.columns = ['Field', 'Value']
                    tables.append({
                        'table_name': table_name,
                        'columns': df.columns.tolist(),
                        'data': df.values.tolist()
                    })
        return tables

    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def explode_nested_columns(df):
    """
    Explode and normalize nested columns in the DataFrame.
    """
    for col in df.columns:
        if isinstance(df[col].iloc[0], list):
            df = df.explode(col).reset_index(drop=True)
        if isinstance(df[col].iloc[0], dict):
            df = df.drop(columns=[col]).join(df[col].apply(pd.Series).add_prefix(f"{col}_"))
    return df



def download_xlsx(request):
    analysis_type = request.session.get('analysis_type', 'N/A')
    user_prompt = request.session.get('user_prompt', 'N/A')
    file_name = request.GET.get('file_name', 'qda.xlsx')  # Get the filename from the query parameters

    # Map analysis type to full names
    analysis_type_full_name = {
        'thematic': 'Thematic Analysis',
        'grounded': 'Grounded Theory',
        'content': 'Content Analysis'
    }.get(analysis_type, 'Unknown Analysis Type')

    # Select the correct instructions based on the analysis type
    instructions_template = {
        'Thematic Analysis': ta_instruction,
        'Grounded Theory': gt_instruction,
        'Content Analysis': ca_instruction
    }.get(analysis_type_full_name, 'N/A')

    instructions = instructions_template.format(user_prompt=user_prompt)

    prompt_table_pairs = request.session.get('prompt_table_pairs', [])

    # Sanitize the filename for use in Content-Disposition
    file_name = quote(file_name)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'

    wb = Workbook()
    ws = wb.active
    ws.title = "Overview"

    # Write analysis type and instructions in the first sheet
    ws.append(['Analysis Type', analysis_type_full_name])
    ws.append([])  # Add an empty row for separation
    ws.append(['Instructions'])
    for line in instructions.split('\n'):
        ws.append([line])
    ws.append([])  # Add an empty row for separation

    for index, pair in enumerate(prompt_table_pairs):
        sheet_title = f'Prompt {index + 1}'
        ws = wb.create_sheet(title=sheet_title)
        ws.append(['Prompt'])
        for line in pair.get('prompt', 'N/A').split('\n'):
            ws.append([line])
        ws.append([])  # Add an empty row for separation
        for table in pair['tables']:
            ws.append([table['table_name']])
            ws.append(table['columns'])
            for row in table['data']:
                if isinstance(row, list):
                    ws.append(row)
                elif isinstance(row, dict):
                    ws.append([row.get(col, '') for col in table['columns']])
            ws.append([])  # Add an empty row for separation

    wb.save(response)

    return response



# Function to wrap text
def wrap_text(text, max_length):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + 1 <= max_length:
            if current_line:
                current_line += " "
            current_line += word
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return "\n".join(lines)


# Function to create the combined flowchart
def create_combined_flowchart(data):
    # Function to clean and parse JSON data
    def clean_and_parse_json(response_text):
        start = response_text.find('{')
        end = response_text.rfind('}') + 1
        if start == -1 or end == -1:
            raise json.JSONDecodeError("Invalid JSON format", response_text, 0)
        response_text = response_text[start:end]
        return json.loads(response_text)

    # Parse JSON data
    json_data = clean_and_parse_json(data)

    # Filter the data to only include tables with "visualization" in their name
    filtered_data = {k: v for k, v in json_data.items() if "visualization" in k}

    # Create a single Digraph instance
    dot = Digraph()

    # Set global graph attributes for spacing
    dot.attr(rankdir='TB')  # Ensure top-to-bottom direction for entire graph

    # Process each CoreCategory in the filtered tables
    for i, table_data in enumerate(filtered_data["table_format_visualization"]):
        core_category = table_data["CoreCategory"]
        relationships = table_data["Relationships"]

        # Add a subgraph for each CoreCategory to maintain separation
        with dot.subgraph(name=f'cluster_{i}') as sub:
            sub.attr(label=core_category, rank='same', style='invis')
            nodes = set()
            for relation in relationships:
                description = wrap_text(relation["Description"], 40)
                # Create a left-aligned label with HTML-like line breaks
                formatted_description = '<' + description.replace('\n', '<br align="left"/>') + '>'
                sub.edge(relation["From"], relation["To"], label=formatted_description)
                nodes.add(relation["From"])
                nodes.add(relation["To"])

            # Set all nodes to be rectangles
            for node in nodes:
                sub.node(node, shape='rect')

    return dot


# Function to save the flowchart as a PNG file
def save_flowchart_as_png(dot, filename):
    # Render the combined flowchart as a PNG file
    dot.render(filename, format='png', cleanup=True)
    print(f"Combined flowchart image generated and saved as {filename}.png")






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

                time.sleep(1)

                print("Waiting for indexing: ", end='', flush=True)
                for i in range(5, -1, -1):  # Adjusted range to include 0
                    print(f"{i} ", end='', flush=True)  # Print the countdown number with a space
                    time.sleep(1)
                    print('\rWaiting for indexing: ', end='',
                          flush=True)  # Return to the beginning of the line and overwrite
                print("0")
                print("Indexing complete.\n")

                request.session['initialized'] = True
                request.session['vector_store_id'] = resources['vector_store'].id
                request.session['assistant_id'] = resources['assistant'].id
                request.session['file_id'] = resources['file'].id
                request.session['file_name'] = file.name
                request.session['model_choice'] = model_choice  # Ensure model_choice is set here
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


import inspect

import inspect


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
        responses = {}

        for idx, phase in enumerate(phases):
            phase_name = phase.__name__
            phase_params = inspect.signature(phase).parameters

            # Prepare the arguments for the current phase
            args = [request]
            if idx == 0:
                result = phase(*args)
            elif analysis_type == 'content' and phase_name == 'phase5':
                result = phase(request, responses['phase1'])
            elif analysis_type == 'thematic' and phase_name == 'phase5':
                result = phase(request, responses['phase4'])
            elif analysis_type == 'thematic' and phase_name == 'phase6':
                result = phase(request, responses['phase2'])
            elif analysis_type == 'thematic' and phase_name == 'phase7':
                result = phase(request, responses['phase1'])
            else:
                result = phase(*args)

            if isinstance(result, tuple):
                response_json, formatted_prompt = result[0], result[1]
                if len(result) == 4:  # Last phase with different return signature
                    response_json, formatted_prompt, analysis_status, deletion_results = result
            else:
                response_json = result

            responses[phase_name] = response_json
            formatted_prompts.append(formatted_prompt)
            tables = generate_tables_from_response(response_json)
            prompt_table_pairs.append({'prompt': formatted_prompt, 'tables': tables})

        return {
            'prompt_table_pairs': prompt_table_pairs,
            'analysis_status': analysis_status if 'analysis_status' in locals() else "",
            'deletion_results': deletion_results if 'deletion_results' in locals() else ""
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
        'prompt_table_pairs': request.session.get('prompt_table_pairs', []),
        'prompt_table_pairs_json': json.dumps(request.session.get('prompt_table_pairs', []), cls=DjangoJSONEncoder)
    }

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'analyze':
            setup_success = handle_setup(request, setup_form)
            if setup_success:
                context_update = handle_analysis(request, analysis_type)
                context.update(context_update)
                request.session['prompt_table_pairs'] = context.get('prompt_table_pairs', [])
                context['prompt_table_pairs_json'] = json.dumps(
                    context.get('prompt_table_pairs', []), cls=DjangoJSONEncoder
                )
            else:
                context['setup_status'] = request.session.get('setup_status', '')

    return render(request, 'qda_gpt/dashboard.html', context)
# views.py
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from asgiref.sync import sync_to_async
from qda_gpt.prompts.prompts_ca import ca_instruction
from qda_gpt.prompts.prompts_gt import gt_instruction
from qda_gpt.prompts.prompts_ta import ta_instruction
from qda_gpt.analyses import thematic_analysis, content_analysis, grounded_theory
from .openai_api import initialize_openai_resources, create_thread
from .forms import LoginForm, SetupForm
from .__version__ import __version__
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from collections import OrderedDict
from urllib.parse import quote
from openpyxl import Workbook
from graphviz import Digraph
from asgiref.sync import async_to_sync
import asyncio
import pandas as pd
import inspect
import os
import time
import json
import logging


logger = logging.getLogger(__name__)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'registration/login.html', {'error': 'Invalid credentials'})
    return render(request, 'registration/login.html')


def logout_view(request):
    logout(request)
    return render(request, 'registration/logout.html')




def clear_session_data(request):
    session_keys = [
        'response', 'setup_status', 'deletion_results', 'console_output', 'analysis_status',
        'second_response', 'third_response', 'fourth_response', 'fifth_response', 'sixth_response', 'seventh_response',
        'eighth_response', 'analysis_type', 'user_prompt', 'file_name', 'tables', 'prompt_table_pairs', 'flowchart_path'
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
        logger.error(f"JSONDecodeError: {e}\n")
        return []
    except Exception as e:
        logger.error(f"An error occurred: {e}\n")
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

def create_combined_flowchart(data):
    logger.debug(f"[DEBUG] create_combined_flowchart received data: {data}\n")  # Debug print

    # Clean and parse JSON data
    start = data.find('{')
    end = data.rfind('}') + 1
    if start == -1 or end == -1:
        raise json.JSONDecodeError("Invalid JSON format", data, 0)
    data = data[start:end]
    json_data = json.loads(data)

    # Filter the data to only include tables with "visualization" in their name
    filtered_data = {k: v for k, v in json_data.items() if "visualization" in k}
    logger.debug(f"[DEBUG] Filtered data: {filtered_data}\n")  # Debug print

    # Create a single Digraph instance
    dot = Digraph()

    # Set global graph attributes for spacing
    dot.attr(rankdir='TB')  # Ensure top-to-bottom direction for entire graph

    # Process each CoreCategory in the filtered tables
    for i, table_data in enumerate(filtered_data["table_format_visualization"]):
        core_category = table_data["core_category"]
        relationships = table_data["relationships"]

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
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        # Render the combined flowchart as a PNG file
        dot.render(filename, format='png', cleanup=True)
        print(f"[DEBUG] Combined flowchart image generated and saved as {filename}.png\n")  # Debug print
    except Exception as e:
        print(f"[DEBUG] Error saving flowchart as PNG: {e}\n")  # Debug print






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
                request.session['setup_status'] = "OpenAI Assistant initialized successfully. Running analysis. This will take a while."
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


def truncate_message(message, max_length=100):
    return (message[:max_length] + '...') if len(message) > max_length else message

async def run_analysis_async(analysis_data):
    analysis_type = analysis_data['analysis_type']
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
        flowchart_path = None

        for idx, phase in enumerate(phases):
            phase_name = phase.__name__
            logger.debug(f"Running phase: {phase_name}")
            phase_params = inspect.signature(phase).parameters

            # Prepare the arguments for the current phase
            args = [analysis_data]
            if idx == 0:
                result = phase(*args)
            elif analysis_type == 'content' and phase_name == 'phase5':
                result = phase(analysis_data, responses['phase1'])
            elif analysis_type == 'thematic' and phase_name == 'phase5':
                result = phase(analysis_data, responses['phase4'])
            elif analysis_type == 'thematic' and phase_name == 'phase6':
                result = phase(analysis_data, responses['phase2'])
            elif analysis_type == 'thematic' and phase_name == 'phase7':
                result = phase(analysis_data, responses['phase1'])
            else:
                result = phase(*args)

            if isinstance(result, tuple):
                response_json, formatted_prompt = result[0], result[1]
                if len(result) == 4:  # Last phase with different return signature
                    response_json, formatted_prompt, analysis_status, deletion_results = result
            else:
                response_json = result

            if response_json is None:
                logger.error(f"Phase {phase_name} returned None")
                continue

            responses[phase_name] = response_json
            formatted_prompts.append(formatted_prompt)

            logger.debug(f"Latest response after phase {phase_name}: {response_json}")

            tables = generate_tables_from_response(response_json)
            prompt_table_pairs.append({'prompt': formatted_prompt, 'tables': tables})

            if "table_format_visualization" in response_json:
                logger.debug(f"Key 'table_format_visualization' found in response_json")
                try:
                    logger.debug(f"Flowchart recognized\n")
                    flowchart = create_combined_flowchart(response_json)
                    if flowchart:
                        flowchart_path = f"static/flowcharts/flowchart_{int(time.time())}"
                        save_flowchart_as_png(flowchart, flowchart_path)
                        flowchart_path = '/' + flowchart_path + ".png"
                        logger.debug(f"Flowchart path: {flowchart_path}\n")
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse response JSON: {e}\n")
                except Exception as e:
                    logger.error(f"Error generating flowchart: {e}\n")
            else:
                logger.debug(f"Key 'table_format_visualization' not found in response_json\n")

            if flowchart_path:
                logger.debug(f"Flowchart path updated: {flowchart_path}\n")

        analysis_result = {
            'prompt_table_pairs': prompt_table_pairs,
            'flowchart_path': flowchart_path,
            'analysis_status': analysis_status,
            'deletion_results': deletion_results
        }

        # Send the results to the WebSocket consumer
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            "analysis_group",
            {
                "type": "send_analysis_result",
                "content": analysis_result,
            }
        )

        return analysis_result
    logger.debug("Invalid analysis type")
    return {}


@csrf_exempt
async def run_analysis_view(request):
    logger.debug("Attempting to start analysis...")
    analysis_data = {
        'analysis_type': request.POST.get('analysis_type'),
        'user_prompt': request.POST.get('user_prompt'),
        'file_name': request.POST.get('file_name'),
        'assistant_id': request.POST.get('assistant_id'),
        'thread_id': request.POST.get('thread_id'),
        'vector_store_id': request.POST.get('vector_store_id'),
        'file_id': request.POST.get('file_id')  # Ensure file_id is passed here
    }
    logger.debug(f"Analysis data: {analysis_data}")

    channel_layer = get_channel_layer()
    await channel_layer.send("analysis_channel", {
        "type": "run_analysis",
        "analysis_data": analysis_data
    })

    return JsonResponse({"status": "Task dispatched successfully"})


@csrf_exempt
def update_session(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        request.session['prompt_table_pairs'] = data.get('prompt_table_pairs', [])
        request.session['flowchart_path'] = data.get('flowchart_path', '')
        request.session['analysis_status'] = data.get('analysis_status', '')
        request.session['deletion_results'] = data.get('deletion_results', '')

        return JsonResponse({'status': 'Session updated successfully'})
    return JsonResponse({'error': 'Invalid request'}, status=400)



@login_required
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
        'prompt_table_pairs_json': json.dumps(request.session.get('prompt_table_pairs', []), cls=DjangoJSONEncoder),
        'flowchart_path': request.session.get('flowchart_path', '')
    }

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'analyze':
            logger.debug("Analyze action triggered")
            setup_success = handle_setup(request, setup_form)
            if setup_success:
                analysis_data = {
                    'analysis_type': analysis_type,
                    'assistant_id': request.session.get('assistant_id'),
                    'thread_id': request.session.get('thread_id'),
                    'vector_store_id': request.session.get('vector_store_id'),
                    'file_name': request.session.get('file_name'),
                    'user_prompt': request.session.get('user_prompt')
                }
                logger.debug(f"Dispatching analysis task: {analysis_data}")
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.send)("analysis_channel", {
                    "type": "run_analysis",
                    "analysis_data": analysis_data
                })
                context['setup_status'] = "Analysis task dispatched."
                request.session.save()
            else:
                context['setup_status'] = request.session.get('setup_status', '')

    return render(request, 'qda_gpt/dashboard.html', context)


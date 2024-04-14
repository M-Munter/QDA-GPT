# views.py
from django.shortcuts import render
from .forms import SetupForm
from .openai_api import initialize_openai_resources, get_openai_response, delete_openai_resources
import os
import time

def dashboard(request):
    setup_form = SetupForm(request.POST or None, request.FILES or None)

    # Clears data for a session
    if request.method == 'GET':
        # Clear session data when the page is refreshed or visited.
        request.session.pop('response', None)
        request.session.pop('response_message', None)
        request.session.pop('deletion_results', None)
        request.session.pop('console_output', None)


    # Initialize context with empty strings or values from the session.
    context = {
        'setup_form': setup_form,
        'response': request.session.get('response', ''),
        'response_message': request.session.get('response_message', ''),
        'console_output': request.session.get('console_output', ''),
        'deletion_results': request.session.get('deletion_results', '')
    }

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'setup':
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
                    context['response_message'] = "OpenAI initialized successfully."
                except Exception as e:
                    context['response_message'] = str(e)
                    request.session['initialized'] = False

        elif action == 'analyze':
            user_prompt = request.POST.get('user_prompt', '')
            if request.session.get('initialized', False) and user_prompt:
                try:
                    context['response'] = get_openai_response(
                        user_prompt,
                        request.session['assistant_id'],
                        request.session['thread_id']
                    )

                    time.sleep(1)
                    # Call delete_openai_resources after obtaining the response
                    deletion_results = delete_openai_resources(
                        request.session['assistant_id'],
                        request.session.get('file_id', ''),
                        request.session['thread_id']
                    )

                    # Construct detailed and clear deletion message
                    deletion_message_parts = []
                    assistant_deletion = deletion_results.get('assistant')
                    file_deletion = deletion_results.get('file')
                    thread_deletion = deletion_results.get('thread')

                    if assistant_deletion.deleted:
                        deletion_message_parts.append("Assistant Deletion: Successful.")
                    else:
                        deletion_message_parts.append("Assistant Deletion: Failed or no data.")

                    if file_deletion.deleted:
                        deletion_message_parts.append("File Deletion: Successful.")
                    else:
                        deletion_message_parts.append("File Deletion: Failed or no data.")

                    if thread_deletion.deleted:
                        deletion_message_parts.append("Thread Deletion: Successful.")
                    else:
                        deletion_message_parts.append("Thread Deletion: Failed or no data.")

                    deletion_message = ", ".join(deletion_message_parts)

                    context['response_message'] = "Analysis completed successfully."
                    context['deletion_results'] = deletion_message
                except Exception as e:
                    context['response_message'] = f"An error occurred: {str(e)}"

                # Print the context here to see what is being passed to the template
                print(context)

            # Save the context to the session
            request.session['response'] = context['response']
            request.session['response_message'] = context['response_message']
            request.session['console_output'] = context['console_output']
            request.session['deletion_results'] = context['deletion_results']

    return render(request, 'qda_gpt/dashboard.html', context)

def handle_uploaded_file(f):
    file_path = os.path.join('uploads', f.name)
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return file_path

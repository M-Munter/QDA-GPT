from celery import shared_task
from .openai_api import get_openai_response

@shared_task
def run_analysis_task(formatted_prompt, assistant_id, thread_id):
    return get_openai_response(formatted_prompt, assistant_id, thread_id)

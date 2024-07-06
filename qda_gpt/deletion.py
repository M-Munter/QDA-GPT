# deletion.py
from .openai_api import delete_openai_resources

def handle_deletion(request):
    assistant_id = request.session.get('assistant_id')
    file_id = request.session.get('file_id')
    thread_id = request.session.get('thread_id')
    vector_store_id = request.session.get('vector_store_id')

    if assistant_id and file_id and thread_id and vector_store_id:
        try:
            deletion_results = delete_openai_resources(assistant_id, file_id, thread_id, vector_store_id)
            request.session['deletion_results'] = deletion_results

            all_deleted = all(result['deleted'] for result in deletion_results.values())
            deletion_message = "All OpenAI elements deleted successfully." if all_deleted else "Not all OpenAI elements were deleted successfully."
            print(deletion_message)
            return deletion_message
        except Exception as e:
            return f"Deletion failed: {str(e)}"
    else:
        return "No resources to delete."

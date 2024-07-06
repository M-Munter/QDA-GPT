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

            deletion_message_parts = []
            all_deleted = True
            #assistant_deletion = deletion_results.get('assistant', {})         tämän voi poistaa
            #file_deletion = deletion_results.get('file', {})                   tämän voi poistaa
            #thread_deletion = deletion_results.get('thread', {})               tämän voi poistaa
            #vector_store_deletion = deletion_results.get('vector_store', {})   tämän voi poistaa

            if not deletion_results['assistant'].deleted:
                all_deleted = False

            if not deletion_results['file'].deleted:
                all_deleted = False

            if not deletion_results['thread'].deleted:
                all_deleted = False

            if not deletion_results['vector_store'].deleted:
                all_deleted = False

            if all_deleted:
                deletion_message = "All OpenAI elements deleted successfully."
            else:
                deletion_message = "Not all OpenAI elements were deleted successfully."

            print(deletion_message)
            return deletion_message

        except Exception as e:
            return f"Deletion failed: {str(e)}"
    else:
        return "No resources to delete."
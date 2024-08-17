# deletion.py
#
# This script handles the deletion of resources associated with an OpenAi Assistant session.
# The script returns a message indicating the success or failure of the deletion process.

from .openai_api import delete_openai_resources  # Import the function to delete OpenAI resources

def handle_deletion(request_data):
    # Extract relevant IDs from the session data
    assistant_id = request_data['session'].get('assistant_id')
    file_id = request_data['session'].get('file_id')
    thread_id = request_data['session'].get('thread_id')
    vector_store_id = request_data['session'].get('vector_store_id')

    # Check if all necessary IDs are available
    if assistant_id and file_id and thread_id and vector_store_id:
        try:
            # Attempt to delete the resources using the delete_openai_resources function
            deletion_results = delete_openai_resources(assistant_id, thread_id, vector_store_id, file_id)
            request_data['session']['deletion_results'] = deletion_results

            try:
                # Check if all resources were successfully deleted
                all_deleted = all(result['deleted'] for result in deletion_results.values())
                deletion_message = "Deletion successful"
                return deletion_message
            except Exception as e:
                # Handle any errors during the deletion check
                return f"Deletion failed: {str(e)}"
        except Exception as e:
            # Handle any errors during the deletion process
            return f"Deletion failed: {str(e)}"
    else:
        return "No resources to delete."

import openai
import os
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()

    # Initialize the OpenAI client with your API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("API key not found. Please check your .env file.")
    client = openai.OpenAI(api_key=api_key)

    # Set the file path and ensure it uses an appropriate string literal for paths
    file_path = r"C:\Users\MM\1 Master's Thesis\Testiaineistoa\Interviews.txt"

    try:
        # Upload the file
        with open(file_path, 'rb') as file:
            file_response = client.files.create(file=file, purpose='assistants')
            file_id = file_response['id']
            print(f"File uploaded with ID: {file_id}")

        # Create an assistant with the uploaded file
        assistant = client.beta.assistants.create(
            name="Document Summarizer",
            instructions="Summarize the key topics from the document.",
            model="gpt-4-turbo",
            tools=[{"type": "retrieval"}],
            file_ids=[file_id]
        )
        assistant_id = assistant['id']
        print(f"Assistant created with ID: {assistant_id}")

        # Create a thread for interaction
        thread = client.beta.threads.create(assistant_id=assistant_id)
        thread_id = thread['id']
        print(f"Thread created with ID: {thread_id}")

        # Add a message to the thread
        message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content="Please summarize the key topics from the uploaded document."
        )
        print("Message sent.")

        # Retrieve and print response
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )
        print(f"Run initiated. Status: {run['status']}")

        # Stream the results
        with client.beta.threads.runs.stream(thread_id=thread_id, assistant_id=assistant_id) as stream:
            for event in stream:
                if 'output' in event:
                    print(event['output'])

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    main()

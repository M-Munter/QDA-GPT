import openai
import os
from dotenv import load_dotenv

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Retrieve the API key from environment variables
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("API key not found. Please check your .env file.")

    # Initialize the OpenAI client
    client = openai.OpenAI(api_key=api_key)

    # Set the file path correctly with raw string notation
    file_path = r"C:\Users\MM\1 Master's Thesis\Testiaineistoa\Interviews.txt"

    try:
        # Open the file and upload it to OpenAI
        with open(file_path, 'rb') as file:
            openai_file = client.files.create(file=file, purpose='assistants')

        # Create an assistant with the uploaded file
        assistant = client.beta.assistants.create(
            instructions="Please provide a summary of the key topics discussed in this document.",
            model="gpt-3.5-turbo",
            tools=[{"type": "retrieval"}],
            file_ids=[openai_file.id]
        )

        # Create a thread and send a prompt to summarize the document
        thread = client.beta.threads.create()  # removed assistant_id
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content="Summarize the key topics from the uploaded document.",
            file_ids=[openai_file.id]
        )

        # Debugging response structure
        print("Response from OpenAI:")
        if hasattr(message, 'content_blocks'):
            for block in message.content_blocks:
                if hasattr(block, 'text'):
                    print(block.text.value)
                else:
                    print(f"Block without text: {block}")
        else:
            print("No content_blocks found in the message. Check the assistant's settings and the request sent.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    main()

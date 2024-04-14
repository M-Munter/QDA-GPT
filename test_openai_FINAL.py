import openai
from dotenv import load_dotenv
import os
import sys  # Import sys to use sys.stdout for printing without new lines
import time

# Load environment variables from .env file
load_dotenv()

# Retrieve the OPENAI_API_KEY environment variable.
api_key = os.getenv('OPENAI_API_KEY')

if api_key:
    # Set the OpenAI API key if it was successfully retrieved.
    openai.api_key = api_key
    print("OpenAI API key loaded successfully.")
else:
    # Inform the user if the OPENAI_API_KEY was not found.
    print("Failed to load the OpenAI API key. Please check your .env file.")

client = openai.OpenAI(api_key=openai.api_key)


my_files = client.files.create(
  file=open("data/Interviews.txt", "rb"),
  purpose="assistants"
)

print(f"File ID: {my_files.id} \n")


# Step 1: Create an Assistant
my_assistant = client.beta.assistants.create(
    model="gpt-3.5-turbo",
    instructions="You are a qualitative data analyst. Answer questions regarding the attached content.",
    name="QDA Bot",
    tools=[{"type": "retrieval"}],
    file_ids=[my_files.id]
)
print(f"This is the assistant object: {my_assistant} \n")

# Step 2: Create a Thread
my_thread = client.beta.threads.create()
print(f"This is the thread object: {my_thread} \n")

# Step 3: Add a Message to a Thread
my_thread_message = client.beta.threads.messages.create(
  thread_id=my_thread.id,
  role="user",
  content="Can you provide thematic analysis for the attached document containing interviews?",
)
print(f"This is the message object: {my_thread_message} \n")

# Step 4: Run the Assistant
my_run = client.beta.threads.runs.create(
  thread_id=my_thread.id,
  assistant_id=my_assistant.id,
  instructions="Please address the user as my Lord."
)
print(f"This is the run object: {my_run} \n")



# Step 5: Periodically retrieve the Run to check on its status to see if it has moved to completed
print("Run status: in_progress", end="")
sys.stdout.flush()  # Ensure "in_progress" is displayed immediately

while my_run.status in ["queued", "in_progress"]:
    keep_retrieving_run = client.beta.threads.runs.retrieve(
        thread_id=my_thread.id,
        run_id=my_run.id
    )

    if keep_retrieving_run.status == "in_progress":
        print(".", end="")
        sys.stdout.flush()  # Print each dot immediately
        time.sleep(0.57)
    elif keep_retrieving_run.status == "completed":
        print("\nRun status: completed\n")

        # Step 6: Retrieve the Messages added by the Assistant to the Thread
        all_messages = client.beta.threads.messages.list(
            thread_id=my_thread.id
        )

        print("------------------------------------------------------------ \n")

        print(f"User: {my_thread_message.content[0].text.value}")
        print(f"Assistant: {all_messages.data[0].content[0].text.value}")

        break
    else:
        print(f"\nRun status: {keep_retrieving_run.status}")
        break
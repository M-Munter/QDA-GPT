import openai
import os
from dotenv import load_dotenv
from openai import OpenAI
client = OpenAI()

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("API key not found. Please check your .env file.")
    client = openai.OpenAI(api_key=api_key)
    print(f"API key ok")



my_assistant = client.beta.assistants.create(
    instructions="You are aqualitative data analyst. When asked a question, write key topics discussed in this document.",
    name="QDA",
    tools=[{"type": "retrieval"}],
    model="gpt-4",
)
print(my_assistant)



assistant_file = client.beta.assistants.files.create(
  assistant_id="asst_abc123",
  file_id="file-abc123"
)

print(assistant_file)



my_assistants = client.beta.assistants.list(
    order="desc",
    limit="20",
)
print(my_assistants.data)




assistant_files = client.beta.assistants.files.list(
  assistant_id="asst_abc123"
)
print(assistant_files)


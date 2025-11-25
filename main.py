import os
import sys
from dotenv import load_dotenv
from google import genai

if len(sys.argv) < 2:
    print("Please provide a prompt")
    sys.exit(1)

prompt = sys.argv[1]

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

response =client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=prompt
)
print(response.text)

metadata = response.usage_metadata
print(f"Prompt tokens: {metadata.prompt_token_count}")
print(f"Response tokens: {metadata.candidates_token_count}")

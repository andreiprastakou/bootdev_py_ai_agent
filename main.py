import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.index import available_functions

if len(sys.argv) < 2:
    print("Please provide a prompt")
    sys.exit(1)

prompt = sys.argv[1]
verbose = "--verbose" in sys.argv

if verbose:
    print(f"User prompt: {prompt}")

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

system_prompt = """
You are a helpful AI coding agent.
When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
- List files and directories
All paths you provide should be relative to the working directory. Do not specify the working directory in your function calls as it is automatically injected for security reasons.
"""

messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
]
response =client.models.generate_content(
    model="gemini-2.0-flash-001",
    config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[available_functions]),
    contents=messages
)
if response.function_calls != None:
    for function_call in response.function_calls:
        print(f"Calling function: {function_call.name}({function_call.args})")
else:
    print(response.text)

metadata = response.usage_metadata
if verbose:
    print(f"Prompt tokens: {metadata.prompt_token_count}")
    print(f"Response tokens: {metadata.candidates_token_count}")

import os
import sys
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.index import available_functions
from call_function import call_function

if len(sys.argv) < 2:
    print("Please provide a prompt")
    sys.exit(1)

prompt = sys.argv[1]
verbose = "--verbose" in sys.argv

if verbose:
    print(f"User prompt: {prompt}")

load_dotenv()
API_KEY = os.environ.get("GEMINI_API_KEY")
DIALOGUE_LIMIT = os.environ.get("DIALOGUE_LIMIT", 20)
LLM_MODEL = os.environ.get("LLM_MODEL", "gemini-2.0-flash-001")

client = genai.Client(api_key=API_KEY)

SYSTEM_PROMPT = """
You are a helpful AI coding agent.
When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files
All paths you provide should be relative to the working directory. Do not specify the working directory in your function calls as it is automatically injected for security reasons.
"""

messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
]

i = 0
while i < DIALOGUE_LIMIT:
    i += 1

    response = client.models.generate_content(
        model=LLM_MODEL,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, tools=[available_functions]),
        contents=messages
    )

    # print usage metadata
    if verbose:
        metadata = response.usage_metadata
        print(f"Prompt tokens: {metadata.prompt_token_count}")
        print(f"Response tokens: {metadata.candidates_token_count}")

    # register all candidates
    for candidate in response.candidates:
        messages.append(candidate.content)

    if response.function_calls != None:
        # call functions
        function_results = []
        for function_call in response.function_calls:
            call_result = call_function(function_call, verbose=verbose)
            text_result = call_result.parts[0].function_response.response
            if text_result is None: raise Exception(f"Error calling function: {function_call.name}")
            if verbose: print(f"-> {text_result}")
            function_results.append(text_result)

        results_message = types.Content(role="user", parts=[types.Part(text=json.dumps(function_results))])
        messages.append(results_message)
    else:
        # end of conversation
        print(response.text)
        break

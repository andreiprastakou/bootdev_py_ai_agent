from google.genai import types

from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file
from functions.run_python_file import run_python_file

working_directory = "./calculator"

supported_functions = {
    "get_file_content": lambda args: get_file_content(working_directory, **args),
    "get_files_info": lambda args: get_files_info(working_directory, **args),
    "write_file": lambda args: write_file(working_directory, **args),
    "run_python_file": lambda args: run_python_file(working_directory, **args),
}

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f" - Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f"Calling function: {function_call_part.name}")

    if function_call_part.name not in supported_functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

    function_result = _call_function(function_call_part.name, function_call_part.args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result},
            )
        ],
    )

def _call_function(function_name, args):
    return supported_functions[function_name](args)

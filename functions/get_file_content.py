import os
from google.genai import types

from functions.config import MAX_FILE_CONTENT_LENGTH

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the content of a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to get the content of, relative to the working directory.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    try:
        resolved_path = _validate_readable_file(working_directory, file_path)

        content = None
        with open(resolved_path, "r") as file:
            content = file.read(MAX_FILE_CONTENT_LENGTH + 1)

        if len(content) > MAX_FILE_CONTENT_LENGTH:
            return content + f"[...File \"{file_path}\" truncated at {MAX_FILE_CONTENT_LENGTH} characters]"

        return content
    except Exception as e:
        return f"Error: {e}"

def _validate_readable_file(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    resolved_path = os.path.realpath(full_path)
    resolved_working_directory = os.path.realpath(working_directory)

    if os.path.commonpath([resolved_path, resolved_working_directory]) != resolved_working_directory:
      raise Exception(f'Cannot read "{file_path}" as it is outside the permitted working directory.')

    if not os.path.exists(resolved_path):
      raise Exception(f"File not found or is not a regular file: {file_path}.")

    if not os.path.isfile(resolved_path):
      raise Exception(f"File not found or is not a regular file: {file_path}.")

    return resolved_path

import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    try:
        resolved_path = _validate_nested_directory(working_directory, directory)
    except Exception as e:
        return f"Error: {e}"

    files = os.listdir(resolved_path)
    formatted_files = []
    for file in files:
        file_path = os.path.join(resolved_path, file)
        size = os.path.getsize(file_path)
        isDir = os.path.isdir(file_path)
        formatted_files.append(f" - {file}: file_size={size} bytes, is_dir={isDir}")
    return "\n".join(formatted_files)

def _validate_nested_directory(working_directory, directory):
    full_path = os.path.join(working_directory, directory)
    resolved_path = os.path.realpath(full_path)
    resolved_working_directory = os.path.realpath(working_directory)

    if os.path.commonpath([resolved_path, resolved_working_directory]) != resolved_working_directory:
      raise Exception(f'Cannot list "{directory}" as it is outside the permitted working directory.')

    if not os.path.exists(resolved_path): raise Exception(f"{directory} does not exist.")

    if not os.path.isdir(resolved_path): raise Exception(f"{directory} is not a directory.")

    return resolved_path

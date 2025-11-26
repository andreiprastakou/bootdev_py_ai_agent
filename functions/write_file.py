import os

def write_file(working_directory, file_path, content):
    try:
        resolved_path = _validate_target_path(working_directory, file_path)

        with open(resolved_path, "w") as file:
            file.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"

def _validate_target_path(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    resolved_path = os.path.realpath(full_path)
    resolved_working_directory = os.path.realpath(working_directory)

    if os.path.commonpath([resolved_path, resolved_working_directory]) != resolved_working_directory:
      raise Exception(f'Cannot read "{file_path}" as it is outside the permitted working directory.')

    return resolved_path

import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
  try:
    resolved_path = _validate_python_file(working_directory, file_path)
    return _run_python_file(resolved_path, args)
  except Exception as e:
    return f"Error: {e}"

def _run_python_file(resolved_path, args=[]):
  try:
    run_result = subprocess.run(["python", resolved_path] + args, check=True, capture_output=True)
    status = f"STDOUT: {run_result.stdout}\nSTDERR: {run_result.stderr}"
    if (run_result.returncode != 0):
      status += f"\nProcess exited with code {run_result.returncode}"
    if (run_result.stdout is None and run_result.stderr is None):
      status += f"\nNo output produced."
    return status
  except Exception as e:
    return f"Error: Executing Python file: {e}"

def _validate_python_file(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    resolved_path = os.path.realpath(full_path)
    resolved_working_directory = os.path.realpath(working_directory)

    if os.path.commonpath([resolved_path, resolved_working_directory]) != resolved_working_directory:
      raise Exception(f'Cannot execute "{file_path}" as it is outside the permitted working directory.')

    if not file_path.endswith(".py"):
      raise Exception(f"File \"{file_path}\" is not a Python file.")

    if not os.path.exists(resolved_path):
      raise Exception(f"File \"{file_path}\" not found.")

    return resolved_path

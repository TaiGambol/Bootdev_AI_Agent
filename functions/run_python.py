import os
import subprocess
from google import genai
from google.genai import types
from .limit_test import limit_test

def run_python_file(working_directory, file_path, args=[]):
    root_path = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))

    try:
        limit_test(working_directory, file_path)
    except Exception as e:
        return f'Error: {str(e)}'

    if not os.path.isfile(full_path):
        return f'Error: File "{file_path}" not found.'
    
    if not full_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        process = subprocess.run(
            ["python", file_path] + args, 
            cwd=working_directory,
            capture_output=True, 
            timeout=30, 
        )
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
    output = ""
    if not process.stdout and not process.stderr:
        output = "No output produced"
    elif process.stdout:
        if process.stderr:
            output += "STDOUT: " + str(process.stdout) + "\nSTDERR: " + str(process.stderr)
        else:
            output += "STDOUT: " + str(process.stdout)
    elif process.stderr:
        output += "STDERR: " + str(process.stderr)
    
    if process.returncode != 0:
        output += "\nProcess exited with code " + str(process.returncode)
    
#    output = "STDOUT: " + str(process.stdout) + "\nSTDERR: " + str(process.stderr) + "\n"
    return output


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the specified Python file, with optional arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to run.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="Arguments to run the file with. Optional.",
            ),
        },
    ),
)
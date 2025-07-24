import os
import sys
from google import genai
from google.genai import types

def get_files_info(working_directory, directory="."):
    root_path = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, directory))

    if not full_path.startswith(root_path):
        return f'Error: cannot list "{directory}" as it is outside the permitted working directory'

    message = ""
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'

    try:
        for file in os.listdir(full_path):
            file_path = os.path.join(full_path, file)

            if len(message)>3:
                message += "\n- " + file + ":"
            else:
                message += "- " + file + ":"
            message += " file_size=" + str(os.path.getsize(os.path.abspath(file_path))) + " bytes, "
            message += "is_dir=" + str(os.path.isdir(os.path.abspath(file_path)))
    except Exception as e:
        return f'Error: {str(e)}'

    return message


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
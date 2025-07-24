import os
import sys
from .config import MAX_CHARS
from google import genai
from google.genai import types

def get_file_content(working_directory, file_path):
    root_path = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not full_path.startswith(root_path):
        return f'Error: cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"' 

    try:
        with open(full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS+1)
            if len(file_content_string) > MAX_CHARS:
                file_content_string = file_content_string[:MAX_CHARS] + f'[...File "{file_path} truncated at {MAX_CHARS} characters]'
    except Exception as e:
        return f'Error: {str(e)}'
    return file_content_string


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Shows the content of the specified file, truncated to a set limit of characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to display content from.",
            ),
        },
    ),
)
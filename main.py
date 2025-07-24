import os
import sys
from dotenv import load_dotenv
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function


system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
You MUST use your available tools to explore the codebase - never ask the user for file paths or more information unless you've already used get_files_info to discover files and get_file_content to read them first.
"""

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from google import genai
from google.genai import types
client = genai.Client(api_key=api_key)

if not len(sys.argv) > 1:
    print(f"Error: no arguments supplied")
    exit(code=1)
user_prompt = sys.argv[1]
verbose = "--verbose" in sys.argv

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)])
]

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_write_file,
        schema_run_python_file,
        schema_get_file_content,
    ]
)


for i in range(20):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-001", 
            contents=messages,

            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt, temperature = 0.0
                )
            )

        for candidate in response.candidates:
            messages.append(candidate.content)

        if response.function_calls:
            for function_call_part in response.function_calls:
                function_call_result = call_function(function_call_part, verbose=verbose)

                if not function_call_result.parts[0].function_response.response:
                    raise Exception("Function call failed")
                
                new_message = types.Content(role="tool", parts=function_call_result.parts)
                #print(new_message)
                messages.append(new_message)

                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
        else:
            print(response.text)
            break
    except Exception as e:
        print(f'Error: {str(e)}')

#for message in messages:
#    print(message)

if verbose:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


def main():
    pass


if __name__ == "__main__":
    main()

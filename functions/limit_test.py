import os

def limit_test(working_directory, testpath):
    root_path = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, testpath))

    if not full_path.startswith(root_path):
        raise Exception(f'File Permissions: Cannot execute "{testpath}" as it is outside the permitted working directory')
    pass
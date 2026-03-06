import os

def write_file(working_directory, file_path, content):
    absolute_path = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(absolute_path, file_path))
    valid_target_file = os.path.commonpath([absolute_path, target_file_path]) == absolute_path
    if not valid_target_file:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    # disallow writing to an existing directory
    if os.path.isdir(target_file_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    try:
        # ensure parent directories exist
        parent = os.path.dirname(target_file_path)
        if parent and not os.path.exists(parent):
            os.makedirs(parent, exist_ok=True)
        with open(target_file_path, "w") as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"
import os
import config

def get_file_content(working_directory, file_path):
    absolute_path = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(absolute_path, file_path))
    valid_target_file = os.path.commonpath([absolute_path, target_file_path]) == absolute_path
    if not valid_target_file:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(target_file_path, "r") as file:
            content = file.read(config.MAX_CHARS)
            if os.path.getsize(target_file_path) > config.MAX_CHARS:
                content += f'\n[...File "{file_path}" truncated to {config.MAX_CHARS} characters]'
            return content
    except Exception as e:
        return f"Error: {e}"
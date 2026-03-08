import os
import call_function
from google.genai import types #type: ignore

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Get a list of files in a directory with their size and type information",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. Default is '.'"
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    try:
        absolute_path = os.path.abspath(working_directory)
        target_directory = os.path.normpath(os.path.join(absolute_path, directory))

        valid_target_dir = os.path.commonpath([absolute_path, target_directory]) == absolute_path
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_directory):
            return f'Error: "{directory}" is not a directory'
        
        files = os.listdir(target_directory)
        files_info = []
        for file in files:
            file_path = os.path.join(target_directory, file)
            # determine if it's a directory or file and gather size
            is_dir = os.path.isdir(file_path)
            try:
                size = os.path.getsize(file_path)
            except OSError:
                size = 0
            files_info.append(
                f"- {file} : file_size={size} bytes, is_dir={is_dir}"
            )
        return files_info
    except Exception as e:
        return f"Error: {e}"
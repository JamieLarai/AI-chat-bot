import os
import subprocess
def run_python_file(working_directory, file_path, args=None):
    try:
        absolute_path = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(absolute_path, file_path))
        valid_target_file = os.path.commonpath([absolute_path, target_file_path]) == absolute_path
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file_path]
        if args:
            command.extend(args)
        
        result = subprocess.run(command, cwd=absolute_path, capture_output=True, text=True, timeout=30)
        
        output = ""
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}\n"
        if not result.stdout and not result.stderr:
            output += "No output produced"
        else:
            if result.stdout:
                output += f"STDOUT:\n{result.stdout}\n"
            if result.stderr:
                output += f"STDERR:\n{result.stderr}\n"
        
        return output.strip()
    except Exception as e:
        return f"Error: executing Python file: {e}"
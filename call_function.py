from google.genai import types #type: ignore
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file

available_functions = types.Tool(function_declarations=[schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file])

function_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

def call_function(function_call, verbose=False):
    """Execute a function based on a FunctionCall object.

    Parameters
    ----------
    function_call : types.FunctionCall
        Object containing the function name and arguments.
    verbose : bool, optional
        If True, prints detailed information about the invocation.

    Returns
    -------
    types.Content
        A Content object wrapping the function result or an error message.
    """
    # ensure we have a string even if function_call.name is None
    function_name = function_call.name or ""

    if verbose:
        print(f"Calling function: {function_name}({function_call.args})")
    else:
        print(f" - Calling function: {function_name}")

    # copy arguments so we can mutate safely
    args = dict(function_call.args) if function_call.args else {}
    # enforce working directory as instructed
    args["working_directory"] = "./calculator"

    func = function_map.get(function_name)
    if not func:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    # call the function with our prepared args
    try:
        function_result = func(**args)
    except Exception as e:
        # guard in case the underlying function raises
        function_result = f"Error executing {function_name}: {e}"

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
import os
import argparse
import prompts
import call_function
from dotenv import load_dotenv #type: ignore
from google import genai #type: ignore
from google.genai import types #type: ignore

def main():
    load_dotenv()
    model_name = "gemini-2.5-flash"
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("The API key is missing")
    
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="The prompt to send to the chatbot")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    available_functions = call_function.available_functions
    function_map = call_function.function_map
    
    client = genai.Client(api_key=api_key)
    
    while True:
        object = client.models.generate_content(
             model=model_name, contents=messages,
             config=types.GenerateContentConfig(tools=[available_functions], system_instruction=prompts.system_prompt, temperature=0, seed=42))
        
        if object.usage_metadata != None and args.verbose:
                print(f"User prompt: {args.user_prompt}")  
                print(f"Prompt tokens: {object.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {object.usage_metadata.candidates_token_count}")
        
        if object.function_calls:
            for function_call in object.function_calls:
                print(f"Calling function: {function_call.name}({function_call.args})")
                func = function_map.get(function_call.name)
                if func:
                    # Assuming the function takes working_directory as first arg, and then the args
                    working_directory = "/home/jamielarai/workspace/bootdotdev"  # workspace root
                    result = func(working_directory, **function_call.args)
                    # Add the tool response to messages
                    messages.append(types.Content(
                        role="user",
                        parts=[types.Part(text=str(result))]
                    ))
                else:
                    print(f"Function {function_call.name} not found")
        else:
            print(object.text)
            break

if __name__ == "__main__":
    main()
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
    
    final_response = False
    for _ in range(20):
        object = client.models.generate_content(
             model=model_name, contents=messages,
             config=types.GenerateContentConfig(tools=[available_functions], system_instruction=prompts.system_prompt, temperature=0, seed=42))
        
        # Append all candidates to the conversation history
        for candidate in object.candidates:
            messages.append(candidate.content)
        
        if object.usage_metadata != None and args.verbose:
                print(f"User prompt: {args.user_prompt}")  
                print(f"Prompt tokens: {object.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {object.usage_metadata.candidates_token_count}")
        
        if object.function_calls:
            function_results = []
            for function_call in object.function_calls:
                function_call_result = call_function.call_function(function_call, verbose=args.verbose)
                if not function_call_result.parts:
                    raise Exception("No parts in function call result")
                part = function_call_result.parts[0]
                if part.function_response is None:
                    raise Exception("No function_response in part")
                if part.function_response.response is None:
                    raise Exception("No response in function_response")
                function_results.append(part)
                if args.verbose:
                    print(f"-> {part.function_response.response}")
            if function_results:
                messages.append(types.Content(role="user", parts=function_results))
        else:
            print(object.text)
            final_response = True
            break
    
    if not final_response:
        print("Maximum iterations reached without a final response. The agent may be stuck.")
        exit(1)

if __name__ == "__main__":
    main()
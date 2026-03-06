import os
import argparse
from dotenv import load_dotenv #type: ignore
from google import genai #type: ignore
from google.genai import types #type: ignore

def main():
    print("Hello from ai-chat-bot!")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("The API key is missing")
    
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="The prompt to send to the chatbot")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    
    client = genai.Client(api_key=api_key)
    object = client.models.generate_content(model="gemini-2.5-flash", contents=messages)

    if object.usage_metadata != None and args.verbose:
            print(f"User prompt: {args.user_prompt}")  
            print(f"Prompt tokens: {object.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {object.usage_metadata.candidates_token_count}")

    print(object.text)

if __name__ == "__main__":
    main()
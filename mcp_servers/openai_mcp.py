from fastapi import APIRouter, Query
import requests
import json

router = APIRouter()

def fetch_openai_docs(function_name):
    # Extract the specific function we're looking for
    # For example, from "openai.ChatCompletion.create" extract "ChatCompletion.create"
    if function_name.startswith("openai."):
        function_name = function_name[7:]  # Remove "openai." prefix
    
    # Mock documentation for different OpenAI functions
    mock_docs = {
        "ChatCompletion.create": """
        # ChatCompletion.create
        
        Creates a chat completion for the provided messages.
        
        ## Parameters:
        - model (string): Required. The model to use for chat completion.
        - messages (array): Required. An array of message objects representing the conversation so far.
        - temperature (number): Optional. Controls randomness. Higher values like 0.8 make output more random, while lower values like 0.2 make it more focused.
        - max_tokens (integer): Optional. The maximum number of tokens to generate in the chat completion.
        
        ## Example:
        ```python
        import openai
        
        response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"}
          ]
        )
        ```
        """,
        "Completion.create": """
        # Completion.create
        
        Creates a completion for the provided prompt.
        
        ## Parameters:
        - model (string): Required. The model to use for the completion.
        - prompt (string): Optional. The prompt to complete from.
        - temperature (number): Optional. Controls randomness. Higher values like 0.8 make output more random, while lower values like 0.2 make it more focused.
        - max_tokens (integer): Optional. The maximum number of tokens to generate in the completion.
        
        ## Example:
        ```python
        import openai
        
        response = openai.Completion.create(
          model="text-davinci-003",
          prompt="Once upon a time",
          max_tokens=50
        )
        ```
        """
    }
    
    # If function is in our mock data, return it
    for key in mock_docs:
        if key.lower() in function_name.lower():
            return mock_docs[key]
    
    # Default fallback
    return f"Documentation for {function_name} not found. Please check the OpenAI API reference at https://platform.openai.com/docs/api-reference"

@router.get("/openai/context")
async def openai_mcp_context(
    language: str = Query(...),
    function: str = Query(...)
):
    doc_snippet = fetch_openai_docs(function)
    
    return {
        "context": {
            "language": language,
            "library": "openai",
            "function": function,
            "documentation": doc_snippet
        }
    } 
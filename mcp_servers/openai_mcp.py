from fastapi import APIRouter, Query
import requests

router = APIRouter()

def fetch_openai_docs():
    url = "https://platform.openai.com/docs/api-reference"
    response = requests.get(url)
    return response.text if response.status_code == 200 else "Error fetching OpenAI docs"

@router.get("/openai/context")
async def openai_mcp_context(
    language: str = Query(...),
    function: str = Query(...)
):
    doc_snippet = fetch_openai_docs()
    
    return {
        "context": {
            "language": language,
            "library": "openai",
            "function": function,
            "documentation": doc_snippet
        }
    } 
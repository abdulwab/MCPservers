from fastapi import APIRouter, Query
import requests

router = APIRouter()

def fetch_firebase_docs():
    url = "https://firebase.google.com/docs/reference"
    response = requests.get(url)
    return response.text if response.status_code == 200 else "Error fetching Firebase docs"

@router.get("/firebase/context")
async def firebase_mcp_context(
    language: str = Query(...),
    function: str = Query(...)
):
    doc_snippet = fetch_firebase_docs()
    
    return {
        "context": {
            "language": language,
            "library": "firebase",
            "function": function,
            "documentation": doc_snippet
        }
    } 
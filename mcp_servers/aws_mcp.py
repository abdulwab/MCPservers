from fastapi import APIRouter, Query
import requests

router = APIRouter()

def fetch_aws_docs():
    url = "https://docs.aws.amazon.com/sdk-for-python/latest/reference/"
    response = requests.get(url)
    return response.text if response.status_code == 200 else "Error fetching AWS docs"

@router.get("/aws/context")
async def aws_mcp_context(
    language: str = Query(...),
    function: str = Query(...)
):
    doc_snippet = fetch_aws_docs()
    
    return {
        "context": {
            "language": language,
            "library": "aws",
            "function": function,
            "documentation": doc_snippet
        }
    } 
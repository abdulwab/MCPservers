from fastapi import APIRouter, Query
import requests
import json

router = APIRouter()

def fetch_aws_docs(function_name):
    # Extract specific function if format like "boto3.client"
    if function_name.startswith("boto3."):
        function_name = function_name[6:]  # Remove "boto3." prefix
    elif function_name.startswith("aws."):
        function_name = function_name[4:]  # Remove "aws." prefix
    
    # Mock documentation for different AWS functions
    mock_docs = {
        "client": """
        # boto3.client
        
        Creates a low-level service client by name.
        
        ## Parameters:
        - service_name (string): Required. The name of the service, e.g., 's3', 'ec2', etc.
        - region_name (string): Optional. The name of the region associated with the client.
        - api_version (string): Optional. The API version to use. By default, the latest API version is used.
        - use_ssl (boolean): Optional. Whether or not to use SSL. By default, SSL is used.
        - verify (boolean/string): Optional. Whether or not to verify SSL certificates.
        - endpoint_url (string): Optional. The complete URL to use for the constructed client.
        - aws_access_key_id (string): Optional. The access key to use when creating the client.
        - aws_secret_access_key (string): Optional. The secret key to use when creating the client.
        - aws_session_token (string): Optional. The session token to use when creating the client.
        
        ## Returns:
        - Client: A low-level service client instance
        
        ## Example:
        ```python
        import boto3
        
        # Create an S3 client
        s3 = boto3.client('s3')
        
        # Upload a file to S3
        s3.upload_file('file.txt', 'mybucket', 'file.txt')
        ```
        """,
        "resource": """
        # boto3.resource
        
        Creates a resource service client by name.
        
        ## Parameters:
        - service_name (string): Required. The name of the service, e.g., 's3', 'ec2', etc.
        - region_name (string): Optional. The name of the region associated with the client.
        - api_version (string): Optional. The API version to use. By default, the latest API version is used.
        - use_ssl (boolean): Optional. Whether or not to use SSL. By default, SSL is used.
        - verify (boolean/string): Optional. Whether or not to verify SSL certificates.
        - endpoint_url (string): Optional. The complete URL to use for the constructed client.
        - aws_access_key_id (string): Optional. The access key to use when creating the client.
        - aws_secret_access_key (string): Optional. The secret key to use when creating the client.
        - aws_session_token (string): Optional. The session token to use when creating the client.
        
        ## Returns:
        - ServiceResource: A resource service client instance
        
        ## Example:
        ```python
        import boto3
        
        # Create an S3 resource
        s3 = boto3.resource('s3')
        
        # Upload a file to S3
        s3.Bucket('mybucket').upload_file('file.txt', 'key/in/s3.txt')
        ```
        """
    }
    
    # If function is in our mock data, return it
    for key in mock_docs:
        if key.lower() in function_name.lower():
            return mock_docs[key]
    
    # Default fallback
    return f"Documentation for {function_name} not found. Please check the AWS boto3 documentation at https://boto3.amazonaws.com/v1/documentation/api/latest/index.html"

@router.get("/aws/context")
async def aws_mcp_context(
    language: str = Query(...),
    function: str = Query(...)
):
    doc_snippet = fetch_aws_docs(function)
    
    return {
        "context": {
            "language": language,
            "library": "aws",
            "function": function,
            "documentation": doc_snippet
        }
    } 
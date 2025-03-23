# MCPservers

A project that hosts multiple Machine Context Provider (MCP) servers on different endpoints, allowing each one to serve different documentation sources or SDKs dynamically.

## Features

- Run multiple MCP servers on different endpoints for different libraries
- Provide real-time documentation context for various SDKs, APIs, or tools
- Scale easily by adding new endpoints dynamically

## Project Structure

```
│── /mcp_servers
│   ├── __init__.py    # Package initialization
│   ├── openai_mcp.py  # MCP for OpenAI SDK
│   ├── firebase_mcp.py # MCP for Firebase SDK
│   ├── aws_mcp.py     # MCP for AWS SDK
│── main.py            # Main entrypoint to run MCP servers
│── requirements.txt   # Dependencies
│── README.md          # Documentation
```

## Setup

1. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Run the server:
   ```sh
   uvicorn main:app --reload
   ```

4. Access the API documentation:
   ```
   http://localhost:8000/docs
   ```

## Available Endpoints

- OpenAI SDK: 
  `http://localhost:8000/mcp/openai/context?language=python&function=openai.ChatCompletion.create`
- Firebase SDK: 
  `http://localhost:8000/mcp/firebase/context?language=javascript&function=firebase.auth.signIn`
- AWS SDK: 
  `http://localhost:8000/mcp/aws/context?language=python&function=boto3.client`

## Extending with New SDKs

To add a new MCP server for a different SDK:

1. Create a new file in the `mcp_servers` directory (e.g., `google_mcp.py`)
2. Follow the existing pattern to create a router and endpoints
3. Import and include the new router in `main.py`
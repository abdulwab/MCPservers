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

## Understanding the MCP Protocol

The Model Context Provider (MCP) protocol is designed to facilitate the dynamic serving of documentation and contextual information for various SDKs and APIs. It acts as a bridge between developers and the vast array of documentation available for different libraries, providing real-time, relevant information based on the context of the request.

### Key Features of MCP Protocol

- **Dynamic Documentation Serving**: MCP servers fetch and serve documentation snippets dynamically based on the requested language and function, ensuring developers have the most relevant information at their fingertips.
- **Multi-Endpoint Support**: Each MCP server can be hosted on a different endpoint, allowing for easy scaling and management of multiple SDKs or APIs.
- **Real-Time Contextual Information**: By querying specific endpoints, developers can receive real-time context for functions and libraries they are working with, enhancing productivity and reducing the need to manually search through documentation.

### Integration with MCPservers Project

In this project, the MCP protocol is implemented through FastAPI routers, each dedicated to a specific SDK or API. These routers handle requests to their respective endpoints, fetch the necessary documentation, and return it in a structured format. This setup allows for easy extension and addition of new MCP servers as needed.

### Benefits

- **Improved Developer Experience**: By providing immediate access to relevant documentation, developers can focus more on coding and less on searching for information.
- **Scalability**: The architecture supports the addition of new endpoints and documentation sources without disrupting existing services.
- **Flexibility**: Easily adaptable to support new SDKs, APIs, or even custom libraries by following the established pattern for creating MCP servers.

This project demonstrates the power and flexibility of the MCP protocol in creating a centralized, dynamic documentation service for developers working with multiple technologies.
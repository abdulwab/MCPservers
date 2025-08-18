from fastapi import FastAPI
from mcp_servers.openai_mcp import router as openai_router
from mcp_servers.firebase_mcp import router as firebase_router
from mcp_servers.aws_mcp import router as aws_router
from mcp_servers.openai_agents_mcp import router as openai_agents_router
from mcp_servers.frontend_mcp import router as frontend_router
from mcp_servers.backend_mcp import router as backend_router

app = FastAPI(title="Multi-MCP Server")

# Register multiple MCP endpoints
app.include_router(openai_router, prefix="/mcp")
app.include_router(firebase_router, prefix="/mcp")
app.include_router(aws_router, prefix="/mcp")
app.include_router(openai_agents_router, prefix="/mcp")
app.include_router(frontend_router, prefix="/mcp/frontend")
app.include_router(backend_router, prefix="/mcp/backend")

@app.get("/")
async def root():
    return {"message": "Multi-MCP Server Running!", 
            "available_endpoints": [
                "/mcp/openai/context",
                "/mcp/firebase/context",
                "/mcp/aws/context",
                "/mcp/openai-agents/context",
                "/mcp/frontend/context",
                "/mcp/backend/context"
            ]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
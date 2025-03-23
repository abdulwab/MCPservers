from fastapi import FastAPI
from mcp_servers.openai_mcp import router as openai_router
from mcp_servers.firebase_mcp import router as firebase_router
from mcp_servers.aws_mcp import router as aws_router

app = FastAPI(title="Multi-MCP Server")

# Register multiple MCP endpoints
app.include_router(openai_router, prefix="/mcp")
app.include_router(firebase_router, prefix="/mcp")
app.include_router(aws_router, prefix="/mcp")

@app.get("/")
async def root():
    return {"message": "Multi-MCP Server Running!", 
            "available_endpoints": [
                "/mcp/openai/context",
                "/mcp/firebase/context",
                "/mcp/aws/context"
            ]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
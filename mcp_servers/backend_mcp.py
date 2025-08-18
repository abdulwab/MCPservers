from fastapi import APIRouter, Query
from typing import Optional, Dict, List
import json

router = APIRouter()

# Sample backend API endpoints data
backend_apis = {
    "users": {
        "GET /api/users": "List all users in the system",
        "GET /api/users/{id}": "Get a specific user by ID",
        "POST /api/users": "Create a new user",
        "PUT /api/users/{id}": "Update a user by ID",
        "DELETE /api/users/{id}": "Delete a user by ID"
    },
    "products": {
        "GET /api/products": "List all products",
        "GET /api/products/{id}": "Get a specific product by ID",
        "POST /api/products": "Create a new product",
        "PUT /api/products/{id}": "Update a product by ID",
        "DELETE /api/products/{id}": "Delete a product by ID"
    },
    "orders": {
        "GET /api/orders": "List all orders",
        "GET /api/orders/{id}": "Get a specific order by ID",
        "POST /api/orders": "Create a new order",
        "PUT /api/orders/{id}": "Update an order by ID",
        "DELETE /api/orders/{id}": "Delete an order by ID"
    }
}

# Sample database schema information
database_schemas = {
    "users": {
        "id": "string (UUID)",
        "username": "string",
        "email": "string",
        "password_hash": "string",
        "created_at": "datetime",
        "updated_at": "datetime"
    },
    "products": {
        "id": "string (UUID)",
        "name": "string",
        "description": "string",
        "price": "float",
        "inventory": "integer",
        "created_at": "datetime",
        "updated_at": "datetime"
    },
    "orders": {
        "id": "string (UUID)",
        "user_id": "string (foreign key to users.id)",
        "status": "string (enum: pending, completed, cancelled)",
        "total": "float",
        "created_at": "datetime",
        "updated_at": "datetime"
    }
}

@router.get("/context")
async def get_backend_context(
    resource: Optional[str] = Query(None, description="Backend resource name (users, products, orders)"),
    endpoint: Optional[str] = Query(None, description="API endpoint"),
    schema: Optional[str] = Query(None, description="Database schema name")
):
    """
    Get context information about backend APIs or database schemas.
    """
    context = {
        "library": "backend",
    }
    
    # If resource and endpoint are specified, provide API details
    if resource and endpoint:
        if resource in backend_apis and endpoint in backend_apis[resource]:
            context["resource"] = resource
            context["endpoint"] = endpoint
            endpoint_info = backend_apis[resource][endpoint]
            context["documentation"] = f"\n# {endpoint} ({resource})\n\n{endpoint_info}\n"
            return {"context": context}
    
    # If only resource is specified, list all endpoints for that resource
    if resource and not endpoint:
        if resource in backend_apis:
            context["resource"] = resource
            context["documentation"] = f"\n# {resource.capitalize()} API Endpoints\n\n"
            for ep, desc in backend_apis[resource].items():
                context["documentation"] += f"- {ep}: {desc}\n"
            return {"context": context}
    
    # If schema is specified, provide schema details
    if schema:
        if schema in database_schemas:
            context["schema"] = schema
            context["documentation"] = f"\n# {schema.capitalize()} Schema\n\n"
            for field, data_type in database_schemas[schema].items():
                context["documentation"] += f"- {field}: {data_type}\n"
            return {"context": context}
    
    # If nothing specific is requested, provide overview of available resources
    context["documentation"] = "\n# Backend Resources\n\n## API Resources\n"
    for res in backend_apis.keys():
        context["documentation"] += f"- {res}\n"
    
    context["documentation"] += "\n## Database Schemas\n"
    for schema in database_schemas.keys():
        context["documentation"] += f"- {schema}\n"
    
    return {"context": context}

@router.get("/apis")
async def list_apis():
    """
    List all available backend API endpoints.
    """
    return {"apis": backend_apis}

@router.get("/schemas")
async def list_schemas():
    """
    List all available database schemas.
    """
    return {"schemas": database_schemas} 
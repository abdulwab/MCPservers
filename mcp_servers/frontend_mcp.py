from fastapi import APIRouter, Query
from typing import Optional
import json

router = APIRouter()

# Sample frontend components data
frontend_components = {
    "Button": "A reusable button component with various styles and states.",
    "Card": "A container component for displaying content in a card format.",
    "Form": "A form component with validation and submission handling.",
    "Navigation": "A navigation bar component for site navigation.",
}

# Sample frontend pages data
frontend_pages = {
    "HomePage": "The main landing page of the application.",
    "Dashboard": "User dashboard with analytics and actions.",
    "Settings": "User settings and preferences page.",
    "Profile": "User profile page with personal information.",
}

@router.get("/context")
async def get_frontend_context(
    component: Optional[str] = Query(None, description="Frontend component name"),
    page: Optional[str] = Query(None, description="Frontend page name"),
):
    """
    Get context information about frontend components or pages.
    """
    context = {
        "library": "frontend",
    }
    
    # If component is specified, provide component details
    if component:
        component_info = frontend_components.get(component, "Component not found")
        context["component"] = component
        context["documentation"] = f"\n# {component}\n\n{component_info}\n"
        return {"context": context}
    
    # If page is specified, provide page details
    if page:
        page_info = frontend_pages.get(page, "Page not found")
        context["page"] = page
        context["documentation"] = f"\n# {page}\n\n{page_info}\n"
        return {"context": context}
    
    # If neither is specified, provide list of available components and pages
    context["documentation"] = "\n# Frontend Resources\n\n## Components\n"
    for comp, desc in frontend_components.items():
        context["documentation"] += f"- {comp}: {desc}\n"
    
    context["documentation"] += "\n## Pages\n"
    for p, desc in frontend_pages.items():
        context["documentation"] += f"- {p}: {desc}\n"
    
    return {"context": context}

@router.get("/components")
async def list_components():
    """
    List all available frontend components.
    """
    return {"components": frontend_components}

@router.get("/pages")
async def list_pages():
    """
    List all available frontend pages.
    """
    return {"pages": frontend_pages} 
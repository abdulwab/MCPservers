from fastapi import APIRouter, Query
import requests
import json
from bs4 import BeautifulSoup
import re

router = APIRouter()

def fetch_openai_agents_docs(function_name):
    """
    Fetch documentation for OpenAI Agents SDK functions.
    Uses the official OpenAI Agents Python SDK documentation site with BeautifulSoup
    for parsing and extracting relevant information.
    """
    base_url = "https://openai.github.io/openai-agents-python/"
    
    # Extract specific parts of the function name
    clean_function_name = function_name
    if function_name.startswith("agents."):
        clean_function_name = function_name[7:]  # Remove "agents." prefix
    elif function_name.startswith("openai.agents."):
        clean_function_name = function_name[13:]  # Remove "openai.agents." prefix
    
    # Create headers to mimic a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    }
    
    # Define mapping of function names to documentation pages
    doc_pages = {
        "Agent": "documentation/agents/",
        "Runner": "documentation/running-agents/",
        "Handoff": "documentation/handoffs/",
        "Guardrails": "documentation/guardrails/",
        "Tool": "documentation/tools/",
        "Tracing": "documentation/tracing/",
        "Voice": "documentation/voice-agents/",
    }
    
    # Try to find the appropriate page based on the function name
    target_url = base_url
    for key, path in doc_pages.items():
        if key.lower() in clean_function_name.lower():
            target_url = base_url + path
            break
    
    # If the function looks like a main concept (Agent, Runner, etc.), try to scrape its documentation
    try:
        response = requests.get(target_url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract main content
            main_content = soup.find('main')
            if not main_content:
                main_content = soup.find('div', {'class': 'markdown-body'})
            
            if main_content:
                # Extract headings and content
                content_text = ""
                for elem in main_content.find_all(['h1', 'h2', 'h3', 'p', 'pre', 'code', 'ul', 'ol', 'li']):
                    if elem.name in ['h1', 'h2', 'h3']:
                        content_text += f"\n## {elem.text.strip()}\n\n"
                    elif elem.name == 'p':
                        content_text += f"{elem.text.strip()}\n\n"
                    elif elem.name == 'pre' or elem.name == 'code':
                        code_text = elem.text.strip()
                        if code_text:
                            content_text += f"```python\n{code_text}\n```\n\n"
                    elif elem.name in ['ul', 'ol']:
                        for li in elem.find_all('li'):
                            content_text += f"- {li.text.strip()}\n"
                        content_text += "\n"
                
                # If we found specific content for the function
                if content_text:
                    # Check if our specific function is mentioned in the content
                    if clean_function_name.lower() in content_text.lower():
                        # Try to extract just the relevant section
                        sections = re.split(r'\n##\s+', content_text)
                        for section in sections:
                            if clean_function_name.lower() in section.lower():
                                return f"## {section.strip()}"
                        
                        # If we couldn't find a specific section, return the whole content
                        return content_text.strip()
                    else:
                        # Return general content if specific function not found
                        return content_text.strip()
    except Exception as e:
        print(f"Error scraping documentation: {str(e)}")
    
    # Fall back to mock documentation if scraping fails or no specific content found
    mock_docs = {
        "Agent": """
        # Agent
        
        The core primitive in the OpenAI Agents SDK. Agents are LLMs equipped with instructions and tools.
        
        ## Usage:
        ```python
        from agents import Agent, Runner

        agent = Agent(name="Assistant", instructions="You are a helpful assistant")
        
        result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")
        print(result.final_output)
        ```
        
        ## Parameters:
        - name (string): Required. A descriptive name for the agent.
        - instructions (string): Required. The system instructions that define the agent's behavior.
        - tools (List[Tool]): Optional. A list of tools the agent can use.
        - model_settings (ModelSettings): Optional. Settings for the LLM backing the agent.
        """,
        
        "Runner.run_sync": """
        # Runner.run_sync
        
        Runs an agent synchronously and returns the result.
        
        ## Parameters:
        - agent (Agent): Required. The agent to run.
        - input (str): Required. The input to the agent.
        - run_context (RunContext): Optional. Context for the run, including values for tool arguments.
        
        ## Returns:
        - AgentResult: Contains the final output and other information about the run.
        
        ## Example:
        ```python
        from agents import Agent, Runner
        
        agent = Agent(name="Assistant", instructions="You are a helpful assistant")
        
        result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")
        print(result.final_output)
        ```
        """,
        
        "Handoff": """
        # Handoff
        
        A feature that allows agents to delegate tasks to other agents.
        
        ## Usage:
        ```python
        from agents import Agent, Handoff
        
        main_agent = Agent(
            name="Main",
            instructions="You are a helpful assistant that can delegate tasks to specialists."
        )
        
        math_agent = Agent(
            name="Math Specialist",
            instructions="You are a math genius who can solve complex math problems."
        )
        
        # Register the math agent as a handoff target
        main_agent.add_handoff(
            Handoff(
                name="math_specialist",
                target=math_agent,
                description="Delegate math problems to a specialist"
            )
        )
        ```
        """,
        
        "Guardrails": """
        # Guardrails
        
        Enables input validation for agents to enforce safety and other constraints.
        
        ## Example:
        ```python
        from agents import Agent, Guardrails
        
        # Create a guardrail that rejects offensive content
        guardrails = Guardrails(
            instructions="Reject any input that contains offensive content."
        )
        
        agent = Agent(
            name="Assistant",
            instructions="You are a helpful assistant",
            guardrails=guardrails
        )
        ```
        """
    }
    
    # Check for main SDK documentation request
    if clean_function_name.lower() in ["agents", "openai_agents", "openai-agents", "sdk"]:
        try:
            response = requests.get(base_url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract title and introduction
                title = soup.find('h1')
                intro_section = soup.find('section', {'id': 'intro'})
                content = ""
                
                if title:
                    content += f"# {title.text.strip()}\n\n"
                
                if intro_section:
                    for p in intro_section.find_all('p'):
                        content += f"{p.text.strip()}\n\n"
                
                # Extract key features and installation info
                features_section = soup.find('h2', string=lambda text: 'Why use' in text if text else False)
                if features_section:
                    content += f"## {features_section.text.strip()}\n\n"
                    next_elem = features_section.find_next(['p', 'ul'])
                    while next_elem and next_elem.name in ['p', 'ul']:
                        if next_elem.name == 'p':
                            content += f"{next_elem.text.strip()}\n\n"
                        elif next_elem.name == 'ul':
                            for li in next_elem.find_all('li'):
                                content += f"- {li.text.strip()}\n"
                            content += "\n"
                        next_elem = next_elem.find_next(['p', 'ul', 'h2'])
                        if next_elem and next_elem.name == 'h2':
                            break
                
                install_section = soup.find('h2', string=lambda text: 'Installation' in text if text else False)
                if install_section:
                    content += f"## {install_section.text.strip()}\n\n"
                    next_elem = install_section.find_next(['p', 'pre'])
                    if next_elem and next_elem.name == 'pre':
                        content += f"```bash\n{next_elem.text.strip()}\n```\n\n"
                
                if content:
                    return content
        except Exception as e:
            print(f"Error scraping main documentation: {str(e)}")
    
    # If function is in our mock data, return it
    for key, doc in mock_docs.items():
        if key.lower() in clean_function_name.lower():
            return doc
    
    # Default fallback
    sdk_overview = """
    # OpenAI Agents SDK

    The OpenAI Agents SDK enables you to build agentic AI apps in a lightweight, easy-to-use package with very few abstractions. It's a production-ready upgrade of previous experimentation for agents.
    
    ## Key Features:
    - **Agents**: LLMs equipped with instructions and tools
    - **Handoffs**: Allow agents to delegate to other agents for specific tasks
    - **Guardrails**: Enable the inputs to agents to be validated
    - **Tracing**: Built-in visualization and debugging of agent workflows
    
    ## Installation:
    ```bash
    pip install openai-agents
    ```
    
    ## Documentation:
    Full documentation available at: https://openai.github.io/openai-agents-python/
    """
    
    return f"Documentation for {function_name} not found in the OpenAI Agents SDK. Here's an overview of the SDK:\n\n{sdk_overview}"

@router.get("/openai-agents/context")
async def openai_agents_mcp_context(
    language: str = Query(...),
    function: str = Query(...)
):
    doc_snippet = fetch_openai_agents_docs(function)
    
    return {
        "context": {
            "language": language,
            "library": "openai-agents",
            "function": function,
            "documentation": doc_snippet
        }
    } 
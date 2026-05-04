"""Streamable HTTP Server for the Personal Fitness Assistant MCP."""

import json
from fastapi import FastAPI
from fastmcp import FastMCP
import uvicorn

from mcp_tools import TOOL_DEFINITIONS
from mcp_resources.fitness_resources import RESOURCE_DEFINITIONS
from mcp_prompts.fitness_prompts import PROMPT_DEFINITIONS

PORT = 8003

# FastAPI app
app = FastAPI(
    title="Personal Fitness Assistant MCP Server",
    description="MCP server exposing fitness tools, resources and prompts over HTTP.",
    version="1.0.0",
)

# FastMCP server
mcp = FastMCP("Personal Fitness Assistant (HTTP)")


# --- Register tools ---
for tool in TOOL_DEFINITIONS:
    mcp.tool(
        name=tool["name"],
        description=tool.get("description", tool["name"])
    )(tool["func"])


# --- Register resources ---
for resource in RESOURCE_DEFINITIONS:
    uri = f"resource://{resource['name']}"
    display_name = resource.get("description", resource["name"])
    mime = resource.get("mime_type", "application/json")
    resource_function = resource["func"]

    def register_resource(uri, name, mime, fn):
        @mcp.resource(uri, name=name, mime_type=mime)
        def _resource():
            result = fn()
            if isinstance(result, (str, bytes)):
                return result
            return json.dumps(result)

    register_resource(uri, display_name, mime, resource_function)


# --- Register prompts ---
for prompt in PROMPT_DEFINITIONS:
    name = prompt["name"]
    desc = prompt.get("description", name)
    prompt_function = prompt["func"]
    mcp.prompt(name=name, description=desc)(prompt_function)


# Mount MCP onto FastAPI
mcp_http_app = mcp.http_app(path="/", transport="streamable-http")
app.router.lifespan_context = mcp_http_app.lifespan
app.mount("/mcp", mcp_http_app)


if __name__ == "__main__":
    print(f"Starting Personal Fitness Assistant MCP Server...")
    print(f"API docs:     http://localhost:{PORT}/docs")
    print(f"MCP endpoint: http://localhost:{PORT}/mcp")

    uvicorn.run(
        app,
        host="localhost",
        port=PORT,
    )
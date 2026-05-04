"""Streamable HTTP Server for the Personal Fitness Assistant MCP."""

import json
from fastapi import FastAPI
from fastmcp import FastMCP
import uvicorn

from mcp_tools import TOOL_DEFINITIONS
from mcp_resources.fitness_resources import hydration_guide, electrolyte_directory
from mcp_prompts.fitness_prompts import PROMPT_DEFINITIONS

PORT = 8003

app = FastAPI(
    title="Personal Fitness Assistant MCP Server",
    description="MCP server exposing fitness tools, resources and prompts over HTTP.",
    version="1.0.0",
)

mcp = FastMCP("Personal Fitness Assistant (HTTP)")


# --- Register tools ---
for tool in TOOL_DEFINITIONS:
    mcp.tool(
        name=tool["name"],
        description=tool.get("description", tool["name"])
    )(tool["func"])


# --- Register resources individually ---
@mcp.resource("resource://hydration_guide", name="Hydration Guide", mime_type="application/json")
def _hydration_guide():
    return json.dumps(hydration_guide())


@mcp.resource("resource://electrolyte_directory", name="Electrolyte Directory", mime_type="application/json")
def _electrolyte_directory():
    return json.dumps(electrolyte_directory())


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
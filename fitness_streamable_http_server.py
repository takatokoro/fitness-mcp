"""Streamable HTTP Server for the Personal Fitness Assistant MCP."""

import json
import uvicorn

from fastapi import FastAPI
from fastmcp import FastMCP

# Importing your definitions
from mcp_tools import TOOL_DEFINITIONS
from mcp_resources.fitness_resources import (
    hydration_guide,
    electrolyte_directory
)
from mcp_prompts.fitness_prompts import PROMPT_DEFINITIONS

PORT = 8003

# ---------------------------------------------------
# Create FastMCP instance
# ---------------------------------------------------

mcp = FastMCP("Personal Fitness Assistant (HTTP)")

# ---------------------------------------------------
# Register tools
# ---------------------------------------------------

for tool in TOOL_DEFINITIONS:
    mcp.tool(
        name=tool["name"],
        description=tool.get("description", tool["name"])
    )(tool["func"])

# ---------------------------------------------------
# Register resources
# ---------------------------------------------------

@mcp.resource(
    "resource://hydration_guide",
    name="Hydration Guide",
    mime_type="application/json"
)
def _hydration_guide():
    return json.dumps(hydration_guide())


@mcp.resource(
    "resource://electrolyte_directory",
    name="Electrolyte Directory",
    mime_type="application/json"
)
def _electrolyte_directory():
    return json.dumps(electrolyte_directory())

# ---------------------------------------------------
# Register prompts
# ---------------------------------------------------

for prompt in PROMPT_DEFINITIONS:
    mcp.prompt(
        name=prompt["name"],
        description=prompt.get("description", prompt["name"])
    )(prompt["func"])

# ---------------------------------------------------
# Create FastAPI app
# ---------------------------------------------------

app = FastAPI(
    title="Personal Fitness Assistant MCP Server",
    description="MCP server exposing fitness tools, resources and prompts over HTTP.",
    version="1.0.0"
)

# ---------------------------------------------------
# Swagger-visible endpoints
# ---------------------------------------------------

@app.get("/tools")
def list_tools():
    return [
        {
            "name": tool["name"],
            "description": tool.get("description", "")
        }
        for tool in TOOL_DEFINITIONS
    ]


@app.get("/resources")
def list_resources():
    return [
        "resource://hydration_guide",
        "resource://electrolyte_directory"
    ]


@app.get("/prompts")
def list_prompts():
    return [
        {
            "name": prompt["name"],
            "description": prompt.get("description", "")
        }
        for prompt in PROMPT_DEFINITIONS
    ]

# ---------------------------------------------------
# Mount MCP app
# ---------------------------------------------------

mcp_app = mcp.http_app(transport="streamable-http")

app.mount("/", mcp_app)

# ---------------------------------------------------
# Run server
# ---------------------------------------------------

if __name__ == "__main__":
    print("Starting Personal Fitness Assistant MCP Server...")
    print(f"API docs:     http://localhost:{PORT}/docs")
    print(f"MCP endpoint: http://localhost:{PORT}/")

    uvicorn.run(
        app,
        host="localhost",
        port=PORT,
    )
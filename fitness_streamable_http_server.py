"""Streamable HTTP Server for the Personal Fitness Assistant MCP."""

import json
from fastapi import FastAPI
from fastmcp import FastMCP
import uvicorn

from mcp_tools import water_intake_router, sweat_loss_router, sweat_loss_v2_router
from mcp_resources.fitness_resources import hydration_guide, electrolyte_directory
from mcp_prompts.fitness_prompts import PROMPT_DEFINITIONS

PORT = 8003

# FastAPI app for plain HTTP
app = FastAPI(
    title="Personal Fitness Assistant MCP Server",
    description="FastAPI endpoints auto-exposed as MCP tools via FastMCP, with resources and prompts.",
    version="1.0.0",
)
app.include_router(water_intake_router)
app.include_router(sweat_loss_router)
app.include_router(sweat_loss_v2_router)

# FastMCP server generated from FastAPI OpenAPI (tools) plus manual resources/prompts
mcp = FastMCP.from_fastapi(
    app,
    name="Personal Fitness Assistant MCP Server",
    instructions="Fitness tools for hydration and sweat loss monitoring.",
)

# --- Resources ---------------------------------------------------------------

@mcp.resource("resource://hydration_guide", name="Hydration Guide", mime_type="application/json")
def _resource_hydration_guide():
    return json.dumps(hydration_guide())


@mcp.resource("resource://electrolyte_directory", name="Electrolyte Directory", mime_type="application/json")
def _resource_electrolyte_directory():
    return json.dumps(electrolyte_directory())


# --- Prompts -----------------------------------------------------------------

for prompt in PROMPT_DEFINITIONS:
    mcp.prompt(
        name=prompt["name"],
        description=prompt.get("description", prompt["name"]),
    )(prompt["func"])


# Build MCP sub-apps and mount onto FastAPI
mcp_http_app = mcp.http_app(path="/", transport="streamable-http")
mcp_sse_app = mcp.http_app(path="/", transport="sse")
app.router.lifespan_context = mcp_http_app.lifespan

app.mount("/mcp", mcp_http_app)
app.mount("/sse", mcp_sse_app)


if __name__ == "__main__":
    print("Starting Personal Fitness Assistant MCP Server...")
    print(f"HTTP docs:      http://localhost:{PORT}/docs")
    print(f"HTTP redoc:     http://localhost:{PORT}/redoc")
    print(f"MCP endpoint:   http://localhost:{PORT}/mcp (HTTP)")
    print(f"MCP endpoint:   http://localhost:{PORT}/sse (SSE)")

    uvicorn.run(
        app,
        host="localhost",
        port=PORT,
    )

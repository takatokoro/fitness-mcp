"""STDIO Server for the Personal Fitness Assistant MCP."""

import json
from fastmcp import FastMCP

from mcp_resources.fitness_resources import hydration_guide, electrolyte_directory
from mcp_prompts.fitness_prompts import PROMPT_DEFINITIONS
from mcp_tools import TOOL_DEFINITIONS

mcp = FastMCP("Personal Fitness Assistant (STDIO)")


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


if __name__ == "__main__":
    mcp.run()
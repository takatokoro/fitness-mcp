"""STDIO Server — Personal Fitness Assistant MCP (Version 2)."""

import json
import logging
from pathlib import Path

from fastmcp import FastMCP

from mcp_resources.fitness_resources import hydration_guide, electrolyte_directory
from mcp_prompts.fitness_prompts import PROMPT_DEFINITIONS
from mcp_tools import TOOL_DEFINITIONS

Path("./logs").mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s — %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("./logs/mcp_log_stdio.log"),
    ],
)
logger = logging.getLogger(__name__)

mcp = FastMCP("Personal Fitness Assistant v2 (STDIO)")

# Tools
for tool in TOOL_DEFINITIONS:
    mcp.tool(
        name=tool["name"],
        description=tool.get("description", tool["name"]),
    )(tool["func"])

# Resources
@mcp.resource("resource://hydration_guide", name="Hydration Guide", mime_type="application/json")
def _hydration_guide():
    return json.dumps(hydration_guide())


@mcp.resource("resource://electrolyte_directory", name="Electrolyte Directory", mime_type="application/json")
def _electrolyte_directory():
    return json.dumps(electrolyte_directory())


@mcp.resource("resource://server_logs", name="Server Logs", mime_type="text/plain")
def _server_logs():
    log_path = Path("./logs/mcp_log_stdio.log")
    if not log_path.exists():
        return "No log entries yet."
    with open(log_path, encoding="utf-8") as f:
        lines = f.readlines()
    return "".join(lines[-50:])


# Prompts
for prompt in PROMPT_DEFINITIONS:
    mcp.prompt(
        name=prompt["name"],
        description=prompt.get("description", prompt["name"]),
    )(prompt["func"])


if __name__ == "__main__":
    mcp.run()

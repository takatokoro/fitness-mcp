"""STDIO Server for the Personal Fitness Assistant MCP."""

import json
from fastmcp import FastMCP

from mcp_resources.fitness_resources import hydration_guide, electrolyte_directory
from mcp_prompts.fitness_prompts import PROMPT_DEFINITIONS
from mcp_tools import TOOL_DEFINITIONS

import logging
from pathlib import Path
from utils.logging_utils import build_log_config, configure_logging

LOG_FILE = Path("./logs/mcp_log_stdio.log")
configure_logging(
    build_log_config(
        LOG_FILE,
        console=True,
        logger_handlers={
            "fastmcp": ["rotating_file", "console"],
        },
        root_level="INFO",
        logger_level="DEBUG",
    )
)
logger = logging.getLogger(__name__)

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

@mcp.resource("resource://server_logs", name="Server Logs", mime_type="text/plain")
def _server_logs():
    """Exposes recent server log entries for AI agents to read."""
    log_path = Path("./logs/mcp_log_stdio.log")
    if not log_path.exists():
        return "No log entries yet."
    with open(log_path, encoding="utf-8") as f:
        lines = f.readlines()
    return "".join(lines[-50:])
# --- Register prompts ---
for prompt in PROMPT_DEFINITIONS:
    name = prompt["name"]
    desc = prompt.get("description", name)
    prompt_function = prompt["func"]
    mcp.prompt(name=name, description=desc)(prompt_function)


if __name__ == "__main__":
    mcp.run()
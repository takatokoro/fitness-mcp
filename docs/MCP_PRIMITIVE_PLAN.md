# MCP Primitive Plan — Version 2

## Tools (4 total)

| Name | File | Description |
|------|------|-------------|
| `calculate_water_intake` | `mcp_tools/fitness_tool_1.py` | Daily water target from weight + workout |
| `estimate_sweat_loss` | `mcp_tools/fitness_tool_2_v1.py` | Fluid/mineral loss via CSV |
| `estimate_sweat_loss_v2` | `mcp_tools/fitness_tool_2_v2.py` | Fluid/mineral loss + recovery foods via API |
| `weather_adjusted_hydration` | `mcp_tools/fitness_tool_3.py` | Hydration target adjusted for live weather |

## Prompts (2 total — unchanged from V1)

| Name | Description |
|------|-------------|
| `hydration_planner` | Sports Nutritionist giving daily hydration suggestions |
| `sweat_analysis` | Performance Nutritionist explaining mineral loss + recovery |

## Resources (3 total)

| URI | Description |
|-----|-------------|
| `resource://hydration_guide` | Beverage hydration efficiency dataset |
| `resource://electrolyte_directory` | Mineral loss and recovery foods reference |
| `resource://server_logs` | Last 50 lines of server log for AI agents |

## Registration Pattern

All tools registered via `TOOL_DEFINITIONS` list in each tool file,
imported and combined in `mcp_tools/__init__.py`, then registered in
the server file via `FastMCP.from_fastapi()`.

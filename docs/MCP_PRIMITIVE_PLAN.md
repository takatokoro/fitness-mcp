# MCP Primitive Plan — Version 2

## Tools (4 total)

| Name | File | Description |
|------|------|-------------|
| `calculate_water_intake` | `mcp_tools/fitness_tool_1.py` | Daily water target from weight + workout |
| `estimate_sweat_loss` | `mcp_tools/fitness_tool_2_v1.py` | Fluid/mineral loss via CSV |
| `estimate_sweat_loss_v2` | `mcp_tools/fitness_tool_2_v2.py` | Fluid/mineral loss + recovery foods via API Ninjas |
| `weather_adjusted_hydration` | `mcp_tools/fitness_tool_3.py` | Hydration target adjusted for live weather via city name |

## Prompts (3 total)

| Name | File | Description |
|------|------|-------------|
| `hydration_planner` | `mcp_prompts/fitness_prompts.py` | Sports Nutritionist giving daily hydration suggestions |
| `sweat_analysis` | `mcp_prompts/fitness_prompts.py` | Performance Nutritionist explaining mineral loss + recovery |
| `ai_fitness_summary` | `mcp_prompts/fitness_prompts.py` | Sends all tool results to OpenRouter/Mistral 7B for a plain English coaching summary |

## Resources (4 total)

| URI | Description |
|-----|-------------|
| `resource://hydration_guide` | Beverage hydration efficiency dataset |
| `resource://electrolyte_directory` | Mineral loss and recovery foods reference |
| `resource://server_logs` | Last 50 lines of server log for AI agents |
| `resource://weather_context` | Most recent Open-Meteo weather data held in memory — avoids a second API call when the AI prompt needs current conditions |

## Registration Pattern

All tools registered via `TOOL_DEFINITIONS` list in each tool file,
imported and combined in `mcp_tools/__init__.py`, then registered in
the server file via `FastMCP.from_fastapi()`.

Prompts and resources are registered directly on the `mcp` FastMCP instance
in `fitness_streamable_http_server.py` using `@mcp.prompt()` and `@mcp.resource()`.

## Integration Between Primitives

```
Tool 3 (weather_adjusted_hydration)
    calls Open-Meteo → calculates adjusted hydration target
        ↓
Resource 3 (weather_context)
    stores the live weather data in memory
        ↓
Prompt 3 (ai_fitness_summary)
    combines all tool results + weather context
    sends to OpenRouter → Mistral 7B
        ↓
User receives plain English coaching summary
```

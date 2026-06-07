# Personal Fitness Assistant MCP Server — Version 2

A FastAPI + FastMCP server providing hydration and sweat loss tools exposed
as MCP primitives. Version 2 adds weather-adjusted hydration via the free
Open-Meteo API and prepares the project for cloud deployment on Render.

---

## Features

| Tool | Endpoint | Description |
|------|----------|-------------|
| Water Intake Calculator | `POST /calculate-water-intake` | Daily water target from weight + workout |
| Sweat Loss Estimator v1 | `POST /estimate-sweat-loss` | Fluid/mineral loss via local CSV |
| Sweat Loss Estimator v2 | `POST /estimate-sweat-loss-v2` | Fluid/mineral loss + recovery foods via API |
| Weather Hydration | `POST /weather-adjusted-hydration` | Water target adjusted for live weather |

**MCP transports:** streamable-http at `/mcp`, SSE at `/sse`  
**Resources:** `hydration_guide`, `electrolyte_directory`, `server_logs`  
**Prompts:** `hydration_planner`, `sweat_analysis`

---

## Setup

```bash
python -m venv .venv
source .venv/bin/activate       # Mac/Linux
# .venv\Scripts\activate        # Windows

pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your API_NINJAS_KEY
```

## Run Locally

```bash
python fitness_streamable_http_server.py
```

- Swagger UI: http://localhost:8003/docs
- Health: http://localhost:8003/health
- MCP: http://localhost:8003/mcp

## Run Tests

```bash
pytest tests/ -v
```

## MCP Inspector

```bash
# Streamable HTTP
npx @modelcontextprotocol/inspector@latest \
  -e DUMMY=1 --url http://localhost:8003/mcp --transport streamable-http

# STDIO
npx @modelcontextprotocol/inspector python fitness_stdio_server.py
```

## Deployment

See `docs/DEPLOYMENT_PLAN.md` for full Render deployment instructions.
The `render.yaml` file in the project root handles service configuration.

---

## Architecture

```
fitness-mcp/
├── fitness_streamable_http_server.py  # Main server (HTTP + MCP)
├── fitness_stdio_server.py            # STDIO server
├── mcp_tools/
│   ├── fitness_tool_1.py              # Water intake
│   ├── fitness_tool_2_v1.py           # Sweat loss (CSV)
│   ├── fitness_tool_2_v2.py           # Sweat loss (API Ninjas)
│   └── fitness_tool_3.py              # Weather hydration (Open-Meteo)
├── services/
│   └── weather_service.py             # Open-Meteo API wrapper
├── mcp_resources/fitness_resources.py
├── mcp_prompts/fitness_prompts.py
├── data/sweat_minerals.csv
├── tests/
├── docs/
├── render.yaml
├── requirements.txt
└── .env.example
```

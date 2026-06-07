# Project Scope — Version 2

## What Version 2 Is

A realistic, deployable upgrade of the Personal Fitness Assistant MCP server.
The goal is a clean, well-structured foundation — not a complete commercial product.

## What Is Included in V2

- All V1 tools, prompts, and resources (unchanged)
- Tool 3: Weather-Adjusted Hydration (Open-Meteo, no API key required)
- `services/` folder for external API wrappers
- `docs/` folder with planning guardrail documents
- `tests/` folder with beginner-readable pytest tests
- Updated `requirements.txt` with correct package names
- `.env.example` with safe placeholders
- `render.yaml` for Render cloud deployment
- `/health` endpoint for Render health checking
- OpenRouter placeholders in `.env.example` (not wired up yet)
- Cleanup of leftover `converter_*.py` files

## What Is Excluded from V2

- Full OpenRouter / AI conversational integration (V3)
- Authentication or API key protection on endpoints
- Rate limiting
- Database or persistent storage
- CI/CD pipeline
- Frontend / UI
- Docker containerisation

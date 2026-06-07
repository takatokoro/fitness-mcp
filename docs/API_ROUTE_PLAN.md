# API Route Plan — Version 2

All FastAPI routes use Pydantic for input validation and return consistent JSON.

| Method | Route | Tool | Description |
|--------|-------|------|-------------|
| GET | `/health` | — | Health check for Render monitoring |
| POST | `/calculate-water-intake` | Tool 1 | Daily water intake from weight + workout |
| POST | `/estimate-sweat-loss` | Tool 2 v1 | Sweat/mineral loss via CSV |
| POST | `/estimate-sweat-loss-v2` | Tool 2 v2 | Sweat/mineral loss + recovery foods via API Ninjas |
| POST | `/weather-adjusted-hydration` | Tool 3 | Hydration target adjusted for live weather |
| GET | `/docs` | — | FastAPI auto-generated Swagger UI |
| GET | `/redoc` | — | FastAPI ReDoc |

## Error Response Format

All routes return errors in this shape:
```json
{"error": "description of the problem", "operation": "route_name"}
```

## MCP Endpoints

| Transport | URL |
|-----------|-----|
| Streamable HTTP | `/mcp` |
| SSE (legacy) | `/sse` |

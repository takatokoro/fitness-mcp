# AI Coding Guardrails

## Architecture — Do Not Remove

- FastAPI as the HTTP framework
- FastMCP wrapping FastAPI for MCP exposure
- `/mcp` streamable-http endpoint on port 8003 (or `$PORT` on Render)
- `/sse` SSE endpoint
- `/health` endpoint
- `/docs` FastAPI auto-generated Swagger UI
- `mcp_tools/`, `mcp_resources/`, `mcp_prompts/` folder structure
- Each tool in its own file inside `mcp_tools/`
- `tests/` and `docs/` folders

## Tool File Pattern

Every tool file must contain:
1. A Pydantic model class for input validation
2. A core logic function (pure, testable)
3. A FastAPI `APIRouter` endpoint
4. A `TOOL_DEFINITIONS` list for MCP registration

## Security Rules

- API keys loaded with `os.getenv()` only — never hardcoded
- `.env` listed in `.gitignore` — never committed
- `.env.example` committed with placeholder values only

## External API Rules

- All external API calls must live in `services/`, never inside tool or route files
- All external calls must have a `timeout` parameter
- All external calls must have error handling with a fallback

## Conflict Resolution

If implementation conflicts with documentation:
1. STOP
2. Explain the conflict
3. Recommend the smallest safe correction
4. Wait for approval before deviating

# API Route Plan — Version 2

All FastAPI routes use Pydantic for input validation and return consistent JSON.

## Fitness Tool Routes (no auth in V2)

| Method | Route | Tool | Description |
|--------|-------|------|-------------|
| GET | `/health` | — | Health check for Render monitoring |
| POST | `/calculate-water-intake` | Tool 1 | Daily water intake from weight + workout |
| POST | `/estimate-sweat-loss` | Tool 2 v1 | Sweat/mineral loss via CSV |
| POST | `/estimate-sweat-loss-v2` | Tool 2 v2 | Sweat/mineral loss + recovery foods via API Ninjas |
| POST | `/weather-adjusted-hydration` | Tool 3 | Hydration target adjusted for live weather via city name |
| GET | `/docs` | — | FastAPI auto-generated Swagger UI |
| GET | `/redoc` | — | FastAPI ReDoc |

## Authentication Routes (new in V2)

| Method | Route | Auth Required | Description |
|--------|-------|---------------|-------------|
| POST | `/register` | No | Create a new user account. Accepts username + password. Password is hashed with passlib before saving to MongoDB. Returns confirmation. |
| POST | `/login` | No | Accepts username + password. Returns a JWT token valid for 24 hours. This token must be sent in the `Authorization: Bearer <token>` header for protected routes. |

## Authentication Plan (V2)

- `/register` and `/login` are public — no token needed
- All fitness routes (`/calculate-water-intake`, `/estimate-sweat-loss`, `/estimate-sweat-loss-v2`, `/weather-adjusted-hydration`) will require a valid JWT token in V2
- Missing or invalid token returns `403 Forbidden`
- JWT secret stored in `.env` as `JWT_SECRET`, loaded via `os.getenv()`
- User data stored in MongoDB Atlas free tier (`fitness` database, `users` collection)

## Error Response Format

All routes return errors in this shape:
```json
{"error": "description of the problem", "operation": "route_name"}
```

Auth errors return:
```json
{"detail": "Could not validate credentials"}
```

## MCP Endpoints

| Transport | URL |
|-----------|-----|
| Streamable HTTP | `/mcp` |
| SSE (legacy) | `/sse` |

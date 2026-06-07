# Deployment Plan — Version 2

## Local Run

```bash
# 1. Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate        # Mac/Linux
# .venv\Scripts\activate         # Windows PowerShell

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy and fill in your .env
cp .env.example .env
# Edit .env and add your real API_NINJAS_KEY

# 4. Start the server
python fitness_streamable_http_server.py
```

Endpoints available locally:
- Swagger UI: http://localhost:8003/docs
- Health: http://localhost:8003/health
- MCP (streamable-http): http://localhost:8003/mcp
- SSE: http://localhost:8003/sse

## Running Tests

```bash
pytest tests/ -v
```

## Render Cloud Deployment

### Prerequisites
- GitHub repo with this code (`.env` must NOT be in repo)
- Render account at https://render.com

### Steps
1. Push code to GitHub
2. Go to Render → New → Web Service
3. Connect your GitHub repo (`takatokoro/fitness-mcp`)
4. Render detects `render.yaml` automatically
5. Under Environment, add secret values:
   - `API_NINJAS_KEY` — your real key
   - `OPENROUTER_API_KEY` — your real key (placeholder for now)
6. Click Deploy

### Why `host="0.0.0.0"` is Required
Render assigns a random internal host. Using `localhost` would make the
server unreachable. The server reads `PORT` from the environment:
```python
PORT = int(os.getenv("PORT", 8003))
uvicorn.run(app, host="0.0.0.0", port=PORT)
```

### Health Check
Render calls `/health` every 30 seconds. If it returns non-200, Render
restarts the service. Our `/health` endpoint returns:
```json
{"status": "ok", "version": "2.0.0"}
```

### MCP Inspector Against Live Server
```bash
npx @modelcontextprotocol/inspector@latest \
  -e DUMMY=1 \
  --url https://YOUR-APP.onrender.com/mcp \
  --transport streamable-http
```

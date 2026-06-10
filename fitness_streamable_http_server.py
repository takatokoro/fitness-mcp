"""Streamable HTTP Server — Personal Fitness Assistant MCP (Version 2)."""


import json
import os
import logging
from pathlib import Path
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from fastmcp import FastMCP
import httpx
import uvicorn
from dotenv import load_dotenv
load_dotenv()


from mcp_tools import (
    water_intake_router,
    sweat_loss_router,
    sweat_loss_v2_router,
    weather_hydration_router,
)
from mcp_resources.fitness_resources import hydration_guide, electrolyte_directory, weather_context
from mcp_prompts.fitness_prompts import PROMPT_DEFINITIONS
from routes.auth_routes import router as auth_router

PORT = int(os.getenv("PORT", 8003))

# Ensure logs directory exists
Path("./logs").mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s — %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("./logs/mcp_log_streamable_http.log"),
    ],
)
logger = logging.getLogger(__name__)

# --- FastAPI app -------------------------------------------------------------

app = FastAPI(
    title="Personal Fitness Assistant MCP Server",
    description=(
        "FastAPI endpoints auto-exposed as MCP tools via FastMCP. "
        "Includes hydration, sweat loss, weather-adjusted hydration tools, "
        "and JWT authentication."
    ),
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Fitness tool routes
app.include_router(water_intake_router)
app.include_router(sweat_loss_router)
app.include_router(sweat_loss_v2_router)
app.include_router(weather_hydration_router)

# Auth routes (/register and /login)
app.include_router(auth_router)


@app.get("/health", tags=["health"])
def health():
    """Health check endpoint — required by Render for deployment monitoring."""
    return {"status": "ok", "version": "2.0.0"}


async def call_gemini(prompt: str) -> str:
    """Helper: sends a prompt to Gemini and returns the text response."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={os.getenv('GEMINI_API_KEY')}",
            json={
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"maxOutputTokens": 200}
            }
        )
        result = r.json()
        if "candidates" not in result:
            raise Exception(f"Gemini error: {result}")
        return result["candidates"][0]["content"]["parts"][0]["text"]


@app.post("/ai-coaching-summary", tags=["ai"])
async def ai_coaching_summary(
    weight_kg: float,
    workout_minutes: int,
    city: str,
    intensity_level: str = "moderate"
):
    """Calls Tool 1, Tool 2, Tool 3 then sends results to Gemini for a coaching summary."""

    base_url = os.getenv("BASE_URL", f"http://localhost:{PORT}")

    async with httpx.AsyncClient(timeout=30.0) as client:
        r1 = await client.post(
            f"{base_url}/calculate-water-intake",
            params={"weight_kg": weight_kg, "workout_minutes": workout_minutes}
        )
        water_data = r1.json()

        r2 = await client.post(
            f"{base_url}/estimate-sweat-loss",
            params={"workout_duration_min": workout_minutes, "intensity_level": intensity_level}
        )
        sweat_data = r2.json()

        r3 = await client.post(
            f"{base_url}/weather-adjusted-hydration",
            params={"weight_kg": weight_kg, "workout_minutes": workout_minutes, "city": city}
        )
        weather_data = r3.json()

    prompt = f"""You are a friendly fitness hydration coach. Write a short coaching summary (3-4 sentences) based on this data:

Location: {city}
Temperature: {weather_data.get('weather', {}).get('temperature_celsius', 'N/A')}°C
Humidity: {weather_data.get('weather', {}).get('relative_humidity_percent', 'N/A')}%
Body weight: {weight_kg}kg
Workout: {workout_minutes} minutes at {intensity_level} intensity
Adjusted water target: {weather_data.get('adjusted_daily_target_litres', 'N/A')}L
Sodium lost: {sweat_data.get('sodium_lost_mg', 'N/A')}mg
Potassium lost: {sweat_data.get('potassium_lost_mg', 'N/A')}mg
Magnesium lost: {sweat_data.get('magnesium_lost_mg', 'N/A')}mg

Give practical, conversational advice on hydration and recovery foods. No bullet points."""

    coaching = await call_gemini(prompt)

    return {
        "coaching_summary": coaching,
        "data": {
            "water": water_data,
            "sweat": sweat_data,
            "weather": weather_data
        }
    }


class CoachingRequest(BaseModel):
    tool_result: str
    context: str = ""


@app.post("/ai-coaching-summary-simple", tags=["ai"])
async def ai_coaching_summary_simple(body: CoachingRequest):
    """Takes any tool result JSON and returns a Gemini coaching tip."""

    prompt = f"""You are a friendly fitness hydration coach. Write a short coaching tip (2-3 sentences) based on this fitness data:

{body.tool_result}

Additional context: {body.context}

Be conversational and practical. No bullet points."""

    coaching = await call_gemini(prompt)
    return {"coaching_summary": coaching}


# --- FastMCP server ----------------------------------------------------------

mcp = FastMCP.from_fastapi(
    app,
    name="Personal Fitness Assistant MCP Server",
    instructions=(
        "Fitness tools available: "
        "1. calculate_water_intake - daily water target from weight and workout. "
        "2. estimate_sweat_loss - fluid and mineral loss from workout. "
        "3. estimate_sweat_loss_v2 - sweat loss with recovery food data. "
        "4. weather_adjusted_hydration - water target adjusted for live weather by city name. "
        "Use weather_adjusted_hydration when user mentions weather, city, or location."
    ),
)

# Resources
@mcp.resource("resource://hydration_guide", name="Hydration Guide", mime_type="application/json")
def _resource_hydration_guide():
    return json.dumps(hydration_guide())


@mcp.resource("resource://electrolyte_directory", name="Electrolyte Directory", mime_type="application/json")
def _resource_electrolyte_directory():
    return json.dumps(electrolyte_directory())


@mcp.resource("resource://server_logs", name="Server Logs", mime_type="text/plain")
def _server_logs():
    """Exposes recent server log entries for AI agents to read."""
    log_path = Path("./logs/mcp_log_streamable_http.log")
    if not log_path.exists():
        return "No log entries yet."
    with open(log_path, encoding="utf-8") as f:
        lines = f.readlines()
    return "".join(lines[-50:])


@mcp.resource("resource://weather_context", name="Weather Context", mime_type="application/json")
def _resource_weather_context():
    """Most recent weather data fetched by Tool 3. Call /weather-adjusted-hydration first."""
    return json.dumps(weather_context())


# Prompts
for prompt in PROMPT_DEFINITIONS:
    mcp.prompt(
        name=prompt["name"],
        description=prompt.get("description", prompt["name"]),
    )(prompt["func"])


# Mount MCP transports
mcp_http_app = mcp.http_app(path="/", transport="streamable-http")
mcp_sse_app = mcp.http_app(path="/", transport="sse")
app.router.lifespan_context = mcp_http_app.lifespan

app.mount("/mcp", mcp_http_app)
app.mount("/sse", mcp_sse_app)


if __name__ == "__main__":
    print("Starting Personal Fitness Assistant MCP Server v2.0.0...")
    print(f"Swagger UI:     http://localhost:{PORT}/docs")
    print(f"Health check:   http://localhost:{PORT}/health")
    print(f"MCP endpoint:   http://localhost:{PORT}/mcp  (streamable-http)")
    print(f"SSE endpoint:   http://localhost:{PORT}/sse")

    uvicorn.run(app, host="0.0.0.0", port=PORT)

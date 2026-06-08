"""OpenRouter service wrapper.

All OpenRouter/Mistral API calls live here, never inside tool or route files.
Sends workout data to Mistral 7B and returns a plain English coaching summary.
"""

import logging
import os
import httpx

logger = logging.getLogger(__name__)

OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "mistralai/mistral-7b-instruct")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")


def get_coaching_summary(
    weight_kg: float,
    workout_minutes: int,
    city: str,
    temperature_celsius: float,
    humidity_percent: int,
    adjusted_daily_target_litres: float,
    heat_adjustment_litres: float,
    humidity_adjustment_litres: float,
    intensity_level: str = "moderate",
    fluid_lost_litres: float = 0.0,
    sodium_lost_mg: float = 0.0,
    potassium_lost_mg: float = 0.0,
    magnesium_lost_mg: float = 0.0,
) -> dict:
    """
    Send workout + weather data to Mistral 7B via OpenRouter.
    Returns a plain English coaching summary.

    Args:
        weight_kg: User body weight in kg.
        workout_minutes: Workout duration in minutes.
        city: City name where the user worked out.
        temperature_celsius: Current temperature at location.
        humidity_percent: Current humidity at location.
        adjusted_daily_target_litres: Final water target after weather adjustment.
        heat_adjustment_litres: Extra water added due to heat.
        humidity_adjustment_litres: Extra water added due to humidity.
        intensity_level: Workout intensity (low/moderate/high).
        fluid_lost_litres: Total fluid lost through sweat.
        sodium_lost_mg: Sodium lost through sweat.
        potassium_lost_mg: Potassium lost through sweat.
        magnesium_lost_mg: Magnesium lost through sweat.

    Returns:
        Dictionary with coaching_summary string and model used.
        Falls back to a default message if OpenRouter is unavailable.
    """
    if not OPENROUTER_API_KEY:
        logger.warning("OPENROUTER_API_KEY not set — skipping AI summary.")
        return {
            "coaching_summary": (
                f"Drink at least {adjusted_daily_target_litres}L today in {city}. "
                f"Current conditions: {temperature_celsius}degC, {humidity_percent}% humidity."
            ),
            "model": "fallback (no API key)",
        }

    prompt = f"""You are a friendly sports nutrition coach. Give a short, practical coaching summary (3-4 sentences max) based on this workout data:

- Location: {city}
- Weather: {temperature_celsius}degC, {humidity_percent}% humidity
- Body weight: {weight_kg}kg
- Workout duration: {workout_minutes} minutes ({intensity_level} intensity)
- Total water target today: {adjusted_daily_target_litres}L
- Heat adjustment: +{heat_adjustment_litres}L (due to temperature)
- Humidity adjustment: +{humidity_adjustment_litres}L (due to humidity)
- Fluid lost through sweat: {fluid_lost_litres}L
- Minerals lost: {sodium_lost_mg}mg sodium, {potassium_lost_mg}mg potassium, {magnesium_lost_mg}mg magnesium

Write a friendly, encouraging coaching message. Include specific food or drink suggestions to replace minerals lost. Keep it practical and conversational."""

    try:
        response = httpx.post(
            f"{OPENROUTER_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": OPENROUTER_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 200,
            },
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()
        summary = data["choices"][0]["message"]["content"].strip()

        logger.info("OpenRouter coaching summary generated via %s", OPENROUTER_MODEL)

        return {
            "coaching_summary": summary,
            "model": OPENROUTER_MODEL,
        }

    except Exception as exc:
        logger.warning("OpenRouter call failed: %s — using fallback.", exc)
        return {
            "coaching_summary": (
                f"Drink at least {adjusted_daily_target_litres}L today in {city}. "
                f"Current conditions: {temperature_celsius}degC, {humidity_percent}% humidity. "
                f"Eat a banana and salted nuts to replace minerals lost."
            ),
            "model": f"fallback (OpenRouter error: {str(exc)})",
        }

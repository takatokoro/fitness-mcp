# Sweat loss logic and HTTP endpoints (v1 - CSV) are defined here so they can
# be reused by both the FastAPI app and the MCP tool registrations.

import csv
from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(prefix="", tags=["fitness"])

# Path to the CSV data file
DATA_FILE = Path(__file__).parent.parent / "data" / "sweat_minerals.csv"


# --- Pydantic model ----------------------------------------------------------

class SweatLossRequest(BaseModel):
    workout_duration_min: int = Field(..., ge=1, le=480, description="Workout duration in minutes, 1-480")
    intensity_level: str = Field(..., description="Intensity level: low, moderate, or high")


# --- Core logic function -----------------------------------------------------

def estimate_sweat_loss_value(workout_duration_min: int, intensity_level: str) -> dict:
    """
    Estimate fluid and mineral loss during a workout.
    Reads mineral data from a local CSV file (Version 1).

    Args:
        workout_duration_min: Duration of workout in minutes.
        intensity_level: Intensity of workout - low, moderate, or high.

    Returns:
        Dictionary with fluid and mineral loss estimates.
    """
    request = SweatLossRequest(
        workout_duration_min=workout_duration_min,
        intensity_level=intensity_level,
    )

    # Read mineral data from CSV
    mineral_data = {}
    with open(DATA_FILE, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            mineral_data[row["intensity"]] = row

    if request.intensity_level.lower() not in mineral_data:
        raise ValueError(
            f"Invalid intensity '{request.intensity_level}'. Choose: low, moderate, high"
        )

    row = mineral_data[request.intensity_level.lower()]

    sweat_rate = float(row["sweat_rate_L_per_hr"])
    litres_lost = round((request.workout_duration_min / 60) * sweat_rate, 2)

    sodium_lost = round(litres_lost * float(row["sodium_mg"]), 1)
    potassium_lost = round(litres_lost * float(row["potassium_mg"]), 1)
    magnesium_lost = round(litres_lost * float(row["magnesium_mg"]), 1)

    return {
        "version": "v1 - CSV",
        "workout_duration_min": request.workout_duration_min,
        "intensity_level": request.intensity_level.lower(),
        "fluid_lost_litres": litres_lost,
        "sodium_lost_mg": sodium_lost,
        "potassium_lost_mg": potassium_lost,
        "magnesium_lost_mg": magnesium_lost,
        "recommended_replacement_litres": round(litres_lost * 1.5, 2),
        "data_source": "sweat_minerals.csv",
    }


# --- FastAPI endpoint ---------------------------------------------------------

@router.post("/estimate-sweat-loss", operation_id="estimate_sweat_loss")
def estimate_sweat_loss(workout_duration_min: int, intensity_level: str):
    """
    HTTP endpoint: estimate sweat and mineral loss (v1 - CSV).

    Args:
        workout_duration_min: Duration of workout in minutes.
        intensity_level: Intensity level - low, moderate, or high.

    Returns:
        JSON dict with fluid and mineral loss estimates.
    """
    try:
        return estimate_sweat_loss_value(
            workout_duration_min=workout_duration_min,
            intensity_level=intensity_level,
        )
    except ValueError as exc:
        return {"error": str(exc), "operation": "estimate_sweat_loss"}


# --- Metadata for MCP tool registration --------------------------------------

TOOL_DEFINITIONS = [
    {
        "name": "estimate_sweat_loss",
        "description": "Estimate fluid and mineral loss after a workout. Intensity: low, moderate, or high. (v1 - CSV)",
        "func": estimate_sweat_loss_value,
        "tags": {"fitness", "sweat", "minerals"},
    },
]
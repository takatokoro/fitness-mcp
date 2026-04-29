"""MCP Tool 2 - Estimate Sweat Loss (Version 1 - CSV)."""

import csv
from pathlib import Path

# Path to the CSV data file
DATA_FILE = Path(__file__).parent.parent / "data" / "sweat_minerals.csv"


def estimate_sweat_loss(workout_duration_min: int, intensity_level: str) -> dict:
    """
    Estimate fluid and mineral loss during a workout.
    Reads mineral data from a local CSV file (Version 1).

    User's input:
        workout_duration_min: Duration of workout in minutes.
        intensity_level: Intensity of workout - low, moderate, or high.

    Returns:
        Dictionary with fluid and mineral loss estimates.
    """
    # Read mineral data from CSV
    mineral_data = {}
    with open(DATA_FILE, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            mineral_data[row["intensity"]] = row

    # Validate intensity level
    if intensity_level.lower() not in mineral_data:
        raise ValueError(
            f"Invalid intensity '{intensity_level}'. Choose: low, moderate, high"
        )

    # Get the row matching the intensity
    row = mineral_data[intensity_level.lower()]

    sweat_rate = float(row["sweat_rate_L_per_hr"])
    litres_lost = round((workout_duration_min / 60) * sweat_rate, 2)

    sodium_lost = round(litres_lost * float(row["sodium_mg"]), 1)
    potassium_lost = round(litres_lost * float(row["potassium_mg"]), 1)
    magnesium_lost = round(litres_lost * float(row["magnesium_mg"]), 1)

    return {
        "version": "v1 - CSV",
        "workout_duration_min": workout_duration_min,
        "intensity_level": intensity_level.lower(),
        "fluid_lost_litres": litres_lost,
        "sodium_lost_mg": sodium_lost,
        "potassium_lost_mg": potassium_lost,
        "magnesium_lost_mg": magnesium_lost,
        "recommended_replacement_litres": round(litres_lost * 1.5, 2),
        "data_source": "sweat_minerals.csv"
    }
from .fitness_tool_1 import calculate_water_intake
from .fitness_tool_2 import estimate_sweat_loss

TOOL_DEFINITIONS = [
    {
        "name": "calculate_water_intake",
        "description": "Calculate daily water intake target based on body weight and workout duration.",
        "func": calculate_water_intake,
    },
    {
        "name": "estimate_sweat_loss",
        "description": "Estimate fluid and mineral loss after a workout. Intensity: low, moderate, or high.",
        "func": estimate_sweat_loss,
    },
]
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
]from .fitness_tool_1 import calculate_water_intake
from .fitness_tool_2_v1 import estimate_sweat_loss
from .fitness_tool_2_v2 import estimate_sweat_loss_v2

TOOL_DEFINITIONS = [
    {
        "name": "calculate_water_intake",
        "description": "Calculate daily water intake target based on body weight and workout duration.",
        "func": calculate_water_intake,
    },
    {
        "name": "estimate_sweat_loss",
        "description": "Estimate fluid and mineral loss after a workout. Intensity: low, moderate, or high. (v1 - CSV)",
        "func": estimate_sweat_loss,
    },
    {
        "name": "estimate_sweat_loss_v2",
        "description": "Estimate fluid and mineral loss with real recovery food data from API Ninjas. (v2 - API)",
        "func": estimate_sweat_loss_v2,
    },
]
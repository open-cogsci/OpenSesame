"""Optionally repeat a cycle from a loop"""

category = "Flow control"
icon = "os-repeat_cycle"
controls = [
    {
        "label": "Repeat if",
        "tooltip": "A conditional expression that determines when the cycle is repeated",
        "type": "conditional_expression",
        "var": "condition",
        "verb": "repeat"
    }
]

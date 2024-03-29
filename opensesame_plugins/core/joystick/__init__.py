"""Collects input from a joystick or gamepad"""

authors = ["Edwin Dalmaijer", "Sebastiaan Mathot"]
category = "Response collection"
icon = "os-joystick"
controls = [
    {
        "type": "combobox",
        "var": "_dummy",
        "label": "Dummy mode (use keyboard instead of joystick)",
        "options": [
            "no",
            "yes"
        ],
        "tooltip": "Enable dummy mode to test the experiment using a keyboard"
    },
    {
        "type": "spinbox",
        "var": "_device",
        "label": "Device nr.",
        "min_val": 0,
        "max_val": 100,
        "tooltip": "Identifies the joystick, in case there are multiple joysticks"
    },
    {
        "type": "line_edit",
        "var": "correct_response",
        "label": "Correct response",
        "tooltip": "Expecting a comma-separated list of numbers between 1 and the number of joybuttons"
    },
    {
        "type": "line_edit",
        "var": "allowed_responses",
        "label": "Allowed responses",
        "tooltip": "Expecting a comma-separated list of numbers between 1 and the number of joybuttons"
    },
    {
        "type": "line_edit",
        "var": "timeout",
        "label": "Timeout",
        "tooltip": "Expecting a value in milliseconds of 'infinite'"
    }
]

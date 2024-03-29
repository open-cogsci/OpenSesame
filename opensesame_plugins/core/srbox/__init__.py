"""A plug-in for using the serial response box."""

category = "Response collection"
help_url = 'manual/response/srbox'
controls = [
    {
        "label": "Dummy mode (use keyboard instead)",
        "var": "_dummy",
        "type": "checkbox",
        "tooltip": "Enable to respond with the keyboard instead of an SR Box"
    },
    {
        "label": "Ignore buttons that are already pressed",
        "var": "require_state_change",
        "type": "checkbox",
        "tooltip": "Require a button-state change, so that already-pressed buttons are ignored"
    },
    {
        "label": "Device name",
        "var": "dev",
        "type": "line_edit",
        "tooltip": "Expecting a valid device name. Leave empty for autodetect."
    },
    {
        "label": "Correct response",
        "var": "correct_response",
        "type": "line_edit",
        "tooltip": "Expecting a button number (1 .. 5)"
    },
    {
        "label": "Allowed responses",
        "var": "allowed_responses",
        "type": "line_edit",
        "tooltip": "Expecting a semicolon-separated list of button numbers, e.g., 1;3;4"
    },
    {
        "label": "Timeout",
        "var": "timeout",
        "type": "line_edit",
        "tooltip": "Expecting a value in milliseconds or 'infinite'",
        "validator": "timeout"
    },
    {
        "label": "Turn on lights",
        "var": "lights",
        "type": "line_edit",
        "tooltip": "Expecting a semicolon-separated list of light numbers, e.g., 1;3;4"
    },
    {
        "label": "<small><b>Note:</b> If there are multiple srbox items in the experiment, the first srbox item determines the device name and whether dummy mode is enabled</small>\n",
        "type": "text"
    }
]

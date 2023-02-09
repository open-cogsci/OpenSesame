"""A grid-based response item, convenient for touch screens"""

category = "Response collection"
icon = "os-touch_response"
controls = [
    {
        "type": "line_edit",
        "var": "correct_response",
        "label": "Correct response",
        "tooltip": "Set the correct response"
    },
    {
        "type": "line_edit",
        "var": "timeout",
        "label": "Timeout",
        "tooltip": "Expecting a value in milliseconds or 'infinite'"
    },
    {
        "type": "spinbox",
        "var": "_ncol",
        "label": "Number of columns",
        "min_val": 1,
        "max_val": 100,
        "tooltip": "Specifies the number of columns"
    },
    {
        "type": "spinbox",
        "var": "_nrow",
        "label": "Number of rows",
        "min_val": 1,
        "max_val": 100,
        "tooltip": "Specifies the number of rows"
    },
    {
        "type": "checkbox",
        "var": "show_cursor",
        "label": "Show cursor",
        "tooltip": "Show a mouse cursor (if supported on device)"
    }
]

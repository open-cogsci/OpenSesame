"""A random delay sampled from either a normal or uniform distribution"""

category = "Flow control"
icon = "clock"
controls = [{
    "type": "spinbox",
    "var": "duration",
    "label": "Duration",
    "min_val": 0,
    "max_val": 1000000,
    "name": "spinbox_duration",
    "suffix": " ms",
    "tooltip": "The average duration in milliseconds"
},
    {
    "type": "spinbox",
    "var": "jitter",
    "label": "Jitter",
    "min_val": 0,
    "max_val": 1000000,
    "name": "spinbox_jitter",
    "suffix": " ms",
    "tooltip": "The jitter of the actual duration in milliseconds (depends on Jitter mode)"
},
    {
    "type": "combobox",
    "var": "jitter_mode",
    "label": "Jitter mode",
    "options": [
        "Std. Dev.",
        "Uniform"
    ],
    "name": "combobox_jitter_mode",
    "tooltip": "The mode for determining the actual duration (see Help)"
}
]

"""A simple notepad to document your experiment. This plug-in does nothing."""

category = 'Miscellaneous'
icon = 'notes'
controls = [
    {
        "type": "editor",
        "var": "note",
        "label": "Note",
        "name": "note_widget",
        "tooltip": "Type your note here",
        "info": None,
        "min_width": None,
        "prefix": "",
        "suffix": "",
        "left_label": "min.",
        "right_label": "max.",
        "syntax": False
    }
]

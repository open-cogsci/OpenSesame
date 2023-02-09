"""Shows the get-started tab and opens an experiment on startup, if one was
passed on the command line
"""
icon = "document-new"
label = "New\u2026"
priority = -1
shortcut = "Ctrl+N"
menu = {
    "index": 0,
    "separator_after": False,
    "separator_before": False,
    "submenu": "File"
}
toolbar = {
    "index": 0,
    "separator_after": False,
    "separator_before": False
}
tooltip = "Start a new experiment"

"""Implements undo/ redo"""

icon = "edit-redo"
label = "Redo"
shortcut = "Alt+Ctrl+Shift+Z"
tooltip = "Redo most recently undone action"
menu = {
    "index": 0,
    "separator_after": True,
    "submenu": "Edit"
}
toolbar = {
    "index": -1,
    "separator_before": True
}
settings = {
    "max_undo_history": 100
}

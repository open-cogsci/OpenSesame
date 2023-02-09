"""Periodically saves your experiment to a back-up folder."""

icon = "folder-open"
label = "Open backup folder"
menu = {
    "index": 1,
    "separator_after": True,
    "submenu": "Tools"
}
settings = {
    "autosave_interval": 600000,
    "autosave_max_age": 7
}

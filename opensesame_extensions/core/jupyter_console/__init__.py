"""A Jupyter console"""

label = "Show console"
tooltip = "Show Jupyter/ IPython console"
priority = 101
icon = "os-debug"
settings = {
    "jupyter_inprocess": False,
    "jupyter_visible": True,
    "jupyter_focus_shortcut": "Ctrl+3",
    "jupyter_kernels": {
        "ide": "",
        "default": "python"
    },
    "jupyter_default_kernel": "python"
}
shortcut = "Ctrl+D"
checkable = True
menu = {
    "index": 8,
    "submenu": "View"
}
toolbar = {
    "index": 13
}
modes = ["default", "ide"]

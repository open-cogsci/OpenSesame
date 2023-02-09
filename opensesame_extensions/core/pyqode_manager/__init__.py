"""Manages PyQode, the code-editor component"""

label = "PyQode manager"
priority = 101
settings = {
    "pyqode_font_size": 14,
    "pyqode_font_name": "Roboto Mono",
    "pyqode_color_scheme": "monokai",
    "pyqode_pyflakes_validation": True,
    "pyqode_pep8_validation": False,
    "pyqode_right_margin": False,
    "pyqode_highlight_caret_line": True,
    "pyqode_code_completion": True,
    "pyqode_code_completion_excluded_mimetypes": "markdown",
    "pyqode_code_folding": False,
    "pyqode_indentation": "auto",
    "pyqode_image_annotations": True,
    "pyqode_show_whitespaces": False,
    "pyqode_show_line_numbers": True,
    "pyqode_fixed_width": False,
    "pyqode_fixed_width_nchar": 80,
    "pyqode_autopep8": False,
    "pyqode_autopep8_lookbehind": 20,
    "pyqode_autopep8_aggressive": False,
    "pyqode_pep8_ignore": {
        "ide": "W191",
        "default": "W191"
    },
    "pyqode_pyflakes_ignore": {
        "ide": "",
        "default": "undefined name"
    },
    "pyqode_enable_breakpoints": {
        "ide": True,
        "default": False
    },
    "pyqode_tab_length": 4,
    "pyqode_line_wrap": True,
    "pyqode_shortcut_duplicate_line": "Ctrl+Shift+D",
    "pyqode_shortcut_swap_line_up": "Ctrl+Up",
    "pyqode_shortcut_swap_line_down": "Ctrl+Down",
    "pyqode_shortcut_toggle_breakpoint": "F12"
}
modes: ["default", "ide"]

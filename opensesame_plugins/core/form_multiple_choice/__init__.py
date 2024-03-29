"""A simple multiple choice item"""

category = "Form"
icon = "os-form_multiple_choice"
help_url = "manual/forms/readymade"
controls = [
    {
        "label": "Form title",
        "name": "line_edit_form_title",
        "tooltip": "Form title",
        "type": "line_edit",
        "var": "form_title"
    },
    {
        "label": "Response variable",
        "tooltip": "Response variable",
        "type": "line_edit",
        "var": "form_var"
    },
    {
        "label": "Allow multiple options to be selected",
        "name": "checkbox_allow_multiple",
        "tooltip": "Allow multiple options to be selected",
        "type": "checkbox",
        "var": "allow_multiple"
    },
    {
        "label": "Advance immediately to the next item once a selection has been made",
        "name": "checkbox_advance_immediately",
        "tooltip": "Advance immediately to the next item once a selection has been made",
        "type": "checkbox",
        "var": "advance_immediately"
    },
    {
        "label": "Button text",
        "name": "line_edit_button_text",
        "tooltip": "Text for the button to advance to the next item",
        "type": "line_edit",
        "var": "button_text"
    },
    {
        "label": "Timeout",
        "name": "line_edit_timeout",
        "tooltip": "Response timeout",
        "type": "line_edit",
        "validator": "timeout",
        "var": "timeout"
    },
    {
        "label": "Your question",
        "name": "editor_widget_question",
        "syntax": False,
        "tooltip": "Your question",
        "type": "editor",
        "var": "question"
    },
    {
        "label": "Response options (different options on different lines)",
        "name": "editor_widget_options",
        "syntax": False,
        "tooltip": "Response options",
        "type": "editor",
        "var": "options"
    }
]

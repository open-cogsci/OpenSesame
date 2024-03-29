"""A simple text input form"""

category = "Form"
icon = "os-form_text_input"
help_url = "manual/forms/readymade"
controls = [
    {
        "label": "Form title",
        "tooltip": "Title to appear above the form text",
        "type": "line_edit",
        "var": "form_title"
    },
    {
        "label": "Response variable",
        "tooltip": "The experimental variable to save the response in",
        "type": "line_edit",
        "var": "form_var"
    },
    {
        "label": "Timeout",
        "tooltip": "A response timeout",
        "type": "line_edit",
        "validator": "timeout",
        "var": "timeout"
    },
    {
        "label": "Your question",
        "tooltip": "A question text",
        "type": "editor",
        "var": "form_question"
    }
]

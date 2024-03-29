"""A simple text display form"""

category = "Form"
icon = "os-form_text_display"
help_url = "manual/forms/readymade"
controls = [
    {
        "type": "line_edit",
        "var": "form_title",
        "label": "Form title",
        "tooltip": "Title to appear above the form text"
    },
    {
        "type": "line_edit",
        "var": "ok_text",
        "label": "Ok-button text",
        "tooltip": "Text for the Ok button"
    },
    {
        "type": "editor",
        "var": "form_text",
        "label": "Main form text",
        "tooltip": "Text to display in the form body"
    }
]

"""A simple consent form"""

category = "Form"
icon = "os-form_consent"
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
        "var": "checkbox_text",
        "label": "Checkbox text",
        "tooltip": "Text for the checkbox"
    },
    {
        "type": "line_edit",
        "var": "accept_text",
        "label": "Accept-button text",
        "tooltip": "Text for the accept button"
    },
    {
        "type": "line_edit",
        "var": "decline_text",
        "label": "Decline-button text",
        "tooltip": "Text for the decline button"
    },
    {
        "type": "line_edit",
        "var": "decline_message",
        "label": "Message on decline",
        "tooltip": "A message shown when the participant declines"
    },
    {
        "type": "editor",
        "var": "form_text",
        "label": "Consent form text",
        "tooltip": "Text to display in the form body"
    }
]

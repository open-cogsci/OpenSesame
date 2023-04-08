"""Updates the Quest test value based on a response"""

category = "Staircase"
controls = [
    {
        "type": "line_edit",
        "var": "response_var",
        "label": "Response variable",
        "info": "Responses should be coded as 0 (incorrect) or 1 (correct)"
    },
    {
        "type": "line_edit",
        "var": "quest_name",
        "label": "Name",
        "info": "Should match a name specified in a quest_staircase_init"
    }
]

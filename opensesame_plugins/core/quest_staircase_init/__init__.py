"""Initializes a new Quest staircase procedure"""

category = "Staircase"
controls = [
    {
        "type": "line_edit",
        "var": "t_guess",
        "label": "Estimated threshold",
        "info": "Used for initial test value"
    },
    {
        "type": "line_edit",
        "var": "t_guess_sd",
        "label": "Std. dev. of estimated threshold",
    },
    {
        "type": "line_edit",
        "var": "p_threshold",
        "label": "Target",
        "info": "Desired proportion of correct responses"
    },
    {
        "type": "line_edit",
        "var": "beta",
        "label": "\u03b2",
        "info": "Steepness of the Weibull psychometric function"
    },
    {
        "type": "line_edit",
        "var": "delta",
        "label": "\u03b4",
        "info": "Proportion of random responses at maximum stimulus intensity"
    },
    {
        "type": "line_edit",
        "var": "gamma",
        "label": "Chance level (\u03b3)",
    },
    {
        "type": "combobox",
        "var": "test_value_method",
        "label": "Method",
        "options": [
            "quantile",
            "mean",
            "mode"
        ],
        "tooltip": "Method to determine optimal test value"
    },
    {
        "type": "line_edit",
        "var": "min_test_value",
        "label": "Minimum test value",
    },
    {
        "type": "line_edit",
        "var": "max_test_value",
        "label": "Maximum test value",
    },
    {
        "type": "line_edit",
        "var": "var_test_value",
        "label": "Experimental variable for test value",
    },
    {
        "type": "line_edit",
        "var": "quest_name",
        "label": "Name",
        "info": "Use different names to run multiple independent Quest procedures"
    }
]

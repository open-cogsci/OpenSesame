# Logger items

*The one rule to rule them all is: Always triple-check whether all relevant variables are logged!*

The `logger` item is the primary way to log your data to file.

## Selecting variables

In the `logger` you can indicate which variables you want to log. By default, the `logger` tries to auto-detect and log all variables. This is a safe bet, but results in large logfiles that contain a lot of unnecessary information. If you uncheck the auto-detect option, you can select variables from a list that contains all variables that OpenSesame is aware of. If, for some reason, the variable that you want to log does not appear in the list, you can add it using the 'Add custom variable' button. If you are unsure which variables you want to log, you can click on the Smart select button, which will select variables that are likely to be of interest.

## Options

- *Use 'NA' for variables that have not been set* indicates that the `logger` should not throw an exception when it tries to log a non-existent variable. Instead, it will log the value 'NA' (for 'not available'). This can be useful when you want to log a variable that has not been set the first time that the `logger` item is called, for example because that variable is only applicable to the last part of your experiment.
- *Automatically detect and log all variables* indicates that the `logger` should auto-detect and log all variables.
- *Put quotes around values* indicates that fields in the logfile should be quoted using double quotes.

## Format of the logfile

The logfile is in plain-text, comma-separated format. This format can be opened in most text-editors (although Windows Notepad may not handle the line-endings properly) and spreadsheets.

For more information, see:

- <http://osdoc.cogsci.nl/usage/logging/>

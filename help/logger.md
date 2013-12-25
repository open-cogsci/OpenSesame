# Logger items

*Always triple-check whether OpenSesame has logged all relevant variables!*

The logger item is the primary way to log your data to file.

## Selecting variables

In the logger item you can indicate which variables you wish to log. By default the logger tries to auto-detect and log all variables. This is a safe bet, but results in large datafiles, with a lot of unnecessary information. If you uncheck the auto-detect option, you can select variables from a list that contains all variables that OpenSesame is aware of. If, for some reason, the variable that you want to log does not appear in the list, you can add it using the 'Add custom variable' button. If you are unsure which variables you want to log, you can click on the Smart select button, which will select all variables that are likely to be of interest.

## Options

- *Use 'NA' for variables that have not been set* indicates that the logger should not throw an exception when a variable has not been set. This can be useful when you want to log a variable that has not been set the first time that the logger item is called.
- *Automatically detect and log all variables* indicates that the logger should auto-detect and log all variables.
- *Put quotes around values* indicates that fields in the logfile should be put in quotes.

## Format of the logfile

The logfile is in plain-text, comma-separated format. This format can be viewed in most text-editors (although Windows Notepad may not handle the line-endings properly) and spreadsheets.

For more information, see:

- <http://osdoc.cogsci.nl/usage/logging/>

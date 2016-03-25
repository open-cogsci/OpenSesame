# Logger items

*The one rule to rule them all is: Always triple-check whether all relevant variables are logged!*

The `logger` is the primary way to log your data to file.

## Logging all variables

By default, OpenSesame detects which variables exist, and logs them all. This is safe and generally recommended. But it also results in large log files that contain many unnecessary variables. To get a cleaner log file, you can disable the 'Log all variables' option, and explicitly indicate which (custom) variables you want to log.

## Custom variables

You can log custom variables by clicking on the 'Add custom variable' button, or by dragging variables from the Variable Inspector onto the table in the `logger` item.

The two main reasons to do this are:

- You have disabled the 'Log all variables' option, and therefore need to explicitly indicate which variables you want to log.
- Some variables are not detected automatically, and you therefore need to indicate explicitly that you want to log them.

## Format of the log file

The log file is in plain-text, comma-separated format. This format can be opened in most text-editors and spreadsheets. You can merge and convert log files using the DataMerger program, which can be downloaded for free.

For more information, see:

- <http://osdoc.cogsci.nl/usage/logging/>

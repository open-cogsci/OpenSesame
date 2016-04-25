title: Doing things in sequence

The `sequence` item has two important functions:

- It runs multiple other items one after another.
- It determines which items should, and which shouldn't, be run.

`sequence`s are run from top to bottom; that is, the item at the top is run first.

## Run-if statements

You can use run-if statements to determine whether or not a particular item should be run. For example, if you want a display to be presented only if a participant has made an incorrect response, you can set the Run-if statement for that item to:

	[correct] = 0

If you leave the Run-if statement empty or enter 'always', the item will always be run.

*Important:* Run-if statements only affect which items are run, not which items are prepared. Phrased differently, the prepare phase of all items in a `sequence` is always executed, regardless of the run-if statement.

Run-if statements use the same syntax as all OpenSesame conditional statements. For more information, see:

- /manual/ifstatements

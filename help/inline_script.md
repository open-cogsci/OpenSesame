# Inline_script items

You can do a lot with the graphical interface of OpenSesame, but for certain complex tasks you will have to use scripting/ programming. This is where the `inline_script` item comes in. You can use regular [Python] code in your `inline_script`. Python is a modern, powerful, high-level programming language. There are numerous libraries available for Python, so there is really no limit to what you can do using `inline_script` items.

For more information about using Python scripting, see:

- <http://osdoc.cogsci.nl/python/about/>

## A tab to prepare and a tab to run

The `inline_script` item contains two scripts. The *Prepare* phase script is called first, before the `sequence` that contains the `inline_script` is executed. This allows you to do perform some time-consuming tasks in advance, so that the *Run* phase goes smoothly. The *Run* phase script is called during the actual running of the sequence that the `inline_script`
is part of. So if you want to present a stimulus display in your `inline_script`, it is good practice to construct the display in the *Prepare* phase and show it in the *Run* phase. Note that this is purely a convention, from which you can deviate as circumstances dictate.

For more information about the prepare-run strategy, see:

- <http://osdoc.cogsci.nl/usage/prepare-run/>

## Printing debug output

You can print to the debug window using the Python `print` statement/ function:

	print('This will appear in the debug window!')

In general, the debug window functions as the standard output while the experiment is running.

[python]: http://www.python.org/
# Sequence items

In an experiment, you generally have a number of events that occur sequentially. For example, in a trial, you may present a fixation point, followed by a number of stimulus displays, followed in turn by response collection and response logging. This is where the `sequence` item comes in.

## Sequences are sequential

`sequence`s are run from top to bottom, i.e. the first item is the item that is presented at the top. You can change the order of the `sequence` by picking up items by their grab handle (on the left) and dragging them to a new position. You can remove items from a `sequence` by right-clicking an item and selecting 'Delete'.

## Appending items to the sequence

You can add items to a `sequence` by clicking on the buttons at the bottom of the tab. The *Append existing item* button appends an existing item to the sequence table, without creating a new item. This way you can add a single item (a fixation dot display, say) multiple times to a `sequence`. The *Append new item* button creates a new item and appends it to the `sequence`.

## Run-if statements

A very convenient feature of the sequence item is that you can use conditional ('if') statements to determine whether or not a particular item should be executed. For example, if you want a display to be presented only if a participant has made an incorrect response, you can set the Run-if statement to

	[correct] = 0

If you leave the Run-if statement empty or enter 'always', the item will always be executed.

For more information, see also:
	
- <http://osdoc.cogsci.nl/usage/variables-and-conditional-statements/#usingconditionalifstatements>

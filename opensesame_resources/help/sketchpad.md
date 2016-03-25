# Sketchpad items

The `sketchpad` item is the main way to present visual stimuli. The `sketchpad` provides simple built-in drawing tools that allow you to very easily draw stimulus displays.

## Duration

The *Duration* entry can be set to any positive numeric value which reflects the duration of the sketchpad in ms. If you want no duration, for example because the next item is a `keyboard_response`, you can enter '0'. You can also enter 'keypress' or 'mouseclick' to show a `sketchpad` until a key is pressed or a mouse button is clicked, respectively.

Note that your experiment will pause for the duration of a `sketchpad` item, and will not automagically start collecting responses. Therefore, if you want to collect the responses to a `sketchpad`, you generally set its *Duration* to 0 ms, and have it followed by a `keyboard_response` item. This principle is demonstrated in the online [tutorials].

## Show-if statements

You can use the Show-if field in the `sketchpad` to specify conditions under which elements should be shown. For example, if you want to have the direction of an arrow depend on the variable `cue`, you could draw two arrows and use `[cue] = left` and `[cue] = right` show-if statements to determine which arrow should be shown on a given trial.

For more information, see:
	
- <http://osdoc.cogsci.nl/usage/variables-and-conditional-statements/#usingconditionalifstatements>

## Sketchpad items are prepared in advance, feedback items are not

For performance considerations, a `sketchpad` is prepared before the execution of the `sequence` that it is part of. Therefore, its contents cannot depend on what happens during the `sequence` (after the `sketchpad` has already been prepared). This is not the case for `feedback` items, which are prepared at runtime and can therefore be used to provide immediate feedback to participants.

[tutorials]: http://osdoc.cogsci.nl/tutorials/

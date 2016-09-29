# Repeat_cycle

This plug-in allows you to repeat cycles from a `loop`. Most commonly, this will be to repeat a trial when a participant made a mistake or was too slow.

For example, to repeat all trials on which a response was slower than 3000 ms, you can add a `repeat_cycle` item after (typically) the `keyboard_response` and add the following repeat-if statement:

	[response_time] > 3000

You can also force a cycle to be repeated by setting the variable `repeat_cycle` to 1 in an `inline_script`, like so:

	var.repeat_cycle = 1

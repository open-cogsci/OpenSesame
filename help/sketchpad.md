**Sketchpad items** {.western}
===================

Generally, an experiment will consist of stimulus displays based on
which a participant makes a response. For example, you may present
strings of text, geometric shapes or bitmap images. This is where the
sketchpad item comes in.

The sketchpad provides simple built-in **drawing tools**, which allow
you to very easily draw stimulus displays.

The sketchpad also has an option **Start response interval**. If you
select this option, OpenSesame will start timing from moment the
sketchpad is presented. This is convenient if you want to record
response time from the presentation of a particular sketchpad.

The **Duration** entry can be set to any positive numeric value which
reflects the duration of the sketchpad in ms. If you want no duration,
for example because the next is a keyboard\_response, you can enter '0'.
You can also enter 'keypress' or 'mouseclick' to show the sketchpad
until a key is pressed or a mouse button is clicked, respectively.

**Conditional statements (show if ...)** {.western}
----------------------------------------

You can use the 'Show if' input field in the sketchpad to specify
conditions under which items should be shown/ hidden. For example, if
you want to have the direction of an arrow depend on the 'cue' variable,
you could draw two arrows and use '[cue] = left' and '[cue] = right'
conditions to determine which arrow should be shown on a given trial.

For performance considerations, a sketchpad is prepared before the
execution of the sequence that it is part of. Therefore, conditional
statements cannot depend on what happens during the sequence (after the
sketchpad has been prepared). This is not the case for feedback items,
which are prepared 'at runtime' and can therefore be used to provide
immediate feedback to participants.

Examples of valid conditional statements are (note that no quotes are
required and that variable names should be placed between square
brackets):

-   always

-   never

-   [variable\_name] = value

-   [variable\_name] != value or [another\_variable\_name] =
    another\_value

-   2 \> 1 and 1 \< 2

For more information about conditional statements, see
\<[http://osdoc.cogsci.nl/usage/variables-and-conditional-qifq-statements](http://osdoc.cogsci.nl/usage/variables-and-conditional-qifq-statements)\>.

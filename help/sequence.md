Sequence items {.western}
==============

In an experiment you will often have a number events that occur
sequentially. For example, you may present, in each trial, a fixation
point, followed by a number of stimulus displays and, finally, perform
response collection and response logging. This is where the sequence
item comes in. Another use for a sequence is as the 'main sequence' of
the experiment.

Order of the sequence {.western}
---------------------

Sequence items are run from top to bottom, i.e. the first item is the
item that is presented at the top. You can move and remove sequence
items using the corresponding buttons on the right of the tab. You can
remove items from the sequence by clicking on the **Remove** button.
This removes the item only from the current sequence.

Appending items to the sequence {.western}
-------------------------------

You can add items to the sequence by clicking on the buttons at the
bottom of the tab. The **Append** **existing item** button appends an
entry to the sequence table, but does not create a corresponding new
item. This way you can add a single item (a fixation dot display, say)
multiple times to a sequence. The **Append new item** button creates a
new items and appends it to the sequence.

**Conditional statements (run if...)** {.western}
--------------------------------------

A very convenient feature of the sequence item is that you can use
conditional ('if') statements. For example, if you want a display to be
presented only if a participant has made an incorrect response (during a
previously called keyboard\_response or mouse\_response item), you can
add '[correct] = 0' to the **Run if** entry of your item (for example, a
sketchpad containing the text 'pay attention!'). If you leave the **Run
if** entry empty or enter 'always', the item will always be called.

Examples of valid conditional statements are (note that no quotes are
required and that variable names should be placed between square
brackets):

-   always

-   never

-   [variable\_name] = value

-   [variable\_name] != value or [another\_variable\_name] =
    another\_value

-   2 \> 1 and 1 \< 2

For more information about conditional statements, go to
\<[http://osdoc.cogsci.nl/usage/variables-and-conditional-qifq-statements](http://osdoc.cogsci.nl/usage/variables-and-conditional-qifq-statements)\>.

\


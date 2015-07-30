# Loop items

A `loop` item calls another item (the 'item to run') multiple times, while varying your independent variables. `loop`s are the main way to define independent variables, and to divide your experiment into trials and blocks.

## The loop table

In the `loop` table you can specify variables, each of which corresponds to a single column. The rows in the table correspond to cycles. A cycle corresponds to a 'level' or one unique combination of independent variables. You can specify the number of cycles by entering a number in the *cycles* input field. The *repeat* option corresponds to the number of times that all cycles should be executed. You can set this to a non-integer value. For example, by setting repeat to 0.5, half of all cycles will be executed.

The *order* option indicates whether the cycles should be executed sequentially or in random order. Randomization is complete, in the sense that the complete list of `number-of-cycles x repeat` trials is randomized.

If you check *Show advanced options*, three more options become visible:

- *Break if* is a conditional statement that allows you to specify a stop criterion. For example, if you enter `[correct] = 1`, the `loop` will be aborted when the participants provides a correct response.
- *At loop start, skip the first [X] cycle(s)* allows you to specify how many cycles should be skipped. For example, if you set this value to '2', the `loop` will skip the first two cycles and start at cycle 3. This options is only available when *order* is set to 'sequential'.
- If you check *Run skipped cycles at end of loop (offset mode)*, the cycles that are skipped initially, as specified above, are still executed at the end of the `loop`.

## Using Python functions

Most of the time you will enter static values into the `loop` table. For example, you may have a variable called `cue`, which is either 'right' or 'left'. However, you can also use functions instead of static values. This is indicated by prepending an '=' character. For example, to draw a random number between 0 and 100, you can enter the following into a cell in the loop table:

	=randint(0,100)

More generally,you can enter any valid Python statement after the '=' sign. See also:

- <http://osdoc.cogsci.nl/python/about/>

## Convenient ways of creating a large loop table

If you have multiple variables with multiple levels, it is a daunting task to create an entire full-factorial `loop` table by hand. In this case you can use the variable wizard, which can be started by clicking on the *Variable wizard* button at the top right of the `loop` table. In the variable wizard you can specify your variables and the levels of your variables to quickly create a full-factorial design. You can also prepare your `loop` variables in your favorite spreadsheet (e.g., OpenOffice Calc or Microsoft Excel) and paste them into the `loop` table.

Fore more information, see:

- <http://osdoc.cogsci.nl/usage/variables-and-conditional-statements/>

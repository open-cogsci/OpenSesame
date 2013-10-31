Loop items
==========

A loop item calls another item (the 'item to run') multiple times, while
varying your independent variables. Loop items are the main way to
define independent variables, and to divide your experiment into trials
and blocks.

The loop table
--------------

In the loop table you can specify variables, which are displayed as
columns. You can add and remove variables using the add variable and
remove variable buttons. The rows in the table correspond to cycles. A
cycle corresponds to a 'level' or one unique combination of independent
variables. You can specify the number of cycles by entering a number in
the cycles input field. The repeat option corresponds to the number of
times that all cycles should be executed. You can set this to a
non-integer value. For example, by setting repeat to 0.5, half of all
cycles will be executed.

The order option indicates whether the cycles should be executed
sequentially or in random order. Randomization is complete, in the sense
that the complete list of [number of cycles] x [repeat] trials is
randomized. If the order is set to 'sequential', you have two more
options. The skip option allows you to skip the first X number of
cycles. This can be convenient, for example when you want to resume a
previously interrupted session. You can also check the offset mode
checkbox. If offset mode is enabled, the skipped cycles are not really
skipped, but executed at the end of the loop. This can be convenient if
you want each participant to start at a different cycle, but to keep the
overall length of the loop equal. Using functions Most of the time you
will enter static values into the loop table. For example, you may have
a variable called 'cue', which is either 'right' or 'left'. However, you
can also use functions instead of static values. This is handled,
similarly as in most spreadsheets, by prepending an '=' character. For
example, to draw a random number between 0 and 100, you can enter the
following into a cell in the loop table: =randint(0,100) More
generally,you can enter any valid Python statement after the '=' sign.
An overview of of useful functions can be found in the Python
documentation: Random functions:
http://docs.python.org/library/random.html Mathematical:
http://docs.python.org/library/math.html Convenient ways of creating a
large loop table If you have multiple variables, each with multiple
levels, it is a daunting task to manually create the entire loop table.
In this case you may want to use the variable wizard, which can be
started by clicking on the variable wizard button at the top right of
the table. In the variable wizard you can specify your variables and the
levels of your variables. OpenSesame will automatically fill the loop
table with all possible combinations. You can also prepare your loop
variables in your favorite spreadsheet (e.g., OpenOffice Calc or
Microsoft Excel) and paste it into the loop table. Fore more
information, visit the website .

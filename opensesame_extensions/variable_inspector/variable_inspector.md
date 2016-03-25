# The variable inspector

The variable inspector provides lists all variables that are detected by OpenSesame.

## Real and hypothetical variables

OpenSesame knows that items usually create certain variables. For example, a `keyboard_response` usually creates a `response` variable. Therefore, if you have a `keyboard_response` item in your experiment, you will see the `response` variable in the variable inspector, even though that variable doesn't exist yet; at that moment, `response` is a hypothetical variable.

Once the experiment is running (or has finished), `response` has likely been created; at that moment, `response` is a real variable.

The variable inspector shows real variables in bold face, and hypothetical variables in regular face (i.e. not bold).

## Live inspection

If you run the experiment using the (default) `multiprocess_runner`, the variable inspector is updated while the experiment is running; that is, you can see the values changing in real time. This is convenient for debugging.

When the experiment is finished, the variable inspector shows the state of the experiment as it was when it finished. Again, this is convenient for debugging. You can view the variables of the current experiment by pressing the 'Reset workspace' button, as indicated in the variable inspector.

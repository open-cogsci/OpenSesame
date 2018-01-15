# External_script

The `external_script` item is an alternative way to include Python code in your experiment. Whereas the `inline_script` allows you to enter Python code directly, the `external_script` item runs a Python script from a file.

## Options

- *Script file* is the name of the Python script that is executed.
- *Prepare function in script* is the name of the function in the script that is called (without parameters) during the prepare phase.
- *Run function in script* is the name of the function in the script that is called (without parameters) during the run phase.

## Script execution and Python workspace

The script is executed in the same Python workspace that is used for `inline_script` items. This means that you can access all the regular objects  and functions, just like you could from an `inline_script`.

When the plug-in is first initialized (during the first prepare phase), the entire script is executed.

## Example

Consider the following script, assuming that you use `prepare` and `run` as the functions to run:

~~~ .python
print('This will be shown when the plug-in is initialized')

def prepare():

    print('This will be shown during the prepare phase')
    global c
    c = Canvas()
    c.fixdot()

def run():

    print('This will be shown during the run phase')
    global c
    c.show()
    clock.sleep(1000)
    c.clear()
    c.show()
~~~

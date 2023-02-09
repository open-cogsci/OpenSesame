# OpenSesame help

*This is the offline help page. If you are connected to the Internet,
you can find the online documentation at <http://osdoc.cogsci.nl>.*

## Introduction

OpenSesame is a graphical experiment builder for the social sciences. With OpenSesame you can easily create experiments using a point-and-click graphical interface. For complex tasks, OpenSesame supports [Python] scripting.

## Getting started

The best way to get started is by walking through a tutorial. Tutorials, and much more, can be found online:

- <http://osdoc.cogsci.nl/tutorials/>

## Citation

To cite OpenSesame in your work, please use the following reference:

- Mathôt, S., Schreij, D., & Theeuwes, J. (2012). OpenSesame: An open-source, graphical experiment builder for the social sciences. *Behavior Research Methods*, *44*(2), 314-324. doi:[10.3758/s13428-011-0168-7](http://dx.doi.org/10.3758/s13428-011-0168-7)

## Interface

The graphical interface has the following components. You can get
context-sensitive help by clicking on the help icons at the top-right of
each tab.

- The *menu* (at the top of the window) shows common options, such as opening and saving files, closing the program, and showing this help page.
- The *main toolbar* (the big buttons below the menu) offers a selection of the most relevant options from the menu.
- The *item toolbar* (the big buttons on the left of the window) shows available items. To add an item to your experiment, drag it from the item toolbar onto the overview area.
- The *overview area* (Control + \\) shows a tree-like overview of your experiment.
- The *tab area* contains the tabs for editing items. If you click on an item in the overview area, a corresponding tab opens in the tab area. Help is displayed in the tab area as well.
- The [file pool](opensesame://help.pool) (Control + P) shows files that are bundled with your experiment.
-   The [variable inspector](opensesame://help.extension.variable_inspector) (Control + I) shows all detected variables.
-   The [debug window](opensesame://help.stdout). (Control + D) is an [IPython] terminal. Everything that your experiment prints to the standard output (i.e. using `print()`) is shown here.

## Items

Items are the building blocks of your experiment. Ten core items provide basic functionality for creating an experiment. To add items to your experiment, drag them from the item toolbar into the overview area.

- The [loop](opensesame://help.loop) item runs another item multiple times. You can also define independent variables in the LOOP item.
- The [sequence](opensesame://help.sequence) item runs multiple other items in sequence.
- The [sketchpad](opensesame://help.sketchpad) item presents visual stimuli. Built-in drawing tools allow you to easily create stimulus displays.
- The [feedback](opensesame://help.feedback) item is similar to the `sketchpad`, but is not prepared in advance. Therefore, FEEDBACK items can be used to provide feedback to participants.
- The [sampler](opensesame://help.sampler) item plays a single sound file.
- The [synth](opensesame://help.synth) item generates a single sound.
- The [keyboard_response](opensesame://help.keyboard_response) item collects key-press responses.
- The [mouse_response](opensesame://help.mouse_response) item collects mouse-click responses.
- The [logger](opensesame://help.logger) item writes variables to the log file.
- The [inline_script](opensesame://help.inline_script) embeds Python code in your experiment.

If installed, plug-in items provide additional functionality. Plug-ins appear alongside the core items in the item toolbar.

## Running your experiment

You can run your experiment in:

- Full-screen mode (*Control+R* or *Run -> Run fullscreen*)
- Window mode (*Control+W* or *Run -> Run in window*)
- Quick-run mode (*Control+Shift+W* or *Run -> Quick run*)

In quick-run mode, the experiments starts immediately in a window, using log file `quickrun.csv`, and subject number 999. This is useful during development.

[python]: http://www.python.org/
[ipython]: http://www.ipython.org/

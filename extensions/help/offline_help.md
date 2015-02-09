# OpenSesame help

*This is the offline help page. If you are connected to the Internet,
you can find the online documentation at <http://osdoc.cogsci.nl>.*

## Introduction

OpenSesame is a graphical experiment builder for the social sciences. With OpenSesame you can easily create experiments using a point-and-click graphical interface. For complex tasks, OpenSesame supports [Python] scripting.

## Getting started

The best way to get started is by walking through one of the tutorials. These, and much more, can be found online:

- <http://osdoc.cogsci.nl/tutorials/>

## Citation

To cite OpenSesame in your work, please use the following reference:

Mathôt, S., Schreij, D., & Theeuwes, J. (2012). OpenSesame: An open-source, graphical experiment builder for the social sciences. *Behavior Research Methods*, *44*(2), 314-324. doi:[10.3758/s13428-011-0168-7](http://dx.doi.org/10.3758/s13428-011-0168-7)

## Interface

The graphical interface consists of the following components. You can get
context-sensitive help by clicking on the help icons at the top-right of
each tab.

- The *menu* (at the top of the window) offers a variety of options, such as opening and saving files, inserting items (see below), and checking for updates. The menu cannot be hidden or closed.
- The *main toolbar* (the big buttons below the menu) offers a selection of the most relevant options from the menu. The main toolbar cannot be hidden, but can be moved or detached from the main window.
- The *item toolbar* (the big buttons on the left of the window) displays a list of available items. You can drag items from the item toolbar into the overview of the experiment. The item toolbar cannot be hidden, but it can be moved or detached from the main window.
- The *overview area* provides an overview of your experiment. The structure of the experiment is visualized as a tree. The overview item can be hidden, moved, and detached from the main window.
- The *tab area* contains the tabs that are used to edit the experiment. If you click on an item in the overview area, a corresponding tab will be opened in the tab area. Help is displayed in the tab area as well. The tab area cannot be moved or hidden.
- The *file pool* (Control + P) provides an overview of the files that are bundled with your experiment. If you save your experiment in `.opensesame.tar.gz` format, the file pool will be saved along with your experiment. The file pool can be hidden, moved, and detached from the main window.
-   The *variable inspector* (Control + I) provides an overview of the variables that are used in your experiment. The variable inspector can be hidden, moved, and detached from the main window.
-   The *debug window*. (Control + D) shows the messages that are written to the standard output during an experiment. This is mostly useful for debugging `inline_script` items. A Python interpreter is provided as well. The debug window can be hidden, moved, and detached from the main window.

## Items

Items are the building blocks of your experiment. There are ten core items that provide the basic functionality that is necessary to create an experiment. Core items can be dragged into to your experiment from the item toolbar.

- The `loop` item runs another item multiple times. You can also define independent variables in the `loop` item.
- The `sequence` item runs multiple other items in sequence.
- The `sketchpad` item presents visual stimuli. A built-in drawing tool allows you to easily create stimulus displays.
- The `feedback` item is similar to the `sketchpad`, but is not prepared in advance. Therefore, `feedback` items can be used to present feedback to the participants.
- The `sampler` item plays back a single sound file.
- The `synth` item generates a single sound.
- The `keyboard_response` item collects keypress responses.
- The `mouse_response` item collects mouseclick responses.
- The `logger` item writes variables to the log file.
- The `inline_script` item allows you to execute Python code and offers a built-in programming editor.

If installed, plug-in items provide additional functionality. Plug-ins appear alongside the core items in the item toolbar. An
overview of available plug-ins can be found online:
	
- <http://osdoc.cogsci.nl/plug-ins/list-of-available-plug-ins/>

## Running your experiment

You can run your experiment in full-screen mode (*Control+R* or *Run -> Run fullscreen*), in a window (*Control+W* or *Run -> Run in window*), or in quick-run mode (*Control+Shift+W* or *Run -> Quick run*). When the 'auto-response' option (*Run -> Enable auto-response*) is enabled, OpenSesame will simulate keypress and mouseclick responses, which can be useful when testing your experiment.

## Saving your experiment

Experiments can be saved in two file formats:

- An `.opensesame` file contains only the experiment script. Therefore, the file pool will not be saved along with your experiment when saving in `.opensesame` format. The `.opensesame` format is a plain-text format.
- An `.opensesame.tar.gz` file contains the experiment script and all the files from the file pool. The `.opensesame.tar.gz` format is a `.tar.gz` compressed archive, which can be opened with most file compression utilities.

[python]: http://www.python.org/
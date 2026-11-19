# Unit tests

The unit tests are organized into three groups of sub-tests, which correspond
to the three sub-folders of the `tests` folder:

- `basic/` — Basic functionality that does not require a running experiment
  or a graphical user interface. This includes the syntax tests, the
  read/write tests, the color tests, etc. These tests are fast and can be
  run anywhere.
- `headless/` — Full experiments are executed headless (i.e. on a virtual,
  offscreen display) to check that the full runtime works. All rendering is
  emulated (`SDL_VIDEODRIVER=dummy` for the legacy backend, offscreen Qt),
  so no real display is needed and no windows are opened on the user's
  desktop.
- `gui/` — The PyQt graphical user interface. These tests start the actual
  application on an offscreen (virtual) display
  (`QT_QPA_PLATFORM=offscreen`), so no X server or Wayland session is
  needed, and no windows are opened on the user's desktop.

Shared configuration for all three groups lives in the `config/` folder, and
example experiments and other test data live in the `data/` folder.

To run all tests:

~~~
pytest tests
~~~

To run a single group:

~~~
pytest tests/basic
pytest tests/headless
pytest tests/gui
~~~

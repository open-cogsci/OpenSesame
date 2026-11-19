# Unit tests

The unit tests are organized into three groups of sub-tests, which correspond
to the three sub-folders of the `tests` folder:

- `basic/` — Basic functionality that does not require a running experiment
  or a graphical user interface. This includes the syntax tests, the
  read/write tests, the color tests, etc. These tests are fast and can be
  run anywhere.
- `headless/` — Full experiments are executed headless (i.e. on a virtual
  display) to check that the full runtime works. These tests take a bit
  longer and require a virtual X server, or offscreen windowing, when no
  real display is available.
- `gui/` — The PyQt graphical user interface. These tests run the actual
  application on a virtual (offscreen) display. They require the Qt
  dependencies, and currently `QT_QPA_PLATFORM=offscreen` is used so that
  no real display is needed.

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

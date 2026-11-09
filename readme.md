# OpenSesame

OpenSesame is a tool to create experiments for psychology, neuroscience, and experimental economics.

Copyright, 2010-2026, Sebastiaan Mathôt and contributors.

<http://osdoc.cogsci.nl/>


## About

OpenSesame is a graphical experiment builder. OpenSesame provides an easy to use, point-and-click interface for creating psychological/ neuroscientific experiments.


## Features

- A user-friendly interface — a modern, professional, and easy-to-use graphical interface
- Online experiments — run your experiment in a browser with OSWeb
- AI — develop your experiments together with [SigmundAI](https://sigmundai.eu/)
- Python — add the power of Python to your experiment
- JavaScript — add the power of JavaScript to your experiment
- Use your devices — use your eye tracker, button box, EEG equipment, and more.
- Free — released under the GPL3
- Crossplatform — Windows, Mac OS, and Linux


## Related repositories

OpenSesame relies on a number repositories that are all hosted by the [Cogsci.nl](https://github.com/open-cogsci/) organization on GitHub. The most important of these are:

- [opensesame](https://github.com/open-cogsci/opensesame) contains core OpenSesame functionality
- [sigmund analyst](https://github.com/open-cogsci/sigmund-analyst) is a code editor that provides various PyQt widgets used by OpenSesame
- [opensesame-extension-sigmund](https://github.com/open-cogsci/opensesame-extension-sigmund) integrates SigmundAI into the OpenSesame user interface
- [osweb](https://github.com/open-cogsci/osweb) implements OSWeb, the online OpenSesame runtime
- [opensesame-extension-osweb](https://github.com/open-cogsci/opensesame-extension-osweb) embeds OSWeb into the OpenSesame user interface
- [datamatrix](https://github.com/open-cogsci/python-datamatrix) implements a tabular data structure that is used by the `loop` item
- [qdatamatrix](https://github.com/open-cogsci/python-qdatamatrix) implements a Qt widget for editing datamatrix objects
- [pseudorandom](https://github.com/open-cogsci/python-pseudorandom) implements pseudorandomization/ randomization constraints


## Branches

Each major version of OpenSesame lives in its own branch.

- `gibson` - 2.8
- `heisenberg` - 2.9
- `ising` - 3.0
- `james` - 3.1
- `koffka` - 3.2
- `loewenfeld` - 3.3
- `milgram` - 4.0
- `nightingale` - 4.1


## Citations

- Mathôt, S., Schreij, D., & Theeuwes, J. (2012). OpenSesame: An open-source, graphical experiment builder for the social sciences. *Behavior Research Methods*, *44*(2), 314-324. [doi:10.3758/s13428-011-0168-7](https://doi.org/doi:10.3758/s13428-011-0168-7)
- Mathôt, S., & March, J. (2022). Conducting linguistic experiments online with OpenSesame and OSWeb. *Language Learning*. [doi:10.1111/lang.12509](https://doi.org/10.1111/lang.12509)


## License

OpenSesame is distributed under the terms of the GNU General Public License 3. The full license should be included in the file `COPYING`, or can be obtained from:

- <http://www.gnu.org/licenses/gpl.txt>

OpenSesame contains works of others. For the full license information, please refer to `debian/copyright`.


## Documentation

Installation instructions and documentation are available on the documentation website ...

- <http://osdoc.cogsci.nl/>

... which is itself also hosted on GitHub:

- <https://github.com/smathot/osdoc>


### Linux installer

The easiest way to install OpenSesame on Linux is to download and run the installer script. This will create a Virtual Environment, pip install OpenSesame and all dependencies into this environment, and add a Desktop file to your system to easily start Sigmund Analyst. To upgrade, simply run the script again.

Currently, the Linux installer is tested on Ubuntu 26.04.

```
bash <(curl -L https://github.com/open-cogsci/OpenSesame/raw/refs/heads/nightingale/linux-installer.sh) --install
```

### macOS installer (Apple Silicon and Intel)

On macOS, the pre-built `.dmg` package is currently only available for Intel Macs. Apple Silicon users can install OpenSesame natively from PyPI by downloading and running the macOS installer script. This creates a Virtual Environment, pip installs OpenSesame and its dependencies, and adds an `OpenSesame.app` launcher to `~/Applications`.

```sh
bash <(curl -L https://github.com/open-cogsci/OpenSesame/raw/refs/heads/nightingale/macos-installer.sh) --install
```

Note that the PyPI package is named `opensesame-core` (not `opensesame`, which is an unrelated package).

The installer requires Python 3.10 or later. If no suitable Python is found, install one first, for example with Homebrew:

```sh
brew install python@3.13
```

On macOS 13 and earlier, the installer automatically pins PyQt6 to version 6.11, which is the last release that supports those macOS versions. If you prefer to install manually with pip on macOS 13 or earlier, install the compatible Qt bindings first:

```
pip install "pyqt6<6.12" "pyqt6-webengine<6.12"
pip install opensesame-core
```

To run experiments with the PsychoPy backend, the installer also attempts to install `psychopy`. If that step fails, OpenSesame still works with the legacy backend.

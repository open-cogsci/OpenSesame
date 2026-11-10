#!/usr/bin/env bash
#
# macos-installer.sh
# ------------------
# Installs OpenSesame and Sigmund Analyst on macOS (both Apple Silicon and
# Intel) in a virtual environment and creates launchers.
#
# Usage:
#   ./macos-installer.sh --install     # Install OpenSesame and Sigmund Analyst
#   ./macos-installer.sh --uninstall   # Remove installations
#
# You can re-run this script with --install at any time to upgrade to a newer
# version.

set -euo pipefail

APP_NAME_OPENSESAME="opensesame-4-1"
APP_NAME_SIGMUND_ANALYST="sigmund-analyst"
VENV_DIR="$HOME/.local/venvs/${APP_NAME_OPENSESAME}"
BIN_DIR="$HOME/.local/bin"
WRAPPER_OPENSESAME="$BIN_DIR/${APP_NAME_OPENSESAME}-launch"
WRAPPER_SIGMUND_ANALYST="$BIN_DIR/${APP_NAME_SIGMUND_ANALYST}-launch"
APP_DIR="$HOME/Applications/OpenSesame.app"
ICON_DIR="$HOME/.local/share/icons"
ICON_OPENSESAME_PATH="$ICON_DIR/opensesame.svg"
ICON_OPENSESAME="https://github.com/open-cogsci/OpenSesame/raw/refs/heads/nightingale/mime/opensesame.svg"
ICON_SIGMUND_ANALYST="https://raw.githubusercontent.com/open-cogsci/opensesame-extension-sigmund/refs/heads/master/opensesame_extensions/sigmund/sigmund/sigmund.png"
ICON_SIGMUND_ANALYST_PATH="$ICON_DIR/sigmund-analyst.png"

# Function to detect if we're in a virtual environment
check_virtual_env() {
    if [[ -n "${VIRTUAL_ENV:-}" ]]; then
        echo "Error: A virtual environment is currently active: $VIRTUAL_ENV"
        echo "Please deactivate it first by running 'deactivate'"
        exit 1
    fi

    if [[ -n "${CONDA_DEFAULT_ENV:-}" ]] && [[ "${CONDA_DEFAULT_ENV}" != "base" ]]; then
        echo "Error: A conda environment is currently active: $CONDA_DEFAULT_ENV"
        echo "Please deactivate it first by running 'conda deactivate'"
        exit 1
    fi
}

# Find a suitable Python interpreter (>= 3.10) that can create a venv
find_python() {
    local candidates=(python3.13 python3.12 python3.11 python3.10 python3)
    for candidate in "${candidates[@]}"; do
        if ! command -v "$candidate" >/dev/null 2>&1; then
            continue
        fi
        local version major minor
        version=$("$candidate" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")' 2>/dev/null) || continue
        major=${version%%.*}
        minor=${version##*.}
        if [[ "$major" -ne 3 || "$minor" -lt 10 ]]; then
            continue
        fi
        # Some Python builds (for example uv-managed interpreters) cannot
        # create virtual environments with 'python -m venv'. Verify that this
        # candidate actually works before selecting it.
        local test_venv
        test_venv=$(mktemp -d "${TMPDIR:-/tmp}/opensesame-venv-test.XXXXXX")
        if "$candidate" -m venv "$test_venv" >/dev/null 2>&1; then
            rm -rf "$test_venv"
            command -v "$candidate"
            return 0
        fi
        rm -rf "$test_venv"
    done
    echo "Error: No suitable Python interpreter found (need Python >= 3.10)" >&2
    echo "Install Python from https://www.python.org or with Homebrew:" >&2
    echo "  brew install python@3.13" >&2
    return 1
}

install() {
    echo "Starting OpenSesame and Sigmund Analyst installation..."

    check_virtual_env

    local PYTHON_BIN
    PYTHON_BIN=$(find_python)
    echo "Using Python: $PYTHON_BIN ($($PYTHON_BIN --version 2>&1))"

    echo "Removing virtual environment in $VENV_DIR ..."
    rm -rf "$VENV_DIR"

    echo "Creating virtual environment in $VENV_DIR ..."
    "$PYTHON_BIN" -m venv "$VENV_DIR"

    echo "Installing packages ..."
    # shellcheck disable=SC1091
    source "$VENV_DIR/bin/activate"
    pip install --upgrade pip

    # PyQt6 6.12 and later require macOS 14. On older macOS versions, install
    # the last compatible PyQt6/Qt WebEngine release first so that pip does not
    # try (and fail) to build them from source.
    local macos_major
    macos_major=$(sw_vers -productVersion | cut -d. -f1)
    if [[ "$macos_major" -lt 14 ]]; then
        echo "macOS $macos_major detected; pinning PyQt6<6.12 for compatibility ..."
        pip install "pyqt6<6.12" "pyqt6-webengine<6.12"
    fi

    # Core OpenSesame and commonly used extensions/plugins.
    pip install \
        opensesame-core \
        opensesame-extension-osweb \
        opensesame-extension-updater \
        opensesame-plugin-media_player_mpy

    # pygame-ce provides the pygame module needed by the legacy and xpyriment
    # backends. It may not have wheels for the newest Python versions, so do
    # not abort the installation if it fails.
    if ! pip install pygame-ce; then
        echo "Warning: pygame-ce could not be installed."
        echo "OpenSesame will still work, but the legacy and xpyriment"
        echo "backends will need pygame installed separately."
    fi

    # Try to install the PsychoPy backend. This pulls in many dependencies and
    # may fail on some systems; OpenSesame remains usable with the legacy
    # backend if this step fails.
    if ! pip install psychopy --ignore-requires-python psychopy_visionscience psychopy_sounddevice; then
        echo "Warning: PsychoPy could not be installed."
        local python_minor
        python_minor=$("$PYTHON_BIN" -c 'import sys; print(sys.version_info.minor)' 2>/dev/null || echo 0)
        if [[ "$python_minor" -ge 15 ]]; then
            echo "On Python 3.15+, ffpyplayer has no prebuilt wheel and cannot be"
            echo "compiled (FFmpeg no longer ships libpostproc)."
            echo "Install Python 3.13 or 3.14 (e.g. 'brew install python@3.13')"
            echo "and re-run this script to enable the PsychoPy backend."
        else
            echo "OpenSesame will still work, but experiments that use the PsychoPy"
            echo "backend will need psychopy installed separately."
        fi
        echo "OpenSesame will still work with the legacy backend."
    fi

    deactivate

    echo "Downloading icons ..."
    mkdir -p "$ICON_DIR"
    curl -L -s -o "$ICON_OPENSESAME_PATH" "$ICON_OPENSESAME" || true
    curl -L -s -o "$ICON_SIGMUND_ANALYST_PATH" "$ICON_SIGMUND_ANALYST" || true

    echo "Creating wrapper scripts in $BIN_DIR ..."
    mkdir -p "$BIN_DIR"
    cat > "$WRAPPER_OPENSESAME" << EOF
#!/usr/bin/env bash
# Wrapper that activates the venv, then starts OpenSesame
VENV_DIR="$VENV_DIR"
source "\$VENV_DIR/bin/activate"
exec opensesame "\$@"
EOF
    chmod +x "$WRAPPER_OPENSESAME"

    cat > "$WRAPPER_SIGMUND_ANALYST" << EOF
#!/usr/bin/env bash
# Wrapper that activates the venv, then starts Sigmund Analyst
VENV_DIR="$VENV_DIR"
source "\$VENV_DIR/bin/activate"
exec sigmund-analyst "\$@"
EOF
    chmod +x "$WRAPPER_SIGMUND_ANALYST"

    echo "Creating macOS application bundle in $APP_DIR ..."
    mkdir -p "$APP_DIR/Contents/MacOS" "$APP_DIR/Contents/Resources"
    # Copy the application icon from the installed package into the bundle.
    local icon_src
    icon_src=$("$VENV_DIR/bin/python" -I -c \
        "import libqtopensesame, os; print(os.path.join(os.path.dirname(libqtopensesame.__file__), 'resources', 'opensesame.icns'))" \
        2>/dev/null || true)
    if [[ -n "$icon_src" && -f "$icon_src" ]]; then
        cp "$icon_src" "$APP_DIR/Contents/Resources/opensesame.icns"
    else
        echo "Warning: opensesame.icns not found; the app will use a generic icon."
    fi
    cat > "$APP_DIR/Contents/MacOS/OpenSesame" << EOF
#!/usr/bin/env bash
# OpenSesame launcher for macOS
VENV_DIR="$VENV_DIR"
source "\$VENV_DIR/bin/activate"
exec opensesame "\$@"
EOF
    chmod +x "$APP_DIR/Contents/MacOS/OpenSesame"
    cat > "$APP_DIR/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>OpenSesame</string>
    <key>CFBundleIdentifier</key>
    <string>org.cogsci.opensesame</string>
    <key>CFBundleName</key>
    <string>OpenSesame</string>
    <key>CFBundleDisplayName</key>
    <string>OpenSesame</string>
    <key>CFBundleIconFile</key>
    <string>opensesame</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>4.1</string>
    <key>CFBundleVersion</key>
    <string>4.1.22</string>
    <key>LSMinimumSystemVersion</key>
    <string>11.0</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
EOF

    echo
    echo "Done!"
    echo ""
    echo "You can start OpenSesame in any of these ways:"
    echo "  - Open '$APP_DIR' from Finder or Launchpad"
    echo "  - Run '$WRAPPER_OPENSESAME' from a terminal"
    echo "  - Run 'opensesame' after adding '$BIN_DIR' to your PATH"
    echo ""
    echo "Sigmund Analyst can be started with:"
    echo "  - '$WRAPPER_SIGMUND_ANALYST'"
    echo ""
    if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
        echo "Note: '$BIN_DIR' is not in your PATH. To use the command-line"
        echo "launchers, add it to your PATH, for example by adding this line"
        echo "to ~/.zshrc:"
        echo ""
        echo "  export PATH=\"$BIN_DIR:\$PATH\""
        echo ""
    fi
}

uninstall() {
    echo "Starting OpenSesame and Sigmund Analyst uninstallation..."

    if [[ -d "$VENV_DIR" ]]; then
        echo "Removing virtual environment at $VENV_DIR ..."
        rm -rf "$VENV_DIR"
    else
        echo "Virtual environment not found at $VENV_DIR (skipping)"
    fi

    for wrapper in "$WRAPPER_OPENSESAME" "$WRAPPER_SIGMUND_ANALYST"; do
        if [[ -f "$wrapper" ]]; then
            echo "Removing wrapper $wrapper ..."
            rm -f "$wrapper"
        fi
    done

    if [[ -d "$APP_DIR" ]]; then
        echo "Removing application bundle $APP_DIR ..."
        rm -rf "$APP_DIR"
    fi

    for icon in "$ICON_OPENSESAME_PATH" "$ICON_SIGMUND_ANALYST_PATH"; do
        if [[ -f "$icon" ]]; then
            echo "Removing icon $icon ..."
            rm -f "$icon"
        fi
    done

    echo "Uninstallation complete!"
}

show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --install     Install OpenSesame and Sigmund Analyst"
    echo "  --uninstall   Remove OpenSesame and Sigmund Analyst installations"
    echo "  --help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 --install"
    echo "  $0 --uninstall"
}

if [[ $# -eq 0 ]]; then
    echo "Error: No arguments provided"
    show_usage
    exit 1
fi

case "$1" in
    --install)
        install
        ;;
    --uninstall)
        uninstall
        ;;
    --help|-h)
        show_usage
        exit 0
        ;;
    *)
        echo "Error: Unknown option: $1"
        show_usage
        exit 1
        ;;
esac

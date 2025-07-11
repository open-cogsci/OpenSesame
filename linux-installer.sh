#!/usr/bin/env bash
#
# install_opensesame.sh
# --------------------------
# Installs OpenSesame and Sigmund Analyst in a virtual environment and registers
# desktop entries.
#
# Usage:
#   ./install_opensesame.sh --install    # Install OpenSesame and Sigmund Analyst
#   ./install_opensesame.sh --uninstall  # Remove installations
#
# You can re-run this script with --install at any time to upgrade to a newer version.

set -euo pipefail

APP_NAME_OPENSESAME="opensesame-4-1"
APP_NAME_SIGMUND_ANALYST="sigmund-analyst"
VENV_DIR="$HOME/.local/venvs/${APP_NAME_OPENSESAME}"
WRAPPER_OPENSESAME="$HOME/.local/bin/${APP_NAME_OPENSESAME}-launch"
WRAPPER_SIGMUND_ANALYST="$HOME/.local/bin/${APP_NAME_SIGMUND_ANALYST}-launch"
DESKTOP_FILE_OPENSESAME="$HOME/.local/share/applications/${APP_NAME_OPENSESAME}.desktop"
DESKTOP_FILE_SIGMUND_ANALYST="$HOME/.local/share/applications/${APP_NAME_SIGMUND_ANALYST}.desktop"
ICON_OPENSAME="https://github.com/open-cogsci/OpenSesame/raw/refs/heads/milgram/mime/opensesame.svg"
ICON_SIGMUND_ANALYST="https://github.com/open-cogsci/sigmund-ai/blob/master/artwork/sigmund-avatar.png?raw=true"
PYTHON_BIN="/usr/bin/python3"

# Function to detect if we're in a virtual environment
check_virtual_env() {
    # Check for active venv
    if [[ -n "${VIRTUAL_ENV:-}" ]]; then
        echo "❌  Error: A virtual environment is currently active: $VIRTUAL_ENV"
        echo "    Please deactivate it first by running 'deactivate'"
        exit 1
    fi
    
    # Check for active conda environment
    if [[ -n "${CONDA_DEFAULT_ENV:-}" ]] && [[ "${CONDA_DEFAULT_ENV}" != "base" ]]; then
        echo "❌  Error: A conda environment is currently active: $CONDA_DEFAULT_ENV"
        echo "    Please deactivate it first by running 'conda deactivate'"
        exit 1
    fi
}

# Function to detect Python version and get appropriate wxpython wheel
get_wxpython_url() {
    local python_cp_version=$("$PYTHON_BIN" -c "import sys; print(f'cp{sys.version_info.major}{sys.version_info.minor}')")
    case "$python_cp_version" in
        cp310)
            echo "https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-24.04/wxpython-4.2.3-cp310-cp310-linux_x86_64.whl"
            ;;
        cp311)
            echo "https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-24.04/wxpython-4.2.3-cp311-cp311-linux_x86_64.whl"
            ;;
        cp312)
            echo "https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-24.04/wxpython-4.2.3-cp312-cp312-linux_x86_64.whl"
            ;;
        cp313)
            echo "https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-24.04/wxpython-4.2.3-cp313-cp313-linux_x86_64.whl"
            ;;
        *)
            echo "❌  Error: Unsupported Python version: $python_version"
            echo "    Supported versions are Python 3.10 through 3.12"
            exit 1
            ;;
    esac
}

install() {
    echo "🚀 Starting OpenSesame and Sigmund Analyst installation..."
    
    # Check for active virtual environments
    check_virtual_env
    
    if ! "$PYTHON_BIN" --version &>/dev/null; then
        echo "❌  System python3 not found at $PYTHON_BIN"
        exit 1
    fi
    
    # Get appropriate wxPython URL
    WXPYTHON_URL=$(get_wxpython_url)
    
    echo "▶ Removing virtual-env in $VENV_DIR ..."
    rm -rf "$VENV_DIR"
    
    echo "▶ Creating virtual-env in $VENV_DIR ..."
    "$PYTHON_BIN" -m venv "$VENV_DIR"
    
    echo "▶ Installing packages ..."
    source "$VENV_DIR/bin/activate"
    pip install --upgrade pip
    
    # The pip-install steps are manually crafted and should not be changed
    pip install https://github.com/open-cogsci/OpenSesame/archive/refs/tags/prerelease/4.1.0a0.tar.gz
    pip install https://github.com/open-cogsci/opensesame-extension-updater/archive/refs/tags/prerelease/0.2.0a0.tar.gz
    pip install https://github.com/open-cogsci/opensesame-extension-osweb/archive/refs/tags/prerelease/2.2.7.1a0.tar.gz
    pip install "$WXPYTHON_URL"
    pip install opensesame-extension-sigmund
    pip install opensesame-plugin-psychopy
    pip install opensesame-plugin-media_player_mpy
    pip install python-pygaze
    pip install https://github.com/open-cogsci/opensesame-windows-build-scripts/raw/refs/heads/master/libs/expyriment-0.10.0+opensesame2-py3-none-any.whl
    pip install psychopy --ignore-requires-python
    pip install psychopy_visionscience psychopy_sounddevice
    deactivate
    
    echo "▶ Creating wrapper in $WRAPPER_OPENSESAME ..."
    mkdir -p "$(dirname "$WRAPPER_OPENSESAME")"
    cat > "$WRAPPER_OPENSESAME" << EOF
#!/usr/bin/env bash
# Wrapper that activates the venv, then starts OpenSesame
VENV_DIR="$VENV_DIR"
source "\$VENV_DIR/bin/activate"
exec opensesame "\$@"
EOF
    chmod +x "$WRAPPER_OPENSESAME"
    
    echo "▶ Writing desktop entry $DESKTOP_FILE_OPENSESAME ..."
    mkdir -p "$(dirname "$DESKTOP_FILE_OPENSESAME")"
    cat > "$DESKTOP_FILE_OPENSESAME" << EOF
[Desktop Entry]
Type=Application
Name=OpenSesame 4.1
Comment=OpenSesame experiment builder
Exec=$WRAPPER_OPENSESAME
Icon=accessories-text-editor
Terminal=false
Categories=Development;IDE;
StartupNotify=true
EOF
    
    echo "▶ Creating wrapper in $WRAPPER_SIGMUND_ANALYST ..."
    mkdir -p "$(dirname "$WRAPPER_SIGMUND_ANALYST")"
    cat > "$WRAPPER_SIGMUND_ANALYST" << EOF
#!/usr/bin/env bash
# Wrapper that activates the venv, then starts Sigmund-Analyst
VENV_DIR="$VENV_DIR"
source "\$VENV_DIR/bin/activate"
exec sigmund-analyst "\$@"
EOF
    chmod +x "$WRAPPER_SIGMUND_ANALYST"
    
    echo "▶ Writing desktop entry $DESKTOP_FILE_SIGMUND_ANALYST ..."
    mkdir -p "$(dirname "$DESKTOP_FILE_SIGMUND_ANALYST")"
    cat > "$DESKTOP_FILE_SIGMUND_ANALYST" << EOF
[Desktop Entry]
Type=Application
Name=Sigmund Analyst
Comment=AI-enhanced code editor for data analysis
Exec=$WRAPPER_SIGMUND_ANALYST
Icon=accessories-text-editor
Terminal=false
Categories=Development;IDE;
StartupNotify=true
EOF
    
    # Refresh desktop-file cache (non-fatal if the cmd is missing)
    update-desktop-database "$(dirname "$DESKTOP_FILE_OPENSESAME")" 2>/dev/null || true
    
    echo
    echo "✅  Done! Look for 'OpenSesame 4.1' and 'Sigmund Analyst' in your application menu."
    echo "    You can also launch them from the command line:"
    echo "    - $WRAPPER_OPENSESAME"
    echo "    - $WRAPPER_SIGMUND_ANALYST"
}

uninstall() {
    echo "🗑️  Starting OpenSesame and Sigmund Analyst uninstallation..."
    
    # Remove virtual environment
    if [[ -d "$VENV_DIR" ]]; then
        echo "▶ Removing virtual environment at $VENV_DIR ..."
        rm -rf "$VENV_DIR"
    else
        echo "▶ Virtual environment not found at $VENV_DIR (skipping)"
    fi
    
    # Remove wrappers
    if [[ -f "$WRAPPER_OPENSESAME" ]]; then
        echo "▶ Removing OpenSesame wrapper ..."
        rm -f "$WRAPPER_OPENSESAME"
    fi
    
    if [[ -f "$WRAPPER_SIGMUND_ANALYST" ]]; then
        echo "▶ Removing Sigmund Analyst wrapper ..."
        rm -f "$WRAPPER_SIGMUND_ANALYST"
    fi
    
    # Remove desktop entries
    if [[ -f "$DESKTOP_FILE_OPENSESAME" ]]; then
        echo "▶ Removing OpenSesame desktop entry ..."
        rm -f "$DESKTOP_FILE_OPENSESAME"
    fi
    
    if [[ -f "$DESKTOP_FILE_SIGMUND_ANALYST" ]]; then
        echo "▶ Removing Sigmund Analyst desktop entry ..."
        rm -f "$DESKTOP_FILE_SIGMUND_ANALYST"
    fi
    
    # Refresh desktop-file cache
    update-desktop-database "$(dirname "$DESKTOP_FILE_OPENSESAME")" 2>/dev/null || true
    
    echo
    echo "✅  Uninstallation complete!"
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

# Main script logic
if [[ $# -eq 0 ]]; then
    echo "❌  Error: No arguments provided"
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
        echo "❌  Error: Unknown option: $1"
        show_usage
        exit 1
        ;;
esac
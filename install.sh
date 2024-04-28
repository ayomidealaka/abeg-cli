#!/usr/bin/env bash
set -euo pipefail

ABEG_VERSION="v0.0.1"
OS="$(uname -s)"
ARCH="$(uname -m)"
echo "OS: ${OS}, CPU Architecture: ${ARCH} detected."

# Function to display error messages
error() {
    echo -e "\033[0;31merror:\033[0m $1" >&2
    exit 1
}

# Function to display success messages
success() {
    echo -e "\033[0;32msuccess:\033[0m $1"
}

case "${OS}" in
Linux)
    case "${ARCH}" in
    x86_64 | amd64) ABEG_URL="https://github.com/ayomidealaka/abeg-cli/releases/download/${ABEG_VERSION}/abeg-linux-amd64" ;;
    aarch64) ABEG_URL="https://github.com/ayomidealaka/abeg-cli/releases/download/${ABEG_VERSION}/abeg-linux-arm64" ;;
    *)
        echo "Unsupported Architecture: ${ARCH}" >&2
        exit 1
        ;;
    esac
    ;;
Darwin)
    case "${ARCH}" in
    x86_64 | amd64 | i386) ABEG_URL="https://github.com/ayomidealaka/abeg-cli/releases/download/${ABEG_VERSION}/abeg-macos-x64" ;;
    arm64) ABEG_URL="https://github.com/ayomidealaka/abeg-cli/releases/download/${ABEG_VERSION}/abeg-macos-arm64" ;;
    *)
        echo "Unsupported Architecture: ${ARCH}" >&2
        exit 1
        ;;
    esac
    ;;
*)
    echo "Unsupported OS: ${OS}" >&2
    exit 1
    ;;
esac

INSTALL_DIR="$HOME/.abeg/bin"
mkdir -p "${INSTALL_DIR}"
ABEG_BIN="${INSTALL_DIR}/abeg"

echo "Downloading Abeg from ${ABEG_URL}..."
curl --fail --location --progress-bar --output "${ABEG_BIN}" "${ABEG_URL}" || error "Failed to download Abeg"

chmod +x "${ABEG_BIN}" || error "Failed to set executable permissions on Abeg"

echo "Moving Abeg to /usr/local/bin..."
sudo mv "${ABEG_BIN}" /usr/local/bin/abeg || error "Failed to move abeg binary to /usr/local/bin/abeg"

echo 'Adding Abeg to PATH in .bashrc and .zshrc...'
{
    echo "# Abeg PATH"
    echo "export PATH=\"${INSTALL_DIR}:\$PATH\""
} >>"$HOME/.bashrc"

if [ -f "$HOME/.zshrc" ]; then
    {
        echo "# Abeg PATH"
        echo "export PATH=\"${INSTALL_DIR}:\$PATH\""
    } >>"$HOME/.zshrc"
fi

success "Abeg ${ABEG_VERSION} was installed successfully to /usr/local/bin/abeg"
echo "You can restart your terminal or source the appropriate profile to update your PATH using 'source ~/.bashrc'"

#!/bin/bash
echo "[CoffeeBar] Installer (Linux)"
echo "============================="

# Python check
if ! command -v python3 &> /dev/null
then
    echo "[Error] python3 could not be found."
    exit 1
fi

echo "[1/3] Installing dependencies..."
pip3 install -r requirements.txt

echo "[2/3] Setting up environment..."
# Create bin symlink or add to path?
# Let's add an alias to .bashrc / .zshrc
PROJECT_ROOT="$(pwd)"
WRAPPER_PATH="$PROJECT_ROOT/bin/coffeebar"
chmod +x "$WRAPPER_PATH"

SHELL_RC="$HOME/.bashrc"
if [[ "$SHELL" == *"zsh"* ]]; then
    SHELL_RC="$HOME/.zshrc"
fi

if ! grep -q "alias coffeebar=" "$SHELL_RC"; then
    echo "" >> "$SHELL_RC"
    echo "# CoffeeBar" >> "$SHELL_RC"
    # We use a function or alias that sources the output env?
    # Simpler: just run the wrapper. But wrapper can't update env of parent.
    # BEST PRACTICE for NVM/SDKMAN style:
    # Use a shell function.
    
    cat <<EOT >> "$SHELL_RC"
coffeebar() {
    "$WRAPPER_PATH" "\$@"
    local EXIT_CODE=\$?
    if [ "\$1" = "use" ] && [ \$EXIT_CODE -eq 0 ]; then
        source "\$HOME/.coffeebar_env"
    fi
}
EOT
    echo "Added 'coffeebar' function to $SHELL_RC"
else
    echo "'coffeebar' alias/function already exists in $SHELL_RC"
fi

echo ""
echo "[3/3] Installation Complete!"
echo "Please restart your terminal or run: source $SHELL_RC"

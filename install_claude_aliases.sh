#!/bin/bash
# install_claude_aliases.sh
# Automatically adds 'cla' and 'fig' aliases to ~/.bashrc for easy access to Claude configuration files

set -e

BASHRC="$HOME/.bashrc"
MARKER="# Claude configuration files - copy to current/new directories"

# Check if aliases already exist
if grep -q "$MARKER" "$BASHRC" 2>/dev/null; then
    echo "Claude aliases already installed in $BASHRC"
    exit 0
fi

echo "Installing Claude aliases to $BASHRC..."

# Append the configuration to .bashrc
cat >> "$BASHRC" << 'EOF'

# Claude configuration files - copy to current/new directories
# Store template files in home directory
CLAUDE_CONFIG_DIR="$HOME/.claude_templates"
mkdir -p "$CLAUDE_CONFIG_DIR"

# Function to initialize templates on first use
_init_claude_templates() {
    if [ ! -f "$CLAUDE_CONFIG_DIR/FIGURE_PROTOCOL_v1.2.md" ]; then
        curl -s "https://raw.githubusercontent.com/olympus-terminal/tools/refs/heads/master/FIGURE_PROTOCOL_v1.2.md" -o "$CLAUDE_CONFIG_DIR/FIGURE_PROTOCOL_v1.2.md"
    fi
    if [ ! -f "$CLAUDE_CONFIG_DIR/GreatClaudeConfig.md" ]; then
        curl -s "https://raw.githubusercontent.com/olympus-terminal/tools/refs/heads/master/GreatClaudeConfig.md" -o "$CLAUDE_CONFIG_DIR/GreatClaudeConfig.md"
    fi
}

# Alias: cla - Copy GreatClaudeConfig.md to current directory
alias cla='_init_claude_templates && cp "$CLAUDE_CONFIG_DIR/GreatClaudeConfig.md" . && echo "✓ GreatClaudeConfig.md copied to current directory"'

# Alias: fig - Copy FIGURE_PROTOCOL_v1.2.md to current directory
alias fig='_init_claude_templates && cp "$CLAUDE_CONFIG_DIR/FIGURE_PROTOCOL_v1.2.md" . && echo "✓ FIGURE_PROTOCOL_v1.2.md copied to current directory"'

EOF

echo "✓ Claude aliases installed successfully!"
echo ""
echo "Run 'source ~/.bashrc' or open a new terminal to use:"
echo "  cla  - Copy GreatClaudeConfig.md to current directory"
echo "  fig  - Copy FIGURE_PROTOCOL_v1.2.md to current directory"

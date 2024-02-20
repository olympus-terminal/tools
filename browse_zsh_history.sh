#!/bin/bash

echo "$HOME/.zsh_history"

cat "$HOME/.zsh_history"

echo "   "

echo "   "

echo "Now searching history for argv1 query"

echo "   "
echo "   "

#nano "$HOME/.zsh_history"

fgrep "$1" "$HOME/.zsh_history"

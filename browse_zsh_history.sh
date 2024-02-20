#!/bin/bash

echo "$HOME/.zsh_history"

cat "$HOME/.zsh_history"

wait 5

echo "Now searching history for argv1 query"

#nano "$HOME/.zsh_history"

fgrep "$1" "$HOME/.zsh_history"

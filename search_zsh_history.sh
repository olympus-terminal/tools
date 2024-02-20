#!/bin/bash

echo "$HOME/.zsh_history"

printf "${RED}Here is your entire history ${NC}\n"


cat "$HOME/.zsh_history"

echo "   "

echo "   "

#echo "Now searching history for argv1 query"

echo "   "
echo "   "

#nano "$HOME/.zsh_history"

RED='\033[0;31m'
NC='\033[0m' # No Color
PURPLE='\033[0;35m' 

printf "${RED}Now searching history for argv1 query ${PURPLE}\n\n"

fgrep "$1" "$HOME/.zsh_history"

printf "\n\n${RED}Results printed ${PURPLE}\n\n"

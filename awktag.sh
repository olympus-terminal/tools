#!/bin/bash

awk '{print $0"<tag>"}' "$1" > "$2"

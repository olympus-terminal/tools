#!/bin/bash

unzip -v $1 | awk '{print $8}' | while read file; do
    unzip -p $1 "$file" > "new_$file"
done

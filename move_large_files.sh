# filename: move_large_files.sh

#!/bin/zsh

for file in *; do
    if [[ -f "$file" && $(stat -f%z "$file") -gt $1 ]]; then 
        mv "$file" $2
    fi
done



#!/bin/zsh
# for when file naming matters

for file in "$@"; do
    if [ -f "$file" ]; then
        file_size=$(wc -l < "$file")
        half_size=$((file_size / 2))
        dir_name=$(dirname "$file")
        base_name=$(basename "$file")
        extension="${base_name##*.}"
        prefix="${base_name%.*}"
        split -l $half_size "$file" "${dir_name}/${prefix}_"
        for split_file in "${dir_name}"/${prefix}_* ; do
            mv "$split_file" "${split_file}.${extension}"
        done
    fi
done


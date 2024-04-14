search_in_files() {
    if [ $# -ne 2 ]; then
        echo "Usage: search_in_files <directory> <string>"
        return 1
    fi

    local directory=$1
    local search_string=$2

    if [ ! -d "$directory" ]; then
        echo "Error: Directory does not exist."
        return 1
    fi

    # Use find and fgrep to search for the string
    find "$directory" -type f -exec fgrep -Hn "$search_string" {} +
}

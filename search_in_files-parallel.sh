search_in_files() {
    if [ $# -ne 3 ]; then
        echo "Usage: search_in_files <directory> <string> <num_processors>";
        return 1;
    fi;
    local directory=$1;
    local search_string=$2;
    local num_processors=$3;
    
    if [ ! -d "$directory" ]; then
        echo "Error: Directory does not exist.";
        return 1;
    fi;

    # Use GNU Parallel with the specified number of processors
    find "$directory" -type f | parallel -j "$num_processors" fgrep -Hn "$search_string" {}
}

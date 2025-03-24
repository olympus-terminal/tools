#shuf-noHedtho
#!/bin/bash

(head -n 1 $1 && tail -n +2 $1 | shuf) > shuffled_file.txt

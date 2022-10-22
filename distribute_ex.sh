#!/bin/bash

for f in Macros_at_lessThan*; do cat $f | while read l; do cp AA_bak/"$l"* SUBSETs_ContamThresh/"${f%.txt}"/ ; done  ; done 

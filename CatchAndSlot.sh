#!/bin/bash

for f in Macros_at_lessThan*; do cat $f | while read l; do grep "$l" HMMer_bak/"$l"* >> HMMer_bak/"${f%.txt}"/"$l".pfams  ; done ; done

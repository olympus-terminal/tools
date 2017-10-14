#!/bin/bash

### clone, imprint && distribute

for i in *.ext
do
 j=$(basename $i .ext)
 sed -r "s/foo/${j}/" /dir/base.template > /dir/"$i".out
done


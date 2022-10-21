#!/bin/bash

awk '{a[$1]+=$2;b[$1]+=$3}END{for(i in a)print i, a[i], b[i]|"sort"}' $1

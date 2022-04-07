#!/bin/bash

cat Renaming_list_utf-8.txt | while read l; do ./mvrnm.sh $l ; done

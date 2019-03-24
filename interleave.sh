#!/bin/bash

awk '$1!=p{print;p=$1}' $1

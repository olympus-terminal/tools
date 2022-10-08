#!/bin/bash

grep -Fvxf "$f" "${f%mod}.orig >> "$f".new

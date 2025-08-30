#!/bin/bash

rsync -avzP --sockopts=SO_SNDBUF=524288,SO_RCVBUF=524288 \
    cwd/ \
    user@server.edu:/cwd

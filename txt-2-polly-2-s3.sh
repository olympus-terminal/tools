#!/bin/bash

aws polly start-speech-synthesis-task \
  --text-type text \
  --region us-west-2 \
  --endpoint-url "https://polly.us-west-2.amazonaws.com/" \
  --output-format mp3 \
  --output-s3-bucket-name polly-x \
  --output-s3-key-prefix "$1"-out \
  --voice-id Salli \
  --text file://"$1"

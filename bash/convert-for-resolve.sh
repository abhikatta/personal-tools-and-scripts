#!/usr/bin/env bash

for f in *.MP4 *.MOV; do ffmpeg -i "$f" -c:v dnxhd -profile:v dnxhr_lb -pix_fmt yuv422p -c:a pcm_s16le "${f%.*}_edit.mov"; done
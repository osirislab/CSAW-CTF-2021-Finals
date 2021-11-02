#!/bin/bash

ffmpeg -i noir.png -pix_fmt rgb24 -f rawvideo noir.webm
exiftool -p \$Matroska:Title noir.webm | base64 -d

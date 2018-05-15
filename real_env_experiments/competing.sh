#!/usr/bin/env bash

echo 'Started Comprting Flow'
youtube-dl --no-continue --no-cache-dir "${1}"  -o '/tmp/%(title)s.%(ext)s' > /dev/null &
pid=$!
sleep 100
echo 'Killing Competing Flow'
kill ${pid}

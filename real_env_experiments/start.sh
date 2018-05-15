#!/usr/bin/env bash

URL='https://vimeo.com/channels/staffpicks/154186123'
DOWNLOAD_URL='https://vimeo.com/channels/staffpicks/154186123'
FILE1='client.csv'
FILE2='competing.csv'
FILE3='playback_rates.csv'

#Prior to streaming, download Dash Manifest File of the Video
youtube-dl -F "${DOWNLOAD_URL}" | grep -i "DASH video"  > bitrates

client_throughput="logs/client.log"
competing_throughput="logs/competing.log"

echo "Start Client Flow"
mm-link ./utilize.trace ./utilize.trace --downlink-log="${client_throughput}" --meter-downlink -- ./client.sh ${URL} &
client_pid=$!

sleep 50

echo "Starting Competing Flow"
mm-link ./utilize.trace ./utilize.trace --downlink-log="${competing_throughput}" --meter-downlink -- ./competing.sh ${URL} &
competing_pid=$!

wait $client_pid
wait $competing_pid

python calculate_playback_rate.py > playback_rates.csv
python calculate_throughput.py "${client_throughput}" > client.csv
python calculate_throughput.py "${competing_throughput}" > competing.csv
python plot.py ${FILE1} ${FILE2} ${FILE3}

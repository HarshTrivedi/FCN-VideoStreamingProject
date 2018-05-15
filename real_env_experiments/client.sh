URL=$1
firefox "${URL}" & > /dev/null
pid=$!

wait $pid

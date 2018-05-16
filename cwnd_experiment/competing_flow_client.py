import os
import sys
# competing flow server here:
# basically iperf client for now
# will change it to something else later 

iperf_server_ip = sys.argv[1]
competing_flow_duration = int(sys.argv[2].strip())
# iperf client start
os.system('iperf -c {} -t {} -i 1'.format(iperf_server_ip, competing_flow_duration))



import os
import sys
# competing flow server here:
# basically iperf client for now
# will change it to something else later 

iperf_server_ip = sys.argv[1]
# iperf client start
os.system('iperf -c {} -t 3600 -i 1 -y -Z cong'.format(iperf_server_ip))



import sys
import lib
from datetime import datetime
import time

interface = sys.argv[1]

throughput_log_file = 'logs/throughput-{}.log'.format(interface)

last_received_bytes = lib.received_bytes(interface)
last_time = time.time()

def throughput_log(throughput):

    with open(throughput_log_file, 'a+') as f:
        line = '\t'.join([str(datetime.fromtimestamp( time.time() )), str(throughput)])
        f.write( line  + '\n')

while True:
    time.sleep(1.0)
    
    received_bytes = lib.received_bytes(interface)
    current_time = time.time()

    throughput = (received_bytes-last_received_bytes)/(current_time-last_time)    
    throughput_log(throughput)

    last_time = current_time
    last_received_bytes = received_bytes

import sys
import lib
from datetime import datetime
import time

port = sys.argv[1]
duration = float(sys.argv[2])
cwnd_log_file = 'logs/cwnd-{}.log'.format(port)

def cwnd_log(cwnd):
    
    with open(cwnd_log_file, 'a+') as f:
        curr_time = time.time()
        line = '\t'.join([ str(curr_time),  str(datetime.fromtimestamp( time.time() )), str(cwnd)])
        f.write( line  + '\n')

while True:
    time.sleep(duration)
    cwnd = lib.get_cwnd(int(port))
    cwnd_log(cwnd)

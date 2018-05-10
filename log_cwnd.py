import sys
import lib
from datetime import datetime
import time

port = sys.argv[1]
logdir = sys.argv[2]

cwnd_log_file = '{}/cwnd-{}.log'.format(logdir, port)

def cwnd_log(cwnd):

    with open(cwnd_log_file, 'a+') as f:
        curr_time = time.time()
        line = '\t'.join([ str(curr_time),  str(datetime.fromtimestamp( time.time() )), str(cwnd)])
        f.write( line  + '\n')

while True:
    time.sleep(0.5)
    cwnd = lib.get_cwnd(int(port))
    cwnd_log(cwnd)

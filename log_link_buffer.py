import sys
import lib
from datetime import datetime
import time

interface = sys.argv[1]

link_buffer_log_file = 'logs/link-buffer-{}.log'.format(interface)

def link_buffer_log(link_buffer):

    with open(link_buffer_log_file, 'a+') as f:
        line = '\t'.join([str(datetime.fromtimestamp( time.time() )), str(link_buffer)])
        f.write( line  + '\n')

while True:
    time.sleep(1.0)
    
    buffer_left = lib.link_buffer_left(interface)
    current_time = time.time()

    link_buffer_log(buffer_left)
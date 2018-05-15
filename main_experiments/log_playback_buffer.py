from playback_buffer import *
import sys
import lib
from datetime import datetime
import time

logdir = sys.argv[1]
playback_buffer_file = '{}/playback_buffer.log'.format(logdir)

def playback_buffer_log(playback_buffer):

    with open(playback_buffer_file, 'a+') as f:
        curr_time = time.time()    	
        line = '\t'.join([ str(curr_time), str(datetime.fromtimestamp( time.time() )), str(playback_buffer)])
        f.write( line  + '\n')

while True:
    time.sleep(1.0)
    playback_buffer = PlaybackBuffer.read()
    playback_buffer_log(playback_buffer)

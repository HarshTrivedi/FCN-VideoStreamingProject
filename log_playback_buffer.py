from playback_buffer import *
import sys
import lib
from datetime import datetime
import time

playback_buffer_file = 'logs/playback_buffer.log'

def playback_buffer_log(playback_buffer):

    with open(playback_buffer_file, 'a+') as f:
        line = '\t'.join([str(datetime.fromtimestamp( time.time() )), str(playback_buffer)])
        f.write( line  + '\n')

while True:
    time.sleep(1.0)
    playback_buffer = PlaybackBuffer.read()
    playback_buffer_log(playback_buffer)
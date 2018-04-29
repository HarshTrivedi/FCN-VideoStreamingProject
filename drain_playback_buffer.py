# decrease 1 second of playback buffer every second

from playback_buffer import *
import time

interval = 1 
while True:
    playback_buffer = PlaybackBuffer.read()
    PlaybackBuffer.add( -interval )
    time.sleep(interval)


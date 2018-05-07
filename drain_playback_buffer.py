# decrease 1 second of playback buffer every second

from playback_buffer import *
import time

interval = 0.5
while True:
    playback_buffer = PlaybackBuffer.read()
    PlaybackBuffer.add( -interval )
    time.sleep(interval)


# video flow client script here

# Make sure to log the request times
# Make sure to log the buffer state times

import socket
import thread
from playback_buffer import *
from datetime import datetime
import sys
import os
import time

ip   = sys.argv[1].strip()
port = int(sys.argv[2].strip())


# initialize playback buffer as 0. It marks the seconds of playback buffer we already have
# at will be full when it crosses 240 seconds, because that is maximum.
PlaybackBuffer.write(0)

thread.start_new_thread(   os.system, ('python drain_playback_buffer.py',)   )


segment_seconds       = 4    
fixed_rate            = 1750 
playback_buffer_limit = 240  # at max hold 4 minutes of buffer is allowed
received_throughput   = []
rate_selection        = True # client-side rate selection is ON for this experiment


request_interval_file = 'logs/request_interval.log'
def request_interval_log(last_request_time, request_interval):
    
    with open(request_interval_file, 'a+') as f:
        line = '\t'.join([ str(datetime.fromtimestamp( last_request_time )) , str(request_interval)])
        f.write( line  + '\n')


playback_rate_file = 'logs/playback_rate.log'
def playback_rate_log(playback_rate):
    
    with open(playback_rate_file, 'a+') as f:
        
        line = '\t'.join([ str(datetime.fromtimestamp( time.time() )) , str(playback_rate)])
        f.write( line  + '\n')


def select_bitrate(throughput):
    # What to get the actual figures??
    rates = [235,   375,    560,     750,    1050,   1400, 1750]
    # bytes per sec
    #       [29375, 46875,  70000,   93750,  131250, 175000, 218750]
    # bytes for 4 seconds
    #       [117500, 187500, 280000, 375000, 525000, 700000, 875000]
    rates = [ x* (1024 / 8) for x in rates] 
    if throughput > (2500 * 1000):
        rate = rates[6] # 1750
    elif throughput > (2150 * 1000):
        rate = rates[5] # 1400
    elif throughput > (1300 * 1000): 
        rate = rates[4] # 1050
    elif throughput > (1100 * 1000): 
        rate = rates[3] # 750
    elif throughput > (740 * 1000): 
        rate = rates[2] # 560
    elif throughput > (500 * 1000): 
        rate = rates[1] # 375
    else: 
        rate = rates[0]	
    return rate

while True:

    recent_samples = received_throughput[-10:]
    if len(recent_samples) == 0:
        estimated_throughput = 1 # we want to choose the lowest bitrate by default
    else:
        estimated_throughput = sum(recent_samples)/float(len(recent_samples))

    if rate_selection:
        playback_rate = select_bitrate(estimated_throughput)
    else:
        playback_rate = fixed_rate
    bytes_needed = playback_rate * segment_seconds

    playback_buffer = PlaybackBuffer.read()

    last_request_time = time.time()
    if (playback_buffer + segment_seconds) <= playback_buffer_limit:
        request_time = time.time()
        request_interval = request_time - last_request_time # first request_interval would be redundant

        request_bytes = playback_rate * segment_seconds

        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((ip,port))

        conn.send(str(request_bytes))
        print 'Sending Message:'
        print request_bytes
        
        request_time_start = time.time()
        received_len = 0
        received_msg = conn.recv(request_bytes).strip()
        received_len = len(received_msg)

        print 'Received Message Length:'
        print received_len

        request_time_end = time.time()
        received_len = (request_time_end - request_time_start)
        receive_throughput = received_len / (request_time_end-request_time_start )

        received_throughput.append(receive_throughput)

        # always 4 seconds should be added? Whatever the bitrate, we always ask for 4 seconds right?
        print "This much will be added: {}".format(segment_seconds)
        PlaybackBuffer.add(segment_seconds)

        request_interval_log(last_request_time, request_interval)
        playback_rate_log(playback_rate)
        last_request_time = request_time
    else:
        time.sleep(1.0)




# video flow client script here

# Make sure to log the request times
# Make sure to log the buffer state times

import socket
import thread
from playback_buffer import *
from datetime import datetime
import sys
import lib
import os
import time
import imp

ip   = sys.argv[1].strip()
port = int(sys.argv[2].strip())
logdir = sys.argv[3]
experiment_name = sys.argv[4]

settings_path = 'settings/settings-{}.py'.format(experiment_name)
if not os.path.exists(settings_path):
    print 'Path to {} does not exists'.format(settings_path)
    exit()
settings = imp.load_source("settings", settings_path)

log_file = '{}/video_client_py.log'.format(logdir)
def py_log(message):
    ##
    with open(log_file, "a+") as f:
        f.write(str(message) + "\n")
    # print message
    ##

# initialize playback buffer as 0. It marks the seconds of playback buffer we already have
# at will be full when it crosses 60 seconds, because that is maximum.
PlaybackBuffer.write(0)

thread.start_new_thread(   os.system, ('python drain_playback_buffer.py',)   )


segment_seconds       = settings.segment_seconds
playback_buffer_limit = settings.playback_buffer_limit
received_throughput   = []
rate_selection        = settings.playback_rate_selection
if not rate_selection:
    fixed_bitrate     = settings.fixed_bitrate # bits/s
buffer_size           = 1024

request_interval_file = '{}/request_interval.log'.format(logdir)
def request_interval_log(last_request_time, request_interval):

    with open(request_interval_file, 'a+') as f:
        line = '\t'.join([ str(last_request_time), str(datetime.fromtimestamp( last_request_time )) , str(request_interval)])
        f.write( line  + '\n')


playback_rate_file = '{}/playback_rate.log'.format(logdir)
def playback_rate_log(playback_rate):

    with open(playback_rate_file, 'a+') as f:
        curr_time = time.time()
        line = '\t'.join([ str(curr_time), str(datetime.fromtimestamp( curr_time )) , str(playback_rate)])
        f.write( line  + '\n')


receive_video_throughput_rate_file = '{}/receive-throughput-vclient.log'.format(logdir)
def receive_video_throughput_log(throughput):

    with open(receive_video_throughput_rate_file, 'a+') as f:
        curr_time = time.time()
        line = '\t'.join([ str(curr_time), str(datetime.fromtimestamp( curr_time )) , str(throughput)])
        f.write( line  + '\n')



def select_playback_bitrate(throughput_bitps, optimistic = False):

    rates_kbitps = [250,   400,    500,     700,    1000,   1400, 1800]
    rates_bitps = [ x* 1024 for x in rates_kbitps]

    if not optimistic:
        if throughput_bitps > (2500 * 1024):
            bit_rate = rates_bitps[6] # 1800*1024 bits/s
        elif throughput_bitps > (2100 * 1024):
            bit_rate = rates_bitps[5] # 1400*1024 bits/s
        elif throughput_bitps > (1300 * 1024):
            bit_rate = rates_bitps[4] # 1000*1024 kbits/s
        elif throughput_bitps > (1100 * 1024):
            bit_rate = rates_bitps[3] # 700*1024 bits/s
        elif throughput_bitps > (750 * 1024):
            bit_rate = rates_bitps[2] # 500*1024 bits/s
        elif throughput_bitps > (500 * 1024):
            bit_rate = rates_bitps[1] # 400*1024 bits/s
        else:
            bit_rate = rates_bitps[0] # 250*1024 bits/s
    else:
        if throughput_bitps > (1800 * 1024):
            bit_rate = rates_bitps[6] # 1800*1024 bits/s
        elif throughput_bitps > (1400 * 1024):
            bit_rate = rates_bitps[5] # 1400*1024 bits/s
        elif throughput_bitps > (1000 * 1024):
            bit_rate = rates_bitps[4] # 1000*1024 kbits/s
        elif throughput_bitps > (700 * 1024):
            bit_rate = rates_bitps[3] # 700*1024 bits/s
        elif throughput_bitps > (500 * 1024):
            bit_rate = rates_bitps[2] # 500*1024 bits/s
        elif throughput_bitps > (400 * 1024):
            bit_rate = rates_bitps[1] # 400*1024 bits/s
        else:
            bit_rate = rates_bitps[0] # 250*1024 bits/s

    return bit_rate


last_request_time = time.time()

buffer_toggle_hit_time_file = '{}/buffer_toggle_hit_time.txt'.format(logdir)
buffer_toggle_hit_time = None

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((ip,port))
last_request_end_time = time.time()

while True:

    recent_samples = received_throughput[-settings.smoothing:]
    if len(recent_samples) == 0:
        estimated_throughput = 1 # we want to choose the lowest bitrate by default
    else:
        estimated_throughput = sum(recent_samples)/float(len(recent_samples))

    py_log('estimated_throughput: {}'.format(estimated_throughput))


    if rate_selection:
        estimated_throughput_bitsps = estimated_throughput*8
        playback_bit_rate = select_playback_bitrate(estimated_throughput_bitsps, settings.optimistic )
        playback_rate     = playback_bit_rate / 8.0 # bytes/s
    else:
        playback_rate = fixed_bitrate / 8.0  # bytes/s
    bytes_needed = playback_rate * segment_seconds
    py_log('playback_rate: {}'.format(playback_rate))

    playback_buffer = PlaybackBuffer.read()


    if (playback_buffer + segment_seconds) <= playback_buffer_limit:
        request_time = time.time()
        request_interval = request_time - last_request_time # first request_interval would be redundant

        request_bytes = int(playback_rate * segment_seconds)

        conn.send(str(request_bytes))

        py_log('Sending Message:')
        py_log(request_bytes)

        received_len = 0
        x = lib.received_bytes('vclient-eth0')
        received_msg = ''
        while True:
            data = conn.recv(buffer_size)
            received_msg += data
            if len(received_msg) >= request_bytes:
                break
            if not data:
                break
        received_len = len(received_msg)

        y = lib.received_bytes('vclient-eth0')

        py_log('Received Message Length:')
        py_log(received_len)
        received_len = y-x

        request_time_end = time.time()
        # receive_throughput = received_len / (request_time_end-last_request_end_time )
        receive_throughput = received_len / (request_time_end-request_time )

        received_throughput.append(receive_throughput)

        # always 4 seconds should be added? Whatever the bitrate, we always ask for 4 seconds right?
        py_log("This much will be added: {}".format(segment_seconds))
        PlaybackBuffer.add(segment_seconds)

        receive_video_throughput_log(receive_throughput)
        request_interval_log(last_request_time, request_interval)
        playback_rate_log(playback_rate)
        last_request_time = request_time
        last_request_end_time = time.time()
    else:
        if not buffer_toggle_hit_time:
            buffer_toggle_hit_time = time.time()
            with open(buffer_toggle_hit_time_file, 'w') as f:
                line = '\t'.join([ str(buffer_toggle_hit_time), str(datetime.fromtimestamp( buffer_toggle_hit_time )) ])
                f.write( line )

        if not settings.radical_client:
            time.sleep(0.1)

        else:
            PlaybackBuffer.add(-1)

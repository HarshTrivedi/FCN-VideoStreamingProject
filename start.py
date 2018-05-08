# This is the main script to run mininet #
############################################

# Load the topology
# assign appropriate link states and all

# start video streaming server on server host
# start video streaming client on client host
    # make sure the client logs request intervals and playback-buffer state
# start bottleneck-link buffer logging on server.

# start throughput logging daemon on client host

# start congestion_window_logging.py on server for port that has video-streaming
# start congestion_window_logging.py on server for port that has competing-flow [redundant]

# wait for X seconds to start the competing-flow
    # start competing_flow_server.py
    # start competing_flow_client.py
# start throughput logging daemon on competing-flow host

############################################

from topo import *
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.cli import CLI
import time
import shutil
import os
from datetime import datetime
import settings


def start_network():

    # Load the topology and assign appropriate link states and all
    topo = ExpTopo()
    net = Mininet( topo=topo, host=CPULimitedHost, link=TCLink )
    net.start()

    # basic sanity check
    dumpNodeConnections(net.hosts)
    net.pingAll()

    experiment_duration       = settings.experiment_duration
    experiment_start_time     = time.time()
    competing_flow_start_time = experiment_start_time + settings.competing_flow_start_at
    competing_flow_duration   = settings.competing_flow_duration
    
    server                = net.get('server')
    video_client          = net.get('vclient')
    competing_client      = net.get('cclient')

    print '---IP Informations---'
    print 'Video     Client: {}'.format(video_client.IP())
    print 'Competing Client: {}'.format(competing_client.IP())
    print 'Server          : {}'.format(server.IP())    


    # Keep CLI anywhere and start to debug what is happening
    # CLI(net) 
    
    video_stream_port   = 5000
    competing_flow_port = 5001

    # # CLI(net) Turn this ON and execute scripts eg. server python video_server.py  <server_ip> to debug
    
    # start video streaming server on server host
    server.cmd('python video_server.py {} {} &'.format(server.IP(), video_stream_port))
    print 'Started Video Streaming Server'
    
    # start video streaming client on client host
    video_client.cmd('python video_client.py {} {} &'.format( server.IP(), video_stream_port))
        # Inside: make sure the client logs request intervals and playback-buffer state
    print 'Started Video Streaming Client'
    
    # start bottleneck-link buffer logging on server.
    # Use tc show <interface name> command and log periodically. Partially coded, don't understand how to parse tc show output.
    # server.cmd('python log_link_buffer.py server-eth1 &')
    # print 'Started  daemon to log queue size left of bottleneck-link on server'

    # start to log the playback buffer periodically on video client
    video_client.cmd('python log_playback_buffer.py &')
    print 'Started  daeomon to log PlayBack Buffer periodically on video client'
    
    # start throughput logging daemon on video client host
    video_client.cmd('python log_throughput.py vclient-eth0 &')
    print 'Started  daeomon to log throughput on video-client interface periodically'

    # start throughput logging daemon on competing-flow host
    competing_client.cmd('python log_throughput.py cclient-eth0 &')                
    print 'Started  daeomon to log throughput on competing client interface periodically'
    
    # start congestion window logging on server for port that has video-streaming
    server.cmd('python log_cwnd.py {} &'.format(video_stream_port) )    

    # start congestion window logging on server for port that has competing-flow
    server.cmd('python log_cwnd.py {} &'.format(competing_flow_port) )    

    # wait for X seconds to start the competing-flow
    print 'Waiting to start the Competing Flow. It will take {} seconds'.format( competing_flow_start_time - experiment_start_time )

    competing_flow_started = False
    while (True):
        current_time = time.time()
        if not competing_flow_started:
            if (current_time > competing_flow_start_time ):

                # for competing flow, because we are using iperf client-server would be exchanged.
                # hence start the client first and server then

                # start competing_flow_client.py
                competing_client.cmd("python competing_flow_server.py &")
                print 'Competing flow server started.'

                # start competing_flow_server.py                
                server.cmd("python competing_flow_client.py {} {} &".format( competing_client.IP(), competing_flow_duration ) )
                print 'Competing flow client started.'

                competing_flow_started = True
        time.sleep(1)

        if current_time - experiment_start_time > experiment_duration:
            break

    # CLI(net)
    
    stop_network(net)
    print 'Experiment complete.'


def stop_network(net):

    # clean up the created processes
    server                = net.get('server')
    video_client          = net.get('vclient')
    competing_client      = net.get('cclient')

    server.cmd('pkill python')
    client.cmd('pkill python')
    client.cmd('pkill python')
    net.stop()



if __name__ == '__main__':

    # clean logs first
    logdir = 'logs/'
    if os.path.exists(logdir):
        shutil.rmtree(logdir)
    os.makedirs(logdir)

    start_network()    





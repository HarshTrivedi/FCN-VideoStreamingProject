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
    
    server                = net.get('server')
    video_client          = net.get('vclient')
    competing_client      = net.get('cclient')

    print '---IP Informations---'
    print 'Video     Client: {}'.format(video_client.IP())
    print 'Competing Client: {}'.format(competing_client.IP())
    print 'Server          : {}'.format(server.IP())    

    video_stream_port   = 5000

    segment_size = settings.seqment_size
    pause_time = settings.pause_time
    competing_flow_duration = 100

    ##############
    # CLI(net)
    competing_client.cmd("python competing_flow_server.py &")
    print 'Competing flow server started.'
    
    # start video streaming server on server host
    server.cmd('python video_server.py {} {} &'.format(server.IP(), video_stream_port))
    print 'Started Video Streaming Server'
    ###############

    time.sleep(2)
    
    ##############
    video_client.cmd('python log_throughput.py vclient-eth0 &')
    competing_client.cmd('python log_throughput.py cclient-eth0 &')

    # start congestion window logging on server for port that has video-streaming
    server.cmd('python log_cwnd.py {} 0.05 &'.format(video_stream_port) )    
    print 'Started cwnd logging'
    #############


    #############
    server.cmd("python competing_flow_client.py {} {} &".format( competing_client.IP(), competing_flow_duration ) )
    print 'Competing flow client started.'

    video_client.cmd('python pseudo_video_client.py {} {} {} {} &'.format( server.IP(), video_stream_port, segment_size, pause_time))
    print 'Started Pseudo Video Streaming Client'
    #############    
    
    time.sleep(90)
    print 'Experiment complete.'
    stop_network(net)


def stop_network(net):

    # clean up the created processes
#    server                = net.get('server')
#    video_client          = net.get('vclient#')
#    competing_client      = net.get('cclient')

#    server.cmd('pkill python')
#    video_client.cmd('pkill python')
#    competing_client.cmd('pkill python')
    net.stop()



if __name__ == '__main__':

    # clean logs first
    logdir = 'logs/'
    if os.path.exists(logdir):
        shutil.rmtree(logdir)
    os.makedirs(logdir)

    start_network()    











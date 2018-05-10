# topo.py
# Take the most basic one as default
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

# Using CPULimitedHost and TCLink is given on first Mininet Doc Tutorial


class ExpTopo(Topo):

    def __init__(self):

        Topo.__init__(self)
        self.full_link_bw        = 100.0#*8 # in Mega bits/s
        self.bottleneck_link_bw  = 5.0#*8   # in Mega bits/s
        self.delay               = '1ms'

        switch = self.addSwitch('s1')

        # Each host gets 20% of my system CPU
        server                = self.addHost('server', cpu=.2) # server
        video_client          = self.addHost('vclient', cpu=.2) # video client
        competing_client      = self.addHost('cclient', cpu=.2) # competing client

        self.addLink(video_client, switch,
                                   bw=self.full_link_bw,
                                   delay=self.delay,
                                   use_htb=True )

        self.addLink(competing_client, switch,
                                   bw=self.full_link_bw,
                                   delay=self.delay,
                                   use_htb=True )

        self.addLink(server, switch,
                                   bw=self.bottleneck_link_bw,
                                   delay=self.delay,
                                   max_queue_size=100,
                                   use_htb=True )


# Connections formed are as follows:
# cclient cclient-eth0:s1-eth2
# server server-eth0:s1-eth3
# vclient vclient-eth0:s1-eth1
# s1 lo:  s1-eth1:vclient-eth0 s1-eth2:cclient-eth0 s1-eth3:server-eth0

# By default all loopback interfaces are 127.0.0.1

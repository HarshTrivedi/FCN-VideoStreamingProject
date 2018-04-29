import os

def received_bytes(interface):

    # eg /proc/net/dev
    # Inter-|   Receive                                                |  Transmit
    #  face |bytes    packets errs drop fifo frame compressed multicast|bytes    packets errs drop fifo colls carrier compressed
    # server-eth0:   82888    1316    0    0    0     0          0         0  2754510    1135    0    0    0     0       0          0
    #     lo:       0       0    0    0    0     0          0         0        0       0    0    0    0     0       0          0
    rbytes = None
    with open('/proc/net/dev', 'r') as f:
       for line in f.readlines(): 
           if interface in line:
               rbytes = float(line.split()[1])
    return rbytes

def transmitted_bytes(interface):

    rbytes = None
    with open('/proc/net/dev', 'r') as f:
       for line in f.readlines(): 
           if interface in line:
               rbytes = float(line.split()[8])
    return rbytes


def link_buffer_left(interface):
    # TODO :
      # Don't understand how to parse this!??
    # eq output:
    # qdisc htb 5: root refcnt 2 r2q 10 default 1 direct_packets_stat 0 direct_qlen 1000
    #  Sent 1933730 bytes 1461 pkt (dropped 0, overlimits 1492 requeues 0)
    #  backlog 0b 0p requeues 0
    # qdisc netem 10: parent 5:1 limit 1000 delay 5.0ms
    #  Sent 1933730 bytes 1461 pkt (dropped 0, overlimits 0 requeues 0)
    #  backlog 0b 0p requeues 0

    result = os.system("tc -s qdisc show dev {}".format(interface))






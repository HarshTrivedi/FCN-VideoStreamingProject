import os
# rather use this directly: cat /sys/class/net/eth0/statistics/rx_bytes
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

# cat /sys/class/net/eth0/statistics/tx_bytes
def transmitted_bytes(interface):

    rbytes = None
    with open('/proc/net/dev', 'r') as f:
       for line in f.readlines(): 
           if interface in line:
               rbytes = float(line.split()[9])
    return rbytes


# get router (link) buffer left on given interface
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


# get cwnd of outgoing tcp flow on this interface
##
# Netid  State      Recv-Q Send-Q   Local Address:Port       Peer Address:Port
# tcp    ESTAB      0      264984        10.0.0.2:46146          10.0.0.1:5001
#    cubic wscale:9,9 rto:244 rtt:42.81/1.531 mss:1448 cwnd:19 ssthresh:6 send 5.1Mbps unacked:19 rcv_space:29200
# tcp    ESTAB      0      0             10.0.0.2:5000           10.0.0.3:36292
#    cubic wscale:9,9 rto:248 rtt:46.804/4.507 ato:40 mss:1448 cwnd:12 ssthresh:8 send 3.0Mbps rcv_space:28960
##
def get_cwnd(port):
    array = os.popen('ss -i').read().strip().split('\n')
    for index, line in enumerate(array):
        if ':{}'.format(port) in line:
            break
    if index + 1 == len(array):
        return None
    line = array[index+1]
    mss_bytes = [ int(e.split(':')[1]) for e in line.split() if 'mss' in e][0]
    cwnd_info = [ int(e.split(':')[1]) for e in line.split() if 'cwnd' in e]

    if len(cwnd_info) == 0:
        cwnd_size = 1
    else:
        cwnd_size = cwnd_info[0]

    cwnd = mss_bytes*cwnd_size
    return cwnd



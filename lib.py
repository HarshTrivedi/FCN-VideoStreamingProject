

def received_bytes(interface):

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

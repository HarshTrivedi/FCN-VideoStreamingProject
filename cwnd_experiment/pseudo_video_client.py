# pseudo_client
import sys
import socket
import time
import lib

ip   = sys.argv[1].strip()
port = int(sys.argv[2].strip())

segment_size = int(sys.argv[3].strip())
pause_time = float(sys.argv[4].strip())


conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((ip,port))

def request_and_get(request_bytes):

    request_time_start = time.time()
    buffer_size = 1024
    conn.send(str(request_bytes))
    initial_bytes = lib.received_bytes('vclient-eth0')
    received_len = 0
    received_msg = ''
    while True:
        data = conn.recv(buffer_size)
        received_msg += data
        if len(received_msg) >= request_bytes:
            break
        if not data: 
            break

    later_bytes = lib.received_bytes('vclient-eth0')
    received_size = later_bytes - initial_bytes
    request_time_end = time.time()
    request_duration = request_time_end - request_time_start
    receive_throughput = received_size / (request_time_end - request_time_start )
    return [received_size, request_duration, receive_throughput]

received_throughputs = []
mark_a = time.time()
print "A {}".format(mark_a)
received_throughput = request_and_get(2350000)
received_throughputs.append(received_throughput)
mark_b = time.time()
print "B {}".format(mark_b)
time.sleep(pause_time)

mark_c = time.time()
print "C {}".format(mark_c)
received_throughput = request_and_get(segment_size)
received_throughputs.append(received_throughput)
mark_d = time.time()
print "D {}".format(mark_d)
time.sleep(pause_time)

mark_e = time.time()
print "E {}".format(mark_e)
received_throughput = request_and_get(segment_size)
received_throughputs.append(received_throughput)
mark_f = time.time()
print "F {}".format(mark_f)


with open('logs/cwnd_experiment_marks.txt', 'w') as f:
    f.write('\t'.join(map(str,[mark_a, mark_b, mark_c, mark_d, mark_e, mark_f])))

with open('logs/apparent_throughputs.txt', 'w') as f:
    f.write('\t'.join(map(str,received_throughputs)))


conn.close()



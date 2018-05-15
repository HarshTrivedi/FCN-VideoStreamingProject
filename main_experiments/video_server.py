# video flow server script here

import socket
import sys

ip   = sys.argv[1].strip()
port = int(sys.argv[2].strip())
logdir = sys.argv[3]

log_file = '{}/video_server_py.log'.format(logdir)
def py_log(message):
    ##
    with open(log_file, "a+") as f:
        f.write(str(message) + "\n")
    # print message
    ##

videofile = "sample-video.mp4"

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind( (ip, port) )
serv.listen(5)
conn, addr = serv.accept()

# with open(videofile, "rb") as f:    
    # while True:
    #     request_size = conn.recv(10)
    #     if request_size.strip():
    #         py_log('Got Message:')
    #         py_log(request_size)
    #         request_size = int(request_size.strip())
    #         requested_bytes = ('*'*request_size)
    #         conn.send(requested_bytes)
    #         py_log('Send Message Length:')
    #         py_log(len(requested_bytes))        

while True:
    request_size = conn.recv(10)
    if request_size.strip():
        py_log('Got Message:')
        py_log(request_size)
        request_size = int(request_size.strip())
        requested_bytes = ('*'*request_size)
        conn.send(requested_bytes)
        py_log('Send Message Length:')
        py_log(len(requested_bytes))        






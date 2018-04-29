# video flow server script here

import socket
import sys

ip   = sys.argv[1].strip()
port = int(sys.argv[2].strip())

videofile = "sample-video.mp4"

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind( (ip, port) )
serv.listen(5)

with open(videofile, "rb") as f:
    
    while True:
        conn, addr = serv.accept()
        request_size = conn.recv(10)
        request_size = int(request_size.strip())
        print 'Got Message:'
        print request_size
        requested_bytes = f.read(request_size)
        conn.send(requested_bytes)
        print 'Send Message Length:'
        print len(requested_bytes)
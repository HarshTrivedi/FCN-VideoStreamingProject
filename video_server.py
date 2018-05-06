# video flow server script here

import socket
import sys

ip   = sys.argv[1].strip()
port = int(sys.argv[2].strip())

log_file = 'logs/video_server_py.log'
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

# with open(videofile, "rb") as f:    
    # while True:
    #     conn, addr = serv.accept()
    #     request_size = conn.recv(10)
    #     request_size = int(request_size.strip())
    #     py_log('Got Message:')
    #     py_log(request_size)
    #     requested_bytes = ('*'*request_size)
    #     conn.send(requested_bytes)
    #     py_log('Send Message Length:')
    #     py_log(len(requested_bytes))        
    #     conn.close()

while True:
    conn, addr = serv.accept()
    request_size = conn.recv(10)
    request_size = int(request_size.strip())
    py_log('Got Message:')
    py_log(request_size)
    requested_bytes = ('*'*request_size)
    conn.send(requested_bytes)
    py_log('Send Message Length:')
    py_log(len(requested_bytes))        
    conn.close()






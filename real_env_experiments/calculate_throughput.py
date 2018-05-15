#!/usr/bin/env python
import sys

log_file = open(sys.argv[1])

time=0
last = 0
num_bytes = 0
for line in log_file:
    element = line.split()

    if(element[0]!='#' and element[1]!='-'):
        ts = int(element[0])

        if time - last > 3000:
            kbps = (num_bytes*8/1000.0)/(interval*1000.0)
            print ("%s , %s") %(last/1000.0),kbps
            interval = time-last
            num_bytes=float(element[2])
            last=time

        else:
            num_bytes += float(element[2])

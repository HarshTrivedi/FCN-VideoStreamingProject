import matplotlib
# matplotlib.use('Agg')
import math
import matplotlib.pyplot as plt
import os
import shutil
import sys

logdir  = '.'

all_timestamps = []

cclient_throughputs = []
with open('competing.csv'.format(logdir) ) as f:
	for line in f.readlines():
		array = line.strip().split(',')
		timestamp = float(array[0])
		throughput = float(array[1])
		cclient_throughputs.append( (timestamp, throughput) )
		all_timestamps.append( int(timestamp) )

cclient_min_timestamp = min([ e[0] for e in cclient_throughputs])
cclient_max_timestamp = max([ e[0] for e in cclient_throughputs])


vclient_throughputs = []
with open('client.csv'.format(logdir)) as f:
	for line in f.readlines():
		array = line.strip().split(',')
		timestamp = float(array[0])
		throughput = float(array[1])
		vclient_throughputs.append( (timestamp, throughput) )
		all_timestamps.append( int(timestamp) )

vclient_min_timestamp = min([ e[0] for e in vclient_throughputs])
vclient_max_timestamp = max([ e[0] for e in vclient_throughputs])


playback_rates = []
with open('playback_rates.csv'.format(logdir)) as f:
	for line in f.readlines():
		array = line.strip().split(',')
		timestamp = float(array[0])
		playback_rate = float(array[1])
		playback_rates.append( (timestamp, playback_rate) )
		all_timestamps.append( int(timestamp) )

playback_rate_min_timestamp = min([ e[0] for e in playback_rates])
playback_rate_max_timestamp = max([ e[0] for e in playback_rates])

min_timestamp = playback_rate_min_timestamp
max_timestamp = playback_rate_max_timestamp
plot_duration = max_timestamp - min_timestamp


extra_cclient_entries = []
for timestamp, _ in vclient_throughputs:
	if timestamp > cclient_max_timestamp:
		extra_cclient_entries.append( (timestamp, 0.0) )
cclient_throughputs += extra_cclient_entries


cclient_throughputs = [  (   e[0]-min_timestamp   ,  ((e[1]) / (1000.0))  )  for e in cclient_throughputs]
vclient_throughputs = [  (   e[0]-min_timestamp   ,  ((e[1]) / (1000.0))  )  for e in vclient_throughputs]
playback_rates      = [  (   e[0]-min_timestamp   ,  ((e[1]) / (1000.0))  )  for e in playback_rates]

competing_start_marker = None
competing_end_marker   = None


# Get the competing flow start / end markers
threshold = 0.1
for entry in cclient_throughputs:
	if entry[0] > 0 and entry[0]<=plot_duration:
		if not competing_start_marker:
			if entry[1] > threshold:
				competing_start_marker = entry[0]
		if competing_start_marker:
			if not competing_end_marker:
				if entry[1] < threshold:
					competing_end_marker = entry[0]



def ksmooth(array, k ):
	return [ sum(array[max(i-k,0):i+1])/float(i+1-max(i-k,0))  for i,x in enumerate(array)]

k = 1

plt.style.use('seaborn-whitegrid')
plt.plot( [ e[0] for e in vclient_throughputs], ksmooth([ e[1] for e in vclient_throughputs],k), '-r', label='video throughput'        , linewidth=2.0)
plt.plot( [ e[0] for e in cclient_throughputs], ksmooth([ e[1] for e in cclient_throughputs],k), '-g', label='competing throughput'    , linewidth=2.0)
plt.plot( [ e[0] for e in playback_rates     ], [ e[1] for e in playback_rates  ]                , '-b' , label='playback rate'        , linewidth=2.0)

plt.xlabel('Time (s)')
plt.ylabel('Mbits/s')
plt.xlim(0,plot_duration)
# plt.ylim(0,5)

plt.axvspan(competing_start_marker, competing_end_marker, alpha=0.3, color='yellow')
plt.legend(loc='lower left', prop=dict(weight='bold'))
# plt.show()
plt.savefig('plot.png')

import math
import matplotlib.pyplot as plt
import numpy as np

log_dir = 'logs'
all_timestamps = []


vclient_throughputs = []
with open('{}/throughput-vclient-eth0.log'.format(log_dir)) as f:
	for line in f.readlines():
		array = line.strip().split('\t')
		timestamp = float(array[0])
		throughput = float(array[2])
		vclient_throughputs.append( (round(timestamp,1), throughput) )
		all_timestamps.append( round(timestamp,1) )


cclient_throughputs = []
with open('{}/throughput-cclient-eth0.log'.format(log_dir) ) as f:
	for line in f.readlines():
		array = line.strip().split('\t')
		timestamp = float(array[0])
		throughput = float(array[2])
		cclient_throughputs.append( (round(timestamp,1), throughput) )
		all_timestamps.append( round(timestamp,1) )



cwnds = []
with open('{}/cwnd-5000.log'.format(log_dir) ) as f:
	for line in f.readlines():
		array = line.strip().split('\t')
		if array[2] != 'None':
			timestamp = float(array[0])
			cwnd = float(array[2])
			cwnds.append( ( round(timestamp,1) , cwnd) )
			all_timestamps.append( round(timestamp,1) )

min_timestamp = min(all_timestamps)


with open('{}/cwnd_experiment_marks.txt'.format(log_dir), 'r') as f:
	marks = [ round(float(e),1) for e in f.read().strip().split()]

def ksmooth(array, k ):
	return [ sum(array[max(i-k,0):i+1])/float(i+1-max(i-k,0))  for i,x in enumerate(array)]


plt.plot( [ x[0]-min_timestamp for x in cwnds], [ x[1]/ 1000.0 for x in cwnds  ], '-b', label='video flow cwnd' )
plt.axvspan( marks[0]-min_timestamp , marks[1]-min_timestamp, alpha=0.2, color='green')
plt.axvspan( marks[1]-min_timestamp , marks[2]-min_timestamp, alpha=0.2, color='red'  )
plt.axvspan( marks[2]-min_timestamp , marks[3]-min_timestamp, alpha=0.2, color='green')
plt.axvspan( marks[3]-min_timestamp , marks[4]-min_timestamp, alpha=0.2, color='red'  )
plt.axvspan( marks[4]-min_timestamp , marks[5]-min_timestamp, alpha=0.2, color='green'  )
plt.xlim( marks[0]-min_timestamp, marks[-1]-min_timestamp)
plt.xlabel('time (seconds)')
plt.ylabel('K Bytes')
plt.legend()
# plt.show()
plt.savefig('plots/cwnd.png')


plt.clf()


k=20

plt.plot( [ x[0]-min_timestamp for x in vclient_throughputs], ksmooth( [ x[1]/(1e6) for x in vclient_throughputs] ,k), '-b', label='video-throughput'  )
plt.plot( [ x[0]-min_timestamp for x in cclient_throughputs], ksmooth( [ x[1]/(1e6) for x in cclient_throughputs] ,k), '-r', label='competing-throughput'  )
plt.axvspan( marks[0]-min_timestamp , marks[1]-min_timestamp, alpha=0.2, color='green')
plt.axvspan( marks[1]-min_timestamp , marks[2]-min_timestamp, alpha=0.2, color='red'  )
plt.axvspan( marks[2]-min_timestamp , marks[3]-min_timestamp, alpha=0.2, color='green')
plt.axvspan( marks[3]-min_timestamp , marks[4]-min_timestamp, alpha=0.2, color='red'  )
plt.axvspan( marks[4]-min_timestamp , marks[5]-min_timestamp, alpha=0.2, color='green'  )
plt.xlim( marks[0]-min_timestamp, marks[-1]-min_timestamp)
plt.xlabel('time (seconds)')
plt.ylabel('M Bits/s')
plt.legend()
# plt.show()
plt.savefig('plots/throughputs.png')





import math
import matplotlib.pyplot as plt

all_timestamps = []


# vclient_throughputs = []
# with open('logs/throughput-cclient-eth0.log') as f:
# 	for line in f.readlines():
# 		array = line.strip().split('\t')
# 		timestamp = float(array[0])
# 		throughput = float(array[2])
# 		vclient_throughputs.append( (timestamp, throughput) )
# 		all_timestamps.append( int(timestamp) )


cwnds = []
with open('logs/cwnd-5000.log') as f:
	for line in f.readlines():
		array = line.strip().split('\t')
		timestamp = float(array[0])
		cwnd = float(array[2])
		cwnds.append( (timestamp, cwnd) )
		all_timestamps.append( int(timestamp) )
min_timestamp = min(all_timestamps)
max_timestamp = max(all_timestamps)

buffer_step_toggle_index = None
with open('logs/buffer_toggle_hit_time.txt', 'r') as f:
	buffer_toggle_timestamp = float(f.read().strip().split()[0])


synchronized_cwnds = []
synchronized_vclient_throughputs = []

step_toggle = None
for index, time_stamp in enumerate(range(min_timestamp, max_timestamp)):

	# vclient_throughput = sorted(vclient_throughputs, key = lambda e: abs(int(e[0]) - time_stamp)  )[0][1]
	cwnd = sorted(cwnds, key = lambda e: abs(int(e[0]) - time_stamp)  )[0][1]

	# synchronized_vclient_throughputs.append( (8*vclient_throughput) / (1024*1024.0) ) # MBits/s
	synchronized_cwnds.append( cwnd )

	if buffer_step_toggle_index is None:
		if time_stamp >= buffer_toggle_timestamp:
			buffer_step_toggle_index = index-1


competing_step_toggle_index = 50
# synchronized_cwnds = synchronized_cwnds[:50]

def ksmooth(array, k ):
	return [ sum(array[max(i-k,0):i+1])/float(i+1-max(i-k,0))  for i,x in enumerate(array)]


x_axis = range(len(synchronized_cwnds))

plt.style.use('seaborn-whitegrid')
plt.plot( x_axis, ksmooth(synchronized_cwnds,2), '-g', label='video flow cwnds')
# plt.plot( x_axis, synchronized_vclient_throughputs, '-r', label='video thr')
plt.axvspan(competing_step_toggle_index, len(x_axis), alpha=0.5, color='yellow')
plt.axvspan(buffer_step_toggle_index, len(x_axis), alpha=0.3, color='blue')
plt.xlabel('seconds')
plt.ylabel('cwnds (bytes)')
plt.xlim(0,len(x_axis))
plt.legend( loc='upper right')
# plt.show()
plt.savefig('plots/cwnds_vs_bufferfill.png')


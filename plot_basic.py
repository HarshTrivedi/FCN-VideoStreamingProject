import math
import matplotlib.pyplot as plt
# playback_buffer.log  request_interval.log         throughput-vclient-eth0.log  video_server_py.log
# playback_rate.log    throughput-cclient-eth0.log  video_client_py.log

all_timestamps = []

cclient_throughputs = []
with open('logs/throughput-cclient-eth0.log') as f:
	for line in f.readlines():
		array = line.strip().split('\t')
		timestamp = float(array[0])
		throughput = float(array[2])
		cclient_throughputs.append( (timestamp, throughput) )
		all_timestamps.append( int(timestamp) )


vclient_throughputs = []
with open('logs/throughput-vclient-eth0.log') as f:
	for line in f.readlines():
		array = line.strip().split('\t')
		timestamp = float(array[0])
		throughput = float(array[2])
		vclient_throughputs.append( (timestamp, throughput) )
		all_timestamps.append( int(timestamp) )


estm_vthroughputs = []
with open('logs/estm-throughput-vclient.log') as f:
	for line in f.readlines():
		array = line.strip().split('\t')
		timestamp = float(array[0])
		throughput = float(array[2])
		estm_vthroughputs.append( (timestamp, throughput) )
		all_timestamps.append( int(timestamp) )



playback_rates = []
with open('logs/playback_rate.log') as f:
	for line in f.readlines():
		array = line.strip().split('\t')
		timestamp = float(array[0])
		playback_rate = float(array[2])
		playback_rates.append( (timestamp, playback_rate) )
		all_timestamps.append( int(timestamp) )


min_timestamp = min(all_timestamps)
max_timestamp = max(all_timestamps)


synchronized_vclient_throughputs = []
synchronized_cclient_throughputs = []
synchronized_playback_rates      = []
synchronized_estm_throughputs    = []

# print range(min_timestamp, max_timestamp)

buffer_step_toggle_index = None
with open('logs/buffer_toggle_hit_time.txt', 'r') as f:
	buffer_toggle_timestamp = float(f.read().strip().split()[0])


for index, time_stamp in enumerate(range(min_timestamp, max_timestamp)):
	# print sorted(vclient_throughputs, key = lambda e: abs(int(e[0]) - time_stamp)  )[0][1]
	vclient_throughput = sorted(vclient_throughputs, key = lambda e: abs(int(e[0]) - time_stamp)  )[0][1]
	cclient_throughput = sorted(cclient_throughputs, key = lambda e: abs(int(e[0]) - time_stamp)  )[0][1]

	estm_throughput    = sorted(estm_vthroughputs, key = lambda e: abs(int(e[0]) - time_stamp)  )[0][1]
	playback_rate      = sorted(playback_rates, key = lambda e: abs(int(e[0]) - time_stamp)  )[0][1]

	synchronized_vclient_throughputs.append( (8*vclient_throughput) / (1024*1024.0) ) # MBits/s
	synchronized_cclient_throughputs.append( (8*cclient_throughput) / (1024*1024.0) ) # MBits/s
	synchronized_estm_throughputs.append( (8*estm_throughput) / (1024*1024.0) ) # MBits/s
	synchronized_playback_rates.append( (8*playback_rate) / (1024*1024.0) )           # MBits/s


	if buffer_step_toggle_index is None:
		if time_stamp >= buffer_toggle_timestamp:
			buffer_step_toggle_index = index-1

competing_step_toggle_index = 49 # because competing flow starts at 50th second
x_axis = range(len(synchronized_vclient_throughputs))

def ksmooth(array, k ):
	return [ sum(array[max(i-k,0):i+1])/float(i+1-max(i-k,0))  for i,x in enumerate(array)]

k = 2
plt.style.use('seaborn-whitegrid')
plt.plot( x_axis, ksmooth(synchronized_vclient_throughputs,k), '-r', label='vid. thr')
plt.plot( x_axis, ksmooth(synchronized_cclient_throughputs,k), '-g', label='compet. thr')
plt.plot( x_axis, ksmooth(synchronized_playback_rates,k), '-b', label='playback rate')
# plt.plot( x_axis, ksmooth(synchronized_estm_throughputs,k), '-', label='estm. client thr')

plt.axvspan(competing_step_toggle_index, len(x_axis), alpha=0.5, color='yellow')
plt.axvspan(buffer_step_toggle_index, len(x_axis), alpha=0.3, color='blue')

plt.xlabel('seconds')
plt.ylabel('Mbits/s')
plt.xlim(0,len(x_axis))
plt.ylim(0,5)
plt.legend( loc='lower left')
plt.show()
# plt.savefig('main_experiment.png')






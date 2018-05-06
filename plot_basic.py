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


# print range(min_timestamp, max_timestamp)

for time_stamp in range(min_timestamp, max_timestamp):
	# print sorted(vclient_throughputs, key = lambda e: abs(int(e[0]) - time_stamp)  )[0][1]
	vclient_throughput = sorted(vclient_throughputs, key = lambda e: abs(int(e[0]) - time_stamp)  )[0][1]
	cclient_throughput = sorted(cclient_throughputs, key = lambda e: abs(int(e[0]) - time_stamp)  )[0][1]
	playback_rate      = sorted(playback_rates, key = lambda e: abs(int(e[0]) - time_stamp)  )[0][1]

	synchronized_vclient_throughputs.append( (8*vclient_throughput) / (1024*1024.0) ) # MBits/s
	synchronized_cclient_throughputs.append( (8*cclient_throughput) / (1024*1024.0) ) # MBits/s
	synchronized_playback_rates.append( (8*playback_rate) / (1024*1024.0) )           # MBits/s

x_axis = range(len(synchronized_vclient_throughputs))

plt.style.use('seaborn-whitegrid')
plt.plot( x_axis, synchronized_vclient_throughputs, '-r', label='video throughput')
plt.plot( x_axis, synchronized_cclient_throughputs, '-g', label='competing throughput')
plt.plot( x_axis, synchronized_playback_rates, '-b', label='playback rate')
plt.xlabel('seconds')
plt.ylabel('Mbits/s')
plt.legend()
# plt.show()
plt.savefig('main_experiment.png')

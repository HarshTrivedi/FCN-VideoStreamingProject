import math
import matplotlib.pyplot as plt

all_timestamps = []

request_intervals = []
with open('logs/request_interval.log') as f:
	for line in f.readlines():
		array = line.strip().split('\t')
		timestamp = float(array[0])
		request_interval = float(array[2])
		request_intervals.append( (timestamp, request_interval) )
		all_timestamps.append( int(timestamp) )
min_timestamp = min(all_timestamps)
max_timestamp = max(all_timestamps)

buffer_step_toggle_index = None
with open('logs/buffer_toggle_hit_time.txt', 'r') as f:
	buffer_toggle_timestamp = float(f.read().strip().split()[0])


synchronized_request_intervals = []

step_toggle = None
for index, time_stamp in enumerate(range(min_timestamp, max_timestamp)):

	request_interval = sorted(request_intervals, key = lambda e: abs(int(e[0]) - time_stamp)  )[0][1]
	synchronized_request_intervals.append( request_interval )

	if buffer_step_toggle_index is None:
		if time_stamp >= buffer_toggle_timestamp:
			buffer_step_toggle_index = index-1

# synchronized_request_intervals = synchronized_request_intervals[:50]

x_axis = range(len(synchronized_request_intervals))

plt.style.use('seaborn-whitegrid')
plt.plot( x_axis, synchronized_request_intervals, '-r', label='vid. thr')
plt.axvspan(buffer_step_toggle_index, len(x_axis), alpha=0.3, color='blue')
plt.xlabel('seconds')
plt.ylabel('request interval (s)')
plt.xlim(0,len(x_axis))
plt.ylim(0,5)
plt.legend( loc='upper left')
# plt.show()
plt.savefig('plots/request_interval_vs_bufferfill.png')


import math
import matplotlib.pyplot as plt

all_timestamps = []

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

step_toggle = None
for index, time_stamp in enumerate(range(min_timestamp, max_timestamp)):

	cwnd = sorted(cwnds, key = lambda e: abs(int(e[0]) - time_stamp)  )[0][1]
	synchronized_cwnds.append( cwnd )

	if buffer_step_toggle_index is None:
		if time_stamp >= buffer_toggle_timestamp:
			buffer_step_toggle_index = index-1


competing_step_toggle_index = 50
# synchronized_cwnds = synchronized_cwnds[:50]

x_axis = range(len(synchronized_cwnds))

plt.style.use('seaborn-whitegrid')
plt.plot( x_axis, synchronized_cwnds, '-g', label='video flow cwnds')
plt.axvspan(competing_step_toggle_index, len(x_axis), alpha=0.5, color='yellow')
plt.axvspan(buffer_step_toggle_index, len(x_axis), alpha=0.3, color='blue')
plt.xlabel('seconds')
plt.ylabel('cwnds (bytes)')
plt.xlim(0,len(x_axis))
plt.legend( loc='upper right')
# plt.show()
plt.savefig('plots/cwnds_vs_bufferfill.png')


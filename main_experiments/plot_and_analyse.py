import matplotlib
matplotlib.use('Agg')
import math
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
import os
import shutil
import sys

# exp = 'A'
# print 'Exp: {}'.format(exp)
# log_dir = 'Final-logs-{}'.format(exp)
# plotdir = 'Final-plots-{}'.format(exp)

exp     = sys.argv[1]
logdir  = 'logs/logs-{}'.format(exp)
plotdir = 'plots/plots-{}'.format(exp)


all_timestamps = []

cclient_throughputs = []
with open('{}/throughput-cclient-eth0.log'.format(logdir) ) as f:
	for line in f.readlines():
		array = line.strip().split('\t')
		timestamp = float(array[0])
		throughput = float(array[2])
		cclient_throughputs.append( (timestamp, throughput) )
		all_timestamps.append( int(timestamp) )


vclient_throughputs = []
with open('{}/throughput-vclient-eth0.log'.format(logdir)) as f:
	for line in f.readlines():
		array = line.strip().split('\t')
		timestamp = float(array[0])
		throughput = float(array[2])
		vclient_throughputs.append( (timestamp, throughput) )
		all_timestamps.append( int(timestamp) )


estm_vthroughputs = []
with open('{}/receive-throughput-vclient.log'.format(logdir)) as f:
	for line in f.readlines():
		array = line.strip().split('\t')
		timestamp = float(array[0])
		throughput = float(array[2])
		estm_vthroughputs.append( (timestamp, throughput) )
		all_timestamps.append( int(timestamp) )



playback_rates = []
with open('{}/playback_rate.log'.format(logdir)) as f:
	for line in f.readlines():
		array = line.strip().split('\t')
		timestamp = float(array[0])
		playback_rate = float(array[2])
		playback_rates.append( (timestamp, playback_rate) )
		all_timestamps.append( int(timestamp) )


request_intervals = []
with open('{}/request_interval.log'.format(logdir)) as f:
	for line in f.readlines():
		array = line.strip().split('\t')
		timestamp = float(array[0])
		request_interval = float(array[2])
		request_intervals.append( (timestamp, request_interval) )
		all_timestamps.append( int(timestamp) )



min_timestamp = min(all_timestamps)
max_timestamp = max(all_timestamps)
plot_duration = max_timestamp - min_timestamp
  

cclient_throughputs = [  (   e[0]-min_timestamp   ,  ((8*e[1]) / (1000*1000.0))  )  for e in cclient_throughputs]
vclient_throughputs = [  (   e[0]-min_timestamp   ,  ((8*e[1]) / (1000*1000.0))  )  for e in vclient_throughputs]
estm_vthroughputs   = [  (   e[0]-min_timestamp   ,  ((8*e[1]) / (1000*1000.0))  )  for e in estm_vthroughputs]
playback_rates      = [  (   e[0]-min_timestamp   ,  ((8*e[1]) / (1000*1000.0))  )  for e in playback_rates]
request_intervals   = [  (   e[0]-min_timestamp   ,  e[1]  )  for e in request_intervals]

def ksmooth(array, k ):
	return [ sum(array[max(i-k,0):i+1])/float(i+1-max(i-k,0))  for i,x in enumerate(array)]

k = 10

##########
playback_buffers = []
with open('{}/playback_buffer.log'.format(logdir)) as f:
	for line in f.readlines():
		array = line.strip().split('\t')
		timestamp = float(array[0])
		playback_buffer = float(array[2])
		playback_buffers.append( (timestamp, playback_buffer) )

timediff = round(playback_buffers[1][0] - playback_buffers[0][0], 2)
playback_rebuffers_count = len([ 1  for playback_buffer in playback_buffers if playback_buffer[1] < 2])
playback_rebuffer_time = round(playback_rebuffers_count*timediff,2)
##########

##########
buffer_toggle_hit_file   = '{}/buffer_toggle_hit_time.txt'.format(logdir)
if os.path.exists(buffer_toggle_hit_file):
    with open(buffer_toggle_hit_file, 'r') as f:
        buffer_toggle_timestamp = float(f.read().strip().split()[0])-min_timestamp
else:
    buffer_toggle_timestamp = plot_duration
##########

##########
competing_flow_start_time_file   = '{}/competing_flow_start_time.txt'.format(logdir)
if os.path.exists(competing_flow_start_time_file):
    with open(competing_flow_start_time_file, 'r') as f:
        competing_flow_start_timestamp = float(f.read().strip().split()[0])-min_timestamp
else:
    competing_flow_start_timestamp = plot_duration
##########

##########
competing_flow_end_time_file   = '{}/competing_flow_end_time.txt'.format(logdir)
if os.path.exists(competing_flow_end_time_file):
    with open(competing_flow_end_time_file, 'r') as f:
        competing_flow_end_timestamp = float(f.read().strip().split()[0])-min_timestamp
else:
    competing_flow_end_timestamp = plot_duration
##########



if not os.path.exists(plotdir):
	os.makedirs(plotdir)

plt.style.use('seaborn-whitegrid')
plt.plot( [ e[0] for e in vclient_throughputs], ksmooth([ e[1] for e in vclient_throughputs],k), '-m', label='video throughput'        , linewidth=2.0)
plt.plot( [ e[0] for e in cclient_throughputs], ksmooth([ e[1] for e in cclient_throughputs],k), '-g', label='competing throughput'    , linewidth=2.0)
plt.plot( [ e[0] for e in playback_rates     ], [ e[1] for e in playback_rates  ]              , '-b', label='playback rate'           , linewidth=2.0)
plt.plot( [ e[0] for e in estm_vthroughputs  ], ksmooth([ e[1] for e in estm_vthroughputs  ],k), '-r', label='video b/w estimates'        , linewidth=2.0)



plt.xlabel('Time (s)')
plt.ylabel('Mbits/s')
plt.xlim(0,plot_duration)
plt.ylim(0,5)
plt.legend(loc='lower left' )
plt.figtext(0.5, 0,"Total Rebuffering Wait Time:  {} (s)".format( playback_rebuffer_time )  , wrap=True,
            horizontalalignment='center')
plt.axvspan(competing_flow_start_timestamp, competing_flow_end_timestamp, alpha=0.3, color='yellow')
plt.axvspan(buffer_toggle_timestamp, plot_duration, alpha=0.3, color='blue')
plt.savefig('{}/main_experiment.png'.format(plotdir),transparent=True, bbox_inches='tight' )
# plt.show()


plt.clf()



###########################################
###########################################

plt.style.use('seaborn-whitegrid')
plt.plot( [ e[0] for e in request_intervals], ksmooth([ e[1] for e in request_intervals],k), '-r' )
plt.axvspan(buffer_toggle_timestamp, plot_duration, alpha=0.3, color='blue')
plt.xlabel('seconds')
plt.ylabel('request interval (s)')
plt.xlim(0,plot_duration)
plt.ylim(0,5)
plt.legend( loc='upper left')
# plt.show()
plt.savefig('{}/request_interval_vs_bufferfill.png'.format(plotdir),transparent=True, bbox_inches='tight')



import matplotlib.pyplot as plt


def select_playback_bitrate(throughput_bitps, optimistic = False):

    rates_kbitps = [235,   375,    560,     750,    1050,   1400, 1750]
    rates_bitps = [ x* 1024 for x in rates_kbitps]

    if not optimistic:
        if throughput_bitps > (2500 * 1024):
            bit_rate = rates_bitps[6] # 1750*1024 bits/s
        elif throughput_bitps > (2150 * 1024):
            bit_rate = rates_bitps[5] # 1400*1024 bits/s
        elif throughput_bitps > (1300 * 1024):
            bit_rate = rates_bitps[4] # 1050*1024 kbits/s
        elif throughput_bitps > (1100 * 1024):
            bit_rate = rates_bitps[3] # 750*1024 bits/s
        elif throughput_bitps > (740 * 1024):
            bit_rate = rates_bitps[2] # 560*1024 bits/s
        elif throughput_bitps > (500 * 1024):
            bit_rate = rates_bitps[1] # 375*1024 bits/s
        else:
            bit_rate = rates_bitps[0]   # 235*1024 bits/s
    else:
        if throughput_bitps > (1750 * 1024):
            bit_rate = rates_bitps[6] # 1750*1024 bits/s
        elif throughput_bitps > (1400 * 1024):
            bit_rate = rates_bitps[5] # 1400*1024 bits/s
        elif throughput_bitps > (1050 * 1024):
            bit_rate = rates_bitps[4] # 1050*1024 kbits/s
        elif throughput_bitps > (750 * 1024):
            bit_rate = rates_bitps[3] # 750*1024 bits/s
        elif throughput_bitps > (560 * 1024):
            bit_rate = rates_bitps[2] # 560*1024 bits/s
        elif throughput_bitps > (375 * 1024):
            bit_rate = rates_bitps[1] # 375*1024 bits/s
        else:
            bit_rate = rates_bitps[0]   # 235*1024 bits/s

    return bit_rate


optimistic = True

for optimistic in [True, False]:
    bandwidths     = range( 0, 3000*1024)
    playback_rates = []
    for bandwidth in bandwidths:
        playback_rate = select_playback_bitrate(bandwidth, optimistic = optimistic)
        playback_rates.append( playback_rate )


    plt.plot([ x/(1024*1024.0) for x in bandwidths], [ x/(1024*1024.0) for x in playback_rates], '-r', label='selected rate')
    plt.plot([ x/(1024*1024.0) for x in bandwidths], [ x/(1024*1024.0) for x in bandwidths], '-b', label='reference line')
    plt.xlabel('estimated throughput (MBit/s)')
    plt.ylabel('playback_rates (MBit/s)')
    plt.xlim(0,3.0)
    plt.ylim(0,3.0)
    plt.legend()
    if not optimistic:
        plt.title('Playback Rate Selection replicating Netflix')
    else:
        plt.title('Playback Rate Selection replicating Netflix (With Optimism)')
    plt.savefig('client_categarization/client-chategorization-optimism-{}'.format(optimistic) )
    plt.clf()





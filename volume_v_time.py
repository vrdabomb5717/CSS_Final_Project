#!/usr/bin/env python3

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt, rc
import pandas as pd


SUMMARY = pd.read_hdf('data/msd_summary_file.h5', 'analysis/songs')
SUMMARY = SUMMARY[['track_id', 'loudness']]
SUMMARY.track_id = SUMMARY.track_id.map(lambda x: x.decode('utf-8'))
SUMMARY.set_index('track_id', inplace=True)


def id_to_loud(track_id):
    return SUMMARY.loc[track_id][0]


# TODO: Remove years with only a couple of songs.
def year_lists():
    result = [[[], []]]
    count = 0
    with open('data/tracks_per_year.txt') as year_data:
        cur_yr, track_id, _, _ = year_data.readline().strip().split('<SEP>')
        cur_yr = int(cur_yr)
        dur = id_to_loud(str(track_id))
        result[0][0] = cur_yr
        result[0][1].append(dur)
        for line in year_data:
            cur_yr, track_id, _, _ = line.strip().split('<SEP>')
            cur_yr = int(cur_yr)
            dur = id_to_loud(str(track_id))
            if cur_yr == result[count][0]:
                result[count][1].append(dur)
            else:
                result.append([cur_yr, [dur]])
                count += 1
    return result


def averager(louds):
    return sum(louds) / len(louds)


def main():
    loud_data = [[ylist[0], averager(ylist[1])] for ylist in year_lists()]
    years, louds = zip(*loud_data)

    rc('text', usetex=True)
    rc('font', family='serif')
    plt.plot(years, louds)
    first = min(years)
    last = max(years)
    plt.title('Average Loudness per Year ({}-{})'.format(first, last))
    plt.xlim((first, last))
    plt.xlabel('Year')
    plt.ylabel('Volume (dBFS)')
    plt.savefig('data/graphs/graph_volume_v_time.png')


if __name__ == '__main__':
    main()

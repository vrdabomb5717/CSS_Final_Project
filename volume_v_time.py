#!/usr/bin/env python3
"""
Make a plot of loudness in decibels relative to full scale versus time. Exclude
years with insufficient data.

"""

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt, rc
import pandas as pd


# We only want part of the hdfs file.
SUMMARY = pd.read_hdf('data/msd_summary_file.h5', 'analysis/songs')
SUMMARY = SUMMARY[['track_id', 'loudness']]
# We need to convert the track_id byte arrays to strings.
SUMMARY.track_id = SUMMARY.track_id.map(lambda x: x.decode('utf-8'))
# The goal is a mapping of track_id to tempo.
SUMMARY.set_index('track_id', inplace=True)


def id_to_loud(track_id):
    """Look up the loudness for a given track_id."""
    return SUMMARY.loc[track_id][0]


def year_lists():
    """
    Return the next list containing a year and a list of loudnesses for songs
    from that year.

    """
    with open('data/tracks_per_year.txt') as year_data:
        cur_yr, track_id, _, _ = year_data.readline().strip().split('<SEP>')
        cur_yr = int(cur_yr)
        dur = id_to_loud(track_id)
        result = [cur_yr, [dur]]
        for line in year_data:
            cur_yr, track_id, _, _ = line.strip().split('<SEP>')
            cur_yr = int(cur_yr)
            dur = id_to_loud(track_id)
            # Append a duration if the year matches.
            if cur_yr == result[0]:
                result[1].append(dur)
            # Append a new year list if the year doesn't match.
            else:
                yield result
                result = [cur_yr, [dur]]
        yield result


def averager(louds):
    """Given a list of loudnesses, find the average."""
    return sum(louds) / len(louds)


def main():
    """Get the loudness information and make a graph."""
    loud_data = [[ylist[0], averager(ylist[1])] for ylist in year_lists() \
                  if len(ylist[1]) >= 10]
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

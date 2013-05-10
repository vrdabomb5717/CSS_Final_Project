#!/usr/bin/env python3
"""
Make a plot of tempo in beats per minute versus time. Exclude years with
insufficient data.

"""

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt, rc
import pandas as pd
import numpy as np


# We only want part of the hdfs file.
SUMMARY = pd.read_hdf('data/msd_summary_file.h5', 'analysis/songs')
SUMMARY = SUMMARY[['track_id', 'tempo']]
# We need to convert the track_id byte arrays to strings.
SUMMARY.track_id = SUMMARY.track_id.map(lambda x: x.decode('utf-8'))
# The goal is a mapping of track_id to tempo.
SUMMARY.set_index('track_id', inplace=True)


def id_to_tempo(track_id):
    """Look up the tempo for a given track_id."""
    return SUMMARY.loc[track_id][0]


def year_lists():
    """
    Return the next list containing a year and a list of tempoes for songs from
    that year.

    """
    with open('data/tracks_per_year.txt') as year_data:
        cur_yr, track_id, _, _ = year_data.readline().strip().split('<SEP>')
        cur_yr = int(cur_yr)
        tempo = id_to_tempo(track_id)
        result = [cur_yr, [tempo]]
        for line in year_data:
            cur_yr, track_id, _, _ = line.strip().split('<SEP>')
            cur_yr = int(cur_yr)
            tempo = id_to_tempo(track_id)
            # Append a tempo if the year matches.
            if cur_yr == result[0]:
                result[1].append(tempo)
            # Reset the year list if the year doesn't match.
            else:
                yield result
                result = [cur_yr, [tempo]]
        yield result


def averager(tempoes):
    """Given a list of tempoes, remove the 0 values and find the average."""
    tempoes = np.array(tempoes)
    tempoes = tempoes[tempoes != 0]
    return np.mean(tempoes)
    


def main():
    """Get the tempo information and make a graph."""
    tempo_data = [[ylist[0], averager(ylist[1])] for ylist in year_lists() \
                   if len(ylist[1]) >= 10]
    years, tempoes = zip(*tempo_data)

    rc('text', usetex=True)
    rc('font', family='serif')
    plt.plot(years, tempoes)
    first = min(years)
    last = max(years)
    plt.title('Average Tempo per Year ({}-{})'.format(first, last))
    plt.xlim((first, last))
    plt.xlabel('Year')
    plt.ylabel('Tempo (beats per minute)')
    plt.savefig('data/graphs/graph_tempo_v_time.png')


if __name__ == '__main__':
    main()

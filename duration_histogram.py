#!/usr/bin/env python3
"""Make a histogram of durations with 30 bins."""

import sqlite3
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt, rc
import numpy as np


def main():
    """Use SQL to get the data and matplotlib to bin it and graph it."""
    conn = sqlite3.connect('data/track_metadata.db')
    curs = conn.cursor()
    curs.execute('select duration from songs;')
    dur_data = curs.fetchall()
    durations = [dur[0] / 60 for dur in dur_data]

    rc('text', usetex=True)
    rc('font', family='serif')
    plt.hist(durations, bins=30)
    plt.title('Distribution of Durations')
    plt.xlabel('Duration (minutes)')
    plt.ylabel('Count')
    plt.savefig('data/graphs/graph_duration_histogram.png')

    print('Statistics on the Distribution:')
    print('\tcount: {}'.format(len(durations)))
    print('\tmean: {} minutes'.format(np.mean(durations)))
    print('\tstd: {} minutes'.format(np.std(durations)))
    print('\tmin: {} minutes'.format(np.min(durations)))
    print('\t25%: {} minutes'.format(np.percentile(durations, 0.25)))
    print('\t50%: {} minutes'.format(np.percentile(durations, 0.5)))
    print('\t75%: {} minutes'.format(np.percentile(durations, 0.75)))
    print('\tmax: {} minutes'.format(np.max(durations)))


if __name__ == '__main__':
    main()

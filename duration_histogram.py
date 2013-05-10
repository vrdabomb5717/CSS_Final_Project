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
    sigma = np.std(dur_data)
    durations = [dur[0] / 60 for dur in dur_data]

    rc('text', usetex=True)
    rc('font', family='serif')
    plt.hist(durations, bins=30)
    plt.title('Distribution of Durations')
    plt.xlabel('Duration (minutes)')
    plt.ylabel('Count')
    plt.savefig('data/graphs/graph_duration_histogram.png')
    print('Standard deviation: {}'.format(sigma))


if __name__ == '__main__':
    main()

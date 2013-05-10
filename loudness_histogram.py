#!/usr/bin/env python3
"""Make a histogram of loudnesses with 40 bins."""

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt, rc
import pandas as pd
import numpy as np


# Pick out the loudness information.
SUMMARY = pd.read_hdf('data/msd_summary_file.h5', 'analysis/songs')
SUMMARY = SUMMARY['loudness']
SUMMARY = SUMMARY.map(float)


def main():
    """Bin the data and plot it."""
    rc('text', usetex=True)
    rc('font', family='serif')
    plt.hist(SUMMARY, bins=40)
    plt.title('Distribution of Loudness')
    plt.xlabel('Loudness (dBFS)')
    plt.ylabel('Count')
    plt.savefig('data/graphs/graph_loudness_histogram.png')
    print('Standard deviation: {}'.format(np.std(SUMMARY)))


if __name__ == '__main__':
    main()
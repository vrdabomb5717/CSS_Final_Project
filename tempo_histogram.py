#!/usr/bin/env python3
"""Make a histogram of tempoes with 60 bins."""

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt, rc
import pandas as pd
import numpy as np


# Pick out the tempo information.
SUMMARY = pd.read_hdf('data/msd_summary_file.h5', 'analysis/songs')
SUMMARY = SUMMARY['tempo']
SUMMARY = SUMMARY.map(float)
# Remove tempoes of 0.
SUMMARY = SUMMARY[SUMMARY != 0]


def main():
    """Bin the data and plot it."""
    rc('text', usetex=True)
    rc('font', family='serif')
    plt.hist(SUMMARY, bins=60)
    plt.title('Distribution of Tempo')
    plt.xlabel('Tempo (beats per minute)')
    plt.ylabel('Count')
    plt.savefig('data/graphs/graph_tempo_histogram.png')

    print('Statistics on the Distribution:')
    print('\tcount: {}'.format(len(SUMMARY)))
    print('\tmean: {} bpm'.format(np.mean(SUMMARY)))
    print('\tstd: {} bpm'.format(np.std(SUMMARY)))
    print('\tmin: {} bpm'.format(np.min(SUMMARY)))
    print('\t25%: {} bpm'.format(np.percentile(SUMMARY, 0.25)))
    print('\t50%: {} bpm'.format(np.percentile(SUMMARY, 0.5)))
    print('\t75%: {} bpm'.format(np.percentile(SUMMARY, 0.75)))
    print('\tmax: {} bpm'.format(np.max(SUMMARY)))


if __name__ == '__main__':
    main()

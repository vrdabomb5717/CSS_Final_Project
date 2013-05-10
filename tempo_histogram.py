#!/usr/bin/env python3

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt, rc
import pandas as pd


SUMMARY = pd.read_hdf('data/msd_summary_file.h5', 'analysis/songs')
SUMMARY = SUMMARY['tempo']
SUMMARY = SUMMARY.map(float)


def main():
    rc('text', usetex=True)
    rc('font', family='serif')
    plt.hist(SUMMARY, bins=20)
    plt.title('Distribution of Tempo')
    plt.xlabel('Tempo (beats per minute)')
    plt.ylabel('Count')
    plt.savefig('data/graphs/graph_tempo_histogram.png')


if __name__ == '__main__':
    main()

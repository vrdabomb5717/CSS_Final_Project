#!/usr/bin/env python3 -O

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt, rc
import pandas as pd


summary = pd.read_hdf('data/msd_summary_file.h5', 'analysis/songs')
summary = summary['tempo']
summary = summary.map(float)


def main():
    #tempoes = list(summary)

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.hist(summary, bins=20)
    plt.title('Distribution of Tempo')
    plt.xlabel('Tempo (beats per minute)')
    plt.ylabel('Count')
    plt.savefig('data/graphs/graph_tempo_histogram.png')


if __name__ == '__main__':
    main()

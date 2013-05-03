import matplotlib
matplotlib.use('Agg')
import pandas as pd
from matplotlib import pyplot as plt, rc


summary = pd.read_hdf('data/msd_summary_file.h5', 'analysis/songs')
summary = summary['loudness']
summary = summary.map(float)

def main():
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.hist(summary, bins=40)
    plt.title('Distribution of Volume')
    plt.xlabel('Volume (dB)')
    plt.ylabel('Count')
    plt.savefig('data/graphs/graph_volume_histogram.png')


if __name__ == '__main__':
    main()
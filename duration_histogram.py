import matplotlib
matplotlib.use('Agg')
import sqlite3
from matplotlib import pyplot as plt, rc


def main():
    conn = sqlite3.connect('data/track_metadata.db')
    curs = conn.cursor()
    curs.execute(
        'select duration from songs;')
    dur_data = curs.fetchall()
    durations = [dur[0] / 60 for dur in dur_data]

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.hist(durations, bins=30)
    plt.title('Distribution of Durations')
    plt.xlabel('Duration (minutes)')
    plt.ylabel('Count')
    plt.savefig('data/graphs/graph_duration_histogram.png')


if __name__ == '__main__':
    main()
import matplotlib
matplotlib.use('Agg')
#import pandas as pd
import sqlite3
from matplotlib import pyplot as plt, rc


def main():
    conn = sqlite3.connect('data/track_metadata.db')
    curs = conn.cursor()
    curs.execute(
        'select year, avg(duration) from songs where year > 0 group by year;')
    dur_data = curs.fetchall()
    years, durations = zip(*dur_data)
    durations = [dur / 60 for dur in durations]

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.plot(years, durations)
    plt.title('Average Song Duration per Year')
    plt.xlim([min(years), max(years)])
    plt.xlabel('Year')
    plt.ylabel('Duration (minutes)')
    plt.savefig('data/graphs/graph_duration_v_time.png')


if __name__ == '__main__':
    main()
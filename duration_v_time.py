#!/usr/bin/env python3
"""
Make a plot of duration in minutes versus time. Exclude years with insufficient
data.

"""

import sqlite3
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt, rc


def main():
    """Use SQL to get and process the data and matplotlib to make a graph."""
    conn = sqlite3.connect('data/track_metadata.db')
    curs = conn.cursor()
    curs.execute('''select year, avgd from (select year as year, count()
                    as count, avg(duration) as avgd from songs group by year)
                    where count >= 10 and year > 0;''')
    dur_data = curs.fetchall()
    years, durations = zip(*dur_data)
    durations = [dur / 60 for dur in durations]

    rc('text', usetex=True)
    rc('font', family='serif')
    plt.plot(years, durations)
    first = min(years)
    last = max(years)
    plt.title('Average Song Duration per Year ({}-{})'.format(first, last))
    plt.xlim((first, last))
    plt.xlabel('Year')
    plt.ylabel('Duration (minutes)')
    plt.savefig('data/graphs/graph_duration_v_time.png')


if __name__ == '__main__':
    main()

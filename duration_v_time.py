import matplotlib
matplotlib.use('Agg')
import pandas as pd
from pandas.io import sql
import sqlite3
from matplotlib import pyplot as plt


dat_dir = 'data/MillionSongSubset/'
conn = sqlite3.connect(dat_dir + 'AdditionalFiles/subset_track_metadata.db')
curs = conn.cursor()


def id_to_dur(id):
    curs.execute('select duration from songs where track_id=?', (id,))
    return curs.fetchone()[0]
    #select duration from songs where track_id="TRBGUUF128F9334B97";


def year_lists():
    result = [[[], []]]
    count = 0
    with open(dat_dir + 'AdditionalFiles/subset_tracks_per_year.txt') as yr:
        cur_yr, id, _, _ = yr.readline().strip().split('<SEP>')
        cur_yr = int(cur_yr)
        dur = id_to_dur(str(id))
        result[0][0] = cur_yr
        result[0][1].append(dur)
        for line in yr:
            cur_yr, id, _, _ = line.strip().split('<SEP>')
            cur_yr = int(cur_yr)
            dur = id_to_dur(str(id))
            if cur_yr == result[count][0]:
                result[count][1].append(dur)
            else:
                result.append([cur_yr, [dur]])
                count += 1
    return result


def averager(durations):
    return sum(durations) / len(durations)


def main():
    dur_data = [[ylist[0], averager(ylist[1])] for ylist in year_lists()]
    years, durations = zip(*dur_data)
    plt.plot(years, durations)
    plt.savefig('data/graphs/graph_duration_v_time.png')


if __name__ == '__main__':
    main()
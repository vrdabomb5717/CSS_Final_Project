import matplotlib
matplotlib.use('Agg')
import pandas as pd
from matplotlib import pyplot as plt, rc


summary = pd.read_hdf('data/msd_summary_file.h5', 'analysis/songs')
summary = summary[['track_id', 'loudness']]
summary.track_id = summary.track_id.map(lambda x: x.decode('utf-8'))
summary.set_index('track_id', inplace=True)


def id_to_loud(id):
    return summary.loc[id][0]


def year_lists():
    result = [[[], []]]
    count = 0
    with open('data/tracks_per_year.txt') as yr:
        cur_yr, id, _, _ = yr.readline().strip().split('<SEP>')
        cur_yr = int(cur_yr)
        dur = id_to_loud(str(id))
        result[0][0] = cur_yr
        result[0][1].append(dur)
        for line in yr:
            cur_yr, id, _, _ = line.strip().split('<SEP>')
            cur_yr = int(cur_yr)
            dur = id_to_loud(str(id))
            if cur_yr == result[count][0]:
                result[count][1].append(dur)
            else:
                result.append([cur_yr, [dur]])
                count += 1
    return result


def averager(louds):
    return sum(louds) / len(louds)


def main():
    loud_data = [[ylist[0], averager(ylist[1])] for ylist in year_lists()]
    years, louds = zip(*loud_data)

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.plot(years, louds)
    plt.title('Average Loudness per Year (1922-2011)')
    plt.xlim([min(years), max(years)])
    plt.xlabel('Year')
    plt.ylabel('Volume (dBFS)')
    plt.savefig('data/graphs/graph_volume_v_time.png')


if __name__ == '__main__':
    main()
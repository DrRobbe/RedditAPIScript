import numpy as np
import matplotlib.pyplot as plt


def plot_daily(source_file):
    dates, upvotes, comments, awards, snap_value, snapshots, weekend = get_plot_data(source_file)
    plt.title('Daily Discussion comments')
    plt.plot(dates, comments, label="comments")
    legened_snapshot = True
    for idx, snapshot in enumerate(snapshots):
        if legened_snapshot:
            plt.axvline(x=snapshot, color="red", label="snapshot day")
            legened_snapshot = False
        else:
            plt.axvline(x=snapshot, color="red")
        plt.text(snapshot, 35000, snap_value[idx])

    legened_weekend = True
    for day in weekend:
        if legened_weekend:
            plt.axvspan(day-1, day, alpha=0.2, color='green', label="weekend")
            legened_weekend = False
        else:
            plt.axvspan(day-1, day, alpha=0.2, color='green')

    plt.xticks(np.arange(0, len(dates), 5.0))
    plt.xlabel('date')
    plt.ylabel('comments')
    plt.legend()
    plt.show()


def get_plot_data(source_file):
    dates = []
    upvotes = []
    comments = []
    awards = []
    snapshots = []
    snap_value = []
    weekend = []
    data_file = open(source_file, "r")
    data_lines = data_file.readlines()
    iterator = 1
    for line in data_lines:
        sub_list = line.split('#')
        tmp_date = sub_list[0].split(',')[0].split(' ')
        dates.append(tmp_date[1]+"."+tmp_date[0])
        upvotes.append(int(sub_list[1].split(' ')[0]))
        comments.append(float((sub_list[2].split(' ')[0])[:-1])*1000)
        awards.append(int(sub_list[3].split(' ')[0]))
        if len(sub_list) > 4:
            if "SnapshotDay" in sub_list[4]:
                snapshots.append(iterator)
                snap_value.append(sub_list[4].split("-")[1])
            if "weekend" in sub_list[5]:
                weekend.append(iterator)
        iterator += 1
    data_file.close()
    return dates, upvotes, comments, awards, snap_value, snapshots, weekend


if __name__ == "__main__":
    plot_daily("D:\\Scripts\\Data\\Daily.txt")

from typing import List
import matplotlib.pyplot as plt


def plot_worth(rounds: List[int], average_price: List[float], ratio_data: List[float], file_name: str, title: str) -> None:
    plt.xlabel("Distribution Round")
    plt.ylabel('Average cents per tip')
    ydata = []
    for i in range(0, len(rounds)):
        ydata.append(100 * average_price[i] * ratio_data[i])
    plt.plot(rounds, ydata, color='red', linestyle="-", marker='D')
    for i in range(0, len(rounds)):
        plt.text(rounds[i], ydata[i], f'{round(ydata[i], 1)}', horizontalalignment='right', weight="bold")
    plt.title(title)
    plt.grid()
    # plt.show()
    plt.savefig(file_name)
    plt.clf()


def plot(rounds: List[int], ydata: List[float], file_name: str, title: str, ylabel_text: str, round_value: int = 1) -> None:
    plt.xlabel("Distribution Round")
    plt.ylabel(ylabel_text)
    plt.plot(rounds, ydata, color='red', linestyle="-", marker='D')
    for i in range(0, len(rounds)):
        plt.text(rounds[i], ydata[i], f'{round(ydata[i], round_value)}', horizontalalignment='right', weight="bold")
    plt.title(title)
    plt.grid()
    # plt.show()
    plt.savefig(file_name)
    plt.clf()


if __name__ == "__main__":
    local_path = 'D:\\Scripts\\RedditAPIScript\\donut-distribution\\input\\ratio\\ratio.txt'
    out_path = 'D:\\Scripts\\RedditAPIScript\\donut-distribution\\output\\ratio\\'
    ratio_data = []
    with open(local_path) as f:
        ratio_data = f.readlines()
    rounds = []
    comment_ratio = []
    post_ratio = []
    pay2post = []
    average_price = []
    for ratio in ratio_data[2:]:
        data_split = ratio.split("|")
        rounds.append(int(data_split[1].strip()))
        comment_ratio.append(float(data_split[2].strip()))
        post_ratio.append(float(data_split[3].strip()))
        pay2post.append(float(data_split[4].strip()))
        average_price.append(float(data_split[5].strip()))

    plot(rounds, comment_ratio, out_path + 'comment_ratio_per_round.png', 'Earned donuts for a tip to a comment', 'Earned Donuts per tip')
    plot(rounds, post_ratio, out_path + 'post_ratio_per_round.png', 'Earned donuts for a tip to a post', 'Earned Donuts per tip')
    plot(rounds, average_price, out_path + 'average_price_per_round.png', 'Average Donut price in $', 'Average Donuts price in $', 4)
    plot_worth(rounds, average_price, comment_ratio, out_path + 'earnings_per_tip_on_comment.png', 'Average cents received per tip to a comment')
    plot_worth(rounds, average_price, post_ratio, out_path + 'earnings_per_tip_on_post.png', 'Average cents received per tip to a post')

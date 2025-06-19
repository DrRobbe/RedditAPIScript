from typing import Dict, List, Any, Tuple
from datetime import datetime
import matplotlib.pyplot as plt


def read_data(file_name: str) -> Tuple[Dict[str, List[List[Any]]], List[str]]:
    data: Dict[str, List[List[Any]]] = {}
    all_dates: List[str] = []
    with open(file_name) as f:
        lines = f.readlines()
    for line in lines:
        entries = line.split(" ")
        date_str = entries[0]
        if date_str not in all_dates:
            all_dates.append(date_str)
        date = datetime.strptime(date_str, '%Y-%m-%d')
        action = entries[1]
        if action not in data.keys():
            data[action] = []
        data[action].append([date, float(entries[2]), float(entries[3].strip())])
    return data, all_dates


def plot(data: Dict[str, List[List[Any]]], all_dates: List[str], index: int) -> None:
    crypto = "ETH"
    if index > 1:
        crypto = "Donuts"
    plt.xlabel("LP interaction date")
    plt.ylabel(crypto)
    yInput, yRewards, yFees = ([] for _ in range(3))
    input_donuts, rewards_donuts, fee_donuts = (0 for _ in range(3))
    for date in all_dates:
        for lp_rewards in data['Rewards']:
            if date == lp_rewards[0].strftime("%Y-%m-%d"):
                rewards_donuts += lp_rewards[index]
        yRewards.append(rewards_donuts)
        for lp_rewards in data['LP-IN']:
            if date == lp_rewards[0].strftime("%Y-%m-%d"):
                input_donuts += lp_rewards[index]
        yInput.append(input_donuts)
        for lp_rewards in data['Fees']:
            if date == lp_rewards[0].strftime("%Y-%m-%d"):
                fee_donuts += lp_rewards[index]
        yFees.append(fee_donuts)

    plt.plot(all_dates, yInput, color='darkred', label="Input", linestyle="-", marker='D')

    if index > 1:
        plt.plot(all_dates, yRewards, color='forestgreen', label="LP rewards", linestyle="-", marker='D')
        for i in range(0, len(all_dates)):
            plt.text(all_dates[i], yInput[i], f'{round(yInput[i])}', horizontalalignment='right', weight="bold")
            plt.text(all_dates[i], yRewards[i], f'{round(yRewards[i])}', horizontalalignment='right', weight="bold")
            plt.text(all_dates[i], yFees[i], f'{round(yFees[i])}', horizontalalignment='left', verticalalignment='top', weight="bold")
    else:
        for i in range(0, len(all_dates)):
            plt.text(all_dates[i], yInput[i], f'{round(yInput[i], 6)}', horizontalalignment='right', weight="bold")
            plt.text(all_dates[i], yFees[i], f'{round(yFees[i], 6)}', horizontalalignment='left', verticalalignment='top', weight="bold")
    plt.plot(all_dates, yFees, color='lime', label="Fee rewards", linestyle="-", marker='D')

    plt.title(f"Liquidity Position - {crypto}")
    plt.legend()
    plt.grid()
    plt.show()


if __name__ == "__main__":
    local_path = 'D:\\Scripts\\RedditAPIScript\\donut-distribution'
    file_name = f'{local_path}\\input\\lp.txt'
    data, all_dates = read_data(file_name)
    input_donuts = 0
    input_eth = 0
    for lp_in in data['LP-IN']:
        input_eth += lp_in[1]
        input_donuts += lp_in[2]
    print(f'I put {round(input_donuts,2)} donuts & {round(input_eth,5)} ETH in the liquidity pool')
    rewards_donuts = 0
    for lp_rewards in data['Rewards']:
        rewards_donuts += lp_rewards[2]
        date = lp_rewards[0].strftime("%Y-%m-%d")
    fees_donuts = 0
    fees_eth = 0
    for lp_fees in data['Fees']:
        fees_eth += lp_fees[1]
        fees_donuts += lp_fees[2]
    print(f'I got {round(rewards_donuts,2)} donuts from rewards and {round(fees_donuts,2)} donuts & {round(fees_eth,5)} ETH from fees, since 2024-03-22 until {date}')
    print(f'Overall i got {round(rewards_donuts + fees_donuts,2)} donuts from rewards & fees, which is {round(100 * (rewards_donuts + fees_donuts) / input_donuts, 2)}% of donuts which where put in the Liquidity Pool.')
    plot(data, all_dates, 2)
    plot(data, all_dates, 1)

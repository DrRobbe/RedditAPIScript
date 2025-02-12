from typing import Dict, List, Tuple
from dataclasses import dataclass
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


@dataclass
class RegisteredUserData:
    name: str
    contrib_history: Dict[int, int]
    donut_history: Dict[int, int]


def create_user(local_path: str) -> Tuple[Dict[str, RegisteredUserData], Dict[int, int]]:
    registered_user: Dict[str, RegisteredUserData] = {}
    user_amount: Dict[int, int] = {}
    for _, _, files in os.walk(local_path):
        for file in files:
            if file.endswith('.txt'):
                path = local_path + '\\' + file
                print(f'Processing: {file}')
                round = int(file.split("_")[1].split(".")[0].split('00')[1])
                with open(path) as f:
                    lines = f.readlines()
                    user_amount[round] = len(lines)
                    for line in lines:
                        data = line.split(",")
                        person = data[0]
                        if 'username' != data[0]:
                            if person not in registered_user:
                                user = RegisteredUserData(person, {round: int(data[2])}, {round: int(data[3])})
                                registered_user[person] = user
                            else:
                                registered_user[person].contrib_history[round] = int(data[2])
                                registered_user[person].donut_history[round] = int(data[3])
    return registered_user, user_amount


def create_active_user(local_path: str) -> Dict[int, int]:
    active_user_amount: Dict[int, int] = {}
    for _, _, files in os.walk(local_path):
        for file in files:
            if file.endswith('.txt'):
                path = local_path + '\\' + file
                print(f'Processing: {file}')
                round = int(file.split("_")[1].split(".")[0].split('00')[1])
                with open(path) as f:
                    lines = f.readlines()
                    active_user_amount[round] = len(lines)
    return active_user_amount


def plot_user(user_amount: Dict[int, int], file_name: str, title: str) -> None:
    rounds: List[int] = []
    user: List[int] = []
    for key, amount in user_amount.items():
        rounds.append(key)
        user.append(amount)
    plt.xlabel("Distribution Round")
    plt.ylabel("User")
    plt.plot(rounds, user, color='red', linestyle="-", marker='D')
    for i in range(1, len(rounds)):
        sign = '+'
        if user[i] - user[i - 1] < 0:
            sign = ''
        plt.text(rounds[i], user[i], f'{sign}{user[i] - user[i - 1]}', horizontalalignment='right', weight="bold")
    plt.title(title)
    plt.grid()
    # plt.show()
    plt.savefig(file_name)
    plt.clf()


def plot_percentage(user_amount: Dict[int, int],
                    active_user: Dict[int, int],
                    zero_user: Dict[int, int],
                    twentyk_user: Dict[int, int],
                    twentyk_contrib: Dict[int, int],
                    file_name: str) -> None:
    rounds: List[int] = []
    zero: List[float] = []
    active: List[float] = []
    twenty: List[float] = []
    twenty_contrib: List[float] = []
    for key, amount in active_user.items():
        rounds.append(key)
        active.append(round(100 * amount / user_amount[key], 1))
    for key, amount in zero_user.items():
        zero.append(round(100 * amount / user_amount[key], 1))
    for key, amount in twentyk_user.items():
        twenty.append(round(100 * amount / user_amount[key], 1))
    for key, amount in twentyk_contrib.items():
        twenty_contrib.append(round(100 * amount / user_amount[key], 1))
    print(active)
    print(zero)
    print(twenty)
    print(twenty_contrib)
    plt.xlabel("Distribution round")
    plt.ylabel("Percentage of all registered users")
    plt.plot(rounds, active, color='red', linestyle="-", marker='D')
    plt.plot(rounds, zero, color='blue', linestyle="-", marker='D')
    plt.plot(rounds, twenty, color='gold', linestyle="-", marker='D')
    plt.plot(rounds, twenty_contrib, color='grey', linestyle="-", marker='D')
    red_patch = mpatches.Patch(color='red', label="user which earned donuts")
    blue_patch = mpatches.Patch(color='blue', label="user with zero balance")
    teal_patch = mpatches.Patch(color='gold', label="user with +20k donuts")
    olive_patch = mpatches.Patch(color='grey', label="user with +20k contrib")
    plt.legend(handles=[red_patch, blue_patch, teal_patch, olive_patch])
    plt.title("Registered users %")
    # plt.show()
    plt.savefig(file_name)
    plt.clf()


if __name__ == "__main__":
    local_path = 'D:\\Scripts\\RedditAPIScript\\donut-distribution\\input\\'
    output_path = 'D:\\Scripts\\RedditAPIScript\\donut-distribution\\output\\registered_user\\'
    registered_user, user_amount = create_user(local_path + 'user')
    active_user = create_active_user(local_path + 'finale_csv')
    band_user = create_active_user(local_path + 'ban_user')
    zero_user: Dict[int, int] = {}
    twentyk_user: Dict[int, int] = {}
    twentyk_contrib_user: Dict[int, int] = {}
    last_distribution = 0
    for _, user in registered_user.items():
        for distribution, amount in user.donut_history.items():
            if distribution not in zero_user:
                zero_user[distribution] = 0
                twentyk_user[distribution] = 0
                twentyk_contrib_user[distribution] = 0
            if amount == 0 and user.contrib_history[distribution] > 0:
                zero_user[distribution] += 1
            if amount > 20000:
                twentyk_user[distribution] += 1
            if user.contrib_history[distribution] > 20000:
                twentyk_contrib_user[distribution] += 1
            last_distribution = distribution
    print(user_amount)
    plot_user(user_amount, output_path + 'new_registered_user.png', "New registered users!")
    print(active_user)
    plot_user(active_user, output_path + 'active_user.png', "User which earned donuts!")
    print(band_user)
    plot_user(band_user, output_path + 'band_user.png', "Perma banned user!")
    print(zero_user)
    plot_user(zero_user, output_path + 'zero_balance_user.png', "Registered users with zero balance!")
    print(twentyk_user)
    plot_user(twentyk_user, output_path + '20k_user.png', "Users which hold +20k donuts!")
    print(twentyk_contrib_user)
    plot_user(twentyk_contrib_user, output_path + '20k_contrib_user.png', "Users which hold +20k contrib!")
    print(f"Currently there are {user_amount[last_distribution]} registered user.")
    zero_contrib_user = 0
    for person, user in registered_user.items():
        if user.contrib_history[last_distribution] == 0:
            zero_contrib_user += 1
    print(f"{zero_contrib_user} registered user have never earned any donuts,\nwhich is {round(100*(zero_contrib_user/user_amount[last_distribution]), 2)}% of all registered user.")
    plot_percentage(user_amount, active_user, zero_user, twentyk_user, twentyk_contrib_user, output_path + 'percentage_of_registered_user.png')

import json
from datetime import datetime
from typing import Dict, List, Tuple, Any

local_path = 'D:\\Scripts\\RedditAPIScript\\donut-distribution\\'


def create_user(file_name: str, date: datetime) -> Tuple[Dict[str, Dict[str, List[float]]], Dict[str, Dict[str, List[float]]]]:
    user_send: Dict[str, Dict[str, List[float]]] = {}
    user_receive: Dict[str, Dict[str, List[float]]] = {}
    with open(file_name) as f:
        file_content = json.load(f)
    for values in file_content:
        time = str(values["created_date"]).split(".")[0]
        if values["to_user_registered"] == 1 and datetime.strptime(time, '%Y-%m-%d %H:%M:%S') > date:
            sender = values["from_user"]
            receiver = values["to_user"]
            if sender not in user_send:
                user_send[sender] = {}
            if receiver not in user_receive:
                user_receive[receiver] = {}
            if receiver not in user_send[sender]:
                user_send[sender][receiver] = [0., 0.]
            if sender not in user_receive[receiver]:
                user_receive[receiver][sender] = [0., 0.]
            user_send[sender][receiver][0] += 1.
            user_receive[receiver][sender][0] += 1.
            user_send[sender][receiver][1] += values["amount"]
            user_receive[receiver][sender][1] += values["amount"]
    print(f"Found {len(user_send)} send user.")
    print(f"Found {len(user_receive)} receive user.")
    return user_send, user_receive


def best_buddy_leaderboard(max_tip_partners: Dict[str, int]) -> None:
    number = 1
    current_rank = number
    last_number = 100
    output = ["| No. | Name | Number of best buddies |",
              "|:-|:--------------|:---------:|"]
    for person in reversed(sorted(max_tip_partners.items(), key=lambda item: item[1])):
        if person[1] > 1:
            if person[1] < last_number:
                last_number = person[1]
                current_rank = number
            output.append(f"| {current_rank} | {person[0]} | {person[1]} |")
        number += 1

    with open(local_path + 'output\\tips\\Best_buddy_leaderboard-tabel.txt', 'w') as f:
        for line in output:
            f.write(f"{line}\n")


def create_table(users: Dict[str, Dict[str, List[float]]], send_table: bool, date: datetime, distribution: int) -> List[str]:
    list_length = 100
    filler = "Send"
    filler1 = "given to"
    separator = "$$$"
    if not send_table:
        filler = "Received"
        filler1 = "received from"
    users_tips: Dict[str, List[Any]] = {}
    users_amount: Dict[str, List[Any]] = {}
    max_tip_partners: Dict[str, int] = {}
    for user, partners in users.items():
        if user not in users_tips:
            users_tips[user] = [0., '']
        if user not in users_amount:
            users_amount[user] = [0., '']
        max_tip_partner = ''
        max_tip = 0.
        max_donut_partner = ''
        max_donut = 0.
        for partner, values in partners.items():
            users_tips[user][0] += values[0]
            users_amount[user][0] += values[1]
            if max_tip < values[0]:
                max_tip = values[0]
                max_tip_partner = partner
            if max_donut < values[1]:
                max_donut = values[1]
                max_donut_partner = partner
        if max_tip_partner not in max_tip_partners:
            max_tip_partners[max_tip_partner] = 0
        max_tip_partners[max_tip_partner] += 1
        users_tips[user][1] = max_tip_partner + separator + str(round(max_tip))
        users_amount[user][1] = max_donut_partner + separator + str(round(max_donut, 1))
    number = 1
    output = [f"| No. | Name | {filler} tips | Most tips {filler1} | {filler} Donuts | Most donuts {filler1} | Average Donuts per tip |",
              "|:-|:--------------|:-------:|:---------------------:|:------:|:---------------------:|:------------:|"]
    current_rank = number
    last_tips = 100000
    for person in reversed(sorted(users_tips.items(), key=lambda item: item[1][0])[-list_length:]):
        max_partner = str(person[1][1]).split("$$$")[0]
        max_amount = str(person[1][1]).split("$$$")[1]
        donuts = users_amount[person[0]][0]
        tips = person[1][0]
        if tips < last_tips:
            last_tips = tips
            current_rank = number
        max_donut_partner = users_amount[person[0]][1].split("$$$")[0]
        max_donut_amount = users_amount[person[0]][1].split("$$$")[1]
        output.append(f"| {current_rank} | {person[0]} | {int(tips)} | {max_partner} ({max_amount}) | {round(donuts, 1)} | {max_donut_partner} ({max_donut_amount}) | {round(donuts/tips, 1)} |")
        number += 1

    with open(local_path + f'output\\tips\\{filler}_since{str(date).split(" ")[0]}-tabel-round{distribution}.txt', 'w') as f:
        for line in output:
            f.write(f"{line}\n")
    if send_table:
        best_buddy_leaderboard(max_tip_partners)
    return output


if __name__ == "__main__":
    date = datetime.strptime("2024-10-14 00:00:00", '%Y-%m-%d %H:%M:%S')
    print("Check all tips since :" + str(date))
    distribution = 142
    file_name = local_path + f'input\\tips_round_{distribution}.json'
    user_send, user_receive = create_user(file_name, date)
    # global data
    all_tips = 0.
    all_donuts = 0.
    max_donuts = 0.
    max_send_donuts = ''
    max_received_donuts = ''
    max_tips = 0.
    max_send_tip = ''
    max_received_tip = ''
    for send_user, data in user_send.items():
        for receive_user, values in data.items():
            all_tips += values[0]
            all_donuts += values[1]
            if max_donuts < values[1]:
                max_donuts = values[1]
                max_send_donuts = send_user
                max_received_donuts = receive_user
            if max_tips < values[0]:
                max_tips = values[0]
                max_send_tip = send_user
                max_received_tip = receive_user
    print(f"{all_tips} tips send")
    print(f"On average {round(all_tips/len(user_send), 1)} tips were send per user")
    print(f"{round(all_donuts, 1)} donuts send")
    print(f"On average {round(all_donuts/len(user_send), 1)} donuts were send per user")
    print(f"Most tips send this week from one person to another: {max_send_tip} send {max_tips} tips to {max_received_tip}")
    print(f"Most donuts send this week from one person to another: {max_send_donuts} send {round(max_donuts, 1)} donuts to {max_received_donuts}")
    send_ranks = create_table(user_send, True, date, distribution)
    received_ranks = create_table(user_receive, False, date, distribution)
    # calculate rank differenc
    ranked_difference = {}
    for entry in send_ranks[2:]:
        user = entry.split(" | ")[1]
        rank = int(entry.split(" | ")[0][2:])
        for stuff in received_ranks[2:]:
            if user in stuff.split(" | ")[1]:
                rank2 = int(stuff.split(" | ")[0][2:])
                ranked_difference[user] = rank - rank2
    print("Top 3 users with highest rank difference, with lower receive rank and higher send rank:")
    for person in sorted(ranked_difference.items(), key=lambda item: item[1])[:3]:
        print(f"* {person[0]} - rank difference: {abs(person[1])}")
    print("Top 3 users with highest rank difference, with lower send rank and higher receive rank:")
    for person in reversed(sorted(ranked_difference.items(), key=lambda item: item[1])[-3:]):
        print(f"* {person[0]} - rank difference: {abs(person[1])}")

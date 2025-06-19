import json
from datetime import datetime
from typing import Dict, List, Tuple, Any

local_path = 'D:\\Scripts\\RedditAPIScript\\donut-distribution\\'


def create_user(file_name: str, date_old: datetime, date_new: datetime) -> Tuple[Dict[str, Dict[str, List[float]]], Dict[str, Dict[str, List[float]]]]:
    user_send: Dict[str, Dict[str, List[float]]] = {}
    user_receive: Dict[str, Dict[str, List[float]]] = {}
    weight = 0
    tips = 0
    with open(file_name) as f:
        file_content = json.load(f)
    for values in file_content:
        time = str(values["created_date"]).split(".")[0]
        if date_new > datetime.strptime(time, '%Y-%m-%d %H:%M:%S') > date_old:  # values["to_user_registered"] == 1 and
            sender = values["from_user"]
            receiver = values["to_user"]
            weight += values["weight"]
            tips += 1
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
    print(f'The {tips} tips, were send with an average tip weight of {round(weight / tips, 3)}.')
    return user_send, user_receive


def create_table(users: Dict[str, Dict[str, List[float]]], send_table: bool, date: datetime, distribution: int, all_tips: int) -> List[str]:
    list_length = 100
    filler = "Send"
    filler1 = "given to"
    if not send_table:
        filler = "Received"
        filler1 = "received from"
    users_tips: Dict[str, List[Any]] = {}
    users_amount: Dict[str, List[Any]] = {}
    max_tip_partners: Dict[str, int] = {}
    for user, partners in users.items():
        if user not in users_tips:
            users_tips[user] = [0., {}]
        if user not in users_amount:
            users_amount[user] = [0., {}]
        i = 0
        for partner, values in reversed(sorted(partners.items(), key=lambda item: item[1][0])):
            users_tips[user][0] += values[0]
            users_amount[user][0] += values[1]
            if i < 3:
                users_tips[user][1][partner] = values[0]
                users_amount[user][1][partner] = values[1]
            i += 1
        max_tip_partner = next(iter(users_tips[user][1]))
        if max_tip_partner not in max_tip_partners:
            max_tip_partners[max_tip_partner] = 0
        max_tip_partners[max_tip_partner] += 1
    number = 1
    output = [f"| No. | Name | {filler} tips | % of all tips {filler} | {filler1} x user | {filler} Donuts | Most tips {filler1} |",
              "|:-|:--------------|:-------:|:-------:|:-------:|:------:|:---------------------:|"]
    current_rank = number
    last_tips = 100000
    for person in reversed(sorted(users_tips.items(), key=lambda item: item[1][0])[-list_length:]):
        tips = int(person[1][0])
        user = person[0]
        friends = ''
        for friend, tip in users_tips[user][1].items():
            friends += f"{friend} ({round(100 * tip / tips,1)}%) "
        donuts = users_amount[user][0]
        contacts = len(users[user])
        if tips < last_tips:
            last_tips = tips
            current_rank = number
        output.append(f"| {current_rank} | {user} | {tips} | {round(100 * tips/all_tips, 1)}% | {contacts} | {round(donuts, 1)} | {friends} |")
        number += 1

    with open(local_path + f'output\\tips\\{filler}_since{str(date).split(" ")[0]}-tabel-round{distribution}.txt', 'w') as f:
        for line in output:
            f.write(f"{line}\n")
    return output


if __name__ == "__main__":
    date_old = datetime.strptime("2025-06-09 00:00:00", '%Y-%m-%d %H:%M:%S')
    date_new = datetime.strptime("2025-06-16 00:00:00", '%Y-%m-%d %H:%M:%S')
    print(f"Check all tips since {str(date_old)} until {str(date_new)}.")
    distribution = 151
    file_name = local_path + f'input\\tips_round_{distribution}.json'
    user_send, user_receive = create_user(file_name, date_old, date_new)
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
    send_ranks = create_table(user_send, True, date_old, distribution, int(all_tips))
    received_ranks = create_table(user_receive, False, date_old, distribution, int(all_tips))
    # calculate rank difference
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

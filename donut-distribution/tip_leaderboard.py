import json
from datetime import datetime
from typing import Dict, List, Tuple, Any

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
                user_send[sender][receiver] = [0. , 0.]
            if sender not in user_receive[receiver]:
                user_receive[receiver][sender] = [0., 0.]
            user_send[sender][receiver][0] += 1.
            user_receive[receiver][sender][0] += 1.
            user_send[sender][receiver][1] += values["amount"]
            user_receive[receiver][sender][1] += values["amount"]
    print(f"Found {len(user_send)} send user.")
    print(f"Found {len(user_receive)} receive user.")
    return user_send, user_receive


def create_table(users: Dict[str, Dict[str, List[float]]], send_table: bool, date: datetime) -> None:
    list_length = 50
    filler = "send"
    filler1 = "given to"
    separator = "$$$"
    if not send_table:
        filler = "received"
        filler1 = "received from"
    users_tips: Dict[str, List[Any]] = {}
    users_amount: Dict[str, List[Any]] = {} 
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
        users_tips[user][1] = max_tip_partner + separator + str(round(max_tip, 1))
        users_amount[user][1] = max_donut_partner + separator + str(round(max_donut, 1))
    number = 1
    output = []
    for user in reversed(sorted(users_tips.items(), key=lambda item: item[1][0])[-list_length:]):
        max_partner = str(user[1][1]).split("$$$")[0]
        max_amount = str(user[1][1]).split("$$$")[1]
        output.append(f"\t{number}. {user[0]}, {filler} {user[1][0]} tips, most {filler1} {max_partner} with {max_amount} tips")
        number += 1
    number = 1

    for user in reversed(sorted(users_amount.items(), key=lambda item: item[1][0])[-list_length:]):
        max_partner = str(user[1][1]).split("$$$")[0]
        max_amount = str(user[1][1]).split("$$$")[1]
        output.append(f"\t{number}. {user[0]}, {filler} {user[1][0]} donuts, most {filler1} {max_partner} with {max_amount} donuts")
        number += 1
    with open(f'output\\{filler}_since{str(date).split(" ")[0]}.txt', 'w') as f:
        for line in output:
            f.write(f"{line}\n")
    

if __name__ == "__main__":
    local_path = 'D:\\Scripts\\RedditAPIScript\\donut-distribution\\'
    date = datetime.strptime("2024-08-05 00:00:00", '%Y-%m-%d %H:%M:%S')
    print("Check all tips since :" + str(date))
    file_name = local_path + 'input\\tips_round_140.json'
    user_send, user_receive = create_user(file_name, date)
    create_table(user_send, True, date)
    create_table(user_receive, False, date)
from typing import Dict, List
import json


def create_user(file_name: str) -> Dict[str, List[int]]:
    user: Dict[str, List[int]] = {}
    with open(file_name) as f:
        print(f"Open {file_name}")
        file_content = json.load(f)
        for values in file_content:
            if values["to_user_registered"] == 1:
                sender = values["from_user"]
                sender_weight = values["weight"]
                if sender_weight < 1.0 or sender in user:
                    if sender not in user:
                        user[sender] = [0, 0]
                    user[sender][0] += 1
        print(f"Found {len(user)} user with less weight than 1.")
        for values in file_content:
            if values["to_user_registered"] == 1:
                receiver = values["to_user"]
                if receiver in user:
                    user[receiver][1] += 1
    return user


if __name__ == "__main__":
    local_path = 'D:\\Scripts\\RedditAPIScript\\donut-distribution\\'
    file_name = local_path + 'input\\tips_round_142.json'
    users = create_user(file_name)
    send = 0
    received = 0
    for user, tips in users.items():
        send += tips[0]
        received += tips[1]
    print(send)
    print(received)
    print(round(received / send, 1))

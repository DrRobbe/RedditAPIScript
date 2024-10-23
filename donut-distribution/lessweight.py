from typing import Dict, List
import json


def create_user(file_name: str) -> Dict[str, List[int]]:
    user: Dict[str, List[int]] = {}
    with open(file_name) as f:
        file_content = json.load(f)
        for values in file_content:
            if values["to_user_registered"] == 1:
                sender = values["from_user"]
                sender_weight = values["weight"]
                if sender_weight < 1.0 or sender in user:
                    if sender not in user:
                        user[sender] = [0, 0]
                    user[sender][0] += 1
        print(f"{len(user)} user had a tip weight less than 1.")
        for values in file_content:
            if values["to_user_registered"] == 1:
                receiver = values["to_user"]
                if receiver in user:
                    user[receiver][1] += 1
    return user


if __name__ == "__main__":
    local_path = 'D:\\Scripts\\RedditAPIScript\\donut-distribution\\'
    distribution = 142
    print(f"For round {distribution}:")
    file_name = f'{local_path}input\\tips_round_{distribution}.json'
    users = create_user(file_name)
    send = 0
    received = 0
    for user, tips in users.items():
        send += tips[0]
        received += tips[1]
    print(f'These users send {send} tips and received {received} tips.')
    print(f'On average they get {round(received / send, 2)} tips back for every tip they send.')

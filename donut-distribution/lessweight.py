from typing import Dict, List, Tuple
import json


def create_user(file_name: str, contrib_name: str) -> Tuple[Dict[str, List[int]], Dict[str, List[int]]]:
    user: Dict[str, List[int]] = {}
    user_contrib: Dict[str, List[int]] = {}
    twentyk_contirb_user = []
    with open(contrib_name) as f:
        lines = f.readlines()
        for line in lines:
            contrib_user = line.split(",")[0]
            if 'username' != contrib_user:
                contrib = int(line.split(",")[2])
                if contrib > 19999:
                    twentyk_contirb_user.append(contrib_user)
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
                    if sender not in twentyk_contirb_user:
                        if sender not in user_contrib:
                            user_contrib[sender] = [0, 0]
                        user_contrib[sender][0] += 1
        print(f"{len(user)} user had a tip weight less than 1.")
        for values in file_content:
            if values["to_user_registered"] == 1:
                receiver = values["to_user"]
                if receiver in user:
                    user[receiver][1] += 1
                if receiver in user_contrib:
                    user_contrib[receiver][1] += 1
    return user, user_contrib


if __name__ == "__main__":
    local_path = 'D:\\Scripts\\RedditAPIScript\\donut-distribution\\'
    distribution = 150
    print(f"For round {distribution}:")
    file_name = f'{local_path}input\\tips_round_{distribution}.json'
    contrib_name = f'{local_path}input\\user\\users.000.task_00{distribution - 1}.txt'
    users, user_contrib = create_user(file_name, contrib_name)
    send = 0
    received = 0
    for user, tips in users.items():
        send += tips[0]
        received += tips[1]
    print(f'These users send {send} tips and received {received} tips.')
    print(f'On average they get {round(received / send, 2)} tips back for every tip they send.')

    contrib_send = 0
    contrib_received = 0
    for user, tips in user_contrib.items():
        contrib_send += tips[0]
        contrib_received += tips[1]
    print(f"{len(user_contrib)} user had a tip weight less than 1. and less than 20k contrib.")
    print(f'Users with less than 20k contrib send {contrib_send} tips and received {contrib_received} tips.')
    print(f'On average they get {round(contrib_received / contrib_send, 2)} tips back for every tip they send.')

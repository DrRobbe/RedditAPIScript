from typing import Dict, List, Tuple, Set
import json


def create_user(file_name: str, contrib_name: str) -> Tuple[Dict[str, List[int]], Dict[str, List[int]]]:
    user: Dict[str, List[int]] = {}
    user_twentyk_contirb: Dict[str, List[int]] = {}
    twentyk_contirb_user: Set[str] = set()
    twentyk_contirb_less_donuts_send_tip: Set[str] = set()
    with open(contrib_name) as f:
        lines = f.readlines()
        for line in lines:
            contrib_user = line.split(",")[0]
            if 'username' != contrib_user:
                contrib = int(line.split(",")[2])
                if contrib > 19999:
                    twentyk_contirb_user.add(contrib_user)
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
                    if sender in twentyk_contirb_user:
                        if sender not in user_twentyk_contirb:
                            user_twentyk_contirb[sender] = [0, 0]
                        user_twentyk_contirb[sender][0] += 1
                        twentyk_contirb_less_donuts_send_tip.add(sender)
        send_less_weight = len(user)
        receiver_count = 0
        full_weight_user = twentyk_contirb_user - twentyk_contirb_less_donuts_send_tip
        for values in file_content:
            if values["to_user_registered"] == 1:
                receiver = values["to_user"]
                if receiver not in full_weight_user:
                    if receiver not in user:
                        user[receiver] = [0, 0]
                        receiver_count += 1
                    user[receiver][1] += 1
                    if receiver in twentyk_contirb_user:
                        if receiver not in user_twentyk_contirb:
                            user_twentyk_contirb[receiver] = [0, 0]
                        user_twentyk_contirb[receiver][1] += 1
        all_user = len(user)
        print(f"{all_user} user had a tip weight less than 1 and send or received a tip.")
        print(f"{send_less_weight} of the {all_user} user send a tip.")
        print(f"{receiver_count} of the {all_user} user received a tip and did not send any.")
        print(f"{len(twentyk_contirb_less_donuts_send_tip)} of the {all_user} user have 20k contrib but still a tip weight less than 1.\n")
    return user, user_twentyk_contirb


if __name__ == "__main__":
    local_path = 'D:\\Scripts\\RedditAPIScript\\donut-distribution\\'
    distribution = 153
    print(f"For round {distribution}:")
    file_name = f'{local_path}input\\tips_round_{distribution}.json'
    contrib_name = f'{local_path}input\\user\\users.000.task_00{distribution - 1}.txt'
    users, user_twentyk_contirb_less_donuts = create_user(file_name, contrib_name)
    send = 0
    received = 0
    for user, tips in users.items():
        send += tips[0]
        received += tips[1]
    print(f'The {len(users)} users send {send} tips and received {received} tips.')
    print(f'On average they get {round(received / send, 2)} tips back for every tip they send.')

    contrib_send = 0
    contrib_received = 0
    for user, tips in user_twentyk_contirb_less_donuts.items():
        contrib_send += tips[0]
        contrib_received += tips[1]
    print(f"From these {len(users)} user {len(user_twentyk_contirb_less_donuts)} user had a tip weight less than 1 but 20k contrib.")
    print(f'These users send {contrib_send} tips and received {contrib_received} tips.')
    print(f'On average they get {round(contrib_received / contrib_send, 2)} tips back for every tip they send.')

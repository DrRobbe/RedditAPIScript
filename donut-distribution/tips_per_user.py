import json
from typing import Dict

local_path = 'D:\\Scripts\\RedditAPIScript\\donut-distribution\\'


def create_user(user_name: str, file_name: str) -> Dict[str, int]:
    user_send: Dict[str, int] = {}
    with open(file_name) as f:
        file_content = json.load(f)
    for values in file_content:
        sender = values["from_user"]
        if values["to_user_registered"] == 1 and sender == user_name:
            receiver = values["to_user"]
            if receiver not in user_send:
                user_send[receiver] = 0
            user_send[receiver] += 1
    print(f"{user_name} tipped {len(user_send)} different user.")
    return user_send


if __name__ == "__main__":
    user = 'DrRobbe'
    distribution = 142
    print(f"Check all tips for {user} in round {distribution}")
    file_name = local_path + f'input\\tips_round_{distribution}.json'
    user_send = create_user(user, file_name)
    # global data
    all_tips = 0
    for receive_user, tips in user_send.items():
        all_tips += tips
    print(f"{user} send {all_tips} tips send")
    output = ["| No. | Send to | tips | % of all tips |",
              "|:-|:--------------|:-------:|:------------:|"]
    number = 1
    current_rank = number
    last_tips = 100000
    for person in reversed(sorted(user_send.items(), key=lambda item: item[1])[-10:]):
        tips = person[1]
        if tips < last_tips:
            last_tips = tips
            current_rank = number
        output.append(f"| {current_rank} | {person[0]} | {tips} | {round(100 * tips / all_tips, 1)}% |")
        number += 1
    with open(local_path + f'output\\tips\\{user}-tabel-round{distribution}.txt', 'w') as f:
        for line in output:
            f.write(f"{line}\n")

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
    return user_send


if __name__ == "__main__":
    ban_user = ['Downtown_Yam9137', 'Every_Hunt_160', 'sadiq_238', 'KIG45', 'lordciders',
                'Master-Score7344', 'Narrow-Professor-126', 'rikbona', 'Sky-876', 'Fredzoor',
                'falk_lhoste', 'Honey_-_Badger', 'Major-Remove-7190']
    ban_user += ['kirtash93', 'BigRon1977', 'AltruisticPops', 'Odd-Radio-8500', 'Extension-Survey3014', 'CreepToeCurrentSea', 'DBRiMatt']
    distributions = [140, 141]
    for user in ban_user:
        output = []
        for distribution in distributions:
            output.append(f"Check all tips for {user} in round {distribution}.")
            file_name = local_path + f'input\\tips_round_{distribution}.json'
            user_send = create_user(user, file_name)
            output.append(f"{user} tipped {len(user_send)} different user.")
            all_tips = 0
            for _, tips in user_send.items():
                all_tips += tips
            output.append(f"{user} send {all_tips} tips.")
            # global data
            output.append("| No. | Send to | tips | % of all tips |")
            # output.append("|:-|:--------------|:-------:|:------------:|")
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

        with open(local_path + f'output\\tips\\user\\{user}-tabel-round{distribution}.txt', 'w') as f:
            for line in output:
                f.write(f"{line}\n")

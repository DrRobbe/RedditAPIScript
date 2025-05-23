from pyvis.network import Network
from typing import Dict, Set
from datetime import datetime
import json


def create_user(file_name: str, date: datetime) -> Dict[str, Set[str]]:
    user: Dict[str, Set[str]] = {}
    with open(file_name) as f:
        file_content = json.load(f)
    for values in file_content:
        time = str(values["created_date"]).split(".")[0]
        if values["to_user_registered"] == 1 and datetime.strptime(time, '%Y-%m-%d %H:%M:%S') > date:
            sender = values["from_user"]
            receiver = values["to_user"]
            if sender not in user:
                user[sender] = set()
            if receiver not in user:
                user[receiver] = set()
            user[sender].add(receiver)
    print(f"Found {len(user)} user.")
    return user


def plot(users: Dict[str, Set[str]], output_file_name: str) -> None:
    net = Network(directed=True, select_menu=True, filter_menu=True, cdn_resources='remote')
    for key, value in users.items():
        color = '#3e66c1'
        if len(value) > 99:
            color = "#ff8800"
        elif len(value) > 9:
            color = "#ff7373"
        net.add_node(key, color=color)
    # send edges
    for key, value in users.items():
        for tip in value:
            net.add_edge(key, tip, color='#5b5b5b')
    net.force_atlas_2based()
    net.save_graph(str(output_file_name))
    print("Created graph: " + output_file_name)


if __name__ == "__main__":
    date_str = "2024-07-31"
    distribution = 150
    date = datetime.strptime(f"{date_str} 00:00:00", '%Y-%m-%d %H:%M:%S')
    local_path = 'D:\\Scripts\\RedditAPIScript\\donut-distribution\\'
    file_name = f'{local_path}input\\tips_round_{distribution}.json'
    users = create_user(file_name, date)
    plot(users, local_path + f'output\\graph_{distribution}_{date_str}.html')

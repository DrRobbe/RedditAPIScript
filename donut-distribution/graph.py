from pyvis.network import Network
from typing import Dict, Set
import json


def create_user(file_name: str) -> Dict[str, Set[str]]:
    user: Dict[str, Set[str]] = {}
    with open(file_name) as f:
        file_content = json.load(f)
    for values in file_content:
        if values["to_user_registered"] == 1:
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
    print("INFO: Created graph")


if __name__ == "__main__":
    local_path = 'D:\\Scripts\\RedditAPIScript\\donut-distribution\\'
    file_name = local_path + 'input\\tips_round_140.json'
    users = create_user(file_name)
    plot(users, local_path + 'output\\graph_140.html')

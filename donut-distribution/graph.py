from pyvis.network import Network
from typing import Dict, List, Set


def create_user(file_name: str) -> Dict[str, Set[str]]:
    user: Dict[str, List[Set]] = {}
    with open(file_name) as current_file:
        file_content = current_file.readlines()
    for line in file_content:
        if "- INFO - tip " in line:
            sender = line.split(" [from]: ")[1].split(" [to]:")[0]
            receiver = line.split(" [to]:")[1].split(" [amount]:")[0]
            if sender not in user:
                user[sender] = set()
            if receiver not in user:
                user[receiver] = set()
            user[sender].add(receiver)
    return user


def plot(users: Dict[str, Set[str]], output_file_name: str) -> None:
    net = Network(directed=False, select_menu=True, filter_menu=True, cdn_resources='remote')
    for key, value in users.items():
        net.add_node(key, color="#ff7373")
    # send edges
    for key, value in users.items():
        for tip in value:
            net.add_edge(key, tip, color='#5b5b5b')
    net.force_atlas_2based()
    net.save_graph(str(output_file_name))
    print("INFO: Created graph")


if __name__ == "__main__":
    file_name = 'distribution_139.txt'
    users = create_user(file_name)
    plot(users, "D:\\Scripts\\RedditAPIScript\\donut-distribution\\user_graph.html")

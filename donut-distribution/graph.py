from pyvis.network import Network
from typing import Dict, Set, List, Any
from datetime import datetime
import json


def create_user(file_name: str, date: datetime, full_round: bool) -> Dict[str, List[Any]]:
    user: Dict[str, Set[str]] = {}
    with open(file_name) as f:
        file_content = json.load(f)
    for values in file_content:
        time = str(values["created_date"]).split(".")[0]
        if datetime.strptime(time, '%Y-%m-%d %H:%M:%S') > date or full_round:
            sender = values["from_user"]
            receiver = values["to_user"]
            if sender not in user:
                user[sender] = [1, set()]
            if receiver not in user:
                user[receiver] = [values["to_user_registered"], set()]
            user[sender][1].add(receiver)
    print(f"Found {len(user)} user.")
    return user


def plot(users: Dict[str, List[Any]], output_file_name: str) -> None:
    net = Network(directed=True, select_menu=True, filter_menu=True, cdn_resources='remote')
    for key, value in users.items():
        color = '#3e66c1'
        connections = len(value[1])
        if connections > 49:
            color = "#ff8800"
        elif connections > 9:
            color = "#ff7373"
        shape = "dot"
        if value[0] != 1:
            shape = "square"
        net.add_node(key, color=color, shape=shape)
    # send edges
    for key, value in users.items():
        for tip in value[1]:
            net.add_edge(key, tip, color='#5b5b5b')
    net.force_atlas_2based()
    net.save_graph(str(output_file_name))
    print("Created graph: " + output_file_name)

def stats(users: Dict[str, List[Any]], output_file_name: str) -> None:
    connection_count: Dict[str, int] = {}
    for key, value in users.items():
        connections = len(value[1])
        if key not in connection_count:
            connection_count[key] = 0
        connection_count[key] += connections
        for receiver in value[1]:
            if receiver not in connection_count:
                connection_count[receiver] = 0
            if key not in users[receiver][1]:
                connection_count[receiver] += 1
    # output
    all_connections = sum(connection_count.values())
    users = len(connection_count)
    print(f"Found {users} user, which build {all_connections} connections.")
    print(f"On average every user has {round(all_connections / users, 2)} connections.")

    output = [f"| No. | Name | connections | % of all connections |", "|:-|:--------------|:-------:|:-------:|"]
    current_rank = 1
    for user, connections in reversed(sorted(connection_count.items(), key=lambda item: item[1])):
        output.append(f"| {current_rank} | {user} | {connections} | {round(100 * connections / all_connections, 2)} |")
        current_rank += 1
        if current_rank == 6:
            break
    with open(output_file_name, 'w') as f:
        for line in output:
            f.write(f"{line}\n")


if __name__ == "__main__":
    date_str = "2024-09-22"
    distribution = 155
    full_round = False
    date = datetime.strptime(f"{date_str} 00:00:00", '%Y-%m-%d %H:%M:%S')
    local_path = 'D:\\Scripts\\RedditAPIScript\\donut-distribution\\'
    file_name = f'{local_path}input\\tips_round_{distribution}.json'
    users = create_user(file_name, date, full_round)
    stats(users, local_path + f'output\\graph_{distribution}_{date_str}.txt')
    plot(users, local_path + f'output\\graph_{distribution}_{date_str}.html')

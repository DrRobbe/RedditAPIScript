import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import statistics
import json
from typing import Dict, List, Tuple


def create_user(file_name: str) -> Tuple[Dict[str, List[int]], List[str]]:
    user: Dict[str, List[int]] = {}
    amounts = []
    with open(file_name) as f:
        file_content = json.load(f)
    for values in file_content:
        if values["to_user_registered"] == 1:
            sender = values["from_user"]
            receiver = values["to_user"]
            amount = values["amount"]
            id_amount = str(amount) + "-" + sender + "-" + receiver
            amounts.append(id_amount)
            if sender not in user:
                user[sender] = [0, 0, 0, 0]
            if receiver not in user:
                user[receiver] = [0, 0, 0, 0]
            user[sender][0] += 1
            user[receiver][1] += 1
            if "t3_" in values["parent_content_id"]:
                user[sender][2] += 1
            elif "t1_" in values["parent_content_id"]:
                user[sender][3] += 1
    return user, amounts


def plot_tip_distribution(send: Dict[int, List[str]], received: Dict[int, List[str]], all_send: int, all_receive: int, all_user: int, file_name: str) -> None:
    plt.clf()
    sender = []
    interval = []
    for _, value in send.items():
        sender.append(len(value))
    receiver = []
    for _, value in received.items():
        receiver.append(len(value))

    combined = sender + list(reversed(receiver))[1:]
    combined[len(sender) - 1] += receiver.pop()
    interval = list(range(-95, 100, 5))

    plt.bar(interval, combined, color="black", width=5)

    plt.xlabel("Distribution")
    plt.ylabel("Users")
    plt.title("Counted " + str(all_user) + " user with more than 10 tips, " + str(all_send) + " send more, " + str(all_receive) + " received more!")
    # plt.show()
    plt.savefig(file_name.split(".")[0] + "_distribution" + '.png')


def plot_tip_amount(users: Dict[str, List[int]], file_name: str) -> None:
    send_amount: List[int] = []
    receive_amount: List[int] = []
    for _, stats in users.items():
        send_amount.append(stats[0])
        receive_amount.append(stats[1])

    send_amount = sorted(send_amount)
    receive_amount = sorted(receive_amount)
    send_all = len([positiv for positiv in send_amount if positiv > 0])
    receive_all = len([positiv for positiv in receive_amount if positiv > 0])
    send_mean = str(round(statistics.mean(send_amount), 0))
    receive_mean = str(round(statistics.mean(receive_amount), 0))
    send_median = str(round(statistics.median(send_amount), 1))
    receive_median = str(round(statistics.median(receive_amount), 1))
    print("Median tips send per user: " + send_median)
    print("Median tips received per user: " + receive_median)
    # Plotting x-axis and y-axis
    plt.yscale("log")
    # naming of x-axis and y-axis
    plt.xlabel("User")
    plt.ylabel("Tips")
    plt.title("Tips send & received for " + str(len(users)) + " user.")

    plt.plot(receive_amount, color='red', linestyle="-")
    plt.plot(send_amount, color='blue', linestyle="--")

    red_patch = mpatches.Patch(color='red', label="Received tips, User: " + str(receive_all) + ", Mean: " + receive_mean)
    blue_patch = mpatches.Patch(color='blue', label="Send tips, User: " + str(send_all) + ", Mean: " + send_mean)
    plt.grid(axis='y')
    plt.legend(handles=[red_patch, blue_patch])
    plt.subplots_adjust(bottom=0.2)
    plt.savefig(file_name.split(".")[0] + "_tip_amount" + '.png')


def analyse_amounts(amounts: List[str]) -> None:
    values = [0.]
    max_sender = ""
    max_receiver = ""
    users_received_tip: Dict[str, float] = {}
    users_send_tip: Dict[str, float] = {}
    for id_amount in amounts:
        current_amount = float(id_amount.split("-")[0])
        sender = id_amount.split("-")[1]
        receiver = id_amount.split("-")[2]
        if max(values) < current_amount:
            max_sender = sender
            max_receiver = receiver
        values.append(current_amount)
        if receiver not in users_received_tip:
            users_received_tip[receiver] = 0.
        users_received_tip[receiver] += current_amount
        if sender not in users_send_tip:
            users_send_tip[sender] = 0.
        users_send_tip[sender] += current_amount
    amount_median = str(round(statistics.median(values), 1))
    amount_mean = str(round(statistics.mean(values), 1))
    amount_max = str(round(max(values), 1))
    print(f"All Donuts send: {round(sum(values), 1)}")
    print(f"Max donuts in one tip: {amount_max}, from {max_sender} to {max_receiver}.")
    print(f"Median of donuts per tip: {amount_median}")
    print(f"Mean of donuts per tip: {amount_mean}")
    print("Top3 users with most donuts received via tips: ")
    number = 1
    for user in reversed(sorted(users_received_tip.items(), key=lambda item: item[1])[-3:]):
        print(f"\t{number}. {user[0]}, with {round(user[1],1)} donuts")
        number += 1
    print("Top3 users with most donuts send via tips: ")
    number = 1
    for user in reversed(sorted(users_send_tip.items(), key=lambda item: item[1])[-3:]):
        print(f"\t{number}. {user[0]}, with {round(user[1],1)} donuts")
        number += 1


def analyse_tips(users: Dict[str, List[int]], all_send_tips: int, all_send_to_post: int, all_send_to_comments: int, file_name: str) -> None:
    print(f"All tips send: {all_send_tips}")
    print(f"Mean tips send per user: {round(all_send_tips/len(users), 1)}")
    print(f"All tips send to posts: {all_send_to_post}")
    print(f"Mean tips send to post per user: {round(all_send_to_post/len(users), 1)}")
    print(f"All tips send to comments: {all_send_to_comments}")
    print(f"Mean tips send to comments per user: {round(all_send_to_comments/len(users), 1)}")
    plot_tip_amount(users, file_name)
    print("Top3 users with most tips received: ")
    number = 1
    for user in reversed(sorted(users.items(), key=lambda item: item[1][1])[-3:]):
        print(f"\t{number}. {user[0]}, with {round(user[1][1], 1)} tips")
        number += 1
    print("Top3 users with most tips send: ")
    number = 1
    for user in reversed(sorted(users.items(), key=lambda item: item[1][0])[-3:]):
        print(f"\t{number}. {user[0]}, with {round(user[1][0], 1)} tips")
        number += 1
        # calculate tip difference
    tip_difference = {}
    for use, tips in users.items():
        tip_difference[use] = tips[0] - tips[1]
    print("Top 5 users with highest tip difference, with more received tips:")
    for person in sorted(tip_difference.items(), key=lambda item: item[1])[:5]:
        print(f"* {person[0]} - tip difference: {abs(person[1])} - tips {round(100 * users[person[0]][0]/users[person[0]][1], 1)}% of the time back.")
    print("Top 5 users with highest tip difference, with more send tips:")
    for person in reversed(sorted(tip_difference.items(), key=lambda item: item[1])[-5:]):
        print(f"* {person[0]} - tip difference: {person[1]} - gets {round(100 * users[person[0]][1]/users[person[0]][0], 1)}% of the time tipped back.")


if __name__ == "__main__":
    path = 'D:\\Scripts\\RedditAPIScript\\donut-distribution\\'
    json_file = 'tips_round_145.json'
    input_file = path + 'input\\' + json_file
    output_file = path + 'output\\distribution\\' + json_file
    users, amounts = create_user(input_file)
    print("All registered users in this distribution: " + str(len(users)))
    print("===== Donuts =====")
    analyse_amounts(amounts)
    send_distribution: Dict[int, List[str]] = {5: [], 10: [], 15: [], 20: [], 25: [], 30: [], 35: [],
                                               40: [], 45: [], 50: [], 55: [], 60: [], 65: [], 70: [],
                                               75: [], 80: [], 85: [], 90: [], 95: [], 100: []}
    receive_distribution: Dict[int, List[str]] = {5: [], 10: [], 15: [], 20: [], 25: [], 30: [], 35: [],
                                                  40: [], 45: [], 50: [], 55: [], 60: [], 65: [], 70: [],
                                                  75: [], 80: [], 85: [], 90: [], 95: [], 100: []}

    all_user = 0
    all_send_tips = 0
    all_send_to_post = 0
    all_send_to_comments = 0
    # normal distribution for 10+ send/received users
    for user, stats in users.items():
        send_uservalue = -1.
        received_uservalue = -1.
        send_tips = stats[0]
        received_tips = stats[1]
        all_send_tips += send_tips
        all_send_to_post += stats[2]
        all_send_to_comments += stats[3]
        if send_tips > 10 or received_tips > 10:
            all_user += 1
            # more send
            if send_tips >= received_tips:
                send_uservalue = round(100 * received_tips / send_tips, 2)
            # more received
            if received_tips > send_tips:
                received_uservalue = round(100 * send_tips / received_tips, 2)
        if send_uservalue > -1:
            for precentage, _ in send_distribution.items():
                if precentage >= send_uservalue:
                    send_distribution[precentage].append(user + ": " + str(send_uservalue) + "%, send: " + str(send_tips) + ", received: " + str(received_tips))
                    break
        if received_uservalue > -1:
            for precentage, _ in receive_distribution.items():
                if precentage > received_uservalue:
                    receive_distribution[precentage].append(user + ": " + str(received_uservalue) + "%, send: " + str(send_tips) + ", received: " + str(received_tips))
                    break
    print("===== Tips =====")
    analyse_tips(users, all_send_tips, all_send_to_post, all_send_to_comments, output_file)
    print(f"Users with more than 10 tips send or received: {all_user}")
    all_receive = 0
    for _, values in receive_distribution.items():
        all_receive += len(values)
    print(f"Amount of users which received more tips: {all_receive}")
    all_send = 0
    for _, values in send_distribution.items():
        all_send += len(values)
    print(f"Amount of users which send more tips: {all_send}")
    plot_tip_distribution(send_distribution, receive_distribution, all_send, all_receive, all_user, output_file)
    # dump user data
    with open(path + 'output\\distribution\\UserStats' + json_file.split("_")[2].split(".")[0] + "_for10tipsSendReceived.txt", "w") as current_file:
        for precentage, data in send_distribution.items():
            current_file.write(f"Users with less than {precentage}% send:\n")
            for line in data:
                current_file.write("\t" + line + "\n")
        for precentage, data in sorted(list(receive_distribution.items()), reverse=True):
            current_file.write(f"Users with less than {precentage}% receive\n")
            for line in data:
                current_file.write("\t" + line + "\n")

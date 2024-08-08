import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import statistics
from typing import Dict, List, Set, Any


def create_user(file_name: str) -> Dict[str, List[Set]]:
    user: Dict[str, List[Set]] = {}
    with open(file_name) as current_file:
        file_content = current_file.readlines()
    for line in file_content:
        if "- INFO - tip " in line:
            number = line.split("INFO - tip [")[1].split(" of ")[0]
            sender = line.split(" [from]: ")[1].split(" [to]:")[0]
            receiver = line.split(" [to]:")[1].split(" [amount]:")[0]
            if sender not in user:
                user[sender] = [set(), set()]
            if receiver not in user:
                user[receiver] = [set(), set()]
            user[sender][0].add(number)
            user[receiver][1].add(number)
    # remove bots
    bots = ["AutoModerator", "donut-bot"]
    for bot in bots:
        user.pop(bot)
    return user

def plot_tip_distribution(send: Dict[int, List[str]], received: Dict[int, List[str]], all_send: int, all_receive: int, all_user: int, file_name: str) -> None:
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

def plot_tip_amount(users: Dict[str, List[Set]], file_name: str) -> None:
    send_amount = []
    receive_amount = []
    for _, stats in users.items():
        send_amount.append(len(stats[0]))
        receive_amount.append(len(stats[1]))

    send_amount = sorted(send_amount)
    receive_amount = sorted(receive_amount)
    send_all = len([positiv for positiv in send_amount if positiv > 0])
    receive_all = len([positiv for positiv in receive_amount if positiv > 0])
    send_mean = statistics.mean(send_amount)
    receive_mean = statistics.mean(receive_amount)
    send_median = statistics.median(send_amount)
    receive_median = statistics.median(receive_amount)   
    print("All users median send: " + send_median)
    print("All users mean send: " + send_mean)
    print("All users median recieved: " + receive_median)
    print("All users mean recieved: " + receive_mean)
    # Plotting x-axis and y-axis
    plt.yscale("log")
    # naming of x-axis and y-axis
    plt.xlabel("User")
    plt.ylabel("Tips")
    plt.title("Tips send & received for " + str(len(users)) + " user.")

    plt.plot(receive_amount, color='red', linestyle="-")
    plt.plot(send_amount, color='blue', linestyle="--")

    red_patch = mpatches.Patch(color='red', label="Received tips, User: " + str(receive_all) + ", Mean: " + str(round(receive_mean, 1)))
    blue_patch = mpatches.Patch(color='blue', label="Send tips, User: " + str(send_all) + ", Mean: " + str(round(send_mean, 1)))
    plt.grid(axis='y')
    plt.legend(handles=[red_patch, blue_patch])
    plt.subplots_adjust(bottom=0.2)
    plt.savefig(file_name.split(".")[0] + "_tip_amount" + '.png')

if __name__ == "__main__":
    file_name = 'distribution_139.txt'
    users = create_user(file_name)

    plot_tip_amount(users, file_name)
    send_distribution: Dict[int, List[str]] = {5: [],  10: [], 15: [], 20: [], 25: [], 30: [], 35: [],
    40: [], 45: [], 50: [], 55: [], 60: [], 65: [], 70: [], 75: [], 80: [], 85: [], 90: [], 95: [], 100: []}
    receive_distribution: Dict[int, List[str]] = {5: [],  10: [], 15: [], 20: [], 25: [], 30: [], 35: [], 
    40: [], 45: [], 50: [], 55: [], 60: [], 65: [], 70: [], 75: [], 80: [], 85: [], 90: [], 95: [], 100: []}

    all_user = 0
    max_send: List[Any] = ["", 0]
    max_recieved: List[Any] = ["", 0]
    for user, stats in users.items():
        send_uservalue = -1.
        received_uservalue = -1.
        len_stats0 = len(stats[0])
        len_stats1 = len(stats[1])
        if len_stats0 > 10 or len_stats1 > 10:
            all_user += 1
            # more send
            if len_stats0 >= len_stats1:
                send_uservalue = round(100 * len_stats1/len_stats0, 2)
            # more received
            if len_stats1 > len_stats0:
                received_uservalue = round(100 * len_stats0/len_stats1, 2)
            if max_recieved[1] < len_stats1:
                max_recieved[1] = len_stats1
                max_recieved[0] = user
            if max_send[1] < len_stats0:
                max_send[1] = len_stats0
                max_send[0] = user
        if send_uservalue > -1:
            for precentage, _ in send_distribution.items():
                if precentage >= send_uservalue:
                    send_distribution[precentage].append(user + ": " + str(send_uservalue) + "%, send: " + str(len_stats0) + ", received: " + str(len_stats1))
                    break
        if received_uservalue > -1:
            for precentage, _ in receive_distribution.items():
                if precentage > received_uservalue:
                    receive_distribution[precentage].append(user + ": " + str(received_uservalue) + "%, send: " + str(len_stats0) + ", received: " + str(len_stats1))
                    break
    print("All users: " + str(all_user))
    all_receive = 0
    for _, value in receive_distribution.items():
        all_receive += len(value)
    print("More receive users: " + str(all_receive))
    all_send = 0
    for _, value in send_distribution.items():
        all_send += len(value)
    print("More send users: " + str(all_send))
    plot_tip_distribution(send_distribution, receive_distribution, all_send, all_receive, all_user, file_name)
    print("Max send: " + max_send[0] + ", with " + str(max_send[1]))
    print("Max received: " + max_recieved[0] + ", with " + str(max_recieved[1]))
    # dump user data
    with open(file_name.split(".")[0] + "_UserStats.txt", "w") as current_file:
        for precentage, value in send_distribution.items():
            current_file.write("Users with less than " + str(precentage) + "% send:\n")
            for line in value:
                current_file.write("\t" + line + "\n")
        for precentage, value in sorted(list(receive_distribution.items()), reverse=True):
            current_file.write("Users with less than " + str(precentage) + "% receive\n")
            for line in value:
                current_file.write("\t" + line + "\n")

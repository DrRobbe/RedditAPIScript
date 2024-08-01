import matplotlib.pyplot as plt

def plot(send, received, all_send, all_receive, all_user, file_name):
    sender = []
    interval = []
    for key, value in send.items():
        sender.append(len(value))
    receiver = []
    for _, value in received.items():
        receiver.append(len(value))


    combined = sender + list(reversed(receiver))[1:]
    combined[len(sender) - 1] +=  receiver.pop()
    interval = list(range(-95, 100, 5))

    plt.bar(interval, combined, color="black", width = 5)

    plt.xlabel("Distribution")
    plt.ylabel("Users")
    plt.title("Counted " + str(all_user) + " user with more than 10 tips, " + str(all_send) + " send more, " + str(all_receive) + " received more!")
    #plt.show()
    plt.savefig(file_name.split(".")[0] + '.pdf')

def create_user(file_name):
    user = {}
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
    return user

if __name__ == "__main__":
    file_name = 'distribution_138.txt'
    user = create_user(file_name)

    send_distribution = {5: [],  10: [], 15: [], 20: [], 25: [], 30: [], 35: [],
                    40: [], 45: [], 50: [], 55: [], 60: [], 65: [], 70: [], 75: [],
                    80: [], 85: [], 90: [], 95: [], 100: []}
    receive_distribution = {5: [],  10: [], 15: [], 20: [], 25: [], 30: [], 35: [],
                    40: [], 45: [], 50: [], 55: [], 60: [], 65: [], 70: [], 75: [],
                    80: [], 85: [], 90: [], 95: [], 100: []}

    all_user = 0
    user_str_list = []
    max_send = ["", 0]
    max_recieved = ["", 0]
    for user, stats in user.items():
        send_uservalue = -1
        received_uservalue = -1
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
    plot(send_distribution, receive_distribution, all_send, all_receive, all_user, file_name)
    print("Max send: " + max_send[0] + ", with " + str(max_send[1]))
    print("Max received: " + max_recieved[0] + ", with " + str(max_recieved[1]))
    with open(file_name.split(".")[0] + "_UserStats.txt", "w") as current_file:
        for precentage, value in send_distribution.items():
            current_file.write("Users with less than " + str(precentage) + "% send:\n")
            for line in value:
                current_file.write("\t" + line + "\n")
        for precentage, value in receive_distribution.items():
            current_file.write("Users with less than " + str(precentage) + "% receive\n")
            for line in value:
                current_file.write("\t" + line + "\n")
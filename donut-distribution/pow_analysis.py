import csv
import os

if __name__ == "__main__":
    path = "D:\\Scripts\\RedditAPIScript\\donut-distribution\\input\\pow\\"
    all_users = {}
    week_count = 0
    current_week = 'No'
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.csv'):
                print(path + file)
                with open(path + file, newline='') as csvfile:
                    spamreader = csv.reader(csvfile, delimiter=",", quotechar='|')
                    for row in spamreader:
                        if row[2] not in ["author", "None"]:
                            if current_week != row[0]:
                                week_count +=1
                                current_week = row[0]
                            if row[2] not in all_users:
                                all_users[row[2]] = [0,0,0,0]   
                            all_users[row[2]][int(row[1])-1] += 1
    output = [f"| No. | Name | Rank 1 | Rank 2 | Rank 3 | Rank 4 |",
              "|:-|:--------------|:-------:|:---------------------:|:------:|:---------------------:|"]
    number = 1
    for person in reversed(sorted(all_users.items(), key=lambda item: item[1][0]*100 + item[1][1]*10 + item[1][2] + item[1][3]*0.1)):
        output.append(f"| {number} | {person[0]} | {all_users[person[0]][0]} | {all_users[person[0]][1]} | {all_users[person[0]][2]} | {all_users[person[0]][3]} | ")
        number += 1
    print(week_count)
    local_path = "D:\\Scripts\\RedditAPIScript\\donut-distribution\\"
    with open(local_path + f'output\\pow-{str(week_count)}-tabel.txt', 'w') as f:
        for line in output:
            f.write(f"{line}\n")



                            




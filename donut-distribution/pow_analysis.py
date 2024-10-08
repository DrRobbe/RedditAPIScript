import json
import os

if __name__ == "__main__":
    path = "D:\\Scripts\\RedditAPIScript\\donut-distribution\\input\\pow\\"
    all_users = {}
    weeks = set()
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.json'):
                print(path + file)
                with open(path + file) as f:
                    file_content = json.load(f)
                    for values in file_content:
                        weeks.add(values['week_number'])
                        author = values["author"]
                        if author not in all_users:
                            all_users[author] = [0,0,0,0]   
                        all_users[author][values["rank"]-1] += 1
    output = [f"| No. | Name | Rank 1 | Rank 2 | Rank 3 | Rank 4 |",
              "|:-|:--------------|:-------:|:---------------------:|:------:|:---------------------:|"]
    number = 1
    for person in reversed(sorted(all_users.items(), key=lambda item: item[1][0]*100 + item[1][1]*10 + item[1][2] + item[1][3]*0.1)):
        output.append(f"| {number} | {person[0]} | {all_users[person[0]][0]} | {all_users[person[0]][1]} | {all_users[person[0]][2]} | {all_users[person[0]][3]} | ")
        number += 1
    print(len(weeks))
    local_path = "D:\\Scripts\\RedditAPIScript\\donut-distribution\\"
    with open(local_path + f'output\\pow-{str(len(weeks))}-tabel.txt', 'w') as f:
        for line in output:
            f.write(f"{line}\n")



                            




import json
import os
from typing import Dict

INPUT_PATH = "D:\\Scripts\\RedditAPIScript\\donut-distribution\\input\\pow\\"
OUPUT_PATH = "D:\\Scripts\\RedditAPIScript\\donut-distribution\\"


def create_leaderboard() -> int:
    all_users = {}
    weeks = set()
    for _, _, files in os.walk(INPUT_PATH):
        for file in files:
            if file.endswith('.json'):
                print(INPUT_PATH + file)
                with open(INPUT_PATH + file) as f:
                    file_content = json.load(f)
                    for values in file_content:
                        weeks.add(values['week_number'])
                        author = values["author"]
                        if author not in all_users:
                            all_users[author] = [0, 0, 0, 0]
                        all_users[author][values["rank"] - 1] += 1
    output = ["| No. | Name | Contrib gained | Rank 1 | Rank 2 | Rank 3 | Rank 4 | ",
              "|:-|:---------------------|:------------------:|:-------:|:-------:|:-------:|:-------:|"]
    number = 1
    current_rank = number
    last_contrib = 1000000000
    for person in reversed(sorted(all_users.items(), key=lambda item: item[1][0] * 5000 + item[1][1] * 3000 + item[1][2] * 1500 + item[1][3] * 500)):
        all_contrib = all_users[person[0]][0] * 5000 + all_users[person[0]][1] * 3000 + all_users[person[0]][2] * 1500 + all_users[person[0]][3] * 500
        if all_contrib < last_contrib:
            last_contrib = all_contrib
            current_rank = number
        output.append(f"| {current_rank} | {person[0]} |  {all_contrib} | {all_users[person[0]][0]} | {all_users[person[0]][1]} | {all_users[person[0]][2]} | {all_users[person[0]][3]} |")
        number += 1
    print(f"Including {len(weeks)} weeks")
    with open(OUPUT_PATH + f'output\\pow\\pow-{str(len(weeks))}-tabel.txt', 'w') as f:
        for line in output:
            f.write(f"{line}\n")
    return len(weeks)


def get_votes(weeks: int) -> None:
    voters: Dict[str, int] = {}
    posts: Dict[str, int] = {}
    file = "historical.txt"
    with open(INPUT_PATH + file) as f:
        lines = f.readlines()
    for line in lines:
        columns = line.split(',')
        if columns[0] != "id":
            voter = columns[2]
            post = columns[1]
            if voter not in voters:
                voters[voter] = 0
            if post not in posts:
                posts[post] = 0
            voters[voter] += 1
            posts[post] += 1
    output = ["| No. | Name | Votes | ", "|:-|:---------------------|:------------------:|"]
    number = 1
    current_rank = number
    last_votes = 1000000000
    for person in reversed(sorted(voters.items(), key=lambda x: int(x[1]))):
        votes = person[1]
        if votes < last_votes:
            last_votes = votes
            current_rank = number
        output.append(f"| {current_rank} | {person[0]} | {votes} |")
        number += 1
    with open(OUPUT_PATH + f'output\\pow\\voters-{str(weeks)}-tabel.txt', 'w') as f:
        for line in output:
            f.write(f"{line}\n")
    print(f"{len(voters)} voters participated in pow votes!")
    post_vote_counts = [0]
    posts_sorted = sorted(posts.items(), key=lambda x: int(x[1]))
    for i in range(1, posts_sorted[-1][1] + 1):
        post_vote_counts.append(0)
        for entry in posts_sorted:
            if entry[1] == i:
                post_vote_counts[i] += 1
            if entry[1] > i:
                break
    print(f"{sum(post_vote_counts)} posts got at least one vote.")
    for i in range(1, len(post_vote_counts)):
        if post_vote_counts[i] != 0:
            print(f"    * {post_vote_counts[i]} posts got {i} votes")
    print(f"Most votes got post {posts_sorted[-1][0]}, with {posts_sorted[-1][1]}!")


if __name__ == "__main__":
    weeks = create_leaderboard()
    get_votes(weeks)

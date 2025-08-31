import os
import json

if __name__ == "__main__":
    round_to_check = 153
    user = "drrobbe"
    local_path = 'D:\\Scripts\\RedditAPIScript\\donut-distribution\\input\\ratio\\ratio.txt'
    out_path = 'D:\\Scripts\\RedditAPIScript\\donut-distribution\\output\\ratio\\'
    ratio_data = []
    comment_ratio = 0
    post_ratio = 0
    with open(local_path) as f:
        ratio_data = f.readlines()
    for ratio in ratio_data[2:]:
        data_split = ratio.split("|")
        if int(data_split[1].strip()) == round_to_check:
            comment_ratio = float(data_split[2].strip())
            post_ratio = float(data_split[3].strip())
    print(f"Round {round_to_check}, comment ratio: {comment_ratio}, post ratio: {post_ratio}.")

    finale_csv_path = "D:\\Scripts\\RedditAPIScript\\donut-distribution\\input\\finale_csv\\"
    comment_score = 0
    post_score = 0
    for root, dirs, files in os.walk(finale_csv_path):
        for file in files:
            if str(round_to_check) in file:
                with open(finale_csv_path + file) as f:
                    lines = f.readlines()
                    for line in lines:
                        if user in line:
                            data = line.split(",")
                            comment_score = float(data[3])
                            post_score = float(data[4])
    print(f"For {user}, comment score: {comment_score}, post score: {post_score}.")    

    tips_comments = 0
    tips_posts = 0
    weight = 0
    real_comment_score = 0
    real_post_score = 0
    local_path_distribution = 'D:\\Scripts\\RedditAPIScript\\donut-distribution\\'
    file_name = local_path_distribution + f'input\\tips_round_{round_to_check}.json'
    with open(file_name) as f:
        file_content = json.load(f)
    for values in file_content:
        if values["to_user"].lower() == user:
            weight = values["weight"]
            if "t3_" in values["parent_content_id"]:
                tips_posts += 1
                real_post_score += weight * post_ratio
            elif "t1_" in values["parent_content_id"]:
                tips_comments += 1
                real_comment_score += weight * comment_ratio
    print(f"For {user}, comment tips: {tips_comments}, post tips: {tips_posts}.")                 
    print(f"Real user ratio, ratio comment: {round(comment_score/tips_comments, 2)}, ratio posts: {round(post_score/tips_posts, 2)}.") 
    print(f"Check comment score: {real_comment_score}, post score: {real_post_score}.")
import praw
import os


def main(last_date, upper_date):
    f = open("account.txt", "r")
    account_details = f.readlines()

    reddit = praw.Reddit(client_id=account_details[0].strip(),
                         client_secret=account_details[1].strip(),
                         user_agent="my user agent")

    bot_love_count = 0
    all_comment = 0
    leaderboard = {}
    subreddit_name = 'ethtrader'
    posts = reddit.subreddit(subreddit_name).new(limit=None)
    post_list = [x for x in posts if upper_date >= x.created_utc >= last_date and "Daily General Discussion" in x.title]
    print("Number of created posts: " + str(len(post_list)))
    for post in post_list:
        post.comments.replace_more(limit=None)
        for comment in post.comments.list():
            all_comment += 1
            if "good bot" in comment.body.lower():
                bot_love_count += 1
                author = comment.author.name
                if author in leaderboard.keys():
                    leaderboard[author] += 1
                else:
                    leaderboard[author] = 1

    f = open(os.path.join("data", str(last_date) + "to" + str(upper_date) + ".txt"), "w")
    f.write("Number of created posts: " + str(len(post_list)) + "\n")
    f.write("All comments: " + str(all_comment) + "\n")
    f.write("Good Bot comments: " + str(bot_love_count) + "\n")
    f.write(str(100 * round(bot_love_count / all_comment, 2)) + "% good comments\n")
    for key, value in leaderboard.items():
        f.write(key + ": " + str(value) + "\n")
    f.close()


if __name__ == "__main__":
    main(1708470001, 1708556401)

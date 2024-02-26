import praw


def main(user_name):
    f = open("account.txt", "r")
    account_details = f.readlines()

    reddit = praw.Reddit(client_id=account_details[0].strip(),
                         client_secret=account_details[1].strip(),
                         user_agent="my user agent")

    bot_love_count = 0
    all_comment = 0
    user = reddit.redditor(user_name)
    for comment in user.comments.new(limit=None):
        all_comment += 1
        if "good bot" in comment.body.lower():
            bot_love_count += 1

    print("All comments: " + str(all_comment))
    print("Good Bot comments: " + str(bot_love_count))
    print(str(100 * round(bot_love_count / all_comment, 2)) + "% good comments")


if __name__ == "__main__":
    main("DrRobbe")

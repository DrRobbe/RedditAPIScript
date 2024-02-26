import os
import operator

def main():
    number_of_posts = 0
    number_of_comments = 0
    number_of_good_comments = 0
    users = {}
    from_date_finale = 9900000000
    to_date_finale = -1
    path = "D:\\Scripts\\goodbot\\data"
    for file in os.listdir(path):
        if file.endswith(".txt"):
            # get first and last dates
            from_date = int(file.split("to")[0])
            to_date = int(file.split("to")[1].split(".")[0])
            if from_date_finale > from_date:
                from_date_finale = from_date
            if to_date_finale < to_date:
                to_date_finale = to_date
            # get data from file
            f = open(path + "\\" + file, "r")
            lines = f.readlines()
            number_of_posts += int(lines[0].split(":")[1].strip())
            number_of_comments += int(lines[1].split(":")[1].strip())
            number_of_good_comments += int(lines[2].split(":")[1].strip())
            for i in range(4, len(lines)):
                comments = int(lines[i].split(":")[1].strip()) 
                user = lines[i].split(":")[0].strip()
                if user in users.keys():
                    users[user] += comments
                else:
                    users[user] = comments
    sorted_dict = dict(sorted(users.items(), key=operator.itemgetter(1), reverse=True))


    f = open(str(from_date_finale) + "to" + str(to_date_finale) + ".txt", "w")
    f.write("Number of created posts: " + str(number_of_posts) + "\n")
    f.write("All comments: " + str(number_of_comments) + "\n")
    f.write("Good Bot comments: " + str(number_of_good_comments) + "\n")
    f.write(str(100 * round(number_of_good_comments / number_of_comments, 2)) + "% good comments\n")
    for key, value in sorted_dict.items():
        f.write(key + ": " + str(value) + "\n")
    f.close()

if __name__ == "__main__":
    main()
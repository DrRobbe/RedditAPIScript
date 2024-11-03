
local_path = "D:\\Scripts\\RedditAPIScript\\coins\\"

if __name__ == "__main__":
    data_file = open(local_path + "input\\31-10-24.txt", "r")
    data_lines = data_file.readlines()
    amount = []
    for line in data_lines:
        amount.append(float(line.strip()))
    print(sum(amount))

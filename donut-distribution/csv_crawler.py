import pandas as pd
import os
import statistics

if __name__ == "__main__":
    path = "D:\\Scripts\\RedditAPIScript\\donut-distribution\\input\\finale_csv\\"
    all_data = []
    for root, dirs, files in os.walk(path):
        for file in files:
            print(path + file)
            csv_data = pd.read_csv(path + file)
            summe = csv_data['pay2post'].sum()
            print(summe)
            all_data.append(summe)
    print("=====")
    print(all_data)
    print(statistics.mean(all_data))
    print(statistics.stdev(all_data))

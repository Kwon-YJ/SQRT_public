import os
import csv

# from pprint import pprint

import matplotlib.pyplot as plt
import numpy as np


def load_csv2list(dir, name):
    f = open(os.path.join(dir, name), "r")
    return [x for x in csv.reader(f)]


def bar2line(bar_dict):

    target = list(bar_dict.values())
    new_valuse = []

    for var in target:
        if len(new_valuse) == 0:
            new_valuse.append(var)
        else:
            new_valuse.append(new_valuse[-1] + var)

    result = {}
    for idx, key in enumerate(bar_dict.keys()):
        result[key] = new_valuse[idx]

    return result


if __name__ == "__main__":

    for time_frame in ["12h", "1d", "3d"]:

        print(time_frame)

        target_folder = f"../daily_result/{time_frame}"
        file_names = sorted(os.listdir(target_folder))

        result_dict = {}

        for file_name in file_names:
            csv_lists = load_csv2list(target_folder, file_name)
            for csv_list in csv_lists:
                _, date, earning = csv_list

                if date in result_dict.keys():
                    # result_dict[date].append(float(earning))
                    result_dict[date] += round(float(earning), 3)
                else:
                    # result_dict[date] = [float(earning)]
                    result_dict[date] = round(float(earning), 3)

        # for i in range(2020, 2025):
        #     os.system("clear")
        #     print(f"year : {i}")

        #     years = [x for x in result_dict.keys() if str(i) in x]
        #     values = [result_dict[x] for x in result_dict.keys() if str(i) in x]

        #     x = np.arange(len(years))
        #     plt.bar(x, values)
        #     plt.xticks(x, years)

        #     plt.show()

        bar_data = bar2line(result_dict)

        years = list(bar_data.keys())
        values = list(bar_data.values())

        x = np.arange(len(years))
        plt.bar(x, values)
        plt.xticks(x, years)

        plt.show()

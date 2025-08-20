import os
import csv

# from pprint import pprint

import matplotlib.pyplot as plt
import numpy as np


def load_csv2list(dir, name):
    encodings = ["utf-8", "euc-kr", "cp949"]
    for encoding in encodings:
        try:
            with open(os.path.join(dir, name), "r", encoding=encoding) as f:
                return [x for x in csv.reader(f)][1:]
        except UnicodeDecodeError:
            continue
    raise Exception(f"Failed to read file with encodings: {encodings}")


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
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--param", type=int, default=20)
    args = parser.parse_args()

    target_folder = f"./runfile_result/result_{args.param}/daily_result"
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

    save_foler = f"./runfile_result/result_{args.param}/"

    for i in range(2001, 2025):
        print(f"year : {i}")

        years = [x for x in result_dict.keys() if str(i) in x]
        values = [result_dict[x] for x in result_dict.keys() if str(i) in x]

        x = np.arange(len(years))
        plt.bar(x, values)
        plt.xticks(x, years)

        # plt.show()
        save_dir = os.path.join(save_foler, f"plot_{i}.png")
        print(save_dir)
        plt.savefig(save_dir)
        plt.clf()

    bar_data = bar2line(result_dict)

    years = list(bar_data.keys())
    values = list(bar_data.values())

    x = np.arange(len(years))
    plt.bar(x, values)
    plt.xticks(x, years)

    # plt.show()

    save_dir = os.path.join(save_foler, "plot_all.png")
    plt.savefig(save_dir)
    print(save_dir)

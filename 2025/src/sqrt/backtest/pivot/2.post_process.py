import os
import random
import toml


def sort_by_val(target_dict):
    return sorted(target_dict.items(), key=lambda item: item[1])

def remove_ticker(file_list, remove_target):
    return [x for x in file_list if remove_target not in x]


def get_result(target_folder):
    distance_result = {}
    total_earn_result = {}

    file_list = os.listdir(target_folder)
    file_list = remove_ticker(file_list, "BTCUSDT")
    file_list = remove_ticker(file_list, "ETHUSDT")

    for file in file_list:
        file_dir = os.path.join(target_folder, file)
        ticker: str = file.split("_pivot_s2")[0]
        f = open(file_dir, "r")
        lines = f.readlines()[-20:]  # 마지막 20줄 파싱

        for i, line in enumerate(lines):
            if "최대 손실" in line:
                total_earn, distance = lines[i + 1 : i + 3]
                total_earn = total_earn.split("\n")[0]
                distance = distance.split("\n")[0]
                distance_result[ticker] = distance
                total_earn_result[ticker] = total_earn
    return sort_by_val(distance_result), sort_by_val(total_earn_result)


def main():
    target_folders = os.listdir()
    target_folders = [x for x in target_folders if "h_" in x]

    result = {}

    for target_folder in target_folders:
        distance_result, total_earn_result = get_result(target_folder)

        # 최대 수익 결과 + 최대 거리 결과의 합이 45개가 될 때까지
        for i in range(20, len(distance_result)):
            sliced_distance_result = [x[0] for x in distance_result][-i:]
            sliced_total_earn_result = [x[0] for x in total_earn_result][-i:]
            merge_result = list(
                set(sliced_distance_result) | set(sliced_total_earn_result)
            )

            if len(merge_result) > 45:
                merge_result = merge_result[:45]
                random.shuffle(merge_result)
                result[target_folder] = merge_result

                print(f"distance_result : {target_folder}")

                final_result = {}

                for var in merge_result:
                    for tup in distance_result:
                        if var == tup[0]:
                            # print(tup)
                            final_result[tup[0]] = float(tup[1])
                
                from pprint import pprint
                pprint(final_result)
                print(sum(final_result.values())/len(final_result))

                print("")
                print("")

                break

    result_items = [result[key] for key in result.keys()]
    result_items = list(set(sum(result_items, [])))
    result["all"] = result_items
    print(result)

    with open("pivot_ticker_list.toml", "w", encoding="utf-8") as file:
        toml.dump({"pivot": result}, file)


if __name__ == "__main__":
    main()

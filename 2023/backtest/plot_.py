import os

all_dir = os.listdir()

txt_dir = [file_name for file_name in all_dir if ".txt" in file_name]
# txt_dir = txt_dir[:2]
# print(txt_dir)

money_dict = {}

for file_name in txt_dir:
    f = open(f"./{file_name}", "r")
    key = file_name.split(".txt")[0]
    value = f.readlines()[-3]
    money_dict[key] = value
    f.close()


# fst_val = [val.split("_")[0] for val in txt_dir]
# scnd_val = [val.split("_")[1][:-4] for val in txt_dir]


print(money_dict)

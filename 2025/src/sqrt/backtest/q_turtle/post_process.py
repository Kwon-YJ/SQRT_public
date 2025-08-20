import os
import re


def dir_arrangement() -> None:
    file_list = os.listdir()
    file_list = [x for x in file_list if ".txt" in x]
    if len(file_list) == 0:
        return

    for time_frame in time_frames:
        os.makedirs(time_frame, exist_ok=True)

    for file_name in file_list:
        if "_8h_" in file_name:
            os.system(f"mv {file_name} ./8h/{file_name} ")
        elif "_2h_" in file_name:
            os.system(f"mv {file_name} ./2h/{file_name} ")
        elif "_12h_" in file_name:
            os.system(f"mv {file_name} ./12h/{file_name} ")
        elif "_6h_" in file_name:
            os.system(f"mv {file_name} ./6h/{file_name} ")
        elif "_4h_" in file_name:
            os.system(f"mv {file_name} ./4h/{file_name} ")
        else:
            os.system(f"mv {file_name} ./1h/{file_name} ")


time_frames = ["12h", "8h", "6h", "4h", "2h", "1h"]

dir_arrangement()

os.makedirs("./result")

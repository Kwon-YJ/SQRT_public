import os

# time_frames = ["1m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d"]
time_frames = ["12h", "1d", "3d"]

for time_frame in time_frames:
    os.makedirs(f"../result/{time_frame}", exist_ok=True)

csv_list = os.listdir("../result")

for csv_file in csv_list:
    for time_frame in time_frames:
        if time_frame == csv_file:
            continue
        if time_frame in csv_file:
            cmd = f"mv ../result/{csv_file} ../result/{time_frame}/{csv_file}"
            os.system(cmd)
            break

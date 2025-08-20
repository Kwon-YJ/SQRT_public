import os

os.makedirs(f"../runfile_result", exist_ok=True)

if os.path.isdir("../csv_raw_file") == False:
    os.system("python3 utils.py")


for i in range(2, 35):
    var = i / 100

    os.system(f"julia -t {os.cpu_count()} stock_816.jl --thres {var}")
    os.system("julia stock_816_postprocess.jl")
    os.system("python3 daily_backtest.py")

    os.makedirs(f"../result_{i}")
    os.system(f"mv ../result ../result_{i}")
    os.system(f"mv ../post_result ../result_{i}")
    os.system(f"mv ../daily_result ../result_{i}")

    os.system(f"mv ../result_{i} ../runfile_result")

    os.system(f"python3 get_perform_daily.py --param {i}")

import subprocess
import os


result = subprocess.run(["julia", "main_data_save.jl"], capture_output=True, text=True)
print(result.stdout)

result = subprocess.run(
    ["julia", "-t", "4", "main_backtest.jl"], capture_output=True, text=True
)
print(result.stdout)

result = subprocess.run(
    ["python3", "time_frame_sort.py"], capture_output=True, text=True
)
print(result.stdout)


result = subprocess.run(
    ["julia", "-t", "4", "main_backtest_daily.jl"], capture_output=True, text=True
)
print(result.stdout)

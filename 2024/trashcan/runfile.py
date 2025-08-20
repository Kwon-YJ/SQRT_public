import os
import time
import psutil
import datetime
import subprocess
import platform
import logging


def kill_julia_process(name):
    for proc in psutil.process_iter(["pid", "name"]):
        if name in proc.info["name"]:
            try:
                psutil.Process(proc.info["pid"]).kill()
                logger.info(
                    f"Process {name} with PID {proc.info['pid']} has been killed."
                )
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass


def kill_other_python_processes():
    current_pid = os.getpid()
    process = subprocess.Popen(
        ["ps", "-eo", "pid,cmd"], stdout=subprocess.PIPE, text=True
    )
    stdout, _ = process.communicate()

    for line in stdout.splitlines():
        if "python" in line and str(current_pid) not in line:
            pid = int(line.split()[0])
            os.kill(pid, 9)


def get_time():
    result = str(datetime.datetime.utcfromtimestamp(time.time()))
    return result[11:13] + result[14:16]


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


time_var = str(datetime.datetime.utcfromtimestamp(time.time()))
date_var = time_var.split(" ")[0]


os.system(f"nohup julia PQ_binance.jl >> PQ_binance{date_var}.out &")
os.system(f"nohup julia R2_pivot.jl >> R2_pivot{date_var}.out &")


if platform.system() == "Windows":
    os.system(f"nohup python PQ_bybit.py >> PQ_bybit{date_var}.out &")
    os.system(
        f"nohup python /root/BTC_daytrade/2024/backtest/stock/stock_816_screener.py > stock{date_var}.out"
    )

elif platform.system() == "Linux":
    os.system(f"nohup python3 PQ_bybit.py >> PQ_bybit{date_var}.out &")
    os.system(
        f"nohup python3 /root/BTC_daytrade/2024/backtest/stock/stock_816_screener.py > stock{date_var}.out"
    )

# nohup python3 runfile.py &

if __name__ == "__main__":
    while True:
        time.sleep(1)
        if get_time() == "0001" or get_time() == "1201":
            time.sleep(10)
            time_var = str(datetime.datetime.utcfromtimestamp(time.time()))
            date_var = time_var.split(" ")[0]

            logger.info("restart system")

            os.system(f"nohup julia PQ_binance.jl >> PQ_binance{date_var}.out &")
            if platform.system() == "Windows":
                os.system(f"nohup python PQ_bybit.py >> PQ_bybit{date_var}.out &")
            elif platform.system() == "Linux":
                os.system(f"nohup python3 PQ_bybit.py >> PQ_bybit{date_var}.out &")

            time.sleep(60)

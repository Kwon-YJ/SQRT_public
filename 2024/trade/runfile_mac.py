import os
import time
import psutil
import datetime
import subprocess
import platform
import logging


def get_time():
    result = str(datetime.datetime.utcfromtimestamp(time.time()))
    return result[11:13] + result[14:16]


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

time_var = str(datetime.datetime.utcfromtimestamp(time.time()))
date_var = time_var.split(" ")[0]

os.system(f"nohup julia PQ_binance.jl >> PQ_binance{date_var}.out &")

if __name__ == "__main__":
    while True:
        time.sleep(1)
        if get_time() == "0001" or get_time() == "1201":
            time.sleep(10)
            time_var = str(datetime.datetime.utcfromtimestamp(time.time()))
            date_var = time_var.split(" ")[0]
            logger.info("restart system")
            os.system(f"nohup julia PQ_binance.jl >> PQ_binance{date_var}.out &")
            time.sleep(60)

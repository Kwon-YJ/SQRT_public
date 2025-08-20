import os

# from multiprocessing import Process
import multiprocessing
import numpy as np
import parmap
import time


def doubler(input_list):
    time.sleep(1)
    return [x * x for x in input_list]


if __name__ == "__main__":
    num_cores = multiprocessing.cpu_count()
    data = list(range(0, 10000000))
    splited_data = np.array_split(data, num_cores)
    splited_data = [x.tolist() for x in splited_data]
    a = time.time()
    # result_ = sum( parmap.map(doubler, splited_data, pm_pbar=True, pm_processes=num_cores) , [])
    # result_ = sum( parmap.map(doubler, [data], pm_pbar=True, pm_processes=num_cores) , [])
    b = time.time()

    print(result_)
    print(b - a)

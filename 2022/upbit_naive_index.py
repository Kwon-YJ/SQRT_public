import ccxt
import time
import numpy as np
import pandas as pd
import datetime
import pandas_ta as ta

import pickle


file_name = f"{79}.pickle"

with open(file_name, "rb") as fr:
    All_ohlcv = pickle.load(fr)

# del All_ohlcv[13]

print(All_ohlcv[13][-1][4])

result = []

for i in range(96):
    open = 0
    high = 0
    low = 0
    close = 0
    for j in range(len(All_ohlcv)):
        open += All_ohlcv[j][i][1]
        high += All_ohlcv[j][i][2]
        low += All_ohlcv[j][i][3]
        close += All_ohlcv[j][i][4]

        print(All_ohlcv[j][i])

    timestamp = All_ohlcv[13][i][0]
    open = open / len(All_ohlcv)
    high = high / len(All_ohlcv)
    low = low / len(All_ohlcv)
    close = close / len(All_ohlcv)
    ohlcv = [timestamp, open, high, low, close]
    result.append(ohlcv)


print(result)

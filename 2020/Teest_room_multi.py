# -*- coding: utf-8 -*-

import multiprocessing
import csv
import math
import ccxt
import time
import datetime
import numpy as np
from pprint import pprint
import parmap


def WMA(df, period):  # 가중이동평균
    result = []
    for epoch in range(len(df) - period + 1):
        value = 0
        for n in range(1, period + 1):
            value = value + (df[n + epoch - 1] * n)
        result.append(value / ((period * (period + 1)) / 2))
    return result


def HMA(df, period):  # Hull 이동평균
    data1 = WMA(df, int(period / 2))
    for i in range(0, len(data1)):
        data1[i] = data1[i] * 2
    data2 = WMA(df, period)
    data3 = []
    for i in range(0, len(data2)):
        data3.append(data1[i + len(data1) - len(data2)] - data2[i])
    return WMA(data3, int(math.sqrt(period)))


"""
a = binance.fetch_ohlcv('BTC/USDT', '5m')

temp_temp = []

a = convert(a)

print(a[-1])


for i in range(len(a)):
    temp_temp.append(a[i][4])

b = HMA(temp_temp, 20)

print(b[-5:])

temp_temp_2 = []


for i in range(len(b)):
    data_ =b[-i] / temp_temp[-i]
    # data_ = abs(1 - (b[-i] / temp_temp[-i]))
    temp_temp_2.append(data_)
result = np.std(temp_temp_2)
print(result)
"""


def get_500ohlcv(ticker):
    time_ = "2020-09-10T00:00:00"
    # ticker_ohlcvs = binance.fetch_ohlcv(ticker, '5m', binance.parse8601(time_))

    """
    for i in range(len(ticker_ohlcvs)):
        basis[idx].append(ticker_ohlcvs[i][4])
    timestamp = ticker_ohlcvs[-1][0]
    datetimeobj = str(datetime.datetime.fromtimestamp(timestamp/1000))
    nexttime = datetimeobj[0:10] + 'T' + datetimeobj[11:19]
    try:
        get_500ohlcv(ticker, nexttime, idx)
    except:
        print(ticker)
    """
    temp = []

    try:
        while True:
            time.sleep(1.1)
            ticker_ohlcvs = binance.fetch_ohlcv(ticker, "5m", binance.parse8601(time_))
            for i in range(len(all_tickers)):
                temp.append(ticker_ohlcvs[i][4])
            timestamp = ticker_ohlcvs[-1][0]
            datetimeobj = str(datetime.datetime.fromtimestamp(timestamp / 1000))
            time_ = datetimeobj[0:10] + "T" + datetimeobj[11:19]
    except:
        return [temp]


if __name__ == "__main__":
    num_cores = 2
    # result_ =sum( parmap.map(log_maker, All_tickers, pm_pbar=True, pm_processes=num_cores), [])

    exchange_class = getattr(ccxt, "binance")
    binance = exchange_class(
        {
            "urls": {
                "api": {
                    "public": "https://fapi.binance.com/fapi/v1",
                    "private": "https://fapi.binance.com/fapi/v1",
                },
            }
        }
    )

    binance.enableRateLimit = True
    binance.RateLimit = 10000
    binance.load_markets()
    is_entering = {}

    all_tickers = list(binance.fetch_tickers().keys())

    basis = []
    for i in range(len(all_tickers)):
        basis.append([])

    result__ = sum(
        parmap.map(get_500ohlcv, all_tickers, pm_pbar=True, pm_processes=num_cores), []
    )

    for i in range(len(result__)):
        print(result__[i][-3:], len(result__[i]))

    # for i, ticker in enumerate(all_tickers):
    #    get_500ohlcv(ticker, start, i)

    all_final = []

    for m in range(len(basis)):
        temp = []
        for k in range(2, len(basis[m]) - 2, 3):
            temp.append(basis[m][k])
        all_final.append(temp)

    f = open("result.csv", "w", encoding="euc-kr", newline="")

    wr = csv.writer(f)

    try:
        for i in range(len(all_final)):
            wr.writerow(all_final[i])
    except:
        print("프로그램 실행 완료")
    f.close()

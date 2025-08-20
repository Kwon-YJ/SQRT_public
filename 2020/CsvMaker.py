# -*- coding: utf-8 -*-

import csv
import math
import ccxt
import time
import datetime
import numpy as np


def get_500ohlcv(ticker, time_, idx):
    ticker_ohlcvs = binance.fetch_ohlcv(ticker, "5m", binance.parse8601(time_))
    for i in range(len(ticker_ohlcvs)):
        basis[idx].append(ticker_ohlcvs[i][4])
    timestamp = ticker_ohlcvs[-1][0]
    datetimeobj = str(datetime.datetime.fromtimestamp(timestamp / 1000))
    nexttime = datetimeobj[0:10] + "T" + datetimeobj[11:19]
    try:
        get_500ohlcv(ticker, nexttime, idx)
    except:
        print(ticker)


if __name__ == "__main__":
    num_cores = 6
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

    start = "2019-08-30T00:00:00"
    a = start[0:10] + " " + start[11:19]
    convert_date = str((datetime.datetime.strptime(a, "%Y-%m-%d %H:%M:%S")).timestamp())
    now = str(datetime.datetime.now().timestamp())
    all_tickers = list(binance.fetch_tickers().keys())
    basis = []
    for i in range(len(all_tickers)):
        basis.append([])
    for i, ticker in enumerate(all_tickers):
        get_500ohlcv(ticker, start, i)
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

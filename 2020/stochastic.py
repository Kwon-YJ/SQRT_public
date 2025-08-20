# -*- coding: utf-8 -*-

import ccxt
import time
import datetime
import pandas as pd


def get_time():
    now = datetime.datetime.now()
    YYYY = str(now.year)
    MM = str(now.month)
    DD = str(now.day)
    hh = str(now.hour)
    mm = str(now.minute)

    if len(MM) != 2:
        MM = "0" + MM
    if len(DD) != 2:
        DD = "0" + DD
    if len(hh) != 2:
        hh = "0" + hh
    if len(mm) != 2:
        mm = "0" + mm

    return YYYY + MM + DD, hh + mm


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


def stochastic(ohlcv, K=5, period=3):
    i = 5
    result = []
    while i < len(ohlcv) - 1:
        i += 1
        high_ = [ohlcv[-x + i][2] for x in range(K)]
        low_ = [ohlcv[-x + i][3] for x in range(K)]
        temp = (ohlcv[i][4] - min(low_)) / (max(high_) - min(low_)) * 100
        result.append(temp)
    return pd.Series(result).rolling(period).mean().tolist()


a = binance.fetch_ohlcv("BTC/USDT", "1h")


b = stochastic(a)


print(b)

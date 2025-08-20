# -*- coding: utf-8 -*-

import ccxt
import time
import datetime
import pandas as pd


def ma(data, length):
    result = []
    for i in range(len(data)):
        result.append(data[i][4])
    return pd.Series(result).rolling(length).mean().tolist()[-1]


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

while True:
    try:
        time.sleep(1)
        time_ = get_time()[1][3:]
        if time_ == "0" or time_ == "5":
            time.sleep(10)
            ohlcv = binance.fetch_ohlcv("BTC/USDT", "5m")
            ma_ = ma(ohlcv, 6)
            if ohlcv[-2][-3] > ma_:
                binance.create_order("BTC/USDT", "market", "sell", 0.1)
                # TR = ohlcv[-2][2] - ohlcv[-2][3]
                price = round(ohlcv[-1][3] * 0.99849, 2)
                binance.create_order("BTC/USDT", "limit", "buy", 0.1, price)
                time.sleep(51)
    except:
        time.sleep(0.5)
        continue

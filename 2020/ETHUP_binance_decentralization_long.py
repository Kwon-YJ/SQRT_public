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
binance = exchange_class()
binance.enableRateLimit = True
binance.RateLimit = 10000
binance.load_markets()


def convert(ohlcv5):  # convert 5m → 15m
    ohlcv15 = []
    temp = str(datetime.datetime.fromtimestamp(ohlcv5[0][0] / 1000))[14:16]
    if int(temp) % 15 == 5:
        del ohlcv5[0]
        del ohlcv5[1]
    elif int(temp) % 15 == 10:
        del ohlcv5[0]
    for i in range(0, len(ohlcv5) - 2, 3):
        highs = [ohlcv5[i + j][2] for j in range(0, 3) if ohlcv5[i + j][2]]
        lows = [ohlcv5[i + j][3] for j in range(0, 3) if ohlcv5[i + j][3]]
        volumes = [ohlcv5[i + j][5] for j in range(0, 3) if ohlcv5[i + j][5]]
        candle = [
            ohlcv5[i + 0][0],
            ohlcv5[i + 0][1],
            max(highs) if len(highs) else None,
            min(lows) if len(lows) else None,
            ohlcv5[i + 2][4],
        ]
        ohlcv15.append(candle)
    return ohlcv15


while True:
    try:
        time.sleep(1)
        time_ = get_time()[1][2:]
        if time_ == "00" or time_ == "15" or time_ == "30" or time_ == "45":
            time.sleep(6)
            ohlcv = convert(binance.fetch_ohlcv("LINKUP/USDT", "5m"))
            ma_ = ma(ohlcv, 6)
            if ohlcv[-1][2] < ma_:
                order = binance.create_order("LINKUP/USDT", "market", "buy", 140)
                TR = ohlcv[-1][2] - ohlcv[-1][3]
                price = float(order["info"]["fills"][0]["price"]) + 0.6 * TR
                binance.create_order("LINKUP/USDT", "limit", "sell", 139.6, price)
                time.sleep(61)
    except:
        time.sleep(0.5)
        continue

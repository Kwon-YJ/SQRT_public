# -*- coding: utf-8 -*-
import ccxt
import time
import pandas as pd
import os
import datetime
import pyupbit


def get_time(temp):
    now = temp
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


def exit_ALL():
    for i in range(len(is_entering)):
        time.sleep(0.7)
        unit = upbit2.get_balance(is_entering[i])
        upbit2.sell_market_order(is_entering[i], unit)
    reset = []
    return reset


def buy_order(item):
    ticker = "KRW-" + item[:-4]
    size = 60000  # KRW
    upbit2.buy_market_order(ticker, size)
    is_entering.append(ticker)
    banList.append(item)



upbit = ccxt.upbit(
    {
        "enableRateLimit": True,
        "RateLimit": 10000,
    }
)
upbit.load_markets()


banList = []
is_entering = []
temp = upbit.fetch_tickers().keys()
tickers = [s for s in temp if "KRW" in s]


upbit2.buy_market_order("KRW-XRP", 5000)


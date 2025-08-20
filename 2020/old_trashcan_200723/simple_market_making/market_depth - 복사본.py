# -*- coding: utf-8 -*-
import ccxt
import time
import datetime
import pandas as pd
from ccxt.base.decimal_to_precision import *
import os
import csv
import telegram
from pprint import pprint


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
bot = telegram.Bot(token=my_token)

binance.enableRateLimit = True
binance.RateLimit = 10000
# binance.apiKey = 'API'
# binance.secret = 'API'
binance.load_markets()

bitmex = ccxt.bitmex()


def Getdiff():
    a = binance.fetch_ticker("BTC/USDT")["close"]
    b = bitmex.fetch_ticker("BTC/USD")["close"]
    c = a / b
    return a, b, c


f = open("abc.csv", "w", encoding="euc-kr", newline="")

wr = csv.writer(f)

try:
    i = 0
    while True:
        x, y, z = Getdiff()
        wr.writerow([datetime.datetime.now(), x, y, z])
        i = i + 3
        time.sleep(60)
except:
    f.close()
    print("프로그램 실행 완료")

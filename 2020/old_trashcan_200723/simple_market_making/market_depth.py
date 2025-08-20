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


def GetMidVwap(ticker, count):
    AskTemp1, AskTemp2, BidTemp1, BidTemp2 = 0, 0, 0, 0
    BaseData = binance.fetch_order_book(ticker)
    AskData = BaseData["asks"][: count + 1]
    BidData = BaseData["bids"][: count + 1]
    for i, askdata in enumerate(AskData):
        AskTemp1 += askdata[1]
        AskTemp2 += askdata[0] * askdata[1]
    for j, biddata in enumerate(BidData):
        BidTemp1 += biddata[1]
        BidTemp2 += biddata[0] * biddata[1]
    return (AskData[0][0] + BidData[0][0]) / 2, (
        AskTemp2 / AskTemp1 + BidTemp2 / BidTemp1
    ) / 2  # MidPrice, MidBwap


"""
while(True):
	#print(binance.fetch_ohlcv('LTC/USDT')[-1][4])
	x, y = GetMidVwap('LTC/USDT', 5)
	print(x,y)
	print('')
"""


f = open("result.csv", "w", encoding="euc-kr", newline="")

wr = csv.writer(f)

try:
    i = 0
    while True:
        if i == 0:
            wr.writerow([datetime.datetime.now()])
            wr.writerow(["midprice", "midvwap"])
        x, y = GetMidVwap("LTC/USDT", 5)
        wr.writerow([x, y])
        i = i + 2
except:
    wr.writerow([datetime.datetime.now()])
    f.close()
    print("프로그램 실행 완료")

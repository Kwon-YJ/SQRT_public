# -*- coding: utf-8 -*-
import ccxt
import os
import csv

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
binance.apiKey = ""
binance.secret = ""
binance.load_markets()


def SignalMaker(ticker, i=2):
    ohlcv = binance.fetch_ohlcv(ticker, "1d")
    while True:
        HH = max(ohlcv[-i][2], ohlcv[-i - 1][2], ohlcv[-i - 2][2], ohlcv[-i - 3][2])
        HC = max(ohlcv[-i][4], ohlcv[-i - 1][4], ohlcv[-i - 2][4], ohlcv[-i - 3][4])
        LC = min(ohlcv[-i][4], ohlcv[-i - 1][4], ohlcv[-i - 2][4], ohlcv[-i - 3][4])
        LL = min(ohlcv[-i][3], ohlcv[-i - 1][3], ohlcv[-i - 2][3], ohlcv[-i - 3][3])
        if ohlcv[-i][4] > ohlcv[-i][1] + (max(HH - LC, HC - LL) * 0.55):
            return "buy"
        elif ohlcv[-i][4] < ohlcv[-i][1] - (max(HH - LC, HC - LL) * 0.55):
            return "sell"
        else:
            i = i + 1
            continue


def Csv_init():
    with open(str(os.getcwd()) + "/savedata3.csv", "w", newline="") as file:
        writer = csv.writer(file)
        tickers = list(binance.fetch_tickers().keys())
        writer.writerow(tickers)
        writer.writerow([SignalMaker(tickers[x]) for x in range(24)])
        writer.writerow([0 for i in range(24)])


Csv_init()

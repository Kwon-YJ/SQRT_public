import ccxt
import pandas as pd
import urllib.request
import json
import time
import numpy


def get_perfomance(trade_log):
    win = []
    lose = []
    risk_free = 0.038 / 365
    avg = numpy.mean(trade_log)
    std = numpy.std(trade_log)
    size = (avg - risk_free) / (std * std)

    for i in range(len(trade_log)):
        if trade_log[i] > 0:
            win.append(trade_log[i])
        elif trade_log[i] < 0:
            lose.append(trade_log[i])

    print("총거래 : ", len(trade_log))
    print("수익거래수 :", len(win))
    print("손실거래수 :", len(lose))
    print("평균거래 :", avg)
    print("평균수익거래 :", numpy.mean(win))
    print("평균손실거래 :", numpy.mean(lose))
    print("평균손익비 :", -1 * numpy.mean(win) / numpy.mean(lose))
    print("승률 :", int(round(len(win) / len(trade_log), 2) * 100), "%")
    print("포지션 사이징 :", size)
    print("")


exchange_class = getattr(ccxt, "binance")
binance = exchange_class()
binance.enableRateLimit = True
binance.RateLimit = 10000
binance.load_markets()


ticker = "XRP/USDT"
timeframe = "1d"
positive = [0, 0, 0, 0, 0, 0, 0]
negative = [0, 0, 0, 0, 0, 0, 0]
buy_sell_log = []

ohlcvs = binance.fetch_ohlcv(ticker, timeframe)

for i, item in enumerate(ohlcvs):
    if item[1] < item[4]:
        positive[i % 7] = positive[i % 7] + 1
    elif item[1] > item[4]:
        negative[i % 7] = negative[i % 7] + 1

for i, item in enumerate(ohlcvs):
    if i % 7 == 1:
        earning = 100 * ((ohlcvs[i][4] / ohlcvs[i][1]) * 0.99925 * 0.99925 - 1)
        # earning = 100 * ((ohlcvs[i][4] / ohlcvs[i][1]) - 1)
        buy_sell_log.append(earning)


print(positive)
print(negative)

print(ohlcvs[0][0])

get_perfomance(buy_sell_log)

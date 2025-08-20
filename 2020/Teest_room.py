# -*- coding: utf-8 -*-

import csv
import math
import time
import datetime
import numpy as np


def bb(x, w=20, k=2):  # 볼린저 밴드
    mbb = HMA(x, w)
    lbb = mbb - k * np.std(x[-w:])
    ubb = mbb + k * np.std(x[-w:])
    return lbb, ubb, mbb


def WMA(df, period):  # 가중이동평균
    result = []
    for epoch in range(len(df) - period + 1):
        value = 0
        for n in range(1, period + 1):
            value = value + ((df[n + epoch - 1]) * n)
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


def log_maker(length_, std_):
    for j in range(len(All_ohlcv)):
        price.clear()
        ohlcv = All_ohlcv[j]
        i = length_ + 6
        first_trade_buy = None
        is_buy_entering = None
        while i < len(ohlcv) - 2:
            close_ = ohlcv[i]
            lbb_, ubb_, mbb = bb(ohlcv[i - 5 - length_ : i], length_, std_)
            i += 1
            if close_ > ubb_[-1] and is_buy_entering != False:
                buy_price = ohlcv[i + 1]
                price.append(buy_price)
                is_buy_entering = False
                if first_trade_buy == None:
                    first_trade_buy = False
            elif close_ < lbb_[-1] and is_buy_entering != True:
                buy_price = ohlcv[i + 1]
                price.append(buy_price)
                is_buy_entering = True
                if first_trade_buy == None:
                    first_trade_buy = True
        for idx in range(len(price) - 1):
            if (first_trade_buy == True and idx % 2 == 0) or (
                first_trade_buy == False and idx % 2 == 1
            ):
                # normal
                earning = 100 * ((price[idx + 1] / price[idx]) * 0.99925 * 0.99925 - 1)
                buy_sell_log.append(earning)
            else:
                # reverse
                earning = 100 * ((price[idx] / price[idx + 1]) * 0.99925 * 0.99925 - 1)
                buy_sell_log.append(earning)


def get_perfomance(trade_log):
    import numpy

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
    print("승률 :", len(win) / len(trade_log))
    print("포지션 사이징 :", size)
    print("")

    return [len(win) / len(trade_log), -1 * numpy.mean(win) / numpy.mean(lose)]


def csv2list(filename):
    file = open(filename, "r")
    csvfile = csv.reader(file)
    lists = []
    for item in csvfile:
        lists.append(item)
    return lists


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


csv_ = csv2list("result.csv")
price = []
buy_sell_log = []

All_ohlcv = []

for i in range(len(csv_)):
    temp = [float(x) for x in csv_[i]]
    All_ohlcv.append(temp)


# log_maker(30, 2.5)
# get_perfomance(buy_sell_log)
# price.clear()
# buy_sell_log.clear()


# a = [MA_value, STD_value, win_rate, avg_P&L, win_rate * (1 + avg_P&L) ]

csv_list = []

for i in range(2, 40, 2):
    for j in range(1, 30):
        log_maker(i, round(j * 0.1, 2))
        aa = get_perfomance(buy_sell_log)
        csv_list.append([i, j, aa[0], aa[1]])
        price.clear()
        buy_sell_log.clear()

print(csv_list)

f = open("output.csv", "w", encoding="euc-kr", newline="")

wr = csv.writer(f)

try:
    i = 0
    while len(csv_list):
        if i == 0:
            wr.writerow(["MA", "STD", "WinRate", "AVG_PNL", "factor"])
        wr.writerow(
            [
                csv_list[i],
                csv_list[i + 1],
                csv_list[i + 2],
                csv_list[i + 3],
                csv_list[i + 4],
            ]
        )
        i = i + 5
except:
    print("프로그램 실행 완료")
f.close()

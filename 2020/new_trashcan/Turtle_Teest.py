import ccxt
import time
import os
import numpy
import datetime


exchange_class = getattr(ccxt, "binance")
binance = exchange_class()
binance.enableRateLimit = True
binance.RateLimit = 10000
binance.apiKey = "FRbVseExyAWjQUtYFnS4memLnPCcgNAeRW7HEBrrw9qyIyPUMCTzUKxZKOJIHcfV"
binance.secret = "CbDX3DE5r9ErdLBOphDB4rjCaAaKbUqITbNK05YIitktZ24VfcNrvVRbIgfK6L87"
binance.load_markets()


def timestamp_to_datetime(timestamp):
    datetimeobj = datetime.datetime.fromtimestamp(timestamp / 1000)
    return datetimeobj


def log_maker_S1():
    for j in range(len(ticker_list)):
        if len(price) != 0:
            earning = 100 * ((ohlcv[-1][4] / price[0]) * 0.99964 * 0.99964 - 1)
            buy_sell_log.append(earning)
        price.clear()
        ohlcv = All_ohlcv[j]

        for i in range(21, len(ohlcv) - 1):
            if len(price) != 0:
                temp = []
                for k in range(-10, 0):
                    temp.append(ohlcv[i + k][3])

                if ohlcv[i][3] < min(temp):
                    earning = 100 * ((min(temp) / price[0]) * 0.99925 * 0.99925 - 1)
                    buy_sell_log.append(earning)
                    price.clear()
                else:
                    continue

            temp = []
            for k in range(-20, 0):
                temp.append(ohlcv[i + k][2])
            if ohlcv[i][2] > max(temp):
                buy_price = max(temp)
                # sell_price = high_ * 1.0015
                price.append(buy_price)
                # price.append(sell_price)


def log_maker_S2():
    for j in range(len(ticker_list)):
        if len(price) != 0:
            earning = 100 * ((ohlcv[-1][4] / price[0]) * 0.99964 * 0.99964 - 1)
            buy_sell_log.append(earning)
        price.clear()
        ohlcv = All_ohlcv[j]

        for i in range(56, len(ohlcv) - 1):
            if len(price) != 0:
                temp = []
                for k in range(-20, 0):
                    temp.append(ohlcv[i + k][3])

                if ohlcv[i][3] < min(temp):
                    earning = 100 * ((min(temp) / price[0]) * 0.99925 * 0.99925 - 1)
                    buy_sell_log.append(earning)
                    price.clear()
                else:
                    continue

            temp = []
            for k in range(-55, 0):
                temp.append(ohlcv[i + k][2])
            if ohlcv[i][2] > max(temp):
                buy_price = max(temp)
                price.append(buy_price)


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


ticker_list = [
    "BTC/USDT",
    "ETH/USDT",
    "BCH/USDT",
    "XRP/USDT",
    "EOS/USDT",
    "LTC/USDT",
    "TRX/USDT",
    "ETC/USDT",
    "LINK/USDT",
    "XLM/USDT",
    "ADA/USDT",
    "XMR/USDT",
    "DASH/USDT",
    "ZEC/USDT",
    "XTZ/USDT",
    "BNB/USDT",
    "ATOM/USDT",
    "ONT/USDT",
    "IOTA/USDT",
    "BAT/USDT",
    "VET/USDT",
    "NEO/USDT",
    "QTUM/USDT",
    "IOST/USDT",
    "THETA/USDT",
    "ALGO/USDT",
    "ZIL/USDT",
    "KNC/USDT",
    "ZRX/USDT",
    "COMP/USDT",
    "OMG/USDT",
    "DOGE/USDT",
]

All_ohlcv = []
price = []
buy_sell_log = []


for i in range(len(ticker_list)):
    temp = binance.fetch_ohlcv(ticker_list[i], "5m")
    All_ohlcv.append(temp)

log_maker_S2()
get_perfomance(buy_sell_log)

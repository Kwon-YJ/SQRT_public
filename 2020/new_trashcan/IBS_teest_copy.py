import ccxt
import time
import os
import numpy
import datetime


exchange_class = getattr(ccxt, "binance")
binance = exchange_class()
binance.enableRateLimit = True
binance.RateLimit = 10000
binance.load_markets()


def timestamp_to_datetime(timestamp):
    datetimeobj = datetime.datetime.fromtimestamp(timestamp / 1000)
    return datetimeobj


def log_maker():
    for j in range(len(ticker_list)):
        ohlcv = All_ohlcv[j]
        for i in range(0, len(ohlcv) - 1):
            open_ = ohlcv[i][1]
            high_ = ohlcv[i][2]
            low_ = ohlcv[i][3]
            close_ = ohlcv[i][4]

            if high_ - low_ == 0:
                IBS = 0.5
                IBS2 = 0.5
            else:
                IBS = (close_ - low_) / (high_ - low_)
                IBS2 = (open_ - low_) / (high_ - low_)

            # if IBS < 0.1 and IBS2 > 0.9:
            if IBS < 0.1:
                buy_price = ohlcv[i + 1][1]
                sell_price = ohlcv[i + 1][4]
                earning = 100 * ((sell_price / buy_price) * 0.99964 * 0.99964 - 1)
                buy_sell_log.append(earning)


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
    print("승률 :", len(win) / len(trade_log))
    print("포지션 사이징 :", size)
    print("")


# IBS = close - low / high - low

time_frame = "1d"

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
"""
day = 101

temp_time = str(timestamp_to_datetime(binance.fetch_ohlcv('BTC/USDT','1d')[-day-2][0]))
convert = temp_time[:10] + 'T' + temp_time[11:19] + 'Z'
timestamp = binance.parse8601(convert)
"""
for i in range(len(ticker_list)):
    temp = binance.fetch_ohlcv(ticker_list[i], time_frame)
    All_ohlcv.append(temp)

log_maker()
get_perfomance(buy_sell_log)

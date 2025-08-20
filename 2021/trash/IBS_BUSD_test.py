# -*- coding: utf-8 -*-
import ccxt
import time
import pandas as pd
import numpy as np
import urllib
import json
import telegram
import datetime
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
    print("승률 :", len(win) / len(trade_log))
    print("포지션 사이징 :", size)
    print("")


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


def ATR(data, length):
    TR = []
    for i in range(int(length)):
        TR.append(
            max(
                (data[i - length][2] - data[i - length][3]),
                abs(data[i - length][2] - data[i - length - 1][4]),
                abs(data[i - length][3] - data[i - length - 1][4]),
            )
        )
    ATR = pd.Series(TR).ewm(length).mean()
    return ATR.tolist()


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
    "SXP/USDT",
    "KAVA/USDT",
    "BAND/USDT",
    "RLC/USDT",
    "WAVES/USDT",
    "MKR/USDT",
    "SNX/USDT",
    "DOT/USDT",
    "DEFI/USDT",
    "YFI/USDT",
    "BAL/USDT",
    "CRV/USDT",
    "TRB/USDT",
    "YFII/USDT",
    "RUNE/USDT",
    "SUSHI/USDT",
    "SRM/USDT",
    "BZRX/USDT",
    "EGLD/USDT",
    "SOL/USDT",
    "ICX/USDT",
    "STORJ/USDT",
    "BLZ/USDT",
    "UNI/USDT",
    "AVAX/USDT",
    "FTM/USDT",
    "HNT/USDT",
    "ENJ/USDT",
    "FLM/USDT",
    "TOMO/USDT",
    "REN/USDT",
    "KSM/USDT",
    "NEAR/USDT",
    "AAVE/USDT",
    "FIL/USDT",
    "RSR/USDT",
    "LRC/USDT",
    "MATIC/USDT",
    "OCEAN/USDT",
    "CVC/USDT",
    "BEL/USDT",
    "CTK/USDT",
    "AXS/USDT",
    "ALPHA/USDT",
    "ZEN/USDT",
    "SKL/USDT",
]  # , 'GRT/USDT', '1INCH/USDT']


bot = telegram.Bot(token=my_token)


Up_group_name = []
Up_group_value = []
Down_group_name = []
Down_group_value = []
result = []
hour_ = -1

final_ = []


All_ohlcv = []

for i in range(len(ticker_list)):
    temp = binance.fetch_ohlcv(ticker_list[i], "1h")
    All_ohlcv.append(temp)


Up_index = []
Down_index = []


for i in range(-1, 497):
    hour_ = i
    if hour_ % 100 == 0:
        print(hour_)
    while 1:
        for j in range(len(All_ohlcv)):
            try:
                # ohlcv = binance.fetch_ohlcv(ticker_list[j], '1h')
                ohlcv = All_ohlcv[j]
                vol = abs(ohlcv[-2 - hour_][1] - ohlcv[-2 - hour_][4])
                atr = ATR(ohlcv, 10)[-1]
                gap = vol / atr

                open_ = ohlcv[-2 - hour_][1]
                high_ = ohlcv[-2 - hour_][2]
                low_ = ohlcv[-2 - hour_][3]
                close_ = ohlcv[-2 - hour_][4]

                if high_ - low_ == 0:
                    continue

                IBS = (close_ - low_) / (high_ - low_)

                if ohlcv[-2 - hour_][1] < ohlcv[-2 - hour_][4] and IBS > 0.9:
                    Up_group_name.append(ticker_list[j])
                    Up_group_value.append(gap)
                    Up_index.append(j)

                elif ohlcv[-2 - hour_][1] > ohlcv[-2 - hour_][4] and IBS < 0.1:
                    Down_group_name.append(ticker_list[j])
                    Down_group_value.append(gap)
                    Down_index.append(j)
            except:
                time.sleep(2)
                print("err1")
                continue

        for k in range(len(Up_group_value)):
            if max(Up_group_value) == Up_group_value[k]:
                result.append([Up_group_name[k], Up_group_value[k]])
                break

        for m in range(len(Down_group_value)):
            if max(Down_group_value) == Down_group_value[m]:
                result.append([Down_group_name[m], Down_group_value[m]])
                break

        while 1:
            try:
                if len(result) != 2:
                    result.clear()
                    Up_group_name.clear()
                    Up_group_value.clear()
                    Up_index.clear()
                    Down_group_name.clear()
                    Down_group_value.clear()
                    Down_index.clear()
                    break

                if result[1][1] > 1:  # long
                    long_ = All_ohlcv[Down_index[0]]
                    b = 100 * (
                        (long_[-1 - hour_][4] / long_[-1 - hour_][1])
                        * 0.99925
                        * 0.99925
                        - 1
                    )
                    final_.append(b)
            except Exception as ex:
                time.sleep(2)
                print("err2", ex)
                continue
            result.clear()
            Up_group_name.clear()
            Up_group_value.clear()
            Up_index.clear()
            Down_group_name.clear()
            Down_group_value.clear()
            Down_index.clear()
            break
        break

get_perfomance(final_)
print("00")
print("00")

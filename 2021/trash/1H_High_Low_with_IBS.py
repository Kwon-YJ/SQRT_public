# -*- coding: utf-8 -*-
import ccxt
import time
import pandas as pd
import numpy as np
import urllib
import json
import telegram
import datetime


def send_MSG(message):
    while True:
        try:
            bot.send_message(chat_id=801167350, text=str(message))
            time.sleep(3)
            return None
        except:
            time.sleep(3)
            continue


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
    "GRT/USDT",
    "1INCH/USDT",
]


bot = telegram.Bot(token=my_token)


Up_group_name = []
Up_group_value = []
Down_group_name = []
Down_group_value = []
result = []


while 1:
    if get_time()[1][2:] != "56":
        time.sleep(25)
        continue
    time.sleep(5)
    for i in range(len(ticker_list)):
        try:
            ohlcv = binance.fetch_ohlcv(ticker_list[i], "1h")
            vol = abs(ohlcv[-2][1] - ohlcv[-2][4])
            atr = ATR(ohlcv, 10)[-1]
            gap = vol / atr

            open_ = ohlcv[-2][1]
            high_ = ohlcv[-2][2]
            low_ = ohlcv[-2][3]
            close_ = ohlcv[-2][4]

            if high_ - low_ == 0:
                continue

            IBS = (close_ - low_) / (high_ - low_)

            if ohlcv[-2][1] < ohlcv[-2][4] and IBS > 0.9:
                Up_group_name.append(ticker_list[i])
                Up_group_value.append(gap)

            elif ohlcv[-2][1] > ohlcv[-2][4] and IBS < 0.1:
                Down_group_name.append(ticker_list[i])
                Down_group_value.append(gap)
        except Exception as ex:
            print("err1", ex)
            time.sleep(2)
            continue

    for k in range(len(Up_group_value)):
        if max(Up_group_value) == Up_group_value[k]:
            result.append([Up_group_name[k], Up_group_value[k]])
            break

    for m in range(len(Down_group_value)):
        if max(Down_group_value) == Down_group_value[m]:
            result.append([Down_group_name[m], Down_group_value[m]])
            break

    if len(result) != 2:
        time.sleep(120)
        result.clear()
        Up_group_name.clear()
        Up_group_value.clear()
        Down_group_name.clear()
        Down_group_value.clear()
        continue

    if (result[0][1] > 1.5 and result[1][1] > 1) or (
        result[0][1] > 1 and result[1][1] > 1.5
    ):
        send_MSG(result)
        time.sleep(60)

    result.clear()
    Up_group_name.clear()
    Up_group_value.clear()
    Down_group_name.clear()
    Down_group_value.clear()

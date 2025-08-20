# -*- coding: utf-8 -*-
import ccxt
import time
import pandas as pd
import numpy as np
import urllib
import json
import datetime
import telegram


def trade_order(ticker, sell_price):
    buy_amount = get_amount(ticker)
    order = binance.create_order(ticker, "market", "buy", buy_amount)
    sell_amount = float(order["amount"]) * 0.99995
    binance.create_order(ticker, "limit", "sell", sell_amount, sell_price)


def get_amount(ticker):
    price = binance.fetch_ohlcv(ticker)[-1][4]
    today_money = 11
    return today_money / price


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
binance = exchange_class()
binance.enableRateLimit = True
binance.RateLimit = 10000
binance.apiKey = "FRbVseExyAWjQUtYFnS4memLnPCcgNAeRW7HEBrrw9qyIyPUMCTzUKxZKOJIHcfV"
binance.secret = "CbDX3DE5r9ErdLBOphDB4rjCaAaKbUqITbNK05YIitktZ24VfcNrvVRbIgfK6L87"
binance.load_markets()


ticker_list = [
    "AXS/BUSD",
    "SNX/BUSD",
    "KSM/BUSD",
    "ZEC/BUSD",
    "BLZ/BUSD",
    "NEAR/BUSD",
    "SKL/BUSD",
    "NEO/BUSD",
    "DOGE/BUSD",
    "EGLD/BUSD",
    "RSR/BUSD",
    "BTC/BUSD",
    "MATIC/BUSD",
    "XTZ/BUSD",
    "FIL/BUSD",
    "LTC/BUSD",
    "BCH/BUSD",
    "ONT/BUSD",
    "QTUM/BUSD",
    "SOL/BUSD",
    "ALGO/BUSD",
    "UNI/BUSD",
    "CTK/BUSD",
    "OCEAN/BUSD",
    "FLM/BUSD",
    "ICX/BUSD",
    "VET/BUSD",
    "TRX/BUSD",
    "YFII/BUSD",
    "YFI/BUSD",
    "COMP/BUSD",
    "ZRX/BUSD",
    "AAVE/BUSD",
    "LRC/BUSD",
    "XLM/BUSD",
    "ATOM/BUSD",
    "BZRX/BUSD",
    "SXP/BUSD",
    "KNC/BUSD",
    "BEL/BUSD",
    "DASH/BUSD",
    "IOTA/BUSD",
    "MKR/BUSD",
    "TRB/BUSD",
    "BNB/BUSD",
    "ADA/BUSD",
    "XRP/BUSD",
    "XMR/BUSD",
    "ZIL/BUSD",
    "ETH/BUSD",
    "BAL/BUSD",
    "BAT/BUSD",
    "ALPHA/BUSD",
    "EOS/BUSD",
    "ETC/BUSD",
    "LINK/BUSD",
    "DOT/BUSD",
    "RUNE/BUSD",
    "SUSHI/BUSD",
    "STORJ/BUSD",
    "CRV/BUSD",
    "ENJ/BUSD",
    "SRM/BUSD",
    "AVAX/BUSD",
    "TOMO/BUSD",
    "WAVES/BUSD",
]


Down_group_name = []
Down_group_value = []
result = []


while 1:
    if get_time()[1][2:] != "57":
        time.sleep(25)
        continue

    for i in range(len(ticker_list)):
        try:
            ohlcv = binance.fetch_ohlcv(ticker_list[i], "1h")
            vol = abs(ohlcv[-1][1] - ohlcv[-1][4])
            atr = ATR(ohlcv, 10)[-1]
            gap = vol / atr
            open_ = ohlcv[-1][1]
            high_ = ohlcv[-1][2]
            low_ = ohlcv[-1][3]
            close_ = ohlcv[-1][4]

            if high_ - low_ == 0:
                continue

            IBS = (close_ - low_) / (high_ - low_)

            if ohlcv[-2][1] > ohlcv[-2][4] and gap > 1:
                Down_group_name.append(ticker_list[i])
                Down_group_value.append(IBS)

        except Exception as ex:
            print("err1", ex)
            time.sleep(2)
            continue

    for m in range(len(Down_group_value)):
        if max(Down_group_value) == Down_group_value[m]:
            result.append(Down_group_name[m])
            result.append(Down_group_value[m])
            break

    if len(result) == 0:
        # print('해당없음')
        time.sleep(300)
        result.clear()
        Down_group_name.clear()
        Down_group_value.clear()
        continue

    if result[1] > 0.1:
        # print(result, 'IBS값 초과')
        time.sleep(300)
        result.clear()
        Down_group_name.clear()
        Down_group_value.clear()
        continue

    while True:
        try:
            sell_price = binance.fetch_ohlcv(result[0], "1h")[-2][2]
            trade_order(result[0], sell_price)
            time.sleep(5)
            break
        except:
            time.sleep(5)
            continue

    # print(result)
    time.sleep(300)
    result.clear()
    Down_group_name.clear()
    Down_group_value.clear()

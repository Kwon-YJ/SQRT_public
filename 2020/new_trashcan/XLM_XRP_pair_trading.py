# -*- coding: utf-8 -*-

import ccxt
import time
import datetime
import os
import numpy as np
import pandas as pd


def n11n_maker(ticker):
    ohlcv = binance.fetch_ohlcv(ticker, "1h")
    result = [ohlcv[i][4] for i in range(len(ohlcv))]
    avg_result = sum(result) / len(result)
    std_result = np.std(result)
    n11n_result = [((result[j] - avg_result) / std_result) for j in range(len(result))]
    return n11n_result[-1]


def get_decimal(ticker):
    if ticker == "XRP/USDT":
        return [1, 4]
    else:
        return [0, 5]


def get_amount(ticker):
    price = binance.fetch_ohlcv(ticker)[-1][4]
    today_money_USDT = float(
        binance.fetch_balance()["info"]["assets"][0]["walletBalance"]
    )
    decimal_amount = get_decimal(ticker)[0]
    result = round(today_money_USDT / price * 0.05, decimal_amount)
    return result


def buy_order():
    XRP_amount = get_amount("XRP/USDT")
    XLM_amount = get_amount("XLM/USDT")
    if is_XRP_long == True:
        XRP_side = "buy"
        XLM_side = "sell"
    else:
        XRP_side = "sell"
        XLM_side = "buy"
    order_1 = binance.create_order("XRP/USDT", "market", XRP_side, XRP_amount)
    order_2 = binance.create_order("XLM/USDT", "market", XLM_side, XLM_amount)
    is_entering.append(float(order_1["amount"]))
    is_entering.append(float(order_2["amount"]))


def sell_order():
    XRP_amount = is_entering[0]
    XLM_amount = is_entering[1]
    if is_XRP_long == True:
        XRP_side = "sell"
        XLM_side = "buy"
    else:
        XRP_side = "buy"
        XLM_side = "sell"
    binance.create_order("XRP/USDT", "market", XRP_side, XRP_amount)
    binance.create_order("XLM/USDT", "market", XLM_side, XLM_amount)


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
is_entering = []
# is_entering = [XRP_amount, XLM_amount]

is_XRP_long = None


while True:
    try:
        spread_ = n11n_maker("XRP/USDT") - n11n_maker("XLM/USDT")

        if len(is_entering) == 0:
            if spread_ > 0.91:
                is_XRP_long = False
                buy_order()
            elif spread_ < -0.91:
                is_XRP_long = True
                buy_order()

        else:
            if abs(spread_) < 0.1:
                sell_order()
                is_entering.clear()
                is_XRP_long = None
    except:
        time.sleep(1)
        continue

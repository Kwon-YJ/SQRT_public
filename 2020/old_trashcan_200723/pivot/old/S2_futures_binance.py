import ccxt
import time
import pandas as pd
import os
import datetime
from pprint import pprint


def get_decimal(ticker):
    Group_41 = [
        "XRP/USDT",
        "ONT/USDT",
        "IOTA/USDT",
        "BAT/USDT",
        "THETA/USDT",
        "ALGO/USDT",
    ]
    Group_31 = ["EOS/USDT", "XTZ/USDT", "QTUM/USDT"]
    Group_50 = ["TRX/USDT", "XLM/USDT", "ADA/USDT", "ZIL/USDT", "KNC/USDT"]
    Group_60 = ["VET/USDT", "IOST/USDT"]
    Group_23 = [
        "BTC/USDT",
        "BCH/USDT",
        "ETH/USDT",
        "LTC/USDT",
        "ETC/USDT",
        "XMR/USDT",
        "DASH/USDT",
        "ZEC/USDT",
        "BNB/USDT",
        "ATOM/USDT",
        "NEO/USDT",
    ]

    if any(ticker in i for i in Group_41):
        return 4, 1
    elif any(ticker in i for i in Group_31):
        return 3, 1
    elif any(ticker in i for i in Group_50):
        return 5, 0
    elif any(ticker in i for i in Group_60):
        return 6, 0
    elif any(ticker in i for i in Group_23):
        return 2, 3
    elif ticker == "LINK/USDT":
        return 3, 2


def get_time(temp):
    now = temp
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


def exit_ALL():
    for i in range(len(is_entering)):
        time.sleep(0.7)
        ticker = list(is_entering.keys())[i]
        sell_amount = is_entering[ticker]
        binance.create_order(
            ticker, "market", "sell", sell_amount, None, {"leverage": 10}
        )
    reset = {}
    return reset


def buy_order(ticker):
    wallet_balance = (
        float(binance.fetch_balance()["info"]["assets"][1]["walletBalance"]) - 15
    )
    decimal_amount = get_decimal(ticker)[1]
    amount = round(
        wallet_balance / binance.fetch_ohlcv(ticker)[-1][-4] * 0.25, decimal_amount
    )
    order = binance.create_order(
        ticker, "market", "buy", amount, None, {"leverage": 10}
    )
    is_entering[ticker] = float(order["amount"])
    banList.append(ticker)


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
binance.apiKey = "FRbVseExyAWjQUtYFnS4memLnPCcgNAeRW7HEBrrw9qyIyPUMCTzUKxZKOJIHcfV"
binance.secret = "CbDX3DE5r9ErdLBOphDB4rjCaAaKbUqITbNK05YIitktZ24VfcNrvVRbIgfK6L87"
binance.load_markets()


banList = []
is_entering = {}

ticker_list = [
    "BTC/USDT",
    "ETH/USDT",
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
]


while True:
    try:
        for i, item in enumerate(ticker_list):
            time.sleep(0.5)
            time_ = get_time(datetime.datetime.now())[1]

            if time_ == "0000" or time_ == "0001" or time_ == "0002" or time_ == "0003":
                is_entering = exit_ALL()
                banList = []
                time.sleep(179)

            if item in banList:
                time.sleep(40)
                continue

            if ohlcv[-1][4] < S2:
                buy_order(item)

    except Exception as ex:
        time.sleep(10)
        continue

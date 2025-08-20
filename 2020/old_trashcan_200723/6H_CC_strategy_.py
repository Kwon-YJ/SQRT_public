# -*- coding: utf-8 -*-
import ccxt
import time
import datetime
import pandas as pd
from ccxt.base.decimal_to_precision import *
import os
import csv
import telegram


def convert(ohlcv1H):  # convert 1H → 6H
    ohlcv6H = []
    temp = str(datetime.datetime.fromtimestamp(ohlcv1H[0][0] / 1000))[11:13]
    if int(temp) % 6 != 0:
        for i in range(9 - int(temp) % 6):
            del ohlcv1H[0]
    for i in range(0, len(ohlcv1H) - 5, 6):
        highs = [ohlcv1H[i + j][2] for j in range(0, 6) if ohlcv1H[i + j][2]]
        lows = [ohlcv1H[i + j][3] for j in range(0, 6) if ohlcv1H[i + j][3]]
        candle = [
            ohlcv1H[i + 0][0],
            ohlcv1H[i + 0][1],
            max(highs) if len(highs) else None,
            min(lows) if len(lows) else None,
            ohlcv1H[i + 5][4],
        ]
        ohlcv6H.append(candle)
    return ohlcv6H


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


def ma(data, length):
    result = []
    for i in range(len(data)):
        result.append(data[i][4])
    return pd.Series(result).rolling(length).mean().tolist()


def signal_maker(ticker, i=1):
    ohlcv6H = convert(binance.fetch_ohlcv(ticker, "1h"))
    ma_ = ma(ohlcv6H, 20)
    atr = ATR(ohlcv6H, 20)
    for i in range(20):
        if ohlcv6H[-i][4] > ma_[-i] + 2 * atr[-i]:
            return "buy"
        elif ohlcv6H[-i][4] < ma_[-i] - 2 * atr[-i]:
            return "sell"
    return "NONE"


def order(ticker, side, temp):
    wallet_balance = float(today_money["walletBalance"])
    best_bids_asks = binance.fetch_order_book(ticker)["bids"][1][0]
    amount = float(
        decimal_to_precision(
            str((wallet_balance / best_bids_asks) * 0.056), TRUNCATE, 3, DECIMAL_PLACES
        )
    )
    print(amount)
    order = binance.create_order(
        ticker,
        "limit",
        side,
        (amount + float(ALL_TICKERS[ticker][1])),
        best_bids_asks,
        {"leverage": 1},
    )
    # order = binance.create_order(ticker , 'market', side, (amount + float(ALL_TICKERS[ticker][1])), None, {'leverage': 1})

    f = open(str(os.getcwd()) + "/savedata.csv", "r")
    data = list(csv.reader(f))[0]
    data[temp] = amount
    f.close()

    f = open(str(os.getcwd()) + "/savedata.csv", "w")
    wr = csv.writer(f)
    wr.writerow(data)
    f.close()

    ALL_TICKERS[ticker] = [side, amount]


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

bot = telegram.Bot(token=my_token)

binance.enableRateLimit = True
binance.RateLimit = 10000
binance.apiKey = "7sXg9HiEgjj1pQ91HytSExmtRcx9hKyvQpdN1Gw6COvmexrZ1NTYYdeExyGeAH9i"
binance.secret = "O0Uk4IerJdpQYFmwyyTJKJFUnrFB39mmE2kChWdSDEgYpAQDDtLcjSds4oGcDuza"
binance.load_markets()
today_money = binance.fetch_balance()["info"]["assets"][1]


f = open(str(os.getcwd()) + "/savedata.csv", "r")
data = list(csv.reader(f))[0]

ALL_TICKERS = {
    "BTC/USDT": ["sell", float(data[0])],
    "XTZ/USDT": ["sell", float(data[1])],
    "LINK/USDT": ["sell", float(data[2])],
}

f.close()


try:
    while True:
        if (
            signal_maker("BTC/USDT") != ALL_TICKERS["BTC/USDT"][0]
            and signal_maker("BTC/USDT") != "NONE"
        ):
            print(signal_maker("BTC/USDT"))
            print(ALL_TICKERS["BTC/USDT"])
            order("BTC/USDT", signal_maker("BTC/USDT"), 0)
        elif (
            signal_maker("XTZ/USDT") != ALL_TICKERS["XTZ/USDT"][0]
            and signal_maker("XTZ/USDT") != "NONE"
        ):
            print(signal_maker("XTZ/USDT"))
            order("XTZ/USDT", signal_maker("XTZ/USDT"), 1)
        elif (
            signal_maker("LINK/USDT") != ALL_TICKERS["LINK/USDT"][0]
            and signal_maker("LINK/USDT") != "NONE"
        ):
            order("LINK/USDT", signal_maker("LINK/USDT"), 2)
        time.sleep(50)
except Exception as ex:
    bot.send_message(chat_id=801167350, text=str(ex))

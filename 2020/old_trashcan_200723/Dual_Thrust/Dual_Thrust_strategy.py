# -*- coding: utf-8 -*-
import ccxt
import time
import datetime
import pandas as pd
import os
import csv
import telegram
from pprint import pprint


def get_decimal(ticker):
    Group_14 = ["XRP/USDT", "ONT/USDT", "IOTA/USDT", "BAT/USDT"]
    Group_13 = ["EOS/USDT", "XTZ/USDT", "QTUM/USDT"]
    Group_05 = ["TRX/USDT", "XLM/USDT", "ADA/USDT"]
    Group_06 = ["VET/USDT", "IOST/USDT"]

    if any(ticker in i for i in Group_14):
        return 1, 4
    elif any(ticker in i for i in Group_13):
        return 1, 3
    elif any(ticker in i for i in Group_05):
        return 0, 5
    elif any(ticker in i for i in Group_06):
        return 0, 6
    elif ticker == "LINK/USDT":
        return 2, 3
    else:
        return 3, 2


def Csv_init():
    with open(str(os.getcwd()) + "/savedata3.csv", "w", newline="") as file:
        writer = csv.writer(file)
        tickers = list(binance.fetch_tickers().keys())
        writer.writerow(tickers)
        writer.writerow([SignalMaker(tickers[x]) for x in range(24)])
        writer.writerow([0 for i in range(24)])


def CsvRead():
    with open(str(os.getcwd()) + "/savedata3.csv", "r", newline="") as file:
        Result = list(csv.reader(file))
    return Result


def CsvWrite(side, amount, temp):
    with open(str(os.getcwd()) + "/savedata3.csv", "w", newline="") as file:
        ALL_TICKERS[1][temp] = side
        ALL_TICKERS[2][temp] = amount
        writer = csv.writer(file)
        writer.writerow(ALL_TICKERS[0])
        writer.writerow(ALL_TICKERS[1])
        writer.writerow(ALL_TICKERS[2])


def SignalMaker(ticker, i=2):
    ohlcv = binance.fetch_ohlcv(ticker, "1d")
    while True:
        HH = max(ohlcv[-i][2], ohlcv[-i - 1][2], ohlcv[-i - 2][2], ohlcv[-i - 3][2])
        HC = max(ohlcv[-i][4], ohlcv[-i - 1][4], ohlcv[-i - 2][4], ohlcv[-i - 3][4])
        LC = min(ohlcv[-i][4], ohlcv[-i - 1][4], ohlcv[-i - 2][4], ohlcv[-i - 3][4])
        LL = min(ohlcv[-i][3], ohlcv[-i - 1][3], ohlcv[-i - 2][3], ohlcv[-i - 3][3])
        if ohlcv[-i][4] > ohlcv[-i][1] + (max(HH - LC, HC - LL) * 0.55):
            return "buy"
        elif ohlcv[-i][4] < ohlcv[-i][1] - (max(HH - LC, HC - LL) * 0.55):
            return "sell"
        else:
            i = i + 1
            continue


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


def order(ticker, side, temp):
    wallet_balance = float(
        binance.fetch_balance()["info"]["assets"][1]["walletBalance"]
    )
    decimal_amount = get_decimal(ticker)[0]
    amount = round(
        wallet_balance / binance.fetch_ohlcv(ticker)[-1][-4] * 0.05, decimal_amount
    )
    order = binance.create_order(
        ticker,
        "market",
        side,
        (amount + float(ALL_TICKERS[2][temp])),
        None,
        {"leverage": 1},
    )
    CsvWrite(side, float(order["amount"]) - float(ALL_TICKERS[2][temp]), temp)


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
binance.apiKey = "FRbVseExyAWjQUtYFnS4memLnPCcgNAeRW7HEBrrw9qyIyPUMCTzUKxZKOJIHcfV"
binance.secret = "CbDX3DE5r9ErdLBOphDB4rjCaAaKbUqITbNK05YIitktZ24VfcNrvVRbIgfK6L87"
binance.load_markets()
tickers = list(binance.fetch_tickers().keys())
ALL_TICKERS = CsvRead()

# Main
while True:
    start = get_time(datetime.datetime.now())[1]
    if start == "1500" or start == "1501":
        try:
            for i in range(24):
                temp = SignalMaker(tickers[i])
                if temp != ALL_TICKERS[1][i]:
                    order(tickers[i], temp, i)
                    ALL_TICKERS = CsvRead()
        except Exception as ex:
            bot.send_message(chat_id=801167350, text=tickers[i] + str(ex))
            continue
    time.sleep(50)

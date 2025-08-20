# -*- coding: utf-8 -*-
from pykrx import stock
import time
from datetime import datetime
from pprint import pprint


def day_ago(day, ohlcv, ticker):
    a = ticker.tail(day)
    b = a[ohlcv]
    c = b.head(1)
    return c


def get_TR(date, ticker):
    a = day_ago(date, "고가", ticker)
    b = day_ago(date, "저가", ticker)
    c = a.values - b.values

    aa = day_ago(date, "고가", ticker)
    bb = day_ago(date + 1, "종가", ticker)
    cc = abs(aa.values - bb.values)

    aaa = day_ago(date, "저가", ticker)
    bbb = day_ago(date + 1, "종가", ticker)
    ccc = abs(aaa.values - bbb.values)

    return max(c, cc, ccc)


def get_ATR(ticker):
    value = 0
    for i in range(15):
        TR = get_TR(i + 2, ticker)
        value = value + TR
    return value / 15


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


tickers = [
    "207940",
    "003230",
    "037070",
    "000080",
    "336370",
    "058470",
    "083450",
    "002840",
]

Result = {}
sell_list = []
now = datetime.now()
Today = get_time(now)[0]

for ticker in tickers:
    time.sleep(4)
    df = stock.get_market_ohlcv_by_date("20190101", Today, ticker)
    name = stock.get_market_ticker_name(ticker)
    ATR = float(get_ATR(df)[0])
    target = float(max(df["종가"])) - (3 * ATR)

    Result[name] = target

    if df.iloc[-1]["종가"] < target:
        sell_list.append(name)


pprint(Result)
print("")

if len(sell_list) == 0:
    print("매도 종목 없음")
else:
    print("매도 종목 :", sell_list)

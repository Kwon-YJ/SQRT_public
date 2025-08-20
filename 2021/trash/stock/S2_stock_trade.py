# -*- coding: utf-8 -*-

from pykrx import stock
import time
import datetime
import numpy as np
import parmap
import pandas as pd
from tabulate import tabulate


def get_time(days=0):
    now = datetime.datetime.now() - datetime.timedelta(days=days)
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


def target_maker(ticker):
    return "pass"


def validation(key_value_pair):
    ticker, target_price = key_value_pair
    try:
        df = stock.get_market_ohlcv_by_date(D_5, Today, ticker)
        live_price = df.iloc[-1]["종가"]
        if live_price < target_price:
            return ticker
    except Exception as e:
        time.sleep(0.5)
        print(f"{ticker} \n{e}")
    return "pass"


# 005930
if __name__ == "__main__":
    global Today
    global D_5

    Today = get_time(0)[0]
    D_5 = get_time(5)[0]

    konex = stock.get_market_ticker_list(market="KONEX")
    tickers = list(set(stock.get_market_ticker_list(market="ALL")) - set(konex))

    targets = parmap.map(target_maker, tickers, pm_pbar=True, pm_processes=8)
    targets = [ticker for ticker in targets if ticker != "pass"]

    validate = parmap.map(validation, targets, pm_pbar=True, pm_processes=8)
    validate = [ticker for ticker in validate if ticker != "pass"]

    # print(validate)

    print([stock.get_market_ticker_name(ticker) for ticker in validate])


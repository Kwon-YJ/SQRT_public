# -*- coding: utf-8 -*-

from pykrx import stock
import time

# from datetime import datetime
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


def Result_output(ticker):
    return "pass"


if __name__ == "__main__":
    global Today
    global D_10

    Today = get_time(0)[0]
    D_10 = get_time(10)[0]

    konex = stock.get_market_ticker_list(market="KONEX")
    tickers = list(set(stock.get_market_ticker_list(market="ALL")) - set(konex))
    result_ = parmap.map(Result_output, tickers, pm_pbar=True, pm_processes=8)

    while 1:
        try:
            result_.remove("pass")
        except:
            break

    print(result_)

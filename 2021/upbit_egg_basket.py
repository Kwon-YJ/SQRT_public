import ccxt
import time
import os
import numpy as np
import pandas as pd
import datetime
import pandas_ta as ta
from all_func import send_MSG


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


def buy_order():
    ticker_list = list(upbit.fetch_tickers().keys())
    ticker_list = [
        ticker_list[s] for s in range(len(ticker_list)) if "/KRW" in ticker_list[s]
    ]
    for ticker in ticker_list:
        price = upbit.fetch_order_book(ticker)["asks"][0][0]
        buy_amount = 9000 / price
        order = upbit.create_order(ticker, "limit", "buy", buy_amount, price)
        # is_entering[ticker] = round(float(order['info']['volume']) * 0.99995, 7)


def sell_order():
    total_data = upbit.fetch_balance()["total"]
    ticker_list = list(set(total_data.keys()) - set(["KRW"]))
    for ticker in ticker_list:
        sell_amount = float(total_data[ticker])
        price = upbit.fetch_order_book(ticker)["bids"][0][0]
        order = upbit.create_order(ticker, "limit", "sell", sell_amount, price)


upbit = ccxt.upbit(
    {
        # "options": {"defaultType": "future"},
        "timeout": 30000,
        "apiKey": "xuTwrDh8DG0pXJNT0mGkkqFCA8kA7CA09QZ7qKMQ",
        "secret": "ntpBwLjtMCh9uA9W9CUKmyITQSgUL50xiJ5pti9Y",
        "enableRateLimit": True,
    }
)
upbit.load_markets()

while True:
    a = get_time()[1]
    if a == "0530":
        break
    time.sleep(25)

buy_order()

time.sleep(36000)

sell_order()

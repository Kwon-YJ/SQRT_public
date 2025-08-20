import ccxt
import time
import os
import numpy as np
import pandas as pd
import datetime
import pandas_ta as ta
import os


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


def buy_order(ticker):
    price = upbit.fetch_order_book(ticker)["asks"][0][0]
    buy_amount = 6000 / price
    order = upbit.create_order(ticker, "limit", "buy", buy_amount, price)
    is_entering[ticker] = round(float(order["info"]["volume"]) * 0.99995, 7)


def custom_convert(ohlcv5):  # convert 5m → 15m
    ohlcv15 = []
    temp = str(datetime.datetime.fromtimestamp(ohlcv5[0][0] / 1000))[14:16]
    if int(temp) % 15 == 5:
        del ohlcv5[0]
        del ohlcv5[1]
    elif int(temp) % 15 == 10:
        del ohlcv5[0]
    for i in range(0, len(ohlcv5) - 2, 3):
        highs = [ohlcv5[i + j][2] for j in range(0, 3) if ohlcv5[i + j][2]]
        lows = [ohlcv5[i + j][3] for j in range(0, 3) if ohlcv5[i + j][3]]
        candle = [
            ohlcv5[i + 0][0],
            ohlcv5[i + 0][1],
            max(highs) if len(highs) else None,
            min(lows) if len(lows) else None,
            ohlcv5[i + 2][4],
        ]
        ohlcv15.append(candle)
    return ohlcv15


def get_ticker_list():

    temp_list = list(upbit.fetch_tickers().keys())
    temp_list = [temp_list[i] for i in range(len(temp_list)) if "/KRW" in temp_list[i]]
    std_time_data = upbit.fetch_ohlcv("BTC/KRW", "1d")[-1][0]
    result_ = []
    for i in range(len(temp_list)):
        time.sleep(0.5)
        try:
            if (
                upbit.fetch_ohlcv(temp_list[i], "1d")[-1][0] == std_time_data
                and len(upbit.fetch_ohlcv(temp_list[i], "1d")) > 15
            ):
                result_.append(temp_list[i])
        except:
            time.sleep(5)
            continue

    return result_


exchange_class = getattr(ccxt, "upbit")
upbit = exchange_class()
upbit.enableRateLimit = True
upbit.RateLimit = 10000
upbit.apiKey = "c4GbrDjW4yMFSxgopAZBlnKtPpxtfPC1MrxUjvLa"
upbit.secret = "xV3nkV6Jk2xvxYyg5DsXATVq8nf33maYEuNI2rzR"
upbit.load_markets()


is_entering = {}


"""
while(1):
    time.sleep(3)
    time_ = get_time()[1][2:]
    if int(time_) % 15 == 0:
        break
    else:
        time.sleep(27)
"""


while 1:
    temp = []
    ticker_list = get_ticker_list()

    for idx, item in enumerate(ticker_list):
        time.sleep(0.5)
        ohlcv_temp = custom_convert(upbit.fetch_ohlcv(item, "5m"))
        df = pd.DataFrame(
            data=np.array(ohlcv_temp), columns=["0", "0", "close", "0", "0"]
        )  ## rsi(10, high)
        rsi_entry = df.ta.rsi(length=10).tolist()
        if rsi_entry[-1] < 19 and item not in list(is_entering.keys()):
            if upbit.fetch_order_book(item)["asks"][1][0] < ohlcv_temp[-1][4]:
                buy_order(item)

    for i in range(len(is_entering)):
        time.sleep(0.5)

        ticker = list(is_entering.keys())[i]

        ohlcv_temp = custom_convert(upbit.fetch_ohlcv(item, "5m"))
        df = pd.DataFrame(
            data=np.array(ohlcv_temp), columns=["0", "0", "0", "close", "0"]
        )  ## rsi(5, low)
        rsi_exit = df.ta.rsi(length=5).tolist()

        if rsi_exit[-1] > 38:
            sell_amount = is_entering[ticker]
            upbit.create_order(
                ticker,
                "limit",
                "sell",
                sell_amount,
                upbit.fetch_order_book(ticker)["bids"][0][0],
            )
            temp.append(ticker)

    for i in range(len(temp)):
        del is_entering[temp[i]]

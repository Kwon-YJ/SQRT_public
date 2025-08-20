# -*- coding: utf-8 -*-
import ccxt
import time
import datetime
import pybithumb
import sys
from random import *


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


def get_amount(ticker):
    price = pybithumb.get_current_price(ticker)
    return (today_money * 0.005) / price


def buy_order(ticker):
    buy_amount = get_amount(ticker)
    bithumb.buy_market_order(ticker, buy_amount)
    is_entering[ticker] = buy_amount * 0.9995


def buy_side(ticker):
    while True:
        try:
            R_num = uniform(1.0, 20.0)
            time.sleep(R_num)

            time1 = get_time(datetime.datetime.now())[0]
            ohlcv = pybithumb.get_candlestick(ticker).tail(2)
            D_1 = ohlcv.iloc[0]
            PP = (D_1["high"] + D_1["low"] + (2 * D_1["close"])) / 4
            R1 = 2 * PP - D_1["low"]

            temp_price = pybithumb.get_current_price(ticker)

            if temp_price > R1:
                # buy_order(ticker)
                return None

            if time1 == "0010":
                sys.exit()

        except:
            time.sleep(1.5)
            continue


def sell_side(ticker):
    while True:
        try:
            time.sleep(5)

            time1 = get_time(datetime.datetime.now())[0]
            ohlcv = pybithumb.get_candlestick(ticker).tail(2)
            D_1 = ohlcv.iloc[0]
            PP = (D_1["high"] + D_1["low"] + (2 * D_1["close"])) / 4

            R2 = PP + D_1["high"] - D_1["low"]

            temp_price = pybithumb.get_current_price(ticker)

            if temp_price > R2 or time1 == "0010":
                R_num = uniform(1.0, 30.0)
                time.sleep(R_num)
                sell_amount = is_entering[ticker]
                # bithumb.sell_market_order(ticker, sell_amount)
                return None

        except:
            time.sleep(1.5)
            continue


def standby():
    R_num = uniform(5.0, 89.0)
    time.sleep(R_num)
    return None
    """
    while(True):
        R_num = uniform(5.0, 89.0)
        time.sleep(R_num)
        time1 = get_time(datetime.datetime.now())[0]
        if time1 == '0001' or time1 == '0002' or time1 == '0003':
            return None
    """


exchange_class = getattr(ccxt, "bithumb")
bithumb2 = exchange_class()
bithumb2.enableRateLimit = True
bithumb2.RateLimit = 10000
bithumb2.apiKey = "06a2eaefc7956173bbd9f7b47c850786"
bithumb2.secret = "322d44201a7894e3cc2c64cadad673c0"
bithumb2.load_markets()


con_key = "06a2eaefc7956173bbd9f7b47c850786"
sec_key = "322d44201a7894e3cc2c64cadad673c0"
bithumb = pybithumb.Bithumb(con_key, sec_key)

today_money = float(bithumb2.fetch_balance()["info"]["data"]["total_krw"])
is_entering = {}

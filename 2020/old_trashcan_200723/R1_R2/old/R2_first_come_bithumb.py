# -*- coding: utf-8 -*-
import ccxt
import time
import datetime
import pybithumb


def get_amount(ticker):
    price = pybithumb.get_current_price(ticker)
    return (today_money * 0.005) / price


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


def buy_order(ticker):
    buy_amount = get_amount(ticker)
    bithumb.buy_market_order(ticker, buy_amount)
    is_entering[ticker] = buy_amount * 0.9995


def buy_side():
    while True:
        for i, item in enumerate(ticker_list):
            try:
                time.sleep(0.1)
                ohlcv = pybithumb.get_candlestick(item).tail(2)
                D_1 = ohlcv.iloc[0]
                D_day = ohlcv.iloc[1]
                PP = (D_1["high"] + D_1["low"] + (2 * D_1["close"])) / 4
                R1 = 2 * PP - D_1["low"]

                temp_price = pybithumb.get_current_price(item)

                if temp_price > R1:
                    buy_order(item)
                    return None

            except Exception as ex:
                print(item)
                print(ex)
                time.sleep(3)
                continue


def sell_side():
    while True:
        try:
            time.sleep(0.1)

            ticker = list(is_entering.keys())[0]

            ohlcv = pybithumb.get_candlestick(ticker).tail(2)
            D_1 = ohlcv.iloc[0]
            D_day = ohlcv.iloc[1]
            PP = (D_1["high"] + D_1["low"] + (2 * D_1["close"])) / 4

            R2 = PP + D_1["high"] - D_1["low"]

            temp_price = pybithumb.get_current_price(ticker)

            if temp_price > R2 or temp_price < PP:
                sell_amount = is_entering[ticker]
                bithumb.sell_market_order(ticker, sell_amount)
                return None

        except Exception as ex:
            time.sleep(3)
            print(ticker)
            print(ex)
            continue


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


ticker_list = pybithumb.get_tickers()
today_money = float(bithumb2.fetch_balance()["info"]["data"]["total_krw"])
is_entering = {}


# R2를 돌파하는 종목을 R3에 팔기 1일 1종목 선착순

while True:
    time1 = get_time(datetime.datetime.now())[0]

    buy_side()
    sell_side()
    is_entering = {}

    while True:
        time2 = get_time(datetime.datetime.now())[0]
        if time1 == time2:
            time.sleep(180)
            continue
        else:
            break

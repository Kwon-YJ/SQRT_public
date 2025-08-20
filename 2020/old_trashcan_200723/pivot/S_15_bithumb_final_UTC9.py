# -*- coding: utf-8 -*-
import ccxt
import time
import datetime
import pybithumb


def get_amount(ticker):
    price = pybithumb.get_current_price(ticker)
    return (today_money * 0.03) / price


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
        ticker = list(is_entering.keys())[i]
        sell_amount = is_entering[ticker]
        bithumb.sell_market_order(ticker, sell_amount)
    reset = {}
    return reset


def buy_order(ticker):
    buy_amount = get_amount(ticker)
    bithumb.buy_market_order(ticker, buy_amount)
    is_entering[ticker] = buy_amount * 0.9995
    banList.append(ticker)


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
banList = []
is_entering = {}


while True:
    for i, item in enumerate(ticker_list):
        try:
            time_ = get_time(datetime.datetime.now())[1]

            if time_ == "2359":
                is_entering = exit_ALL()
                banList = []
                today_money = float(
                    bithumb2.fetch_balance()["info"]["data"]["total_krw"]
                )
                ticker_list = pybithumb.get_tickers()
                time.sleep(600)

            if len(is_entering) == 6:
                time.sleep(25)
                continue

            time.sleep(0.2)

            ohlcv = pybithumb.get_candlestick(item).tail(2)
            D_1 = ohlcv.iloc[0]
            D_day = ohlcv.iloc[1]
            PP = (D_1["high"] + D_1["low"] + (2 * D_1["close"])) / 4
            S1_5 = 1.97 * PP - D_1["high"]

            if D_day["close"] < S1_5 and item not in banList:
                buy_order(item)

        except Exception as ex:
            time.sleep(3)
            continue

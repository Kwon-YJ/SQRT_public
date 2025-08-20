# -*- coding: utf-8 -*-
import ccxt
import time
import datetime
import pybithumb


def get_amount(ticker):
    price = pybithumb.get_current_price(ticker)
    return (today_money * 0.1) / price


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
temp_list = []


while True:
    for i, item in enumerate(ticker_list):
        try:
            time.sleep(0.1)
            ohlcv = pybithumb.get_candlestick(item).tail(1)
            temp = round((float(ohlcv["high"] / ohlcv["open"] - 1)) * 100, 3)
            if temp < 19.9:
                continue

            IBS0382 = 0.382 * float(ohlcv["high"]) + 0.618 * float(ohlcv["low"])

            if float(ohlcv["close"]) < IBS0382 and item not in banList:
                buy_order(item)

        except Exception as ex:
            time.sleep(3)
            print(item)
            print(ex)
            continue

    for i in range(len(is_entering)):
        try:
            ticker = list(is_entering.keys())[i]
            ohlcv = pybithumb.get_candlestick(ticker).tail(1)
            IBS0382 = 0.382 * float(ohlcv["high"]) + 0.618 * float(ohlcv["low"])

            if float(ohlcv["close"]) > IBS0382 * 1.01:
                sell_amount = is_entering[ticker]
                bithumb.sell_market_order(ticker, sell_amount)
                temp_list.append(ticker)

        except Exception as ex:
            time.sleep(3)
            print(item)
            print(ex)
            continue

    for k in range(len(temp_list)):
        del is_entering[temp_list[k]]
    temp_list.clear()

    time_ = get_time(datetime.datetime.now())[1]
    if time_ == "2359":
        is_entering = exit_ALL()
        banList = []
        today_money = float(bithumb2.fetch_balance()["info"]["data"]["total_krw"])
        time.sleep(240)

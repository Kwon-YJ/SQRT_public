# -*- coding: utf-8 -*-

import ccxt
import time
import datetime

# import urllib.request
# import json

"""
def get_funding_rate(ticker):
    ticker = ticker[:-5] + 'USDT'
    EndPoint = len(binance.fetch_tickers().keys())
    url = 'https://fapi.binance.com/fapi/v1/premiumIndex'
    text_data = urllib.request.urlopen(url).read().decode('utf-8')
    tickers = json.loads(text_data)
    All_funding_rate = {}
    for i in range(EndPoint):
        All_funding_rate[tickers[i]['symbol']] = abs(float(tickers[i]['lastFundingRate']))
    return All_funding_rate[ticker]
"""


def get_decimal(ticker):
    Group_14 = [
        "XRP/USDT",
        "ONT/USDT",
        "IOTA/USDT",
        "BAT/USDT",
        "LEND/USDT",
        "SXP/USDT",
        "OMG/USDT",
        "ZRX/USDT",
        "ALGO/USDT",
        "THETA/USDT",
        "KAVA/USDT",
        "BAND/USDT",
        "RLC/USDT",
        "WAVES/USDT",
    ]
    Group_13 = [
        "EOS/USDT",
        "XTZ/USDT",
        "QTUM/USDT",
        "SNX/USDT",
        "DOT/USDT",
        "BAL/USDT",
        "CRV/USDT",
        "TRB/USDT",
    ]
    Group_05 = [
        "TRX/USDT",
        "XLM/USDT",
        "ADA/USDT",
        "KNC/USDT",
        "ZIL/USDT",
        "RUNE/USDT",
        "SUSHI/USDT",
        "SRM/USDT",
        "BZRX/USDT",
    ]
    Group_06 = ["VET/USDT", "IOST/USDT", "DOGE/USDT"]

    if any(ticker in i for i in Group_14):
        return 1, 4
    elif any(ticker in i for i in Group_13):
        return 1, 3
    elif any(ticker in i for i in Group_05):
        return 0, 5
    elif any(ticker in i for i in Group_06):
        return 0, 6
    elif ticker == "LINK/USDT" or ticker == "COMP/USDT":
        return 2, 3
    elif ticker == "DEFI/USDT" or "YFI/USDT" or "YFII/USDT":
        return 3, 1
    else:  # MKR/USDT, others...
        return 3, 2


def get_amount(ticker):
    price = binance.fetch_ohlcv(ticker)[-1][4]
    today_money_USDT = float(
        binance.fetch_balance()["info"]["assets"][0]["walletBalance"]
    )
    decimal_amount = get_decimal(ticker)[0]
    result = round(today_money_USDT / price * 0.01, decimal_amount)
    return result


def buy_order(ticker, sell_price):
    buy_amount = get_amount(ticker)
    order = binance.create_order(ticker, "market", "sell", buy_amount)
    case = is_full_count(ticker)[1]
    if case == 1:
        is_entering1[ticker] = [float(order["amount"]), sell_price]

    if case == 2:
        is_entering2[ticker] = [float(order["amount"]), sell_price]

    if case == 3:
        is_entering3[ticker] = [float(order["amount"]), sell_price]

    if case == 4:
        is_entering4[ticker] = [float(order["amount"]), sell_price]

    if case == 5:
        is_entering5[ticker] = [float(order["amount"]), sell_price]

    if case == 6:
        is_entering6[ticker] = [float(order["amount"]), sell_price]

    if case == 7:
        is_entering7[ticker] = [float(order["amount"]), sell_price]

    if case == 8:
        is_entering8[ticker] = [float(order["amount"]), sell_price]

    if case == 9:
        is_entering9[ticker] = [float(order["amount"]), sell_price]

    if case == 10:
        is_entering10[ticker] = [float(order["amount"]), sell_price]


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

binance.enableRateLimit = True
binance.RateLimit = 10000
binance.load_markets()
is_entering1 = {}
is_entering2 = {}
is_entering3 = {}
is_entering4 = {}
is_entering5 = {}
is_entering6 = {}
is_entering7 = {}
is_entering8 = {}
is_entering9 = {}
is_entering10 = {}


def is_full_count(ticker):
    if item not in list(is_entering1.keys()):
        return [True, 1]
    if item not in list(is_entering2.keys()):
        return [True, 2]
    if item not in list(is_entering3.keys()):
        return [True, 3]
    if item not in list(is_entering4.keys()):
        return [True, 4]
    if item not in list(is_entering5.keys()):
        return [True, 5]
    if item not in list(is_entering6.keys()):
        return [True, 6]
    if item not in list(is_entering7.keys()):
        return [True, 7]
    if item not in list(is_entering8.keys()):
        return [True, 8]
    if item not in list(is_entering9.keys()):
        return [True, 9]
    if item not in list(is_entering10.keys()):
        return [True, 10]
    return False


ticker_list = [
    "BTC/USDT",
    "ETH/USDT",
    "BCH/USDT",
    "XRP/USDT",
    "XLM/USDT",
    "EOS/USDT",
    "LTC/USDT",
    "ETC/USDT",
    "XMR/USDT",
    "DASH/USDT",
    "ZEC/USDT",
    "BAT/USDT",
    "NEO/USDT",
    "DOGE/USDT",
]

print(list(binance.fetch_tickers().keys()))

exit()

while 1:
    time_ = get_time()[1][2:]
    if time_ == "00":
        break
    else:
        time.sleep(27)

while True:
    time_ = get_time()[1][2:]
    if time_ == "00":
        for i, item in enumerate(ticker_list):
            try:
                ohlcv = binance.fetch_ohlcv(item, "1h")
                open_ = ohlcv[-2][1]
                high_ = ohlcv[-2][2]
                low_ = ohlcv[-2][3]
                close_ = ohlcv[-2][4]
                if high_ - low_ == 0:
                    continue
                IBS = (close_ - low_) / (high_ - low_)
                if IBS >= 0.94 and is_full_count(item)[0] == True:
                    buy_order(item, low_ * 0.99855)
            except Exception as e:
                print(e, "line185")
                time.sleep(1)
                continue
        time.sleep(59)

    temp = []
    for i in range(len(is_entering1)):
        try:
            ticker = list(is_entering1.keys())[i]
            now_price = binance.fetch_ohlcv(ticker, "1h")[-1][4]
            sell_price = is_entering1[ticker][1]
            if sell_price > now_price:
                sell_amount = is_entering1[ticker][0]
                binance.create_order(ticker, "market", "buy", sell_amount)
                temp.append(ticker)
        except Exception as e:
            print(e, "line203")
            continue
    for i in range(len(temp)):
        del is_entering1[temp[i]]

    temp = []
    for i in range(len(is_entering2)):
        try:
            ticker = list(is_entering2.keys())[i]
            now_price = binance.fetch_ohlcv(ticker, "1h")[-1][4]
            sell_price = is_entering2[ticker][1]
            if sell_price > now_price:
                sell_amount = is_entering2[ticker][0]
                binance.create_order(ticker, "market", "buy", sell_amount)
                temp.append(ticker)
        except Exception as e:
            print(e, "line221")
            time.sleep(0.2)
            continue
    for i in range(len(temp)):
        del is_entering2[temp[i]]

    temp = []
    for i in range(len(is_entering3)):
        try:
            ticker = list(is_entering3.keys())[i]
            now_price = binance.fetch_ohlcv(ticker, "1h")[-1][4]
            sell_price = is_entering3[ticker][1]
            if sell_price > now_price:
                sell_amount = is_entering3[ticker][0]
                binance.create_order(ticker, "market", "buy", sell_amount)
                temp.append(ticker)
        except Exception as e:
            print(e, "line240")
            continue
    for i in range(len(temp)):
        del is_entering3[temp[i]]

    temp = []
    for i in range(len(is_entering4)):
        try:
            ticker = list(is_entering4.keys())[i]
            now_price = binance.fetch_ohlcv(ticker, "1h")[-1][4]
            sell_price = is_entering4[ticker][1]
            if sell_price > now_price:
                sell_amount = is_entering4[ticker][0]
                binance.create_order(ticker, "market", "buy", sell_amount)
                temp.append(ticker)
        except Exception as e:
            print(e, "line257")
            time.sleep(0.2)
            continue
    for i in range(len(temp)):
        del is_entering4[temp[i]]

    temp = []
    for i in range(len(is_entering5)):
        try:
            ticker = list(is_entering5.keys())[i]
            now_price = binance.fetch_ohlcv(ticker, "1h")[-1][4]
            sell_price = is_entering5[ticker][1]
            if sell_price > now_price:
                sell_amount = is_entering5[ticker][0]
                binance.create_order(ticker, "market", "buy", sell_amount)
                temp.append(ticker)
        except Exception as e:
            print(e, "line275")
            time.sleep(0.2)
            continue
    for i in range(len(temp)):
        del is_entering5[temp[i]]

    temp = []
    for i in range(len(is_entering6)):
        try:
            ticker = list(is_entering6.keys())[i]
            now_price = binance.fetch_ohlcv(ticker, "1h")[-1][4]
            sell_price = is_entering6[ticker][1]
            if sell_price > now_price:
                sell_amount = is_entering6[ticker][0]
                binance.create_order(ticker, "market", "buy", sell_amount)
                temp.append(ticker)
        except Exception as e:
            print(e, "line293")
            continue
    for i in range(len(temp)):
        del is_entering6[temp[i]]

    temp = []
    for i in range(len(is_entering7)):
        try:
            ticker = list(is_entering7.keys())[i]
            now_price = binance.fetch_ohlcv(ticker, "1h")[-1][4]
            sell_price = is_entering7[ticker][1]
            if sell_price > now_price:
                sell_amount = is_entering7[ticker][0]
                binance.create_order(ticker, "market", "buy", sell_amount)
                temp.append(ticker)
        except Exception as e:
            print(e, "line309")
            continue
    for i in range(len(temp)):
        del is_entering7[temp[i]]

    temp = []
    for i in range(len(is_entering8)):
        try:
            ticker = list(is_entering8.keys())[i]
            now_price = binance.fetch_ohlcv(ticker, "1h")[-1][4]
            sell_price = is_entering8[ticker][1]
            if sell_price > now_price:
                sell_amount = is_entering8[ticker][0]
                binance.create_order(ticker, "market", "buy", sell_amount)
                temp.append(ticker)
        except Exception as e:
            print(e, "line326")
            time.sleep(0.2)
            continue
    for i in range(len(temp)):
        del is_entering8[temp[i]]

    temp = []
    for i in range(len(is_entering9)):
        try:
            ticker = list(is_entering9.keys())[i]
            now_price = binance.fetch_ohlcv(ticker, "1h")[-1][4]
            sell_price = is_entering9[ticker][1]
            if sell_price > now_price:
                sell_amount = is_entering9[ticker][0]
                binance.create_order(ticker, "market", "buy", sell_amount)
                temp.append(ticker)
        except Exception as e:
            print(e, "line344")
            time.sleep(0.2)
            continue
    for i in range(len(temp)):
        del is_entering9[temp[i]]

    temp = []
    for i in range(len(is_entering10)):
        try:
            ticker = list(is_entering10.keys())[i]
            now_price = binance.fetch_ohlcv(ticker, "1h")[-1][4]
            sell_price = is_entering10[ticker][1]
            if sell_price > now_price:
                sell_amount = is_entering10[ticker][0]
                binance.create_order(ticker, "market", "buy", sell_amount)
                temp.append(ticker)
        except Exception as e:
            print(e, "line362")
            time.sleep(0.2)
            continue
    for i in range(len(temp)):
        del is_entering10[temp[i]]

    time.sleep(0.2)

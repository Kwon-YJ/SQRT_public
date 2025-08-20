# -*- coding: utf-8 -*-

import ccxt
import time
import datetime
import urllib.request
import json


def get_funding_rate():
    url = "https://fapi.binance.com/fapi/v1/premiumIndex"
    text_data = urllib.request.urlopen(url).read().decode("utf-8")
    tickers = json.loads(text_data)
    EndPoint = len(tickers)
    All_funding_rate = {}
    for i in range(EndPoint):
        funding_rate = float(tickers[i]["lastFundingRate"])
        if funding_rate <= 0.0001:
            ticker = tickers[i]["symbol"][:-4] + "/USDT"
            if ticker in ticker_list:
                All_funding_rate[ticker] = float(tickers[i]["lastFundingRate"])
    time_diff = (
        float(tickers[0]["nextFundingTime"]) - float(tickers[0]["time"])
    ) / 1000
    return All_funding_rate, time_diff


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
    today_money_USDT = (
        float(binance.fetch_balance()["info"]["assets"][0]["walletBalance"]) * 0.8
    )
    decimal_amount = get_decimal(ticker)[0]
    result = round(today_money_USDT / price / global_num, decimal_amount)
    return result


def entry_order(ticker, fees, side):
    buy_amount = get_amount(ticker)
    order = binance.create_order(ticker, "market", side, buy_amount)
    is_entering[ticker] = [float(order["amount"]), fees]


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
is_entering = {}

ticker_list = [
    "BTC/USDT",
    "ETH/USDT",
    "BCH/USDT",
    "XRP/USDT",
    "XLM/USDT",
    "EOS/USDT",
    "LTC/USDT",
    "TRX/USDT",
    "ETC/USDT",
    "LINK/USDT",
    "ADA/USDT",
    "XMR/USDT",
    "DASH/USDT",
    "ZEC/USDT",
    "XTZ/USDT",
    "BNB/USDT",
    "ATOM/USDT",
    "ONT/USDT",
    "IOTA/USDT",
    "BAT/USDT",
    "VET/USDT",
    "NEO/USDT",
    "QTUM/USDT",
    "IOST/USDT",
    "THETA/USDT",
    "ALGO/USDT",
    "ZIL/USDT",
    "KNC/USDT",
    "ZRX/USDT",
    "COMP/USDT",
    "OMG/USDT",
    "DOGE/USDT",
    "SXP/USDT",
    "LEND/USDT",
    "KAVA/USDT",
    "BAND/USDT",
    "RLC/USDT",
    "WAVES/USDT",
    "MKR/USDT",
    "SNX/USDT",
    "DOT/USDT",
    "DEFI/USDT",
    "YFI/USDT",
    "BAL/USDT",
    "CRV/USDT",
    "TRB/USDT",
    "YFII/USDT",
    "RUNE/USDT",
    "SUSHI/USDT",
    "SRM/USDT",
    "BZRX/USDT",
]

global_num = 0

funding_fee, time_ = get_funding_rate()

while True:
    time.sleep(11)
    funding_fee, time_ = get_funding_rate()
    if time_ < 50:
        exit_list = []
        contains_next_case = list(set(is_entering.keys()) & set(funding_fee.keys()))

        for key_, value_ in is_entering.items():
            try:
                if key_ in contains_next_case:
                    continue
                if value_[1] > 0:
                    side = "buy"
                else:
                    side = "sell"
                binance.create_order(key_, "market", side, value_[0])
                exit_list.append(key_)
            except:
                time.sleep(0.5)
                continue

        for i in range(len(exit_list)):
            del is_entering[exit_list[i]]

        global_num = len(funding_fee)
        for key_, value_ in funding_fee.items():
            try:
                if key_ in contains_next_case and key_ in is_entering:
                    continue
                if value_ > 0:
                    side = "sell"
                else:
                    side = "buy"
                entry_order(key_, value_, side)
            except:
                time.sleep(0.5)
                continue
        global_num = 0

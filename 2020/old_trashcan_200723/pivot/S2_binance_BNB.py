import ccxt
import time
import pandas as pd
import os
import datetime
from pprint import pprint


def get_amount(ticker):
    price = binance.fetch_ohlcv(ticker)[-1][4]
    return (today_money_BNB / 11) / price


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
        time.sleep(0.7)
        ticker = list(is_entering.keys())[i]
        sell_amount = is_entering[ticker]
        binance.create_order(ticker, "market", "sell", sell_amount)
    reset = {}
    return reset


def buy_order(ticker):
    buy_amount = get_amount(ticker)
    order = binance.create_order(ticker, "market", "buy", buy_amount)
    is_entering[ticker] = float(order["amount"]) * 0.998
    banList.append(ticker)


def get_tickers(base):
    # base = '/USDT' or '/BNB' or '/BTC' or ...
    All_ticker = binance.fetch_tickers().keys()
    tickers = [s for s in All_ticker if base in s]
    result = []
    for i, item in enumerate(tickers):
        ohlcv = binance.fetch_order_book(item)
        if len(ohlcv["bids"]) != 0:
            result.append(item)
    return result


exchange_class = getattr(ccxt, "binance")
binance = exchange_class()
binance.enableRateLimit = True
binance.RateLimit = 10000
binance.apiKey = "FRbVseExyAWjQUtYFnS4memLnPCcgNAeRW7HEBrrw9qyIyPUMCTzUKxZKOJIHcfV"
binance.secret = "CbDX3DE5r9ErdLBOphDB4rjCaAaKbUqITbNK05YIitktZ24VfcNrvVRbIgfK6L87"
binance.load_markets()


# ticker_list = get_tickers('/BNB'))
ticker_list = [
    "WTC/BNB",
    "BAT/BNB",
    "NEO/BNB",
    "XZC/BNB",
    "IOTA/BNB",
    "XLM/BNB",
    "WABI/BNB",
    "LTC/BNB",
    "WAVES/BNB",
    "ICX/BNB",
    "AION/BNB",
    "NEBL/BNB",
    "BRD/BNB",
    "RLC/BNB",
    "STEEM/BNB",
    "BLZ/BNB",
    "ZIL/BNB",
    "ONT/BNB",
    "WAN/BNB",
    "ADA/BNB",
    "ZEN/BNB",
    "EOS/BNB",
    "THETA/BNB",
    "XRP/BNB",
    "ENJ/BNB",
    "TRX/BNB",
    "ETC/BNB",
    "SC/BNB",
    "MFT/BNB",
    "VET/BNB",
    "RVN/BNB",
    "MITH/BNB",
    "BTT/BNB",
    "HOT/BNB",
    "ZRX/BNB",
    "FET/BNB",
    "XMR/BNB",
    "ZEC/BNB",
    "IOST/BNB",
    "CELR/BNB",
    "DASH/BNB",
    "MATIC/BNB",
    "ATOM/BNB",
    "ONE/BNB",
    "FTM/BNB",
    "ALGO/BNB",
    "ERD/BNB",
    "ANKR/BNB",
    "WIN/BNB",
    "COS/BNB",
    "COCOS/BNB",
    "TOMO/BNB",
    "PERL/BNB",
    "CHZ/BNB",
    "BAND/BNB",
    "XTZ/BNB",
    "HBAR/BNB",
    "NKN/BNB",
    "STX/BNB",
    "KAVA/BNB",
    "ARPA/BNB",
    "BCH/BNB",
    "TROY/BNB",
    "FTT/BNB",
    "OGN/BNB",
    "WRX/BNB",
    "MBL/BNB",
    "COTI/BNB",
    "SOL/BNB",
    "CTSI/BNB",
    "HIVE/BNB",
    "CHR/BNB",
    "MDT/BNB",
    "STMX/BNB",
    "IQ/BNB",
    "DGB/BNB",
]

banList = []
is_entering = {}

today_money_BNB = binance.fetch_balance()["BNB"]["total"]


while True:
    try:
        for i, item in enumerate(ticker_list):
            time.sleep(0.5)
            time_ = get_time(datetime.datetime.now())[1]
            # if time_ == '0000' or time_ == '0001' or time_ == '0002' or time_ == '0003':
            if time_ == "0000" or time_ == "0001" or time_ == "0002" or time_ == "0003":
                is_entering = exit_ALL()
                banList = []
                today_money_BNB = binance.fetch_balance()["BNB"]["total"]
                time.sleep(179)

            if len(is_entering) > 33 or item in banList:
                time.sleep(40)
                continue


    except Exception as ex:
        print("err", item)
        time.sleep(15)
        continue

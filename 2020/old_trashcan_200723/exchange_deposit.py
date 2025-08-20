import ccxt
import time
import pandas as pd
import os
import telegram
import datetime


def buy():
    print("매수 완료")


def sell():
    print("매도 완료")


def send():
    print("송금 완료")


exchange_class = getattr(ccxt, "binance")
binance = exchange_class()
binance.enableRateLimit = True
binance.RateLimit = 10000
binance.load_markets()


def buy_order(item):
    ticker = "KRW-" + item[:-4]
    size = 25000  # 25000KRW
    upbit2.buy_market_order(ticker, size)
    is_entering.append(ticker)
    banList.append(item)


upbit_address = {"XRP": ["raQwCVAJVqjrVm1Nj5SFRcX8i22BhdC9WA", "410823337"]}

# XRP = 6min


# binance.withdraw("XRP", 85, "raQwCVAJVqjrVm1Nj5SFRcX8i22BhdC9WA", tag = "410823337", params = {})

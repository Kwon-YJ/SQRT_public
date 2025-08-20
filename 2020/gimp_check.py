# -*- coding: utf-8 -*-
import ccxt
import time
import urllib.request
import json
from urllib.request import Request, urlopen
import requests


exchange_class = getattr(ccxt, "binance")
binance = exchange_class()
binance.enableRateLimit = True
binance.RateLimit = 10000
binance.load_markets()

exchange_class = getattr(ccxt, "upbit")
upbit = exchange_class()
upbit.enableRateLimit = True
upbit.RateLimit = 10000
upbit.load_markets()

upbit_key = list(upbit.fetch_tickers().keys())
binance_key = list(binance.fetch_tickers().keys())

# upbit_key = [upbit_key[i][:-4] for i in range(len(upbit_key))]
# binance_key = [binance_key[i][:-5] for i in range(len(binance_key))]

upbit_key = [upbit_key[i][:-4] for i in range(len(upbit_key)) if "/KRW" in upbit_key[i]]
binance_key = [
    binance_key[i][:-5] for i in range(len(binance_key)) if "/USDT" in binance_key[i]
]
all_ticker = list(set(upbit_key) & set(binance_key) - set(["BSV", "BTC"]))


# while(1):
standard_USDT = (
    upbit.fetch_ohlcv("BTC/KRW", "1m")[-1][4]
    / binance.fetch_ohlcv("BTC/USDT", "1m")[-1][4]
)
for i, ticker in enumerate(all_ticker):
    upbit_url = "https://api.upbit.com/v1/ticker?markets=KRW-" + str(ticker)
    upbit_price = json.loads(urlopen(upbit_url).read().decode("utf-8"))[0][
        "trade_price"
    ]
    binance_url = (
        "https://api.binance.com/api/v1/klines?symbol=" + ticker + "USDT&interval=1m"
    )
    binance_price = float(requests.get(binance_url).json()[-1][4]) * standard_USDT
    value_ = round(100 * upbit_price / binance_price - 100, 3)
    temp = abs(value_)
    if temp > 1.5 and temp < 10:
        print(ticker, value_)

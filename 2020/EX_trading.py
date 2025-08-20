# -*- coding: utf-8 -*-

import ccxt
import time
import datetime


exchange_class = getattr(ccxt, "huobipro")
huobi = exchange_class()
huobi.enableRateLimit = True
huobi.RateLimit = 10000
huobi.load_markets()


exchange_class = getattr(ccxt, "binance")
binance = exchange_class()
binance.enableRateLimit = True
binance.RateLimit = 10000
binance.load_markets()


exchange_class = getattr(ccxt, "gateio")
gateio = exchange_class()
gateio.enableRateLimit = True
gateio.RateLimit = 10000
gateio.load_markets()


exchange_class = getattr(ccxt, "upbit")
upbit = exchange_class()
upbit.enableRateLimit = True
upbit.RateLimit = 10000
upbit.load_markets()


standard_USDT = (
    upbit.fetch_ohlcv("BTC/KRW", "1m")[-1][4]
    / gateio.fetch_ohlcv("BTC/USDT", "1m")[-1][4]
)

print(standard_USDT)


a = upbit.fetch_ohlcv("ADA/KRW", "5m")[-1][4]

b = gateio.fetch_ohlcv("ADA/USDT", "5m")[-1][4] * standard_USDT

print(a)
print(b)


"""
huobi_key = list(huobi.fetch_tickers().keys())
huobi_key = [huobi_key[i] for i in range(len(huobi_key)) if '/USDT' in huobi_key[i]]

binance_key = list(binance.fetch_tickers().keys())

binance_key = [binance_key[i] for i in range(len(binance_key)) if '/USDT' in binance_key[i]]

c = list(set(huobi_key) & set(binance_key) - set(['BSV/USDT', 'HIVE/USDT', 'DAI/USDT', 'MCO/USDT', 'CHR/USDT']))

print(len(c))



d = {}

for i in range(len(c)):
    binance_price = binance.fetch_ohlcv(c[i], '1d')[-1][4]
    huobi_price = huobi.fetch_ohlcv(c[i], '1d')[-1][4]
    temp = binance_price / huobi_price
    d[c[i]] = [temp, binance_price, huobi_price]

e = sorted(d.items(), key=lambda x: x[1], reverse=True)

ticker = [e[0][0], e[-1][0]]

value = [e[0][1], e[-1][1]]

print(e[0], e[-1])


if value[0][0] > 1:
    buy = huobi.fetch_order_book(ticker[0])['asks'][0][0]
    sell = binance.fetch_order_book(ticker[0])['bids'][0][0]
else:
    sell = huobi.fetch_order_book(ticker[0])['asks'][0][0]
    buy = binance.fetch_order_book(ticker[0])['bids'][0][0]
print(sell/buy * 0.9949)  

if value[1][0] > 1:
    buy = huobi.fetch_order_book(ticker[1])['asks'][0][0]
    sell = binance.fetch_order_book(ticker[1])['bids'][0][0]
else:
    sell = huobi.fetch_order_book(ticker[1])['asks'][0][0]
    buy = binance.fetch_order_book(ticker[1])['bids'][0][0]
print(sell/buy * 0.997)  
"""


"""

d = {}

for i in range(len(c)):
    binance_price = binance.fetch_ohlcv(c[i], '1d')[-1][4]
    huobi_price = huobi.fetch_ohlcv(c[i], '1d')[-1][4]
    # d[c[i]] = [binance_price, huobi_price]
    temp = binance_price / huobi_price
    #if temp > 1.003 or temp < 0.997:
    d[c[i]] = [temp, binance_price, huobi_price]

e = sorted(d.items(), key=lambda x: x[1], reverse=True)

ticker = [e[0][0], e[-1][0]]

value = [e[0][1], e[-1][1]]

print(e[0], e[-1])


if value[0][0] > 1:
    buy = huobi.fetch_order_book(ticker[0])['asks'][0][0]
    sell = binance.fetch_order_book(ticker[0])['bids'][0][0]
else:
    sell = huobi.fetch_order_book(ticker[0])['asks'][0][0]
    buy = binance.fetch_order_book(ticker[0])['bids'][0][0]
print(sell/buy * 0.9949)  

if value[1][0] > 1:
    buy = huobi.fetch_order_book(ticker[1])['asks'][0][0]
    sell = binance.fetch_order_book(ticker[1])['bids'][0][0]
else:
    sell = huobi.fetch_order_book(ticker[1])['asks'][0][0]
    buy = binance.fetch_order_book(ticker[1])['bids'][0][0]
print(sell/buy * 0.997)  


"""

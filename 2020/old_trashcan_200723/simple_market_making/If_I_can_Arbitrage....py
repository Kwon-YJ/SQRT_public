# -*- coding: utf-8 -*-
import ccxt
import time
from pprint import pprint
import pandas as pd

# bid = 매수호가
# ask = 매도호가

binance = ccxt.binance()
bithumb = ccxt.bithumb()

global USDKRW
# USDKRW = 1227
USDKRW = 1250


def binance_to_bithumb(ticker):

    binance_temp = binance.fetch_order_book(ticker + "/USDT")["asks"]
    depth = int(binance_temp[0][0] * binance_temp[0][1] * USDKRW)
    binance_best_buy = binance_temp[0][0] * USDKRW * 0.99925

    bithumb_temp = bithumb.fetch_order_book(ticker + "/KRW")["bids"]
    bithumb_best_sell = bithumb_temp[0][0] * 0.9988

    ratio = round(bithumb_best_sell / binance_best_buy, 4)

    ratio_data[ratio] = ticker

    return binance_best_buy, bithumb_best_sell, depth, ratio


def bithumb_to_binance(ticker):

    bithumb_temp = bithumb.fetch_order_book(ticker + "/KRW")["asks"]
    depth = int(bithumb_temp[0][0] * bithumb_temp[0][1])
    bithumb_best_buy = bithumb_temp[0][0] * 0.9988

    binance_temp = binance.fetch_order_book(ticker + "/USDT")["bids"]
    binance_best_sell = binance_temp[0][0] * USDKRW * 0.99925

    ratio = round(binance_best_sell / bithumb_best_buy, 4)

    ratio_data[ratio] = ticker

    return bithumb_best_buy, binance_best_sell, depth, ratio


# ticker_list = ['ZRX','XMR','ZEC','BTT','TRX','QTUM','BAT','ADA','OMG','EOS','LINK','AION','ETH','COS','STRAT','WAVES','ETC','ZIL','VET','ICX','ANKR','MCO','IOST','MTL','ENJ','LTC','THETA','XRP','DASH','XLM','NPXS']
ticker_list = [
    "ZEC",
    "BTT",
    "TRX",
    "QTUM",
    "ADA",
    "EOS",
    "AION",
    "STRAT",
    "WAVES",
    "ETC",
    "ZIL",
    "VET",
    "ICX",
    "ANKR",
    "IOST",
    "LTC",
    "THETA",
    "XRP",
    "DASH",
    "XLM",
]


# for i, value in enumerate(ticker_list):
# binance_depth, binance_price, bithumb_price, bithumb_depth, ratio = binance_to_bithumb(value)

ratio_data = {}


for i, value in enumerate(ticker_list):
    binance_to_bithumb(value)
    # print(value)
    # pprint(list(binance_to_bithumb(value)))
    # print('')

print(ratio_data[max(ratio_data.keys())])
print(max(ratio_data.keys()))

print("")

ratio_data = {}

for i, value in enumerate(ticker_list):
    bithumb_to_binance(value)
    # print(value)
    # pprint(list(bithumb_to_binance(value)))
    # print('')

print(ratio_data[max(ratio_data.keys())])
print(max(ratio_data.keys()))


"""
diff1 = []
diff2 = []

for i in range(len(ticker_list)):
	c, d, e, f = aaaa(ticker_list[i])
	diff1.append(round(d/c,4))
	diff2.append(round(e/f,4))

a = ([[ticker_list[i],value] for i, value in enumerate(diff1) if value == max(diff1)])[0]
b = ([[ticker_list[i],value] for i, value in enumerate(diff2) if value == max(diff2)])[0]

temp1 = binance.fetch_order_book(a[0]+'/USDT')['asks']
temp2 = bithumb.fetch_order_book(b[0]+'/KRW')['bids']

binance_book = round((temp1[0][0] * temp1[0][1]) * 1211.81, 2)
bithumb_book = round((temp2[0][0] * temp2[0][1]), 2)


a.append(binance_book)
a.append(temp1[0][0])


b.append(bithumb_book)
b.append(temp2[0][0])

print(a)
print(b)
print(a[1]*b[1])

"""
"""
bithumb = ccxt.bithumb()

bithumb = ccxt.bithumb({'apiKey': '16d430f1eac8f9da8187a4bfcc42275c','secret': '0217b73ae8869be05d61a530934b77dc',
	'enableRateLimit': True,})
	
print(bithumb.fetch_balance()['BTC'])
print(bithumb.fetch_balance()['EOS'])

print(bithumb.fetch_balance()['KRW'])

"""


"""
100만원으로 해보자
0.1 두번
0.25 두번
+
송금 수수료
11000원

"""


"""
ZRX
바낸 : 15
빗썸 : 3.5
가격 : 203.9원
누계 : 3772.1원

XMR
바낸 : 0.0002
빗썸 : 0.05
가격 : 44960.0원
누계 : 2256.9원

ZEC
바낸 : 0.01
빗썸 : 0.001
가격 : 33020.0원
누계 : 363.2원

BTT
바낸 : 100
빗썸 : 100
가격 : 0.2442원
누계 : 48.8원

TRX 확인 요망
바낸
빗썸 : 5
가격 : 12.49원
누계 : 

QTUM
바낸 : 0.022
빗썸 : 0.05
가격 : 1474.0원
누계 : 106.1원

BAT
바낸 : 20
빗썸 : 10
가격 : 159.5원
누계 : 4770.0원

ADA
바낸 : 2
빗썸 : 0.5
가격 : 33.39원
누계 : 83.4원

OMG
바낸 : 5.46
빗썸 : 0.4
가격 : 616.6원
누계 : 3616.2원

EOS
바낸 : 0.2
빗썸 : 0.1
가격 : 2467.0원
누계 : 740.1원

LINK
바낸 : 1.2
빗썸 : 1
가격 : 2853.0원
누계 : 6276.6원

AION 확인
바낸
빗썸 : 0.5
가격 : 75.21원
누계 : 

ETH
바낸 : 0.02
빗썸 : 0.01
가격 : 159800.0원
누계 : 4794.0원 

COS
바낸 : 496
빗썸 : 50
가격 : 7.236원
누계 : 3950.8원

STRAT
바낸 : 0.2
빗썸 : 0.2
가격 : 228.5원
누계 : 91.4

WAVES
바낸 : 0.004
빗썸 : 0.01
가격 : 1115.0원
누계 : 15.6원

ETC
바낸 : 0.02
빗썸 : 0.01
가격 : 5930.0원
누계 : 117.9원

ZIL 확인
바낸 
빗썸 : 30
가격 : 4.22원
누계 : 

VET 
바낸 : 200
빗썸 : 100
가격 : 3.218원
누계 : 965.4원

ICX
바낸 : 0.04
빗썸 : 0.1
가격 : 226.0원
누계 : 31.64원

ANKR 확인
바낸
빗썸 : 200
가격 : 1.251원
누계 : 

MCO
바낸 : 0.9
빗썸 : 0.5
가격 : 3300.0원
누계 : 4620.0원

IOST 확인
바낸
빗썸 : 100
가격 : 2.946원
누계 : 

MTL
바낸 : 15
빗썸 : 3
가격 : 204.5원
누계 : 3681.0원

ENJ
바낸 : 52
빗썸 : 35
가격 : 57.63원
누계 : 5013.8원

LTC
바낸 : 0.002
빗썸 : 0.01
가격 : 45290.0원
누계 : 543.4원

THETA
바낸 : 0.19
빗썸 : 10
가격 : 72.75원
누계 : 741.3원

XRP
바낸 : 0.5
빗썸 : 1
가격 : 190.4원
누계 : 285.6원

DASH
바낸 : 0.004
빗썸 : 0.01
가격 : 60400.0원
누계 : 845.6원

XLM
바낸 : 0.02
빗썸 : 0.01
가격 : 47.19원
누계 : 1.4원

NPXS
바낸 : 25262
빗썸 : 970
가격 : 0.127원
누계 : 3331.4원

"""

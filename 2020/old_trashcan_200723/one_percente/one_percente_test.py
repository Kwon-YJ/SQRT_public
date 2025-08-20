import ccxt
import time
import datetime
from pprint import pprint
from matplotlib import pyplot as plt
import numpy

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
binance.apiKey = "FRbVseExyAWjQUtYFnS4memLnPCcgNAeRW7HEBrrw9qyIyPUMCTzUKxZKOJIHcfV"
binance.secret = "CbDX3DE5r9ErdLBOphDB4rjCaAaKbUqITbNK05YIitktZ24VfcNrvVRbIgfK6L87"
binance.load_markets()


def get_data(ticker):
    ohlcv = binance.fetch_ohlcv(ticker, "1d")[:-5]

    for i in range(len(ohlcv)):
        open_ = ohlcv[i][1]
        high_ = ohlcv[i][2]
        low_ = ohlcv[i][3]
        close_ = ohlcv[i][4]

        data_0 = high_ / open_
        data_1 = open_ / low_

        earning = 1.08

        # if data_0 > earning:
        #    result.append(earning * 0.99964 * 0.99964 - 1)
        # else:
        #    temp = (close_ / open_) * 0.99964 * 0.99964 - 1
        #    result.append(temp)

        if data_1 > earning:
            result.append(earning * 0.99964 * 0.99964 - 1)
        else:
            temp = (open_ / close_) * 0.99964 * 0.99964 - 1
            result.append(temp)


tickers = [
    "BTC/USDT",
    "ETH/USDT",
    "BCH/USDT",
    "XRP/USDT",
    "EOS/USDT",
    "LTC/USDT",
    "TRX/USDT",
    "ETC/USDT",
    "LINK/USDT",
    "XLM/USDT",
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
]

"""
for i,item in enumerate(tickers):

    print('종목 :', item)
    result = []
    get_data(item)

    risk_free = 0.038 / 365
    avg = numpy.mean(result)
    std = numpy.std(result)
    size = (avg - risk_free) / (std * std)
    print('평균수익 :',avg)
    print('포지션 사이징 :', size)

"""
result = []
for i, item in enumerate(tickers):
    get_data(item)

risk_free = 0.038 / 365
avg = numpy.mean(result)
std = numpy.std(result)
size = (avg - risk_free) / (std * std)
print("평균수익 :", avg)
print("포지션 사이징 :", size)

# -*- coding: utf-8 -*-
import urllib.request
from pprint import pprint
import json
import time
import ccxt


def get_tickerlist():
    url = "https://fapi.binance.com/fapi/v1/premiumIndex"
    text_data = urllib.request.urlopen(url).read().decode("utf-8")
    result = json.loads(text_data)
    result = [result[s]["symbol"][:-4] + "/USDT" for s in range(len(result))]
    return result


def get_time_diff():
    url = "https://fapi.binance.com/fapi/v1/premiumIndex"
    text_data = urllib.request.urlopen(url).read().decode("utf-8")
    All_tickers = json.loads(text_data)
    time_diff = (
        float(All_tickers[0]["nextFundingTime"]) - float(All_tickers[0]["time"])
    ) / 1000
    return time_diff


binance = ccxt.binance(
    {
        "options": {"defaultType": "future"},
        "timeout": 30000,
        "apiKey": "FRbVseExyAWjQUtYFnS4memLnPCcgNAeRW7HEBrrw9qyIyPUMCTzUKxZKOJIHcfV",
        "secret": "CbDX3DE5r9ErdLBOphDB4rjCaAaKbUqITbNK05YIitktZ24VfcNrvVRbIgfK6L87",
        "enableRateLimit": True,
    }
)


def get_ohlcv(ticker="BTC/USDT", interval="1m", limit=200):
    ticker = ticker[:-5] + "USDT"
    url = "https://fapi.binance.com/fapi/v1/klines?symbol={0}&interval={1}&limit={2}".format(
        ticker, interval, str(limit)
    )
    text_data = urllib.request.urlopen(url).read().decode("utf-8")
    result = json.loads(text_data)
    return result


for i in range(200):
    # time.sleep(0.1)
    print(get_ohlcv("BTC/USDT", "1h", 200)[-1][5])


# https://fapi.binance.com/fapi/v1/klines?symbol=BNBUSDT&interval=1m&limit=1


"""
for i in range(len(All_tickers)):
    if All_tickers[i]['symbol'] == 'XRPUSDT':
        result = float(All_tickers[i]['lastFundingRate'])
        return result
"""

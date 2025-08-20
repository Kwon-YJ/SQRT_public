import multiprocessing
import urllib.request
import pandas as pd
import datetime
import operator
import parmap
import ccxt
import time
import json

from all_func import send_MSG

binance = ccxt.binance(
    {
        # "options": {"defaultType": "future"},
        "timeout": 30000,
        "apiKey": "FRbVseExyAWjQUtYFnS4memLnPCcgNAeRW7HEBrrw9qyIyPUMCTzUKxZKOJIHcfV",
        "secret": "CbDX3DE5r9ErdLBOphDB4rjCaAaKbUqITbNK05YIitktZ24VfcNrvVRbIgfK6L87",
        "enableRateLimit": True,
    }
)


def get_data(all_ticker, ticker_list):
    list_ = []

    all_diff = {}
    for i in range(len(all_ticker)):
        ohlcv_ = all_ticker[i]
        price_diff = float(ohlcv_[-2][4]) / float(ohlcv_[-2][1])
        all_diff[ticker_list[i]] = price_diff
        list_.append([ohlcv_[s][4] for s in range(len(ohlcv_))])

    MDD_ticker = min(all_diff.items(), key=operator.itemgetter(1))[0]

    return MDD_ticker, all_diff


def get_ticker_list():
    temp_list = list(binance.fetch_tickers().keys())
    temp_list = [
        temp_list[i] for i in range(len(temp_list)) if ("/USDT" in temp_list[i])
    ]
    std_time_data = binance.fetch_ohlcv("BTC/USDT", "1d")[-1][0]
    result_ = [
        temp_list[i]
        for i in range(len(temp_list))
        if binance.fetch_ohlcv(temp_list[i], "1d")[-1][0] == std_time_data
    ]  # 상폐 종목 제외
    return result_


ticker_list = get_ticker_list()

All_ohlcv = {}
for i in range(len(ticker_list)):
    if "UP/" in ticker_list[i]:
        continue
    if "DOWN/" in ticker_list[i]:
        continue

    temp = binance.fetch_ohlcv(ticker_list[i], "1d")
    if temp != None:
        All_ohlcv[ticker_list[i]] = temp
min_, all_diff = get_data(list(All_ohlcv.values()), list(All_ohlcv.keys()))

# print(min_, all_diff[min_]) # 최대 하락종목, 하락 폭
send_MSG([min_, all_diff[min_]])

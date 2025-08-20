# -*- coding: utf-8 -*-
import ccxt
import time
import pandas as pd
import numpy as np
import urllib
import json
import datetime
import telegram


# https://api1.binance.com/sapi/v1/capital/config/getall


def get_funding_rate():
    url = "https://api1.binance.com/sapi/v1/capital/config/getall"
    text_data = urllib.request.urlopen(url).read().decode("utf-8")

    print(json.loads(text_data))
    """
    tickers = 
    EndPoint = len(tickers)
    All_funding_rate = {}
    for i in range(EndPoint):
        funding_rate = float(tickers[i]['lastFundingRate'])
        if funding_rate <= 0.0001:
                ticker = tickers[i]['symbol'][:-4] + '/USDT'
                if ticker in ticker_list:
                    All_funding_rate[ticker] = (float(tickers[i]['lastFundingRate']))
    time_diff = (float(tickers[0]['nextFundingTime']) - float(tickers[0]['time']))/1000
    return All_funding_rate, time_diff
    """


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


get_funding_rate()

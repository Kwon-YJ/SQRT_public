# -*- coding: utf-8 -*-
import ccxt
import time
import datetime


def Bitmex_time_parameter():
    temp_time = str(
        datetime.datetime.now()
        - datetime.timedelta(minutes=100)
        - datetime.timedelta(hours=9)
    )
    convert = temp_time[:10] + "T" + temp_time[11:19]
    timestamp = bitmex.parse8601(convert)
    return timestamp


def get_BTC_XBT_spread():
    timeframe = "1h"
    XBT_ohlcv = bitmex.fetch_ohlcv("BTC/USD", timeframe, Bitmex_time_parameter())
    BTC_ohlcv = binance.fetch_ohlcv("BTC/USDT", timeframe)

    return BTC_ohlcv[-1][4] - XBT_ohlcv[-1][4]


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

bitmex = ccxt.bitmex(
    {
        "apiKey": "3pFJ5lblk8ff8brlz2plOG2o",
        "secret": "KKFk0a-YvtW8aEcS33HbQlxJ63rHpdA95D7IWNALSOTVraB1",
        "enableRateLimit": True,
        "RateLimit": 10000,
    }
)
bitmex.load_markets()


while 1:
    print(get_BTC_XBT_spread())
    time.sleep(1)

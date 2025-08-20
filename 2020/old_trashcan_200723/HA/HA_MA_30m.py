# -*- coding: utf-8 -*-
import ccxt
import time
from pprint import pprint
import pandas as pd
import datetime


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


status = 0


def get_HA_ohlcv(ohlcv):
    # ohlcv = binance.fetch_ohlcv('BTC/USDT','1h')
    ha_ohlcv = []
    for i in range(1, len(ohlcv)):
        if i == 1:
            ha_open = (ohlcv[i - 1][1] + ohlcv[i - 1][4]) / 2
        else:
            ha_open = (ha_ohlcv[i - 2][1] + ha_ohlcv[i - 2][4]) / 2
        timestamp = ohlcv[i][0]
        ha_close = (ohlcv[i][1] + ohlcv[i][2] + ohlcv[i][3] + ohlcv[i][4]) / 4
        ha_high = max(ohlcv[i][2], ha_close, ha_open)
        ha_low = min(ohlcv[i][3], ha_close, ha_open)
        ha_ohlcv.append(
            [
                timestamp,
                round(ha_open, 2),
                round(ha_high, 2),
                round(ha_low, 2),
                round(ha_close, 2),
            ]
        )
    return ha_ohlcv


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


ticker = "BCH/USDT"
timeframe = "1h"
mode_switch = 0
size = 0.045


while 1:
    try:
        time.sleep(1)
        HA_ohlcv = get_HA_ohlcv(binance.fetch_ohlcv(ticker, timeframe))
        HA_ohlcv_close = [HA_ohlcv[s][4] for s in range(len(HA_ohlcv))]
        ma20 = (pd.Series(HA_ohlcv_close).rolling(window=20).mean()).to_list()

        now = get_time(datetime.datetime.now())[1][2:]

        if now != "01":
            time.sleep(25)
            continue

        if mode_switch != 0:
            size = 0.09

        if HA_ohlcv_close[-1] > ma20[-1] and mode_switch <= 0:
            binance.create_order(ticker, "market", "buy", size)
            mode_switch = 1
        elif HA_ohlcv_close[-1] < ma20[-1] and mode_switch >= 0:
            binance.create_order(ticker, "market", "sell", size)
            mode_switch = -1
    except:
        time.sleep(15)
        continue

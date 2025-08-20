# -*- coding: utf-8 -*-
import ccxt
import pandas as pd
import numpy as np
import datetime
import time
import telegram


def send_MSG(message):
    while True:
        try:
            bot.send_message(chat_id=801167350, text=message)
            time.sleep(3)
            return None
        except:
            time.sleep(3)
            continue


def get_time():
    now = datetime.datetime.now()
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

bot = telegram.Bot(token=my_token)

ticker = "BTC/USDT"

while 1:
    time.sleep(0.5)
    temp = int(get_time()[1][2:])
    if temp % 5 == 0:
        ohlcv = binance.fetch_ohlcv(ticker, "5m")
        volume = [ohlcv[i][5] for i in range(len(ohlcv))]
        avg = sum(volume) / len(volume)
        if volume[-2] > avg * 1.2 and volume[-2] > volume[-3] * 3:
            send_MSG("BTC volume over!")
            time.sleep(60)

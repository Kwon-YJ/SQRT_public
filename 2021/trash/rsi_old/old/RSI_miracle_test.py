# -*- coding: utf-8 -*-
import ccxt
import time
import datetime
import telegram
import pandas as pd
import numpy as np
import pandas_ta as ta


def get_time():
    now = datetime.datetime.now()
    # now = datetime.datetime.now() + datetime.timedelta(seconds=55)
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


def send_MSG(message):
    while True:
        try:
            bot.send_message(chat_id=801167350, text=str(message))
            time.sleep(3)
            return None
        except:
            time.sleep(3)
            continue


def custom_convert(ticker):  # convert 5m → 15m
    ohlcv5 = binance.fetch_ohlcv(ticker, "5m")
    if len(ohlcv5) < 499:
        return None
    ohlcv15 = []
    temp = str(datetime.datetime.fromtimestamp(ohlcv5[0][0] / 1000))[14:16]
    if int(temp) % 15 == 5:
        del ohlcv5[0]
        del ohlcv5[1]
    elif int(temp) % 15 == 10:
        del ohlcv5[0]
    for i in range(0, len(ohlcv5) - 2, 3):
        highs = [ohlcv5[i + j][2] for j in range(0, 3) if ohlcv5[i + j][2]]
        lows = [ohlcv5[i + j][3] for j in range(0, 3) if ohlcv5[i + j][3]]
        candle = [
            ohlcv5[i + 0][0],
            ohlcv5[i + 0][1],
            max(highs) if len(highs) else None,
            min(lows) if len(lows) else None,
            ohlcv5[i + 2][4],
        ]
        ohlcv15.append(candle)
    if int(temp) % 15 == 0:
        ohlcv15.append(
            [
                ohlcv5[-1][0],
                ohlcv5[-2][1],
                max([ohlcv5[-1][2], ohlcv5[-2][2]]),
                min([ohlcv5[-1][3], ohlcv5[-2][3]]),
                ohlcv5[-1][4],
            ]
        )
    if int(temp) % 15 == 10:
        ohlcv15.append(ohlcv5[-1][:-1])
    return ohlcv15


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

all_tickers = list(binance.fetch_tickers().keys())
all_tickers = list(set(all_tickers) - set(["DOTECOUSDT", "DOTECO/USDT"]))


result = []

while 1:
    print("123123")
    time.sleep(4)
    # temp = int(get_time()[1][2:])%15
    temp = 0
    if temp == 0:
        result.clear()
        for i, item in enumerate(all_tickers):

            ohlcv15 = custom_convert(all_tickers[i])

            if ohlcv15 == None:
                continue

            df = pd.DataFrame(
                data=np.array(ohlcv15),
                columns=["time_stamp", "open", "close", "low", "1"],
            )  # RSI(high, 10)
            rsi_20 = df.ta.rsi(length=10)
            rsi_20 = rsi_20.values.tolist()

            if rsi_20[-2] < 19 and rsi_20[-3] > 19:
                result.append(all_tickers[i])

    if len(result) > 0:
        send_MSG(result)
        result.clear()
        time.sleep(60)

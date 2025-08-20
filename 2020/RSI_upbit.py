# -*- coding: utf-8 -*-
import ccxt
import time
import pandas as pd
import numpy as np


def calcRSI(df, period):
    U = np.where(
        df.diff(1)["close"] > 0, df.diff(1)["close"], 0
    )  # df.diff를 통해 (기준일 종가 - 기준일 전일 종가)를 계산하여 0보다 크면 증가분을 감소했으면 0을 넣어줌
    D = np.where(
        df.diff(1)["close"] < 0, df.diff(1)["close"] * (-1), 0
    )  # df.diff를 통해 (기준일 종가 - 기준일 전일 종가)를 계산하여 0보다 작으면 감소분을 증가했으면 0을 넣어줌
    AU = pd.DataFrame(U).ewm(period).mean()  # AU, period=14일 동안의 U의 평균
    AD = pd.DataFrame(D).ewm(period).mean()  # AD, period=14일 동안의 D의 평균
    RSI = AU / (AD + AU) * 100  # 0부터 1로 표현되는 RSI에 100을 곱함
    return RSI  # .tail(1).values[0][0]


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

ohlcv = binance.fetch_ohlcv("BTC/USDT", "1d")
dt_list = [ohlcv[i][0] for i in range(len(ohlcv))]
df = pd.DataFrame(
    data=np.array(ohlcv),
    columns=["time_stamp", "open", "high", "low", "close", "volume"],
)
temp = calcRSI(df, 14)
print(temp)

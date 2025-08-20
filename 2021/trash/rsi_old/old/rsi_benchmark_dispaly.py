# -*- coding: utf-8 -*-
import ccxt
import pandas as pd
import numpy as np
import datetime
from pprint import pprint
import os

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


"""
def convert(ohlcv5): # convert 5m → 15m
	ohlcv15 = []
	temp = str(datetime.datetime.fromtimestamp(ohlcv5[0][0]/1000))[14:16]
	if int(temp) % 15 == 5:
		del ohlcv5[0]
		del ohlcv5[1]
	elif int(temp) % 15 == 10:
		del ohlcv5[0]
	for i in range(0, len(ohlcv5) - 2, 3):
		highs = [ohlcv5[i + j][2] for j in range(0, 3) if ohlcv5[i + j][2]]
		lows = [ohlcv5[i + j][3] for j in range(0, 3) if ohlcv5[i + j][3]]
		volumes = [ohlcv5[i + j][5] for j in range(0, 3) if ohlcv5[i + j][5]]
		candle = [
			ohlcv5[i + 0][0],
			ohlcv5[i + 0][1],
			max(highs) if len(highs) else None,
			min(lows) if len(lows) else None,
			ohlcv5[i + 2][4]
		]
		ohlcv15.append(candle)
	ohlcv15.append([ohlcv5[-1][0],ohlcv5[-1][1],ohlcv5[-1][2],ohlcv5[-1][3],ohlcv5[-1][4]])
	return ohlcv15
"""


def convert(ohlcv5):  # convert 5m → 15m
    # ohlcv5 = binance.fetch_ohlcv(ticker, "5m")
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


def calcRSI(ticker, period):
    ohlcv = convert(binance.fetch_ohlcv(ticker, "5m"))
    # df = pd.DataFrame(data=np.array(ohlcv), columns=['time_stamp','open', 'high', 'low', 'close', 'volume'])
    df = pd.DataFrame(
        data=np.array(ohlcv), columns=["time_stamp", "open", "high", "low", "close"]
    )
    U = np.where(
        df.diff(1)["close"] > 0, df.diff(1)["close"], 0
    )  # df.diff를 통해 (기준일 종가 - 기준일 전일 종가)를 계산하여 0보다 크면 증가분을 감소했으면 0을 넣어줌
    D = np.where(
        df.diff(1)["close"] < 0, df.diff(1)["close"] * (-1), 0
    )  # df.diff를 통해 (기준일 종가 - 기준일 전일 종가)를 계산하여 0보다 작으면 감소분을 증가했으면 0을 넣어줌
    AU = pd.DataFrame(U).ewm(period).mean()  # AU, period=14일 동안의 U의 평균
    AD = pd.DataFrame(D).ewm(period).mean()  # AD, period=14일 동안의 D의 평균
    RSI = AU / (AD + AU) * 100  # 0부터 1로 표현되는 RSI에 100을 곱함
    # return RSI
    return float(RSI.tail(1)[0])


ticker_list = [
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
    "ALGO/USDT",
    "ZIL/USDT",
    "KNC/USDT",
    "ZRX/USDT",
    "COMP/USDT",
    "OMG/USDT",
    "DOGE/USDT",
    "SXP/USDT",
    "KAVA/USDT",
    "BAND/USDT",
    "RLC/USDT",
    "WAVES/USDT",
    "MKR/USDT",
    "SNX/USDT",
    "DOT/USDT",
    "DEFI/USDT",
    "YFI/USDT",
    "BAL/USDT",
    "CRV/USDT",
    "TRB/USDT",
    "YFII/USDT",
    "RUNE/USDT",
    "SUSHI/USDT",
    "SRM/USDT",
    "BZRX/USDT",
    "EGLD/USDT",
    "SOL/USDT",
    "ICX/USDT",
    "STORJ/USDT",
    "BLZ/USDT",
    "UNI/USDT",
    "AVAX/USDT",
    "FTM/USDT",
    "HNT/USDT",
    "ENJ/USDT",
    "FLM/USDT",
    "TOMO/USDT",
    "REN/USDT",
    "KSM/USDT",
    "NEAR/USDT",
    "AAVE/USDT",
    "FIL/USDT",
    "RSR/USDT",
    "LRC/USDT",
    "MATIC/USDT",
    "OCEAN/USDT",
    "CVC/USDT",
    "BEL/USDT",
    "CTK/USDT",
    "AXS/USDT",
    "ALPHA/USDT",
    "ZEN/USDT",
    "SKL/USDT",
    "GRT/USDT",
    "1INCH/USDT",
]

display = [{0: 0}, {0: 0}]

while 1:
    result = {}
    for i, item in enumerate(ticker_list):
        value = int(calcRSI(item, 20))
        if value < 30 or value > 70:
            result[item[:-5]] = value
    display.append(result)
    # os.system('cls')
    os.system("clear")
    del display[0]
    print(len(display[0]))
    pprint(display[0])
    print("---------------")
    print(len(display[1]))
    pprint(display[1])
    print("---------------")
    print("in")
    print(list(set(display[1].keys()) - set(display[0].keys())))
    print("---------------")
    print("out")
    print(list(set(display[0].keys()) - set(display[1].keys())))

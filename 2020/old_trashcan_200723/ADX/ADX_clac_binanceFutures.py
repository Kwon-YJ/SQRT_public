import ccxt
import time
import pandas as pd
import os


def ATR(data, length):
    TR = []
    for i in range(int(length)):
        TR.append(
            max(
                (data[i - length][2] - data[i - length][3]),
                abs(data[i - length][2] - data[i - length - 1][4]),
                abs(data[i - length][3] - data[i - length - 1][4]),
            )
        )
    ATR = pd.Series(TR).ewm(length).mean()
    return ATR.tolist()


def ADX(ohlcv, length):
    DMP = []
    DMM = []
    PDI = []
    MDI = []
    DX = []
    for i in range(1, len(ohlcv)):
        if (ohlcv[i][2] - ohlcv[i - 1][2] > ohlcv[i - 1][3] - ohlcv[i][3]) == True:
            DMP.append(ohlcv[i][2] - ohlcv[i - 1][2])
        else:
            DMP.append(0)

        if (ohlcv[i - 1][3] - ohlcv[i][3] > ohlcv[i][2] - ohlcv[i - 1][2]) == True:
            DMM.append(ohlcv[i - 1][3] - ohlcv[i][3])
        else:
            DMM.append(0)

    smoothTR = ATR(ohlcv, 14)
    smoothDMP = pd.Series(DMP).ewm(length).mean().tolist()[-length:]
    smoothDMM = pd.Series(DMM).ewm(length).mean().tolist()[-length:]
    for i in range(len(smoothTR)):
        PDI.append(smoothDMP[i] / smoothTR[i] * 100)
        MDI.append(smoothDMM[i] / smoothTR[i] * 100)
    for i in range(len(smoothTR)):
        DX.append(abs(PDI[i] - MDI[i]) / (PDI[i] + MDI[i]) * 100)
    ADX = pd.Series(DX).ewm(length).mean().tolist()
    return ADX


ticker = "BTC/USDT"
time_frame = "1h"
length = 14

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

ohlcv = binance.fetch_ohlcv(ticker, time_frame)
ADX_data = ADX(ohlcv, length)

print(ADX_data[-1])

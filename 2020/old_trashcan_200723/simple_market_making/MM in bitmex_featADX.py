# -*- coding: utf-8 -*-
import ccxt
import time
import pandas as pd
import datetime


def Bitmex_time_parameter():
    # temp_time = str(datetime.datetime.now() - datetime.timedelta(minutes = 500) - datetime.timedelta(hours = 9))
    temp_time = str(datetime.datetime.now() - datetime.timedelta(minutes=500))
    convert = temp_time[:10] + "T" + temp_time[11:19]
    timestamp = bitmex.parse8601(convert)
    return timestamp


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


def make_order():
    try:
        data = bitmex.fetch_order_book(symbol)
        target_ask = data["asks"][2][0]
        target_bid = data["bids"][2][0]
        # order2 = bitmex.create_order(symbol, 'limit', 'buy', size, target_bid, {'leverage': 5})
        # order1 = bitmex.create_order(symbol, 'limit', 'sell', size, target_ask, {'leverage': 5})
        bitmex.create_order(symbol, "limit", "buy", size, target_bid, {"leverage": 5})
        bitmex.create_order(symbol, "limit", "sell", size, target_ask, {"leverage": 5})
        return None
    except:
        time.sleep(5)
        return None


bitmex = ccxt.bitmex(
    {
        "apiKey": "3pFJ5lblk8ff8brlz2plOG2o",
        "secret": "KKFk0a-YvtW8aEcS33HbQlxJ63rHpdA95D7IWNALSOTVraB1",
        "enableRateLimit": True,
        "RateLimit": 10000,
    }
)

symbol = "BTC/USD"
size = 30
time_frame = "5m"

# Main
while True:
    ohlcv = bitmex.fetch_ohlcv(symbol, time_frame, Bitmex_time_parameter())
    ADX_data = ADX(ohlcv, 14)[-1]

    time.sleep(1)

    if ADX_data < 15:
        make_order()
        time.sleep(144)

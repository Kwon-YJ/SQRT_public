import ccxt
import time
import pandas as pd
import os
import telegram


def _entry(ticker, ohlcv):
    if ohlcv[-2][4] > ohlcv[-6][4]:
        order = binance.create_order(
            ticker, "market", "buy", 0.002, None, {"leverage": 1}
        )
        status_[0] = 1
        status_[1] = 0

    elif ohlcv[-2][4] < ohlcv[-6][4]:
        order = binance.create_order(
            ticker, "market", "sell", 0.002, None, {"leverage": 1}
        )
        status_[0] = 1
        status_[1] = 1

    else:
        return None


def _exit(ticker, ohlcv):
    if status_[1] == 0:
        temp_ = [ohlcv[-5][3], ohlcv[-4][3], ohlcv[-3][3], ohlcv[-2][3]]
        side = "sell"
        point = min(temp_)
    elif status_[1] == 1:
        temp_ = [ohlcv[-5][2], ohlcv[-4][2], ohlcv[-3][2], ohlcv[-2][2]]
        side = "buy"
        point = max(temp_)
    else:
        return None
    if temp_[-1] == point:
        order = binance.create_order(
            ticker, "market", side, 0.002, None, {"leverage": 1}
        )
        status_[0] = 0
        status_[1] = -1


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


bot = telegram.Bot(token=my_token)

ticker = "ETH/USDT"
time_frame = "3m"
length = 14
status_ = [0, -1]

# status_[0] = 0 // none
# status_[0] = 1 // entering

# status_[1] = -1 // none
# status_[1] = 0 // long entering
# status_[1] = 1 // short entering

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


# status_[0] = 0 // none
# status_[0] = 1 // entering

# status_[1] = -1 // none
# status_[1] = 0 // long entering
# status_[1] = 1 // short entering

while True:
    ohlcv = binance.fetch_ohlcv(ticker, time_frame)

    long_target = ohlcv[-2][2]
    short_target = ohlcv[-2][3]

    current_price = ohlcv[-1][4]

    if status_[0] == 0:
        if current_price > long_target:
            order = binance.create_order(
                ticker, "market", "buy", 0.02, None, {"leverage": 1}
            )
            status_ = [1, 0]
        elif current_price < short_target:
            order = binance.create_order(
                ticker, "market", "sell", 0.02, None, {"leverage": 1}
            )
            status_ = [1, 1]
    else:  # status_[0] == 1:
        if status_[1] == 0 and current_price < short_target:
            order = binance.create_order(
                ticker, "market", "sell", 0.02, None, {"leverage": 1}
            )
            status_ = [0, -1]
        elif status_[1] == 1 and current_price > long_target:
            order = binance.create_order(
                ticker, "market", "buy", 0.02, None, {"leverage": 1}
            )
            status_ = [0, -1]

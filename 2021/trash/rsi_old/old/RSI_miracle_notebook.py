import pandas as pd
import numpy as np
import pandas_ta as ta
import ccxt
import datetime
import time

temp__ = datetime.datetime.now()

"""
def log_maker():
    for i in range(len(rsi_20)):
        if str(rsi_20[i]) == 'nan' or str(rsi_10[i]) == 'nan':
            continue

        if len(price) == 0:
            if rsi_20[i] < _temp25:
                price.append(_temp[i][4])
        else:
            if rsi_10[i] > 50:
                earning = 100 * (ohlcv[i][4] / price[0] * Slippage- 1)
                price.clear()
                buy_sell_log.append(earning)
"""


def log_maker():
    for i in range(len(rsi_20)):
        if str(rsi_20[i]) == "nan" or str(rsi_10[i]) == "nan":
            continue

        if len(price) == 0:
            if rsi_20[i] < 19:
                price.append(ohlcv_temp[i][4])
        else:
            if rsi_10[i] > 38:
                earning = 100 * (ohlcv_temp[i][4] / price[0] * Slippage - 1)
                # earning = 100 * (price[0] / ohlcv_temp[i][4] * Slippage- 1)
                price.clear()
                buy_sell_log.append(earning)


def get_perfomance(trade_log):
    if len(trade_log) == 0:
        return None
    win = []
    lose = []
    risk_free = 0.038 / 365
    avg = np.mean(trade_log)
    std = np.std(trade_log)
    size = (avg - risk_free) / (std * std)

    for i in range(len(trade_log)):
        if trade_log[i] > 0:
            win.append(trade_log[i])
        elif trade_log[i] < 0:
            lose.append(trade_log[i])

    print("총거래 : ", len(trade_log))
    print("수익거래수 :", len(win))
    print("손실거래수 :", len(lose))
    print("평균거래 :", avg)
    print("평균수익거래 :", np.mean(win))
    print("평균손실거래 :", np.mean(lose))
    print("평균손익비 :", -1 * np.mean(win) / np.mean(lose))
    print("승률 :", int(round(len(win) / len(trade_log), 2) * 100), "%")
    print("포지션 사이징 :", size)
    if len(lose) > 0:
        print("최대 손실 :", min(lose))
    print("")


def calculate(ticker, time_):
    while True:
        try:
            ohlcv_temp = binance.fetch_ohlcv(ticker, "5m", binance.parse8601(time_))
            timestamp = ohlcv_temp[0][0] - 182500000
            datetimeobj = str(datetime.datetime.fromtimestamp(timestamp / 1000))
            time_ = datetimeobj[0:10] + "T" + datetimeobj[11:19]
            ohlcv_temp.reverse()
            ohlcv.extend(ohlcv_temp)
        except:
            print(" ")
            return None


def custom_convert(ohlcv5):  # convert 5m → 15m
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


binance = ccxt.binance()


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


# --------------------------------------


all_tickers = list(binance.fetch_tickers().keys())

all_tickers = list(set(all_tickers) - set(["DOTECOUSDT"]))

print(len(all_tickers))

all_ohlcv = []
start = str(
    datetime.datetime.fromtimestamp(
        binance.fetch_ohlcv("BTC/USDT", "5m")[-220][0] / 1000
    )
)
start = start[0:10] + "T" + start[11:19]

for i in range(len(all_tickers)):
    print(i)
    ohlcv = []
    calculate(all_tickers[i], start)
    ohlcv.reverse()
    ohlcv = custom_convert(ohlcv)
    all_ohlcv.append(ohlcv)


# --------------------------------------

buy_sell_log = []

for i in range(len(all_tickers)):

    print(all_tickers[i])

    ohlcv_temp = all_ohlcv[i]

    Slippage = 0.9992 * 0.9992

    buy_sell_log = []
    price = []

    # df = pd.DataFrame(data=np.array(ohlcv_temp), columns=['time_stamp','open', 'high', 'low', 'close', 'volume'])
    df = pd.DataFrame(
        data=np.array(ohlcv_temp),
        columns=["time_stamp", "open", "high", "low", "close"],
    )

    rsi_20 = df.ta.rsi(length=20)
    rsi_20 = rsi_20.values.tolist()

    rsi_10 = df.ta.rsi(length=10)
    rsi_10 = rsi_10.values.tolist()

    log_maker()
    get_perfomance(buy_sell_log)

import pandas as pd
import numpy as np
import pandas_ta as ta
import ccxt
import datetime
import time


binance = ccxt.binance()


def log_maker(name_, ohlcv_temp, rsi_entry, rsi_exit):
    ohlcv_ = ohlcv_temp[-384:]
    rsi_20 = rsi_entry[-384:]
    rsi_10 = rsi_exit[-384:]

    for i in range(len(rsi_20)):
        if str(rsi_20[i]) == "nan" or str(rsi_10[i]) == "nan":
            continue

        if len(price) == 0:
            if rsi_20[i] < 19:
                price.append(ohlcv_[i][4])
        else:
            if rsi_10[i] > 38:
                earning = 100 * (ohlcv_[i][4] / price[0] * Slippage - 1)
                price.clear()
                buy_sell_log.append(earning)

                name_save.append(name_)

    if len(price) != 0:
        earning = 100 * (ohlcv_[-1][4] / price[0] * Slippage - 1)
        price.clear()
        buy_sell_log.append(earning)
        name_save.append(name_)


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


def custom_convert(ohlcv5):  # convert 5m → 15m
    if len(ohlcv5) < 2000:
        return None
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


def calculate(ticker, time_):
    for i in range(5):
        try:
            ohlcv_temp = binance.fetch_ohlcv(ticker, "5m", binance.parse8601(time_))
            timestamp = ohlcv_temp[0][0] - 182500000
            datetimeobj = str(datetime.datetime.fromtimestamp(timestamp / 1000))
            time_ = datetimeobj[0:10] + "T" + datetimeobj[11:19]
            ohlcv_temp.reverse()
            ohlcv.extend(ohlcv_temp)
        except:
            abcedfg = 0
            return None


"""
all_tickers = list(binance.fetch_tickers().keys())

all_tickers = list(set(all_tickers) - set(['YFIDOWN/USDT','UNIDOWN/USDT','DOTDOWN/USDT','BNBBULL/USDT', 'BNBDOWN/USDT', 'LINKDOWN/USDT', 'SXPDOWN/USDT']))

# all_tickers = [all_tickers[i] for i in range(len(all_tickers)) if '/ETH' in all_tickers[i] or '/BTC' in all_tickers[i] or '/USDT' in all_tickers[i] or '/BUSD' in all_tickers[i] or '/BNB' in all_tickers[i]]
# all_tickers = [all_tickers[i] for i in range(len(all_tickers)) if '/ETH' in all_tickers[i] or '/USDT' in all_tickers[i] or '/BUSD' in all_tickers[i] or '/BNB' in all_tickers[i]]
all_tickers = [all_tickers[i] for i in range(len(all_tickers)) if '/BUSD' in all_tickers[i]]



print(len(all_tickers))
all_ohlcv = []
buy_sell_log = []
name_save = []

all_tickers_final = []

for i in range(len(all_tickers)):
    flag = custom_convert('ETH/BUSD')
    _temp = custom_convert(all_tickers[i])
    if _temp[-1][0] == flag[-1][0]:
        all_ohlcv.append(_temp)
        all_tickers_final.append(all_tickers[i])

print(len(all_ohlcv))

"""


# --------------------------------------

all_tickers = list(binance.fetch_tickers().keys())

# all_tickers = [all_tickers[i] for i in range(len(all_tickers)) if '/ETH' in all_tickers[i] or '/BTC' in all_tickers[i] or '/USDT' in all_tickers[i] or '/BUSD' in all_tickers[i] or '/BNB' in all_tickers[i]]
all_tickers = [
    all_tickers[i]
    for i in range(len(all_tickers))
    if "/ETH" in all_tickers[i] or "/BUSD" in all_tickers[i] or "/BNB" in all_tickers[i]
]

# all_tickers = [all_tickers[i] for i in range(len(all_tickers)) if '/BTC' in all_tickers[i]]

print(len(all_tickers))

all_ohlcv = []
start = str(
    datetime.datetime.fromtimestamp(
        binance.fetch_ohlcv("BTC/USDT", "5m")[-220][0] / 1000
    )
)
start = start[0:10] + "T" + start[11:19]

all_tickers_final = []
buy_sell_log = []
name_save = []

for i in range(len(all_tickers)):
    ohlcv = []
    calculate(all_tickers[i], start)
    ohlcv.reverse()
    ohlcv = custom_convert(ohlcv)
    if ohlcv != None:
        # 703
        all_tickers_final.append(all_tickers[i])
        all_ohlcv.append(ohlcv)
# --------------------------------------


for i in range(len(all_ohlcv)):

    ohlcv_temp = all_ohlcv[i]

    Slippage = 0.9992 * 0.9992

    price = []

    # df = pd.DataFrame(data=np.array(ohlcv_temp), columns=['time_stamp','open', 'high', 'low', 'close', 'volume'])
    df = pd.DataFrame(
        data=np.array(ohlcv_temp), columns=["time_stamp", "open", "close", "low", "1"]
    )

    # rsi_20 = df.ta.rsi(length=10)
    rsi_20 = df.ta.rsi(length=10)
    rsi_20 = rsi_20.values.tolist()

    df = pd.DataFrame(
        data=np.array(ohlcv_temp), columns=["time_stamp", "open", "high", "close", "1"]
    )

    # rsi_10 = df.ta.rsi(length=5)
    rsi_10 = df.ta.rsi(length=5)
    rsi_10 = rsi_10.values.tolist()

    log_maker(all_tickers_final[i], ohlcv_temp, rsi_20, rsi_10)


get_perfomance(buy_sell_log)
print(name_save)
print(len(name_save))

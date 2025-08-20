import ccxt
import time
import os
import numpy as np
import pandas as pd
import datetime
import pandas_ta as ta
import os


exchange_class = getattr(ccxt, "binance")
binance = exchange_class()
binance.enableRateLimit = True
binance.RateLimit = 10000
binance.apiKey = "FRbVseExyAWjQUtYFnS4memLnPCcgNAeRW7HEBrrw9qyIyPUMCTzUKxZKOJIHcfV"
binance.secret = "CbDX3DE5r9ErdLBOphDB4rjCaAaKbUqITbNK05YIitktZ24VfcNrvVRbIgfK6L87"
binance.load_markets()


def timestamp_to_datetime(timestamp):
    datetimeobj = datetime.datetime.fromtimestamp(timestamp / 1000)
    return datetimeobj


def log_maker(name_, ohlcv_temp, rsi_entry, rsi_exit):
    price = []

    for i in range(len(rsi_entry)):
        if (
            str(rsi_entry[i]) == "nan"
            or str(rsi_exit[i]) == "nan"
            or rsi_exit[i] == None
        ):
            continue

        if len(price) == 0:
            if rsi_entry[i] < 19:
                price.append(ohlcv_temp[i][4])
        else:
            if rsi_exit[i] > 38:
                earning = 100 * (ohlcv_temp[i][4] / price[0] * Slippage - 1)
                price.clear()
                buy_sell_log.append(earning)

                name_save.append(name_)

    if len(price) != 0:
        earning = 100 * (ohlcv_temp[-1][4] / price[0] * Slippage - 1)
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
    # if len(ohlcv5) < 2000:
    #     return None
    # ohlcv5 = binance.fetch_ohlcv(ticker, "5m")

    if len(ohlcv5) == 0:
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
    """
    if int(temp) % 15 == 0:
        ohlcv15.append([ohlcv5[-1][0], ohlcv5[-2][1], max([ohlcv5[-1][2], ohlcv5[-2][2]]), min([ohlcv5[-1][3], ohlcv5[-2][3]]), ohlcv5[-1][4]])
    
    if int(temp) % 15 == 10:
        ohlcv15.append(ohlcv5[-1][:-1])
    """
    return ohlcv15


All_ohlcv = []
price = []
buy_sell_log = []
name_save = []
all_tickers_final = []
time_frame = "5m"
ticker_list = list(binance.fetch_tickers().keys())
ticker_list = [
    ticker_list[i]
    for i in range(len(ticker_list))
    if "/ETH" in ticker_list[i] or "/BUSD" in ticker_list[i] or "/BNB" in ticker_list[i]
]
Slippage = 0.9992 * 0.9992

for j in range(2, 200, 2):
    print(j, "일 전 부터", j - 2, "일 전 까지")

    day = j
    temp_time = str(
        timestamp_to_datetime(binance.fetch_ohlcv("BTC/USDT", "1d")[-day - 2][0])
    )
    convert = temp_time[:10] + "T" + temp_time[11:19] + "Z"
    timestamp = binance.parse8601(convert)

    for i in range(len(ticker_list)):
        try:
            temp = custom_convert(
                binance.fetch_ohlcv(ticker_list[i], time_frame, timestamp)
            )
            all_tickers_final.append(ticker_list[i])
            All_ohlcv.append(temp)
        except:
            time.sleep(0.5)
            print(ticker_list[i])

    for i in range(len(All_ohlcv)):
        ohlcv_temp = All_ohlcv[i]

        if ohlcv_temp == None:
            continue

        df = pd.DataFrame(
            data=np.array(ohlcv_temp),
            columns=["time_stamp", "open", "close", "low", "1"],
        )
        rsi_entry = df.ta.rsi(length=10).tolist()

        df = pd.DataFrame(
            data=np.array(ohlcv_temp),
            columns=["time_stamp", "open", "high", "close", "1"],
        )
        rsi_exit = df.ta.rsi(length=5).tolist()

        log_maker(all_tickers_final[i], ohlcv_temp[20:], rsi_entry[20:], rsi_exit[20:])

    get_perfomance(buy_sell_log)
    print(name_save)
    print(len(name_save))

    All_ohlcv.clear()
    price.clear()
    buy_sell_log.clear()
    name_save.clear()
    all_tickers_final.clear()

import ccxt
import time
import os
import numpy as np
import pandas as pd
import datetime
import pandas_ta as ta
import os
from pprint import pprint


def timestamp_to_datetime(timestamp):
    datetimeobj = datetime.datetime.fromtimestamp(timestamp / 1000)
    original_time_data = str(datetimeobj)
    entry_time_data = str(datetimeobj)[11:-3]
    exit_time_data = str(datetimeobj)[5:-3]
    return entry_time_data, exit_time_data, original_time_data


def log_maker(name_, ohlcv_temp, rsi_entry, rsi_exit):
    price = 0
    entry_time_buffer = []

    for i in range(len(rsi_entry) - 1):
        if (
            str(rsi_entry[i]) == "nan"
            or str(rsi_exit[i]) == "nan"
            or rsi_exit[i] == None
        ):
            continue

        if price == 0:
            if rsi_entry[i] < 19:
                price = ohlcv_temp[i + 1][1]
                entry_time_buffer.append(timestamp_to_datetime(ohlcv_temp[i + 1][0])[1])
        else:
            if rsi_exit[i] > 38:
                earning = 100 * (ohlcv_temp[i + 1][1] / price * Slippage - 1)
                buy_sell_log.append(earning)
                exit_time = timestamp_to_datetime(ohlcv_temp[i + 1][0])[0]
                name_save.append("0")
                print(
                    name_
                    + "  "
                    + entry_time_buffer[0][:5]
                    + "  buy : "
                    + entry_time_buffer[0][6:]
                    + "  // sell : "
                    + exit_time
                    + "  "
                    + str(earning)
                )
                entry_time_buffer.clear()
                price = 0

    if price != 0:
        earning = 100 * (ohlcv_temp[-1][4] / price * Slippage - 1)
        buy_sell_log.append(earning)
        exit_time = timestamp_to_datetime(ohlcv_temp[i + 1][0])[0]
        name_save.append("0")
        print(
            name_
            + "  "
            + entry_time_buffer[0][:5]
            + "  buy : "
            + entry_time_buffer[0][6:]
            + "  // sell : "
            + exit_time
            + "  "
            + str(earning)
        )
        entry_time_buffer.clear()
        price = 0
        return None


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
        # print(lose)
        print("최대 손실 :", min(lose))
    print("")


def custom_convert(ohlcv5):  # convert 5m → 15m
    # if len(ohlcv5) < 2000:
    #     return None

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
    return ohlcv15


def get_ticker_list():
    temp_list = list(binance.fetch_tickers().keys())
    temp_list = [
        temp_list[i]
        for i in range(len(temp_list))
        if "/ETH" in temp_list[i] or "/BUSD" in temp_list[i] or "/BNB" in temp_list[i]
    ]
    std_time_data = binance.fetch_ohlcv("BTC/USDT", "1d")[-1][0]
    result_ = [
        temp_list[i]
        for i in range(len(temp_list))
        if binance.fetch_ohlcv(temp_list[i], "1d")[-1][0] == std_time_data
        and len(binance.fetch_ohlcv(temp_list[i], "1d")) > 200
    ]  # 상폐 종목 제외, 데이터 200일 이상 보유
    return result_


"""
def get_ticker_list():
    temp_list = list(binance.fetch_tickers().keys())
    temp_list = [temp_list[i] for i in range(len(temp_list)) if '/ETH' in temp_list[i] or '/BUSD' in temp_list[i]]
    std_time_data = binance.fetch_ohlcv('BTC/USDT', '1d')[-1][0]
    result_ = [temp_list[i] for i in range(len(temp_list)) if binance.fetch_ohlcv(temp_list[i], '1d')[-1][0] == std_time_data] # 상폐 종목 제외
    return result_
"""

exchange_class = getattr(ccxt, "binance")
binance = exchange_class()
binance.enableRateLimit = True
binance.RateLimit = 10000
# binance.apiKey = 'key'
# binance.secret = 'key'
binance.load_markets()


All_ohlcv = []
price = []
buy_sell_log = []
name_save = []
all_tickers_final = []
time_frame = "5m"
Slippage = 0.9992 * 0.9992
ticker_list = get_ticker_list()


# ticker_list = ['BTC/USDT', 'BNB/BUSD', 'XRP/BTC']


print(len(ticker_list))


for j in range(2, 200):
    print(j, "일 전 부터", j - 1, "일 전 까지")

    day = j
    # temp_time = timestamp_to_datetime(binance.fetch_ohlcv('BTC/USDT','1d')[-day-2][0])[2]
    temp_time = timestamp_to_datetime(
        binance.fetch_ohlcv("BTC/USDT", "1d")[-day - 2][0] - 9300000
    )[2]
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
            data=np.array(ohlcv_temp), columns=["0", "0", "close", "0", "0"]
        )  ## rsi(10, high)
        rsi_entry = df.ta.rsi(length=10).tolist()

        df = pd.DataFrame(
            data=np.array(ohlcv_temp), columns=["0", "0", "0", "close", "0"]
        )  ## rsi(5, low)
        rsi_exit = df.ta.rsi(length=5).tolist()
        # log_maker(all_tickers_final[i], ohlcv_temp[20:],rsi_entry[20:], rsi_exit[20:])
        log_maker(all_tickers_final[i], ohlcv_temp[70:], rsi_entry[70:], rsi_exit[70:])

    get_perfomance(buy_sell_log)
    All_ohlcv.clear()
    buy_sell_log.clear()
    name_save.clear()
    all_tickers_final.clear()
    # print(len(name_save))
    print("")

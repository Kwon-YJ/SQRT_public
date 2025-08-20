import matplotlib.pyplot as plt
import numpy as np
import datetime
import ccxt
import time
import os


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

binance = ccxt.binance({"enableRateLimit": True, "options": {"defaultType": "future"}})
binance.enableRateLimit = True
binance.RateLimit = 10000
binance.apiKey = "Wofk7BIStGtvLeCLCIbXVAbxl3KAy03BHafkmGtVqOILF8FZKonaSxqIPCzK4j6i"
binance.secret = "n91lmhQJCOB1ZySmbuTeuefoFlytnnAkjivYazRF1DW4x22v34RN3LXEq5OlHZtR"
binance.load_markets()


All_ohlcv = []
price = []
buy_sell_log = []
name_save = []
all_tickers_final = []
time_frame = "5m"

# ticker_list = get_ticker_list()


# ticker_list = ['BTC/USDT', 'BNB/BUSD', 'XRP/BTC']

# ticker_list = ['BTC/USDT']

ticker = "XRP/USDT"

result = []

for j in range(150, 200):
    print(j, "일 전 부터", j - 1, "일 전 까지")

    day = j
    temp_time = timestamp_to_datetime(
        binance.fetch_ohlcv("BTC/USDT", "1d")[-day - 2][0] - 9300000
    )[2]
    convert = temp_time[:10] + "T" + temp_time[11:19] + "Z"
    timestamp = binance.parse8601(convert)

    temp = custom_convert(binance.fetch_ohlcv(ticker, time_frame, timestamp))[70:]
    # print(float(temp[6][1]) - float(temp[0][1]))
    result.append(float(temp[1][1]) - float(temp[0][1]))

up = []
down = []
for i in range(len(result)):
    temp = result[i]
    if temp > 0:
        up.append(temp)
    else:
        down.append(temp)
    plt.scatter(i, temp)

print(len(up) / (len(up) + len(down)))
print(sum(up + down))
plt.axhline(y=0, color="r", linewidth=1)

plt.show()

"""
0 = 0900
1 = 0915
2 = 0930
3 = 0945
4 = 1000
5 = 1015
6 = 1030
"""

import ccxt
import time
import numpy as np
import pandas as pd
import datetime
import pandas_ta as ta

temp_temp = []

count = []


def TW(odd):
    return np.round(-np.log(0.99) / (np.log(1 + 0.01 * odd) - np.log(0.99)), 4)


def shortest_distance(odd, winrate, n=100000):
    lins = np.linspace(0, 10, n)
    y = TW(lins)
    least_distance = 1e100
    for i in range(n):
        dx = lins[i] - odd
        dy = y[i] - winrate
        distance = np.sqrt(dx**2 + dy**2)
        if distance < least_distance:
            least_distance = distance
    if winrate > TW(odd):
        return np.round(least_distance, 10)
    else:
        return -1 * np.round(least_distance, 10)


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
            # if rsi_entry[i] < 19:
            # if rsi_entry[i] < 15:
            # if rsi_entry[i] < 17.5:
            # if rsi_entry[i-1] < 25 and ohlcv_temp[i][1] > ohlcv_temp[i][4] and ohlcv_temp[i][5] > ohlcv_temp[i-1][5] and ohlcv_temp[i][5] > ohlcv_temp[i-2][5] and rsi_entry[i-2] > 25:
            # if rsi_entry[i-1] < 25 and ohlcv_temp[i][1] > ohlcv_temp[i][4] and ohlcv_temp[i][5] > ohlcv_temp[i-1][5] and ohlcv_temp[i][5] > ohlcv_temp[i-2][5] and rsi_entry[i-2] > 24:
            if (
                rsi_entry[i - 1] < 23
                and ohlcv_temp[i][1] > ohlcv_temp[i][4]
                and ohlcv_temp[i][5] > ohlcv_temp[i - 1][5]
                and ohlcv_temp[i][5] > ohlcv_temp[i - 2][5]
            ):
                price = ohlcv_temp[i + 1][1]
                entry_time_buffer.append(timestamp_to_datetime(ohlcv_temp[i + 1][0])[1])
        else:
            if rsi_exit[i] > 38:
                earning = 100 * (ohlcv_temp[i + 1][1] / price * Slippage - 1)
                buy_sell_log.append(earning)
                temp_temp.append(earning)
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
        temp_temp.append(earning)
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
        count.append(0)
        return None

    count.append(len(trade_log))

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
    avg_W_L_ratio = -1 * np.mean(win) / np.mean(lose)
    print("평균손익비 :", avg_W_L_ratio)
    win_rate = int(round(len(win) / len(trade_log), 2) * 100)
    print("승률 :", win_rate, "%")
    print("포지션 사이징 :", size)
    if len(lose) > 0:
        # print(lose)
        print("최대 손실 :", min(lose))
    total_perform = shortest_distance(avg_W_L_ratio, len(win) / len(trade_log))
    print(total_perform)
    chart_data.append(total_perform)
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
            ohlcv5[i][5] + ohlcv5[i + 1][5] + ohlcv5[i + 2][5],
        ]
        ohlcv15.append(candle)
    return ohlcv15


exchange_class = getattr(ccxt, "bithumb")
binance = exchange_class()
binance.enableRateLimit = True
binance.RateLimit = 10000
# binance.apiKey = 'key'
# binance.secret = 'key'
binance.load_markets()

chart_data = []

All_ohlcv = []
price = []
buy_sell_log = []
name_save = []
all_tickers_final = []
time_frame = "5m"
# Slippage = 0.9992 * 0.9992
Slippage = 0.9982 * 0.9982
# Slippage = 0.9952 * 0.9952


# ticker_list = list(binance.fetch_tickers().keys())

# ticker_list = [s for s in ticker_list if '/KRW' in s]

ticker_list = [
    "BTC/KRW",
    "ETH/KRW",
    "LTC/KRW",
    "ETC/KRW",
    "XRP/KRW",
    "BCH/KRW",
    "QTUM/KRW",
    "BTG/KRW",
    "EOS/KRW",
    "ICX/KRW",
    "TRX/KRW",
    "ELF/KRW",
    "OMG/KRW",
    "KNC/KRW",
    "GLM/KRW",
    "ZIL/KRW",
    "WAXP/KRW",
    "POWR/KRW",
    "LRC/KRW",
    "STEEM/KRW",
    "STRAX/KRW",
    "ZRX/KRW",
    "REP/KRW",
    "XEM/KRW",
    "SNT/KRW",
    "ADA/KRW",
    "CTXC/KRW",
    "BAT/KRW",
    "WTC/KRW",
    "THETA/KRW",
    "LOOM/KRW",
    "WAVES/KRW",
    "TRUE/KRW",
    "LINK/KRW",
    "ENJ/KRW",
    "VET/KRW",
    "MTL/KRW",
    "IOST/KRW",
    "TMTG/KRW",
    "QKC/KRW",
    "HDAC/KRW",
    "AMO/KRW",
    "BSV/KRW",
    "ORBS/KRW",
    "TFUEL/KRW",
    "VALOR/KRW",
    "CON/KRW",
    "ANKR/KRW",
    "MIX/KRW",
    "CRO/KRW",
    "FX/KRW",
    "CHR/KRW",
    "MBL/KRW",
    "MXC/KRW",
    "FCT/KRW",
    "TRV/KRW",
    "DAD/KRW",
    "WOM/KRW",
    "EM/KRW",
    "BOA/KRW",
    "FLETA/KRW",
    "SXP/KRW",
    "COS/KRW",
    "APIX/KRW",
    "EL/KRW",
    "BASIC/KRW",
    "HIVE/KRW",
    "XPR/KRW",
    "VRA/KRW",
    "FIT/KRW",
    "EGG/KRW",
    "BORA/KRW",
    "ARPA/KRW",
    "APM/KRW",
    "CKB/KRW",
    "AERGO/KRW",
    "ANW/KRW",
    "CENNZ/KRW",
    "EVZ/KRW",
    "CYCLUB/KRW",
    "SRM/KRW",
    "QTCON/KRW",
    "UNI/KRW",
    "YFI/KRW",
    "UMA/KRW",
    "AAVE/KRW",
    "COMP/KRW",
    "REN/KRW",
    "BAL/KRW",
    "RSR/KRW",
    "NMR/KRW",
    "RLC/KRW",
    "UOS/KRW",
    "SAND/KRW",
    "GOM2/KRW",
    "RINGX/KRW",
    "BEL/KRW",
    "OBSR/KRW",
    "ORC/KRW",
    "POLA/KRW",
    "AWO/KRW",
    "ADP/KRW",
    "DVI/KRW",
    "GHX/KRW",
    "MVC/KRW",
    "BLY/KRW",
    "WOZX/KRW",
    "ANV/KRW",
    "GRT/KRW",
    "MM/KRW",
    "BIOT/KRW",
    "XNO/KRW",
    "SNX/KRW",
    "RAI/KRW",
    "COLA/KRW",
    "NU/KRW",
    "OXT/KRW",
    "LINA/KRW",
    "MAP/KRW",
    "AQT/KRW",
    "WIKEN/KRW",
    "CTSI/KRW",
    "MANA/KRW",
    "LPT/KRW",
    "MKR/KRW",
    "SUSHI/KRW",
    "ASM/KRW",
    "PUNDIX/KRW",
    "CELR/KRW",
    "LF/KRW",
    "ARW/KRW",
    "MSB/KRW",
    "RLY/KRW",
    "OCEAN/KRW",
    "BFC/KRW",
    "ALICE/KRW",
    "CAKE/KRW",
    "BNT/KRW",
    "XVS/KRW",
    "CHZ/KRW",
    "AXS/KRW",
    "DAI/KRW",
    "MATIC/KRW",
    "BAKE/KRW",
    "VELO/KRW",
    "BCD/KRW",
    "XLM/KRW",
    "GXC/KRW",
    "BTT/KRW",
    "VSYS/KRW",
    "IPX/KRW",
    "WICC/KRW",
    "ONT/KRW",
    "LUNA/KRW",
    "AION/KRW",
    "META/KRW",
    "KLAY/KRW",
    "ONG/KRW",
    "ALGO/KRW",
    "JST/KRW",
    "XTZ/KRW",
    "MLK/KRW",
    "WEMIX/KRW",
    "DOT/KRW",
    "ATOM/KRW",
    "SSX/KRW",
    "TEMCO/KRW",
    "HIBS/KRW",
    "BURGER/KRW",
    "DOGE/KRW",
    "KSM/KRW",
    "CTK/KRW",
    "XYM/KRW",
    "BNB/KRW",
    "SUN/KRW",
    "XEC/KRW",
    "PCI/KRW",
    "SOL/KRW",
]


for j in range(2, 10):
    print(j, "일 전 부터", j - 1, "일 전 까지")

    day = j
    temp_time = timestamp_to_datetime(
        binance.fetch_ohlcv("BTC/KRW", "1d")[-day - 2][0] - 9300000
    )[2]
    convert = temp_time[:10] + "T" + temp_time[11:19] + "Z"
    timestamp = binance.parse8601(convert)

    for i in range(len(ticker_list)):
        # try:
        # print(ticker_list[i])
        temp = custom_convert(
            binance.fetch_ohlcv(ticker_list[i], time_frame, timestamp)
        )
        # print(len(temp))
        all_tickers_final.append(ticker_list[i])
        All_ohlcv.append(temp)
        # except:
        #    time.sleep(0.5)
        #    print(ticker_list[i])

    for i in range(len(All_ohlcv)):
        ohlcv_temp = All_ohlcv[i]

        if ohlcv_temp == None:
            print("?")
            continue

        # df = pd.DataFrame(data=np.array(ohlcv_temp), columns=['0','0', 'close', '0', '0']) ## rsi(15, high)
        df = pd.DataFrame(
            data=np.array(ohlcv_temp), columns=["0", "0", "close", "0", "0", "0"]
        )  ## rsi(15, high)
        rsi_entry = df.ta.rsi(length=15).tolist()

        df = pd.DataFrame(
            data=np.array(ohlcv_temp), columns=["0", "0", "0", "close", "0", "0"]
        )  ## rsi(8, low)
        rsi_exit = df.ta.rsi(length=8).tolist()
        log_maker(all_tickers_final[i], ohlcv_temp[70:], rsi_entry[70:], rsi_exit[70:])

    get_perfomance(buy_sell_log)
    get_perfomance(temp_temp)
    All_ohlcv.clear()
    buy_sell_log.clear()
    name_save.clear()
    all_tickers_final.clear()
    print("")

print(count)

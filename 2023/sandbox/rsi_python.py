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
            if rsi_entry[i] < 19:
                # if rsi_entry[i] < 15:
                # if rsi_entry[i] < 17.5:
                # if rsi_entry[i-1] < 25 and ohlcv_temp[i][1] > ohlcv_temp[i][4] and ohlcv_temp[i][5] > ohlcv_temp[i-1][5] and ohlcv_temp[i][5] > ohlcv_temp[i-2][5] and rsi_entry[i-2] > 25:
                # if rsi_entry[i-1] < 25 and ohlcv_temp[i][1] > ohlcv_temp[i][4] and ohlcv_temp[i][5] > ohlcv_temp[i-1][5] and ohlcv_temp[i][5] > ohlcv_temp[i-2][5] and rsi_entry[i-2] > 24:

                # if rsi_entry[i-1] < 21 and ohlcv_temp[i][1] > ohlcv_temp[i][4] and ohlcv_temp[i][5] > ohlcv_temp[i-1][5] and ohlcv_temp[i][5] > ohlcv_temp[i-2][5]:
                # if rsi_entry[i-1] < 23 and ohlcv_temp[i][1] > ohlcv_temp[i][4] and ohlcv_temp[i][5] > ohlcv_temp[i-1][5] and ohlcv_temp[i][5] > ohlcv_temp[i-2][5]:
                # if rsi_entry[i-1] < 19 and ohlcv_temp[i][1] > ohlcv_temp[i][4] and ohlcv_temp[i][5] > ohlcv_temp[i-1][5] and ohlcv_temp[i][5] > ohlcv_temp[i-2][5]:
                # if rsi_entry[i-1] < 25 and ohlcv_temp[i][1] > ohlcv_temp[i][4] and ohlcv_temp[i][5] > ohlcv_temp[i-1][5] and ohlcv_temp[i][5] > ohlcv_temp[i-2][5]:
                # if rsi_entry[i-1] < 27 and ohlcv_temp[i][1] > ohlcv_temp[i][4] and ohlcv_temp[i][5] > ohlcv_temp[i-1][5] and ohlcv_temp[i][5] > ohlcv_temp[i-2][5]:

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


exchange_class = getattr(ccxt, "binance")
binance = exchange_class()
binance.enableRateLimit = False
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


# ticker_list = list(set(ticker_list) - set(['AUD/USDT', 'BRL/USDT', 'EUR/USDT', 'GBP/USDT', 'RUB/USDT', 'TRY/USDT', 'TUSD/USDT', 'USDC/USDT', 'PAX/USDT', 'BIDR/USDT', 'DAI/USDT', 'IDRT/USDT', 'UAH/USDT', 'NGN/USDT', 'VAI/USDT', 'BNVD/USDT']))

# ticker_list = ['BTC/USDT', 'AUD/USDT', 'BCH/USDT', 'DOGE/USDT', 'ETH/USDT', 'GBP/USDT', 'EUR/USDT', 'EOS/USDT', 'BUSD/USDT', 'PAX/USDT', 'TUSD/USDT', 'USDC/USDT', 'XRP/USDT', 'LTC/USDT', 'TRX/USDT', 'BNB/USDT', 'DOT/USDT', 'CAKE/USDT', 'ADA/USDT', 'LINK/USDT', 'FIL/USDT', 'XMR/USDT', 'MDX/USDT', 'ETC/USDT', 'XLM/USDT', 'THETA/USDT', 'UNI/USDT', 'SXP/USDT', 'AAVE/USDT', 'MATIC/USDT', 'CHZ/USDT', 'ZEN/USDT', 'PUNDIX/USDT', 'SOL/USDT', 'GRT/USDT', 'NEO/USDT', 'NEAR/USDT', 'ONT/USDT', 'BAT/USDT', 'ZEC/USDT', 'VET/USDT', 'REEF/USDT', 'LUNA/USDT', 'WAVES/USDT', 'HARD/USDT', 'HOT/USDT', 'ALGO/USDT', 'DASH/USDT', '1INCH/USDT', 'SNX/USDT', 'CELR/USDT', 'ATOM/USDT', 'BTT/USDT', 'IOTX/USDT', 'TRB/USDT', 'QTUM/USDT', 'ZIL/USDT', 'MIR/USDT', 'RSR/USDT', 'IOST/USDT', 'FLM/USDT', 'ENJ/USDT', 'RUNE/USDT', 'XTZ/USDT', 'SUSHI/USDT', 'MANA/USDT', 'ANKR/USDT', 'OMG/USDT', 'BNT/USDT', 'FTM/USDT', 'CRV/USDT', 'SHIB/USDT', 'ICP/USDT', 'BAND/USDT', 'PAXG/USDT', 'MKR/USDT', 'ALPHA/USDT', 'ALICE/USDT', 'BAR/USDT', 'KSM/USDT', 'HBAR/USDT', 'JST/USDT', 'COMP/USDT', 'YFI/USDT', 'EGLD/USDT', 'OCEAN/USDT', 'AVAX/USDT', 'SC/USDT', 'XVS/USDT', 'DODO/USDT', 'BAL/USDT', 'WIN/USDT', 'ANT/USDT', 'VTHO/USDT', 'SRM/USDT', 'XEM/USDT', 'AXS/USDT', 'KAVA/USDT', 'YFII/USDT', 'ICX/USDT', 'AUDIO/USDT', 'RVN/USDT', 'ONE/USDT', 'SAND/USDT', 'IOTA/USDT', 'BAKE/USDT', 'TRU/USDT', 'OGN/USDT', 'DGB/USDT', 'FTT/USDT', 'RLC/USDT', 'CTSI/USDT', 'CELO/USDT', 'MTL/USDT', 'COTI/USDT', 'FET/USDT', 'CVC/USDT', 'RAMP/USDT', 'REN/USDT', 'LRC/USDT', 'ETH/BTC', 'LINK/BTC', 'MATIC/BTC', 'XRP/BTC', 'ALGO/BTC', 'SOL/BTC', 'XVS/BTC', 'BNB/BTC', 'NXS/BTC', 'CELO/BTC', 'EOS/BTC', 'LTC/BTC', 'KNC/BTC', 'ADA/BTC', 'SKL/BTC', 'GAS/BTC', 'DOT/BTC', 'FIL/BTC', 'MANA/BTC', 'ETC/BTC', 'ONT/BTC', 'XLM/BTC', 'BQX/BTC', 'CTSI/BTC', 'XTZ/BTC', 'UNI/BTC', 'ZRX/BTC', 'AVAX/BTC', 'AAVE/BTC', 'THETA/BTC', 'ATOM/BTC', 'BNT/BTC', 'GLM/BTC', 'DOGE/BTC', 'GXS/BTC', 'NAV/BTC', 'MDA/BTC', 'CHZ/BTC', 'WTC/BTC', 'LUNA/BTC', 'ICX/BTC', 'FET/BTC', 'TOMO/BTC', 'ENJ/BTC', 'VIDT/BTC', 'AGI/BTC', 'BAT/BTC', 'POWR/BTC', 'QTUM/BTC', 'GVT/BTC', 'EPS/BTC', 'NEBL/BTC', 'ZEC/BTC', 'ARDR/BTC', 'AUDIO/BTC', 'SUSHI/BTC', 'ANT/BTC', 'IOTA/BTC', 'OMG/BTC', 'LTO/BTC', 'BLZ/BTC', 'CAKE/BTC', 'OXT/BTC', 'OCEAN/BTC', 'KAVA/BTC', 'LSK/BTC', 'SRM/BTC', 'MTL/BTC', 'XEM/BTC', 'NULS/BTC', 'RUNE/BTC', 'NEO/BTC', 'EVX/BTC', 'NANO/BTC', 'WAVES/BTC', 'ARK/BTC', 'GRT/BTC', 'BAND/BTC', 'XMR/BTC', 'CTK/BTC', 'FLM/BTC', 'SNX/BTC', 'SXP/BTC', 'RLC/BTC', 'UTK/BTC', 'FTT/BTC', 'ICP/BTC', '1INCH/BTC', 'STX/BTC', 'BZRX/BTC', 'CVC/BTC', 'CRV/BTC', 'STRAX/BTC', 'SKY/BTC', 'NEAR/BTC', 'BCD/BTC', 'DODO/BTC', 'OGN/BTC', 'AVA/BTC', 'BEL/BTC', 'LRC/BTC', 'PERP/BTC', 'POLY/BTC', 'REN/BTC', 'SCRT/BTC', 'SUSD/BTC', 'INJ/BTC', 'POLS/BTC', 'ELF/BTC', 'NKN/BTC', 'STORJ/BTC', 'VIA/BTC', 'SYS/BTC', 'HBAR/BTC', 'MIR/BTC', 'KMD/BTC', 'VET/BTC', 'COTI/BTC', 'SAND/BTC', 'ZIL/BTC', 'HIVE/BTC', 'BNB/ETH', 'VET/ETH', 'XRP/ETH', 'TRX/ETH', 'LINK/ETH', 'ADA/ETH', 'DEXE/ETH', 'EOS/ETH', 'RLC/ETH', 'PROS/ETH', 'LTC/ETH', 'XLM/ETH', 'SNT/ETH', 'STMX/ETH', 'GRT/ETH', 'NEO/ETH', 'ZIL/ETH', 'QTUM/ETH', 'SLP/ETH', 'ZRX/ETH', 'THETA/ETH', 'ETC/ETH', 'LRC/ETH', 'OMG/ETH', 'HOT/ETH', 'FRONT/ETH', 'KEY/ETH', 'NANO/ETH', 'QSP/ETH', 'IOTX/ETH', 'PIVX/ETH', 'BAT/ETH', 'NAS/ETH', 'XVG/ETH', 'IOST/ETH', 'ONT/ETH', 'BQX/ETH', 'BNT/ETH', 'SCRT/ETH', 'VIB/ETH', 'WAVES/ETH', 'FUN/ETH', 'BAKE/BNB', 'CAKE/BNB', 'DOT/BNB', 'XRP/BNB', 'ADA/BNB', 'TRX/BNB', 'LTC/BNB', 'BURGER/BNB', 'LUNA/BNB', 'BTT/BNB', 'ZEN/BNB', 'SUSHI/BNB', 'HOT/BNB', 'UNI/BNB', 'CHR/BNB', 'PROM/BNB', 'ICP/BNB', 'CHZ/BNB', 'RUNE/BNB', 'VET/BNB', 'EOS/BNB', 'BAT/BNB', 'SOL/BNB', 'ATOM/BNB', 'ETC/BNB', 'FIL/BNB', 'OGN/BNB', 'MATIC/BNB', 'ENJ/BNB', 'AAVE/BNB', 'WABI/BNB', 'CELR/BNB', 'INJ/BNB', 'DIA/BNB', 'XLM/BNB', 'CTK/BNB', 'EGLD/BNB', 'NEO/BNB', 'COS/BNB', 'WRX/BNB', 'ANT/BNB', 'BAND/BNB', 'AXS/BNB', 'XVS/BNB', 'AVAX/BNB', 'FTT/BNB', 'FTM/BNB', 'RVN/BNB', 'OCEAN/BNB', 'ZEC/BNB', 'SRM/BNB', 'THETA/BNB', 'ZIL/BNB']
# ticker_list = list(set(ticker_list) - set(['AUD/USDT', 'BRL/USDT', 'EUR/USDT', 'GBP/USDT', 'RUB/USDT', 'TRY/USDT', 'TUSD/USDT', 'USDC/USDT', 'PAX/USDT', 'BIDR/USDT', 'DAI/USDT', 'IDRT/USDT', 'UAH/USDT', 'NGN/USDT', 'VAI/USDT', 'BNVD/USDT']))
# ticker_list = [ticker_list[i] for i in range(len(ticker_list)) if '/USDT' in ticker_list[i]]

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
    "AKRO/USDT",
    "CHZ/USDT",
    "SAND/USDT",
    "ANKR/USDT",
    "LUNA/USDT",
    "BTS/USDT",
    "LIT/USDT",
    "UNFI/USDT",
    "DODO/USDT",
    "REEF/USDT",
    "RVN/USDT",
    "SFP/USDT",
    "XEM/USDT",
    "COTI/USDT",
    "CHR/USDT",
    "MANA/USDT",
    "ALICE/USDT",
    "HBAR/USDT",
    "ONE/USDT",
    "LINA/USDT",
    "STMX/USDT",
    "DENT/USDT",
    "CELR/USDT",
    "HOT/USDT",
    "MTL/USDT",
    "OGN/USDT",
    "BTT/USDT",
    "NKN/USDT",
    "SC/USDT",
    "DGB/USDT",
    "ICP/USDT",
    "BAKE/USDT",
    "GTC/USDT",
    "KEEP/USDT",
]

# for j in range(1, 200):
for j in range(2, 365):
    print(j, "일 전 부터", j - 1, "일 전 까지")

    day = j
    temp_time = timestamp_to_datetime(
        binance.fetch_ohlcv("BTC/USDT", "1d")[-day - 2][0] - 9300000
    )[2]
    convert = temp_time[:10] + "T" + temp_time[11:19] + "Z"
    timestamp = binance.parse8601(convert)

    for i in range(len(ticker_list)):
        # try:
        temp = custom_convert(
            binance.fetch_ohlcv(ticker_list[i], time_frame, timestamp)
        )
        all_tickers_final.append(ticker_list[i])
        All_ohlcv.append(temp)
        # except:
        #    time.sleep(0.5)
        #    print(ticker_list[i])

    for i in range(len(All_ohlcv)):
        ohlcv_temp = All_ohlcv[i]

        if ohlcv_temp == None:
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

# %%cython

import pandas as pd
import numpy as np
import datetime
import urllib
import ccxt
import time
import json


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
    perform_value.append(total_perform)
    winrate.append(win_rate)
    print("")


def timestamp_to_datetime(timestamp):
    datetimeobj = datetime.datetime.fromtimestamp(timestamp / 1000)
    original_time_data = str(datetimeobj)
    entry_time_data = str(datetimeobj)[11:-3]
    exit_time_data = str(datetimeobj)[5:-3]
    return entry_time_data, exit_time_data, original_time_data


def log_maker():
    time_frame = "1h"
    buy_sell_log = []
    all_names = []
    all_ohlcvs = []
    all_dict = {}

    # Slippage = 0.9992 * 0.9992
    Slippage = 0.9982 * 0.9982
    # Slippage = 0.9952 * 0.9952

    # temp_time = get_ohlcv('BTC/USDT', time_frame, 1000)
    # all_times = [temp_time[i][0] for i in range(len(temp_time))]

    for i in range(len(ticker_list)):
        temp = get_ohlcv(ticker_list[i], time_frame, 1000)
        # if len(temp) != 1000:
        if int(temp[0][0]) != startTime:
            # print(len(temp))
            continue
        all_names.append(ticker_list[i])
        all_ohlcvs.append(temp)
        all_dict[ticker_list[i]] = temp

    print(len(all_names))

    for magic_number in range(0, 1000):
        a = {}
        b = {}
        c = {}
        for i in range(len(all_ohlcvs)):

            ohlcv = all_ohlcvs[i]
            open_ = ohlcv[magic_number][1]
            high_ = ohlcv[magic_number][2]
            low_ = ohlcv[magic_number][3]
            close_ = ohlcv[magic_number][4]

            if (high_ - low_) == 0:
                continue

            IBS = (close_ - low_) / (high_ - low_)
            if IBS < 0.1:
                a[all_names[i]] = close_ / open_

            open_ = ohlcv[magic_number - 1][1]
            high_ = ohlcv[magic_number - 1][2]
            low_ = ohlcv[magic_number - 1][3]
            close_ = ohlcv[magic_number - 1][4]

            if (high_ - low_) == 0:
                continue

            IBS = (close_ - low_) / (high_ - low_)

            if IBS < 0.1:
                b[all_names[i]] = close_ / open_

            open_ = ohlcv[magic_number - 2][1]
            high_ = ohlcv[magic_number - 2][2]
            low_ = ohlcv[magic_number - 2][3]
            close_ = ohlcv[magic_number - 2][4]

            if (high_ - low_) == 0:
                continue

            IBS = (close_ - low_) / (high_ - low_)

            if IBS < 0.1:
                c[all_names[i]] = close_ / open_

        # if len(a) == 0 or len(b) == 0 or len(c) == 0:
        if len(a) == 0:
            buy_sell_log.append(None)
            continue

        sort_total = sorted(a.items(), key=lambda item: item[1])

        sort_total2 = sorted(b.items(), key=lambda item: item[1])

        sort_total3 = sorted(c.items(), key=lambda item: item[1])

        buy_sell_log.append(sort_total[0][0])

        """
        if sort_total[0][1] < sort_total2[0][1] and sort_total[0][1] < sort_total3[0][1]:
            buy_sell_log.append(sort_total[0][0])
        else:
            buy_sell_log.append(None)
        """

    # buy_sell_log.reverse()
    for i in range(1, len(buy_sell_log)):
        if i == 998:
            break
        cnt = 0
        if buy_sell_log[i] != None:
            base_ohlcv = all_dict[buy_sell_log[i]]
            entry_price = base_ohlcv[i + 1][4]
            # exit_price = (base_ohlcv[i+1][1] + base_ohlcv[i+1][3]) * 0.5
            exit_price = base_ohlcv[i + 1][2]

            for j in range(1, 1000 - i):
                try:
                    cnt += 1
                    if exit_price < base_ohlcv[i + 1 + j][2]:
                        earning = 100 * (exit_price / entry_price * Slippage - 1)
                        win_earn.append(earning)
                        all_earn.append(earning)
                        success.append(cnt)

                        """
                        entry_time = timestamp_to_datetime(base_ohlcv[i+1][0])[1]
                        exit_time = timestamp_to_datetime(base_ohlcv[i+cnt][0])[1]
                        temp_all.append([buy_sell_log[i], round(earning, 2), cnt, entry_time, exit_time])
                        """

                        cnt = 0
                        break
                except:
                    earning = 100 * (base_ohlcv[-1][4] / entry_price * Slippage - 1)
                    lose_earn.append(earning)
                    all_earn.append(earning)
                    fail.append(cnt)

                    """
                    entry_time = timestamp_to_datetime(base_ohlcv[i+1][0])[1]
                    exit_time = timestamp_to_datetime(base_ohlcv[i+cnt][0])[1]
                    temp_all.append([buy_sell_log[i], round(earning, 2), cnt, entry_time, exit_time])
                    """

                    cnt = 0
                    break
    # print(success)
    # print('')
    # print(fail)
    # print('')
    # print(win_earn)
    # print('')
    # print(lose_earn)
    # print('')
    # print(all_earn)


# ccxt ex.fetch_ohlcv() 보다 훨씬 빠르게 ohlcv 얻기
def get_ohlcv(ticker="BTC/USDT", interval="1m", limit=200):
    # cdef int i = 0
    try:
        temp = ticker.split("/")
        ticker = f"{temp[0]}{temp[1]}"
        # url = f'https://api.binance.com/api/v3/klines?symbol={ticker}&interval={interval}&limit={str(limit)}'
        url = f"https://api.binance.com/api/v3/klines?symbol={ticker}&interval={interval}&startTime={startTime}&limit={str(limit)}"
        text_data = urllib.request.urlopen(url).read().decode("utf-8")
        buy_sell_log = json.loads(text_data)
    # except Exception as e:
    except Exception as e:
        print(
            e,
            "\n",
            "ccxt.base.errors.BadSymbol: binance does not have market symbol {0}".format(
                ticker
            ),
        )
        return [[0]]
    buy_sell_log = [list(map(float, buy_sell_log[i])) for i in range(len(buy_sell_log))]
    return buy_sell_log


binance = ccxt.binance(
    {
        # "options": {"defaultType": "future"},
        "timeout": 30000,
        # "apiKey":"",
        # "secret": "",
        "enableRateLimit": False,
    }
)
binance.load_markets()

ticker_list = [
    "FIO/USDT",
    "WAVES/USDT",
    "BNT/USDT",
    "TKO/USDT",
    "DODO/USDT",
    "MANA/USDT",
    "YFI/USDT",
    "SOL/USDT",
    "ZEC/USDT",
    "RVN/USDT",
    "CRV/USDT",
    "NEO/USDT",
    "SXP/USDT",
    "SNX/USDT",
    "SRM/USDT",
    "MIR/USDT",
    "IOTX/USDT",
    "ETC/USDT",
    "ADA/USDT",
    "COTI/USDT",
    "WRX/USDT",
    "AVAX/USDT",
    "EGLD/USDT",
    "DASH/USDT",
    "OGN/USDT",
    "PAXG/USDT",
    "ROSE/USDT",
    "DOT/USDT",
    "TLM/USDT",
    "MKR/USDT",
    "KSM/USDT",
    "STMX/USDT",
    "COMP/USDT",
    "KNC/USDT",
    "CHR/USDT",
    "ZEN/USDT",
    "LUNA/USDT",
    "THETA/USDT",
    "ALICE/USDT",
    "NEAR/USDT",
    "RLC/USDT",
    "BCH/USDT",
    "XEM/USDT",
    "1INCH/USDT",
    "BAND/USDT",
    "SUSHI/USDT",
    "TRX/USDT",
    "ALGO/USDT",
    "BTS/USDT",
    "RSR/USDT",
    "LIT/USDT",
    "LRC/USDT",
    "CHZ/USDT",
    "SKL/USDT",
    "GRT/USDT",
    "FTM/USDT",
    "ANKR/USDT",
    "ETH/USDT",
    "RUNE/USDT",
    "DOGE/USDT",
    "OCEAN/USDT",
    "FTT/USDT",
    "ATOM/USDT",
    "XRP/USDT",
    "AXS/USDT",
    "RAMP/USDT",
    "TWT/USDT",
    "PUNDIX/USDT",
    "MATIC/USDT",
    "EOS/USDT",
    "HOT/USDT",
    "IOTA/USDT",
    "BTT/USDT",
    "STORJ/USDT",
    "QTUM/USDT",
    "ALPHA/USDT",
    "ONE/USDT",
    "REEF/USDT",
    "SFP/USDT",
    "KAVA/USDT",
    "XMR/USDT",
    "ONT/USDT",
    "FUN/USDT",
    "HBAR/USDT",
    "AAVE/USDT",
    "XLM/USDT",
    "LINK/USDT",
    "UNI/USDT",
    "DEGO/USDT",
    "TRU/USDT",
    "BZRX/USDT",
    "OXT/USDT",
    "BNB/USDT",
    "STX/USDT",
    "LTC/USDT",
    "BTCUP/USDT",
    "OMG/USDT",
    "FIL/USDT",
    "BAT/USDT",
    "CAKE/USDT",
    "XTZ/USDT",
    "CELR/USDT",
    "ZIL/USDT",
    "BTC/USDT",
    "PERP/USDT",
    "ENJ/USDT",
    "VET/USDT",
]

# ticker_list = ['ETH/BTC', 'BNB/BTC', 'LTC/BTC', 'ADA/BTC', 'LINK/BTC', 'PPT/BTC', 'ONT/BTC', 'ZRX/BTC', 'DOT/BTC', 'XRP/BTC', 'UNI/BTC', 'PIVX/BTC', 'SUPER/BTC', 'ETC/BTC', 'SNX/BTC', 'KNC/BTC', 'EOS/BTC', 'SUSHI/BTC', 'INJ/BTC', 'QTUM/BTC', 'ATA/BTC', 'BAND/BTC', 'ZEC/BTC', 'AVAX/BTC', 'FIL/BTC', 'GAS/BTC', 'MATIC/BTC', 'XLM/BTC', 'BNT/BTC', 'DOGE/BTC', 'ENJ/BTC', 'AUDIO/BTC', 'NU/BTC', 'LSK/BTC', 'FET/BTC', 'CTSI/BTC', 'ALGO/BTC', 'THETA/BTC', 'TOMO/BTC', 'STX/BTC', 'BZRX/BTC', 'NAV/BTC', 'LUNA/BTC', 'LPT/BTC', 'OCEAN/BTC', 'SCRT/BTC', 'IOTA/BTC', 'NEAR/BTC', 'ADX/BTC', 'GLM/BTC', 'FLM/BTC', 'ATOM/BTC', 'SOL/BTC', 'NULS/BTC', 'AVA/BTC', 'NEO/BTC', 'AXS/BTC', 'MANA/BTC', 'CHZ/BTC', 'GRT/BTC', 'REN/BTC', 'WTC/BTC', 'ONG/BTC', 'ICP/BTC', 'NANO/BTC', 'BAT/BTC', 'CRV/BTC', 'RUNE/BTC', 'WABI/BTC', 'POLY/BTC', 'SXP/BTC', 'CAKE/BTC', 'MIR/BTC', 'LTO/BTC', 'ICX/BTC', 'COTI/BTC', 'TFUEL/BTC', 'SRM/BTC', 'ARK/BTC', 'LIT/BTC', 'MDX/BTC', 'KAVA/BTC', 'BLZ/BTC', 'STRAX/BTC', 'CHR/BTC', 'AION/BTC', 'OMG/BTC', '1INCH/BTC', 'WAVES/BTC', 'XTZ/BTC', 'POLS/BTC', 'OGN/BTC', 'STORJ/BTC', 'SKL/BTC', 'DIA/BTC', 'ALICE/BTC', 'XVS/BTC', 'CTK/BTC', 'MDA/BTC', 'LRC/BTC', 'NXS/BTC', 'TLM/BTC', 'FTT/BTC', 'FTM/BTC', 'UTK/BTC', 'SUSD/BTC', 'SAND/BTC', 'WRX/BTC', 'ALPHA/BTC', 'BQX/BTC', 'RLC/BTC', 'HNT/BTC', 'HIVE/BTC', 'CFX/BTC', 'UMA/BTC', 'SKY/BTC', 'FIRO/BTC', 'POWR/BTC', 'TWT/BTC', 'ANT/BTC', 'ELF/BTC', 'VET/BTC']

# ticker_list = ['BNB/ETH', 'RLC/ETH', 'XRP/ETH', 'ADA/ETH', 'TRX/ETH', 'LTC/ETH', 'VET/ETH', 'MTL/ETH', 'EOS/ETH', 'XLM/ETH', 'NEO/ETH', 'DEXE/ETH', 'ETC/ETH', 'LINK/ETH', 'OMG/ETH', 'GRT/ETH', 'ZIL/ETH', 'ENJ/ETH', 'IOST/ETH', 'THETA/ETH', 'BAT/ETH', 'MFT/ETH', 'NANO/ETH', 'LRC/ETH', 'HOT/ETH', 'QTUM/ETH', 'IOTA/ETH', 'FUN/ETH', 'ZRX/ETH', 'BQX/ETH', 'XEM/ETH', 'IOTX/ETH', 'WAVES/ETH', 'HEGIC/ETH', 'GXS/ETH', 'ELF/ETH', 'ADX/ETH', 'ICX/ETH', 'KNC/ETH', 'LOOM/ETH', 'ONT/ETH', 'STRAX/ETH']

# ticker_list = ['DOT/BNB', 'MATIC/BNB', 'VET/BNB', 'SOL/BNB', 'ADA/BNB', 'XRP/BNB', 'FIL/BNB', 'BTT/BNB', 'SPARTA/BNB', 'TRX/BNB', 'XLM/BNB', 'UNI/BNB', 'RUNE/BNB', 'LTC/BNB', 'ALGO/BNB', 'ICP/BNB', 'CHR/BNB', 'ZEN/BNB', 'LUNA/BNB', 'BAKE/BNB', 'AAVE/BNB', 'CTK/BNB', 'CTSI/BNB', 'CAKE/BNB', 'CELR/BNB', 'EOS/BNB', 'SUSHI/BNB', 'IOTA/BNB', 'AVAX/BNB', 'CHZ/BNB', 'INJ/BNB', 'ETC/BNB', 'ENJ/BNB', 'HOT/BNB', 'NEO/BNB', 'ATOM/BNB', 'THETA/BNB', 'OGN/BNB', 'XTZ/BNB', 'IQ/BNB', 'STX/BNB', 'MASK/BNB', 'WRX/BNB', 'SXP/BNB', 'NEAR/BNB', 'IOST/BNB', 'HBAR/BNB', 'ONT/BNB', 'WAVES/BNB', 'XVS/BNB', 'ANKR/BNB', 'KSM/BNB', 'EGLD/BNB', 'JST/BNB']

global startTime
# startTime = int(binance.fetch_ohlcv('BTC/USDT','1d')[-43][0])

perform_value = []
winrate = []

# temp_all = []

for day in range(1, 11):
    print(f"{day*43}일 전")
    startTime = int(binance.fetch_ohlcv("BTC/USDT", "1d")[-day * 43][0])

    success = []
    fail = []
    lose_earn = []
    win_earn = []
    all_earn = []

    print("")
    aaaa = log_maker()
    print("")
    print(success)
    print("")
    print(fail)
    get_perfomance(all_earn)
    # print('')
    # print(temp_all)


print(perform_value)
print(winrate)
print("")


# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

### 이전 값 고려
# 1h 고점 USDT [-0.0484298468, -0.0127975204, 0.1062898688, 0.1177685072, 0.1338578133, 0.0679625499, 0.0191968812, 0.047720869, 0.0426244305, 0.0445186959]
# 1h 고점 USDT [82, 84, 90, 90, 92, 90, 87, 90, 89, 89]

# 1h 중간 USDT [-0.0198395989, -0.0023085804, 0.0366284043, 0.0479275724, 0.0353391783, 0.0321545577, -0.0034611249, 0.0118378173, 0.0095005011, 0.0095583984]
# 1h 중간 USDT [93, 94, 96, 96, 98, 98, 94, 96, 95, 96]

# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

### 이전 값 고려
# 1h 고점 BTC [-0.0028956152, 0.0624045394, 0.0949077536, 0.1345273713, 0.1080408743, -0.009569056, -0.0263189711, 0.0212102297, 0.008206186, 0.0108551665]
# 1h 고점 BTC [83, 89, 90, 92, 81, 79, 79, 86, 81, 85]

# 1h 중간 BTC [-0.003339255, 0.0437715133, 0.0448071422, 0.0758772794, 0.0274469048, 0.0210255741, -0.0015802816, 0.0127248869, 0.0076247193, 0.0069409529]
# 1h 중간 BTC [92, 95, 97, 97, 97, 96, 94, 96, 96, 95]

# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

### 이전 값 고려
# 1h 고점 ETH [-0.0160402624, -0.0271212659, 0.0518653247, 0.0546642959, 0.0474941959, 0.0250297482, -0.0070992947, 0.0473004861, 0.0853857638, 0.0649715064]
# 1h 고점 ETH [86, 86, 88, 91, 92, 88, 86, 93, 94, 94]

# 1h 중간 ETH [-0.008438366, -0.0119527607, 0.0301587365, 0.0214918811, 0.0156328673, 0.011124456, -0.0067792551, 0.0270093743, 0.0466640431, 0.0430980877]
# 1h 중간 ETH [95, 94, 95, 97, 96, 94, 94, 97, 96, 94]


# -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

### 이전 값 고려
# 1h 고점 BNB [0.0311535568, -0.0541969139, 0.004830603, 0.1374070047, 0.1185190411, -0.0128185844, -0.0365182395, 0.0077544477, 0.0054502009, 0.0022665082]
# 1h 고점 BNB [89, 83, 89, 93, 94, 86, 84, 88, 87, 87]

# 1h 중간 BNB [-0.0014079809, -0.0165566492, -0.0027761915, 0.0368109038, 0.0604290149, 0.0050842167, -0.0009413147, 0.0135922153, 0.0104332484, 0.0116778236]
# 1h 중간 BNB [94, 93, 95, 97, 98, 95, 95, 96, 96, 97]

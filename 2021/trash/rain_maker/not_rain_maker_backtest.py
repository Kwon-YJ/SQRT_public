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
        if len(temp) != 1000:
            print(len(temp))
            continue
        all_names.append(ticker_list[i])
        all_ohlcvs.append(temp)
        all_dict[ticker_list[i]] = temp

    print(len(all_names))

    for magic_number in range(0, 998):
        a = {}
        b = {}
        c = {}
        for i in range(len(all_ohlcvs)):

            ohlcv = all_ohlcvs[i]
            open_ = ohlcv[-magic_number][1]
            high_ = ohlcv[-magic_number][2]
            low_ = ohlcv[-magic_number][3]
            close_ = ohlcv[-magic_number][4]

            # if (high_ - low_) == 0:
            #    continue

            # IBS = (close_ - low_) / (high_ - low_)
            # if IBS < 0.1:
            a[all_names[i]] = close_ / open_

            open_ = ohlcv[-magic_number - 1][1]
            high_ = ohlcv[-magic_number - 1][2]
            low_ = ohlcv[-magic_number - 1][3]
            close_ = ohlcv[-magic_number - 1][4]

            # if (high_ - low_) == 0:
            #    continue

            # IBS = (close_ - low_) / (high_ - low_)

            # if IBS < 0.1:
            b[all_names[i]] = close_ / open_

            open_ = ohlcv[-magic_number - 2][1]
            high_ = ohlcv[-magic_number - 2][2]
            low_ = ohlcv[-magic_number - 2][3]
            close_ = ohlcv[-magic_number - 2][4]

            # if (high_ - low_) == 0:
            #    continue

            # IBS = (close_ - low_) / (high_ - low_)

            # if IBS < 0.1:
            c[all_names[i]] = close_ / open_

        if len(a) == 0 or len(b) == 0 or len(c) == 0:
            buy_sell_log.append(None)
            continue

        sort_total = sorted(a.items(), key=lambda item: item[1])

        sort_total2 = sorted(b.items(), key=lambda item: item[1])

        sort_total3 = sorted(c.items(), key=lambda item: item[1])

        # buy_sell_log.append(sort_total[0][0])

        """
        if sort_total[0][1] < sort_total2[0][1]:
            buy_sell_log.append(sort_total[0][0])
        else:
            buy_sell_log.append(None)
        """
        if (
            sort_total[0][1] < sort_total2[0][1]
            and sort_total[0][1] < sort_total3[0][1]
        ):
            buy_sell_log.append(sort_total[0][0])
        else:
            buy_sell_log.append(None)

    buy_sell_log.reverse()
    for i in range(1, len(buy_sell_log)):
        if i == 998:
            break
        cnt = 0
        if buy_sell_log[i] != None:
            base_ohlcv = all_dict[buy_sell_log[i]]
            entry_price = base_ohlcv[i + 1][4]
            exit_price = base_ohlcv[i + 2][4]

            earning = 100 * (exit_price / entry_price * Slippage - 1)
            all_earn.append(earning)
            success.append(cnt)
            continue


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

# ticker_list = ['FIO/USDT', 'WAVES/USDT', 'BNT/USDT', 'TKO/USDT', 'DODO/USDT', 'MANA/USDT', 'YFI/USDT', 'SOL/USDT', 'ZEC/USDT', 'RVN/USDT', 'CRV/USDT', 'NEO/USDT', 'SXP/USDT', 'SNX/USDT', 'SRM/USDT', 'MIR/USDT', 'IOTX/USDT', 'ETC/USDT', 'ADA/USDT', 'COTI/USDT', 'WRX/USDT', 'AVAX/USDT', 'EGLD/USDT', 'DASH/USDT', 'OGN/USDT', 'PAXG/USDT', 'ROSE/USDT', 'DOT/USDT', 'TLM/USDT', 'MKR/USDT', 'KSM/USDT', 'STMX/USDT', 'COMP/USDT', 'KNC/USDT', 'CHR/USDT', 'ZEN/USDT', 'LUNA/USDT', 'THETA/USDT', 'ALICE/USDT', 'NEAR/USDT', 'RLC/USDT', 'BCH/USDT', 'XEM/USDT', '1INCH/USDT', 'BAND/USDT', 'SUSHI/USDT', 'TRX/USDT', 'ALGO/USDT', 'BTS/USDT', 'RSR/USDT', 'LIT/USDT', 'LRC/USDT', 'CHZ/USDT', 'SKL/USDT', 'GRT/USDT', 'FTM/USDT', 'ANKR/USDT', 'ETH/USDT', 'RUNE/USDT', 'DOGE/USDT', 'OCEAN/USDT', 'FTT/USDT', 'ATOM/USDT', 'XRP/USDT', 'AXS/USDT', 'RAMP/USDT', 'TWT/USDT', 'PUNDIX/USDT', 'MATIC/USDT', 'EOS/USDT', 'HOT/USDT', 'IOTA/USDT', 'BTT/USDT', 'STORJ/USDT', 'QTUM/USDT', 'ALPHA/USDT', 'ONE/USDT', 'REEF/USDT', 'SFP/USDT', 'KAVA/USDT', 'XMR/USDT', 'ONT/USDT', 'FUN/USDT', 'HBAR/USDT', 'AAVE/USDT', 'XLM/USDT', 'LINK/USDT', 'UNI/USDT', 'DEGO/USDT', 'TRU/USDT', 'BZRX/USDT', 'OXT/USDT', 'BNB/USDT', 'STX/USDT', 'LTC/USDT', 'BTCUP/USDT', 'OMG/USDT', 'FIL/USDT', 'BAT/USDT', 'CAKE/USDT', 'XTZ/USDT', 'CELR/USDT', 'ZIL/USDT', 'BTC/USDT', 'PERP/USDT', 'ENJ/USDT', 'VET/USDT']

ticker_list = [
    "BTC/USDT",
    "AUD/USDT",
    "ETH/USDT",
    "BNB/USDT",
    "DOGE/USDT",
    "ATA/USDT",
    "BCH/USDT",
    "LTC/USDT",
    "GBP/USDT",
    "EUR/USDT",
    "PAXG/USDT",
    "PAX/USDT",
    "USDC/USDT",
    "TUSD/USDT",
    "BUSD/USDT",
    "TRX/USDT",
    "1INCH/USDT",
    "XLM/USDT",
    "THETA/USDT",
    "UNFI/USDT",
    "FIL/USDT",
    "NEO/USDT",
    "MATIC/USDT",
    "EOS/USDT",
    "BTT/USDT",
    "ZEC/USDT",
    "LINK/USDT",
    "XRP/USDT",
    "CTSI/USDT",
    "DASH/USDT",
    "ADA/USDT",
    "ONT/USDT",
    "DOT/USDT",
    "CRV/USDT",
    "XMR/USDT",
    "OMG/USDT",
    "AAVE/USDT",
    "ATOM/USDT",
    "UNI/USDT",
    "CELR/USDT",
    "RVN/USDT",
    "YFI/USDT",
    "NEAR/USDT",
    "CHZ/USDT",
    "DIA/USDT",
    "TWT/USDT",
    "XTZ/USDT",
    "TLM/USDT",
    "BAND/USDT",
    "SUSHI/USDT",
    "VET/USDT",
    "GRT/USDT",
    "BADGER/USDT",
    "BAT/USDT",
    "ETC/USDT",
    "REEF/USDT",
    "HOT/USDT",
    "BAKE/USDT",
    "LPT/USDT",
    "WAVES/USDT",
    "EGLD/USDT",
    "ZIL/USDT",
    "ZEN/USDT",
    "KSM/USDT",
    "ANKR/USDT",
    "ALGO/USDT",
    "FTM/USDT",
    "INJ/USDT",
    "QTUM/USDT",
    "LUNA/USDT",
    "ICP/USDT",
    "STRAX/USDT",
    "IOTA/USDT",
    "RAMP/USDT",
    "NU/USDT",
    "BNT/USDT",
    "BTS/USDT",
    "KNC/USDT",
    "BEAM/USDT",
    "SOL/USDT",
    "RUNE/USDT",
    "KAVA/USDT",
    "LTO/USDT",
    "SXP/USDT",
    "TRU/USDT",
    "AVAX/USDT",
    "WRX/USDT",
    "MKR/USDT",
    "TFUEL/USDT",
    "COMP/USDT",
    "WIN/USDT",
    "JST/USDT",
    "IOST/USDT",
    "ALPHA/USDT",
    "TKO/USDT",
    "CVC/USDT",
    "SFP/USDT",
    "ARPA/USDT",
    "OXT/USDT",
    "CAKE/USDT",
    "XEM/USDT",
    "ENJ/USDT",
    "BTCDOWN/USDT",
    "RSR/USDT",
    "LINKUP/USDT",
    "ONE/USDT",
    "IOTX/USDT",
    "MANA/USDT",
    "HBAR/USDT",
    "PERP/USDT",
    "REN/USDT",
    "FLM/USDT",
    "UMA/USDT",
    "SNX/USDT",
    "COS/USDT",
    "MIR/USDT",
    "DODO/USDT",
    "SHIB/USDT",
    "ADAUP/USDT",
    "LIT/USDT",
    "STORJ/USDT",
    "ZRX/USDT",
]

# ticker_list = ['ADA/BTC', 'BNB/BTC', 'ETH/BTC', 'LTC/BTC', 'DOT/BTC', 'POLS/BTC', 'EPS/BTC', 'SUSHI/BTC', 'ETC/BTC', 'UNI/BTC', 'ZEC/BTC', 'XRP/BTC', 'MDA/BTC', 'SOL/BTC', 'SNX/BTC', 'LINK/BTC', 'XLM/BTC', 'SUSD/BTC', 'ORN/BTC', 'DOGE/BTC', 'THETA/BTC', 'LPT/BTC', 'ALGO/BTC', 'LRC/BTC', 'ICP/BTC', 'TOMO/BTC', 'FET/BTC', 'FTM/BTC', 'MATIC/BTC', 'BZRX/BTC', 'CAKE/BTC', 'BAND/BTC', 'SXP/BTC', 'FLM/BTC', 'GAS/BTC', 'CELO/BTC', 'ATOM/BTC', 'OMG/BTC', 'ENJ/BTC', 'OG/BTC', 'EOS/BTC', 'AVAX/BTC', 'NEO/BTC', 'LUNA/BTC', 'POWR/BTC', 'MANA/BTC', 'CHZ/BTC', 'QTUM/BTC', 'NANO/BTC', 'REN/BTC', 'ALPHA/BTC', 'WAVES/BTC', 'ZRX/BTC', 'WTC/BTC', 'BAT/BTC', 'FIL/BTC', 'SRM/BTC', 'LTO/BTC', 'RDN/BTC', 'CRV/BTC', 'BNT/BTC', 'MIR/BTC', 'HBAR/BTC', 'UMA/BTC', 'FTT/BTC', 'AUDIO/BTC', 'KNC/BTC', 'CTSI/BTC', 'ICX/BTC', 'COTI/BTC', 'STORJ/BTC', 'CTK/BTC', 'OCEAN/BTC', 'ONT/BTC', 'HIVE/BTC', 'WRX/BTC', 'IOTA/BTC', 'RIF/BTC', 'TFUEL/BTC', 'NULS/BTC', 'SYS/BTC', 'GRT/BTC', 'INJ/BTC', 'NAV/BTC', 'SKL/BTC', 'XTZ/BTC', 'KAVA/BTC', 'RLC/BTC', 'BCD/BTC', 'AST/BTC', 'DNT/BTC', 'OAX/BTC', 'LSK/BTC', 'NU/BTC', 'FRONT/BTC', '1INCH/BTC', 'BRD/BTC', 'NEAR/BTC', 'UTK/BTC', 'ATA/BTC', 'OGN/BTC', 'CVC/BTC', 'GLM/BTC', 'BQX/BTC', 'AVA/BTC', 'HNT/BTC', 'RUNE/BTC', 'PIVX/BTC', 'ONG/BTC', 'ACM/BTC', 'PERP/BTC', 'GVT/BTC', 'ADX/BTC', 'MDX/BTC', 'POLY/BTC', 'XVS/BTC', 'ELF/BTC', 'EZ/BTC', 'VET/BTC', 'STX/BTC', 'WABI/BTC', 'PHA/BTC', 'ZIL/BTC', 'DUSK/BTC', 'BEL/BTC', 'STRAX/BTC', 'KMD/BTC', 'AXS/BTC', 'ALICE/BTC', 'STEEM/BTC', 'ARDR/BTC', 'SFP/BTC', 'POND/BTC', 'TRU/BTC', 'ANKR/BTC', 'SAND/BTC', 'ANT/BTC', 'CTXC/BTC', 'CHR/BTC', 'DEGO/BTC', 'GXS/BTC', 'ONE/BTC', 'AION/BTC', 'PNT/BTC', 'CFX/BTC', 'BLZ/BTC', 'ARK/BTC', 'SUN/BTC', 'XEM/BTC', 'DIA/BTC', 'SNT/BTC', 'FIO/BTC', 'DREP/BTC', 'VITE/BTC', 'NKN/BTC', 'DLT/BTC', 'OM/BTC', 'REQ/BTC', 'DODO/BTC', 'BEAM/BTC', 'APPC/BTC', 'TLM/BTC', 'PSG/BTC', 'TKO/BTC', 'RAMP/BTC', 'TRX/BTC', 'LIT/BTC', 'RVN/BTC', 'WAN/BTC', 'GRS/BTC', 'ROSE/BTC', 'OXT/BTC', 'BADGER/BTC', 'SKY/BTC', 'LOOM/BTC', 'PPT/BTC', 'REP/BTC', 'JUV/BTC', 'ATM/BTC', 'TWT/BTC', 'NXS/BTC', 'RCN/BTC', 'VIDT/BTC', 'FIRO/BTC', 'DGB/BTC', 'SCRT/BTC', 'UNFI/BTC', 'GTO/BTC', 'AERGO/BTC', 'HARD/BTC', 'VIA/BTC', 'MTL/BTC', 'NEBL/BTC', 'ASR/BTC', 'EVX/BTC']

# ticker_list = ['BTC/USDT', 'ETH/USDT', "XRP/USDT"]

# ticker_list = ['BNB/ETH', 'RLC/ETH', 'XRP/ETH', 'ADA/ETH', 'TRX/ETH', 'LTC/ETH', 'VET/ETH', 'MTL/ETH', 'EOS/ETH', 'XLM/ETH', 'NEO/ETH', 'DEXE/ETH', 'ETC/ETH', 'LINK/ETH', 'OMG/ETH', 'GRT/ETH', 'ZIL/ETH', 'ENJ/ETH', 'IOST/ETH', 'THETA/ETH', 'BAT/ETH', 'MFT/ETH', 'NANO/ETH', 'LRC/ETH', 'HOT/ETH', 'QTUM/ETH', 'IOTA/ETH', 'FUN/ETH', 'ZRX/ETH', 'BQX/ETH', 'XEM/ETH', 'IOTX/ETH', 'WAVES/ETH', 'HEGIC/ETH', 'GXS/ETH', 'ELF/ETH', 'ADX/ETH', 'ICX/ETH', 'KNC/ETH', 'LOOM/ETH', 'ONT/ETH', 'STRAX/ETH']

# ticker_list = ['DOT/BNB', 'MATIC/BNB', 'VET/BNB', 'SOL/BNB', 'ADA/BNB', 'XRP/BNB', 'FIL/BNB', 'BTT/BNB', 'SPARTA/BNB', 'TRX/BNB', 'XLM/BNB', 'UNI/BNB', 'RUNE/BNB', 'LTC/BNB', 'ALGO/BNB', 'ICP/BNB', 'CHR/BNB', 'ZEN/BNB', 'LUNA/BNB', 'BAKE/BNB', 'AAVE/BNB', 'CTK/BNB', 'CTSI/BNB', 'CAKE/BNB', 'CELR/BNB', 'EOS/BNB', 'SUSHI/BNB', 'IOTA/BNB', 'AVAX/BNB', 'CHZ/BNB', 'INJ/BNB', 'ETC/BNB', 'ENJ/BNB', 'HOT/BNB', 'NEO/BNB', 'ATOM/BNB', 'THETA/BNB', 'OGN/BNB', 'XTZ/BNB', 'IQ/BNB', 'STX/BNB', 'MASK/BNB', 'WRX/BNB', 'SXP/BNB', 'NEAR/BNB', 'IOST/BNB', 'HBAR/BNB', 'ONT/BNB', 'WAVES/BNB', 'XVS/BNB', 'ANKR/BNB', 'KSM/BNB', 'EGLD/BNB', 'JST/BNB']

global startTime
# startTime = int(binance.fetch_ohlcv('BTC/USDT','1d')[-43][0])

perform_value = []
winrate = []

# temp_all = []

print(len(ticker_list))

for day in range(1, 11):
    print(f"{day*43}일 전")
    startTime = int(binance.fetch_ohlcv("BTC/USDT", "1d")[-day * 43][0])

    success = []
    fail = []
    lose_earn = []
    all_earn = []

    print("")
    aaaa = log_maker()
    print("")
    get_perfomance(all_earn)


print(perform_value)
print(winrate)
print("")

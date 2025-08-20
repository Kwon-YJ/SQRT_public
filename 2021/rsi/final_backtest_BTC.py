import ccxt
import time
import numpy as np
import pandas as pd
import datetime
import pandas_ta as ta
import json
import urllib


# get_time()[1] = 현재 시각 str
def get_time():
    now = datetime.datetime.now()
    YYYY = str(now.year)
    MM = str(now.month)
    DD = str(now.day)
    hh = str(now.hour)
    mm = str(now.minute)

    if len(MM) != 2:
        MM = "0" + MM
    if len(DD) != 2:
        DD = "0" + DD
    if len(hh) != 2:
        hh = "0" + hh
    if len(mm) != 2:
        mm = "0" + mm

    return YYYY + MM + DD, hh + mm


# ccxt 전용 5분봉 4개를 합쳐 20분봉으로 바꿔주는 함수
def custom_convert(ohlcv5):  # convert 5m → 20m
    std_time = int(timestamp_to_datetime(ohlcv5[0][0])[0][3:])
    for i in range(int((std_time % 20) / 5) + 2):
        del ohlcv5[i]
    ohlcv20 = []
    for i in range(0, len(ohlcv5) - 3, 4):
        highs = [ohlcv5[i + j][2] for j in range(0, 4) if ohlcv5[i + j][2]]
        lows = [ohlcv5[i + j][3] for j in range(0, 4) if ohlcv5[i + j][3]]
        candle = [
            ohlcv5[i][0],
            ohlcv5[i][1],
            max(highs) if len(highs) else None,
            min(lows) if len(lows) else None,
            ohlcv5[i + 3][4],
            ohlcv5[i][5] + ohlcv5[i + 1][5] + ohlcv5[i + 2][5] + ohlcv5[i + 3][5],
        ]
        ohlcv20.append(candle)
    return ohlcv20


temp_temp = []


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

    for i in range(2, len(rsi_entry) - 1):
        if (
            str(rsi_entry[i]) == "nan"
            or str(rsi_exit[i]) == "nan"
            or rsi_exit[i] == None
        ):
            continue
        if price == 0:
            # 1 if rsi_entry[i] < 19 and ohlcv_temp[i][5] > ohlcv_temp[i-1][5] and ohlcv_temp[i][5] > ohlcv_temp[i-2][5] and rsi_entry[i-1] > 19:
            # 2 if rsi_entry[i] < 19 and ohlcv_temp[i][5] > ohlcv_temp[i-1][5] * 2 and ohlcv_temp[i][5] > ohlcv_temp[i-2][5] * 2 and rsi_entry[i-1] > 19:
            # 3 if rsi_entry[i] < 19 and ohlcv_temp[i][5] > ohlcv_temp[i-1][5] * 1.3 and ohlcv_temp[i][5] > ohlcv_temp[i-2][5] * 1.3  and rsi_exit[i] < 25:
            # 4 if rsi_entry[i] < 19 and ohlcv_temp[i][5] * 2 > ohlcv_temp[i-1][5] + ohlcv_temp[i-2][5] and rsi_exit[i] < 25:
            # 5 if rsi_entry[i] < 18.5 and ohlcv_temp[i][5] > ohlcv_temp[i-1][5] and ohlcv_temp[i][5] > ohlcv_temp[i-2][5]:
            # 6 if (rsi_entry[i] + rsi_entry[i-1]) / 2  < 23.5:
            # 7 if rsi_entry[i] < 25 and ohlcv_temp[i][5] > ohlcv_temp[i-1][5] * 2 and ohlcv_temp[i][5] > ohlcv_temp[i-2][5] * 2 and rsi_entry[i-1] > 30:
            # 8 if rsi_entry[i-1] < 25 and ohlcv_temp[i][1] > ohlcv_temp[i][4]:
            # 9 if rsi_entry[i-1] < 25 and ohlcv_temp[i][1] > ohlcv_temp[i][4] and ohlcv_temp[i][5] > ohlcv_temp[i-1][5] and ohlcv_temp[i][5] > ohlcv_temp[i-2][5]:
            # 10 if rsi_entry[i-2] < 25 and ohlcv_temp[i-1][1] > ohlcv_temp[i-1][4] and ohlcv_temp[i][1] > ohlcv_temp[i][4]:
            # 11 if rsi_entry[i-2] < 25 and ohlcv_temp[i-1][1] > ohlcv_temp[i-1][4] and ohlcv_temp[i][1] > ohlcv_temp[i][4] and ohlcv_temp[i][5] > ohlcv_temp[i-1][5] and ohlcv_temp[i][5] > ohlcv_temp[i-2][5]:
            # 12 if rsi_entry[i-1] < 25 and ohlcv_temp[i][1] > ohlcv_temp[i][4] and ohlcv_temp[i][5] > ohlcv_temp[i-1][5] and ohlcv_temp[i][5] > ohlcv_temp[i-2][5] and rsi_entry[i-2] > 25:
            # 13 if rsi_entry[i-1] < 23.5 and ohlcv_temp[i][1] > ohlcv_temp[i][4] and ohlcv_temp[i][5] > ohlcv_temp[i-1][5] and ohlcv_temp[i][5] > ohlcv_temp[i-2][5] and rsi_entry[i-2] > 23.5:
            # 14 if rsi_entry[i-1] < 27 and ohlcv_temp[i][1] > ohlcv_temp[i][4] and ohlcv_temp[i][5] > ohlcv_temp[i-1][5] and ohlcv_temp[i][5] > ohlcv_temp[i-2][5] and rsi_entry[i-2] > 27:
            # 15 if rsi_entry[i-1] < 23.5 and ohlcv_temp[i][1] > ohlcv_temp[i][4]:
            # 16 if rsi_entry[i-1] < 25 and ohlcv_temp[i][1] > ohlcv_temp[i][4] and ohlcv_temp[i][5] > ohlcv_temp[i-1][5] and ohlcv_temp[i][5] > ohlcv_temp[i-2][5] and rsi_entry[i-2] > 25: ## the best
            # 17 if rsi_entry[i-1] < 25 and ohlcv_temp[i][1] > ohlcv_temp[i][4] and ohlcv_temp[i][5] > ohlcv_temp[i-1][5] and ohlcv_temp[i][5] > ohlcv_temp[i-2][5]:
            # 18 if rsi_entry[i-1] < 17.5:
            # if rsi_entry[i] < 17.5:
            # if rsi_entry[i] < 19:
            if rsi_entry[i] < 19 and rsi_entry[i - 1] < 19:
                price = ohlcv_temp[i + 1][1]
                entry_time_buffer.append(timestamp_to_datetime(ohlcv_temp[i + 1][0])[1])
        else:
            if rsi_exit[i] > 39:
                # if rsi_exit[i-1] > 36 and ohlcv_temp[i][1] < ohlcv_temp[i][4]:
                # if (rsi_exit[i] + rsi_exit[i-1]) / 2 > 38:
                # if rsi_exit[i] > 55:
                # if rsi_exit[i] > 38 and rsi_exit[i-1] > 38 and rsi_exit[i-2] > 38:
                # if rsi_exit[i] > 38:
                earning = 100 * (ohlcv_temp[i + 1][1] / price * Slippage - 1)
                buy_sell_log.append(earning)
                temp_temp.append(earning)
                exit_time = timestamp_to_datetime(ohlcv_temp[i + 1][0])[0]
                # name_save.append('0')
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
        # name_save.append('0')
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
    # print(trade_log)
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

    avg_W_L_ratio = -1 * np.mean(win) / np.mean(lose)
    total_perform = shortest_distance(avg_W_L_ratio, len(win) / len(trade_log))

    print("총거래 : ", len(trade_log))
    print("수익거래수 :", len(win))
    print("손실거래수 :", len(lose))
    print("평균손익 :", avg)
    print("평균수익거래 :", np.mean(win))
    print("평균손실거래 :", np.mean(lose))
    print("평균손익비 :", avg_W_L_ratio)
    win_rate = int(round(len(win) / len(trade_log), 2) * 100)
    print("승률 :", win_rate, "%")
    if len(lose) > 0:
        # print(lose)
        print("MDD :", min(lose))
    print("시그마 포지션 사이징 :", size)
    win_rate = win_rate * 0.01
    temp = (1 - win_rate) / avg_W_L_ratio
    kelly = win_rate - temp
    print("켈리 레이쇼 :", kelly)

    print("성능 지수 :", total_perform)

    # base_return = ((1+ (np.mean(win)*0.01)) ** win_rate) * ((1- (np.mean(lose)*-0.01)) ** (1-win_rate))
    # print('매매 당 기대 수익률 :', (base_return-1) * kelly)
    # print('총 수익률 :', (base_return-1) * kelly * len(trade_log))
    print("")


# ccxt ex.fetch_ohlcv() 보다 훨씬 빠르게 ohlcv 얻기
def get_ohlcv(ticker="BTC/USDT", interval="1m", limit=200):

    # cdef int i = 0
    try:
        temp = ticker.split("/")
        ticker = f"{temp[0]}{temp[1]}"
        # url = f'https://api.binance.com/api/v3/klines?symbol={ticker}&interval={interval}&limit={str(limit)}'
        # url = f'https://api.binance.com/api/v3/klines?symbol={ticker}&interval={interval}&endTime={endTime}&limit={str(limit)}'
        # url = f'https://fapi.binance.com/fapi/v1/klines?symbol={ticker}&interval={interval}&limit={str(limit)}' # monitoring
        # url = f'https://fapi.binance.com/fapi/v1/klines?symbol={ticker}&interval={interval}&endTime={endTime}&limit={str(limit)}' # backtesting
        url = f"https://api.binance.com/api/v3/klines?symbol={ticker}&interval={interval}&endTime={endTime}&limit={str(limit)}"  # backtesting
        text_data = urllib.request.urlopen(url).read().decode("utf-8")
        buy_sell_log = json.loads(text_data)
    # except Exception as e:
    except Exception as e:
        # print(e, '\n', 'ccxt.base.errors.BadSymbol: binance does not have market symbol {0}'.format(ticker))
        # return [[0]]
        return None
    buy_sell_log = [list(map(float, buy_sell_log[i])) for i in range(len(buy_sell_log))]
    return buy_sell_log


exchange_class = getattr(ccxt, "binance")
binance = exchange_class()
binance.enableRateLimit = False
binance.RateLimit = 10000
# binance.apiKey = 'key'
# binance.secret = 'key'
binance.load_markets()


All_ohlcv = []
price = []
buy_sell_log = []
name_save = []
all_tickers_final = []
# time_frame = '15m'
# time_frame = '30m'
time_frame = "5m"

Slippage = 0.9992 * 0.9992
# Slippage = 0.9982 * 0.9982
# Slippage = 0.9996 * 0.9996


a = [
    "FIL/BNB",
    "SWRV/BNB",
    "UNI/BNB",
    "CHR/BNB",
    "LTC/BNB",
    "SUSHI/BNB",
    "VET/BNB",
    "EOS/BNB",
    "DOT/BNB",
    "SOL/BNB",
    "XRP/BNB",
    "ADA/BNB",
    "CHZ/BNB",
    "FTT/BNB",
    "LUNA/BNB",
    "CAKE/BNB",
    "BAKE/BNB",
    "SPARTA/BNB",
    "IOTA/BNB",
    "MATIC/BNB",
    "AAVE/BNB",
    "BCH/BNB",
    "ENJ/BNB",
    "INJ/BNB",
    "THETA/BNB",
    "TRX/BNB",
    "HARD/BNB",
    "ATA/BNB",
    "NEO/BNB",
    "ATOM/BNB",
    "ETC/BNB",
    "SAND/BNB",
    "CTSI/BNB",
    "ICP/BNB",
    "XLM/BNB",
    "COS/BNB",
    "BTT/BNB",
    "ANT/BNB",
    "FTM/BNB",
    "ZIL/BNB",
    "OGN/BNB",
    "ANKR/BNB",
    "MBL/BNB",
    "ALGO/BNB",
    "KSM/BNB",
    "XVS/BNB",
    "C98/BNB",
    "SXP/BNB",
    "DGB/BNB",
    "EGLD/BNB",
    "AXS/BNB",
    "ONE/BNB",
    "BAT/BNB",
    "WABI/BNB",
    "ICX/BNB",
    "WAVES/BNB",
    "BLZ/BNB",
]
b = [
    "ETH/BTC",
    "ETC/BTC",
    "BNB/BTC",
    "SOL/BTC",
    "ADA/BTC",
    "LINK/BTC",
    "DOT/BTC",
    "UNI/BTC",
    "THETA/BTC",
    "LIT/BTC",
    "LUNA/BTC",
    "AVAX/BTC",
    "ONT/BTC",
    "LTC/BTC",
    "RUNE/BTC",
    "XRP/BTC",
    "GRT/BTC",
    "BAT/BTC",
    "1INCH/BTC",
    "WTC/BTC",
    "MATIC/BTC",
    "SKY/BTC",
    "ENJ/BTC",
    "BCD/BTC",
    "ADX/BTC",
    "XMR/BTC",
    "OCEAN/BTC",
    "ICX/BTC",
    "ALGO/BTC",
    "GAS/BTC",
    "SUSHI/BTC",
    "AUDIO/BTC",
    "CRV/BTC",
    "ATOM/BTC",
    "FIL/BTC",
    "WAVES/BTC",
    "EVX/BTC",
    "SXP/BTC",
    "REN/BTC",
    "HIVE/BTC",
    "TFUEL/BTC",
    "BAND/BTC",
    "RLC/BTC",
    "KAVA/BTC",
    "SNX/BTC",
    "TOMO/BTC",
    "ALPHA/BTC",
    "CAKE/BTC",
    "KNC/BTC",
    "OXT/BTC",
    "FTT/BTC",
    "OGN/BTC",
    "IOTA/BTC",
    "XLM/BTC",
    "LSK/BTC",
    "CHZ/BTC",
    "ZRX/BTC",
    "SRM/BTC",
    "SAND/BTC",
    "DASH/BTC",
    "MANA/BTC",
    "POLY/BTC",
    "LRC/BTC",
    "GXS/BTC",
    "NEAR/BTC",
    "AXS/BTC",
    "FTM/BTC",
    "QTUM/BTC",
    "CTK/BTC",
    "MTL/BTC",
    "DOGE/BTC",
    "NAV/BTC",
    "CTSI/BTC",
    "ICP/BTC",
    "GVT/BTC",
    "ALICE/BTC",
    "VIDT/BTC",
    "OMG/BTC",
    "CELO/BTC",
    "POWR/BTC",
    "EOS/BTC",
    "BAR/BTC",
    "PNT/BTC",
    "KMD/BTC",
    "SUSD/BTC",
    "BNT/BTC",
    "WING/BTC",
    "POLS/BTC",
    "TLM/BTC",
    "NEO/BTC",
    "FET/BTC",
    "XEM/BTC",
    "WABI/BTC",
    "PERP/BTC",
    "TKO/BTC",
    "STORJ/BTC",
    "ONG/BTC",
    "PHA/BTC",
    "C98/BTC",
    "MDX/BTC",
    "XTZ/BTC",
    "CVC/BTC",
    "INJ/BTC",
    "DREP/BTC",
    "GTC/BTC",
    "NANO/BTC",
    "ASR/BTC",
    "REP/BTC",
    "FIS/BTC",
    "CHR/BTC",
    "HNT/BTC",
    "AST/BTC",
    "SCRT/BTC",
    "OM/BTC",
    "COTI/BTC",
    "TVK/BTC",
    "NULS/BTC",
    "WRX/BTC",
    "ANT/BTC",
    "UMA/BTC",
    "JUV/BTC",
    "FIRO/BTC",
    "LTO/BTC",
    "AION/BTC",
]
c = [
    "BTC/USDT",
    "ETH/USDT",
    "MATIC/USDT",
    "BCH/USDT",
    "BNB/USDT",
    "XMR/USDT",
    "DOT/USDT",
    "ADA/USDT",
    "AUD/USDT",
    "EUR/USDT",
    "TFUEL/USDT",
    "BUSD/USDT",
    "PAX/USDT",
    "TUSD/USDT",
    "USDC/USDT",
    "OMG/USDT",
    "EOS/USDT",
    "COCOS/USDT",
    "GBP/USDT",
    "DOGE/USDT",
    "ROSE/USDT",
    "XRP/USDT",
    "RVN/USDT",
    "TRX/USDT",
    "THETA/USDT",
    "PAXG/USDT",
    "XLM/USDT",
    "ZEC/USDT",
    "FIL/USDT",
    "LTC/USDT",
    "ICP/USDT",
    "VET/USDT",
    "AVAX/USDT",
    "LTO/USDT",
    "LINK/USDT",
    "REEF/USDT",
    "ETC/USDT",
    "NEO/USDT",
    "BTCUP/USDT",
    "CVC/USDT",
    "COMP/USDT",
    "SLP/USDT",
    "BTT/USDT",
    "DASH/USDT",
    "BAT/USDT",
    "AAVE/USDT",
    "BEL/USDT",
    "LINKUP/USDT",
    "CAKE/USDT",
    "UNI/USDT",
    "ATOM/USDT",
    "ONT/USDT",
    "OCEAN/USDT",
    "ALGO/USDT",
    "CHZ/USDT",
    "COTI/USDT",
    "BZRX/USDT",
    "DENT/USDT",
    "TKO/USDT",
    "ANKR/USDT",
    "GRT/USDT",
    "ZIL/USDT",
    "SAND/USDT",
    "SNX/USDT",
    "AXS/USDT",
    "DEGO/USDT",
    "IOST/USDT",
    "FIO/USDT",
    "YFI/USDT",
    "SXP/USDT",
    "SC/USDT",
    "XTZ/USDT",
    "SOL/USDT",
    "ALICE/USDT",
    "TLM/USDT",
    "XEM/USDT",
    "NEAR/USDT",
    "GTO/USDT",
    "FTM/USDT",
    "STMX/USDT",
    "BAKE/USDT",
    "FTT/USDT",
    "GXS/USDT",
    "WAVES/USDT",
    "HNT/USDT",
    "C98/USDT",
    "LUNA/USDT",
    "MANA/USDT",
    "KSM/USDT",
    "EGLD/USDT",
    "BLZ/USDT",
    "KNC/USDT",
    "SUSHI/USDT",
    "ENJ/USDT",
    "CELR/USDT",
    "BTCDOWN/USDT",
    "1INCH/USDT",
    "STORJ/USDT",
    "CTK/USDT",
    "SRM/USDT",
    "QTUM/USDT",
    "RUNE/USDT",
    "INJ/USDT",
    "REN/USDT",
    "UMA/USDT",
    "VTHO/USDT",
    "AUDIO/USDT",
    "HOT/USDT",
    "WIN/USDT",
    "NANO/USDT",
    "PUNDIX/USDT",
    "OGN/USDT",
    "CELO/USDT",
    "IOTA/USDT",
    "ETHDOWN/USDT",
    "YFII/USDT",
    "DUSK/USDT",
    "MKR/USDT",
    "DGB/USDT",
    "SUSHIUP/USDT",
    "ZRX/USDT",
    "CHR/USDT",
    "TOMO/USDT",
    "XVG/USDT",
    "PERP/USDT",
    "MITH/USDT",
]
d = [
    "XRP/ETH",
    "BNB/ETH",
    "ETC/ETH",
    "NEO/ETH",
    "LTC/ETH",
    "QLC/ETH",
    "ADX/ETH",
    "XLM/ETH",
    "ADA/ETH",
    "EOS/ETH",
    "GRT/ETH",
    "VET/ETH",
    "THETA/ETH",
    "ZIL/ETH",
    "TRX/ETH",
    "NANO/ETH",
    "REP/ETH",
    "OMG/ETH",
    "LINK/ETH",
    "IOST/ETH",
    "SCRT/ETH",
    "BLZ/ETH",
    "QTUM/ETH",
    "PIVX/ETH",
    "ZRX/ETH",
    "MTL/ETH",
    "BAT/ETH",
    "SNT/ETH",
    "ENJ/ETH",
    "MANA/ETH",
    "WAVES/ETH",
    "EZ/ETH",
    "XVG/ETH",
    "KMD/ETH",
    "ONT/ETH",
    "KEY/ETH",
    "SLP/ETH",
    "VIB/ETH",
    "RLC/ETH",
    "IOTX/ETH",
]


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
    "DEFI/USDT",
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
    "BTC/BUSD",
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
    "1000SHIB/USDT",
    "ICP/USDT",
    "BAKE/USDT",
]
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
    "BTC/BUSD",
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
]
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

# ticker_list = ticker_list + a + b + d

ticker_list = b


for day in range(2, 20):
    # for day in range(20, 30):
    multiple = 4
    print(f"{day*multiple}일 전")

    # startTime = str(binance.fetch_ohlcv('BTC/USDT','1d')[-day*multiple][0])
    endTime = str(binance.fetch_ohlcv("BTC/USDT", "1d")[(-day + 1) * multiple][0])

    for i in range(len(ticker_list)):
        try:
            # temp = get_ohlcv(ticker_list[i], time_frame, 1000)
            temp = custom_convert(get_ohlcv(ticker_list[i], time_frame, 1000))
            all_tickers_final.append(ticker_list[i])
            All_ohlcv.append(temp)
            # time.sleep(0.001)
        except Exception as e:
            print(e)
            # time.sleep(0.5)
            print(ticker_list[i])

    for i in range(len(All_ohlcv)):
        ohlcv_temp = All_ohlcv[i]

        if ohlcv_temp == None or len(ohlcv_temp) == 0:
            continue

        # df = pd.DataFrame(data=np.array(ohlcv_temp), columns=['0','0', 'close', '0', '0', '0','0','0','0','0','0','0']) ## rsi(15, high)
        df = pd.DataFrame(
            data=np.array(ohlcv_temp), columns=["0", "0", "close", "0", "0", "0"]
        )  ## rsi(15, high)
        # df = pd.DataFrame(data=np.array(ohlcv_temp), columns=['0','0', '0', '0', 'close', '0','0','0','0','0','0','0']) ## rsi(15, high)
        rsi_entry = df.ta.rsi(length=14).tolist()

        # df = pd.DataFrame(data=np.array(ohlcv_temp), columns=['0','0', '0', 'close', '0', '0','0','0','0','0','0','0']) ## rsi(8, low)
        df = pd.DataFrame(
            data=np.array(ohlcv_temp), columns=["0", "0", "0", "close", "0", "0"]
        )  ## rsi(8, low)
        rsi_exit = df.ta.rsi(length=8).tolist()

        # log_maker(all_tickers_final[i], ohlcv_temp[-97:],rsi_entry[-97:], rsi_exit[-97:])
        # log_maker(all_tickers_final[i], ohlcv_temp[-72:],rsi_entry[-72:], rsi_exit[-72:])
        log_maker(
            all_tickers_final[i], ohlcv_temp[-289:], rsi_entry[-289:], rsi_exit[-289:]
        )
        # log_maker(all_tickers_final[i], ohlcv_temp[-49:],rsi_entry[-49:], rsi_exit[-49:])
        # log_maker(all_tickers_final[i], ohlcv_temp[-193:],rsi_entry[-193:], rsi_exit[-193:])
        # log_maker(all_tickers_final[i], ohlcv_temp[-673:],rsi_entry[-673:], rsi_exit[-673:])

    get_perfomance(buy_sell_log)
    # print('')
    get_perfomance(temp_temp)
    All_ohlcv.clear()
    buy_sell_log.clear()
    all_tickers_final.clear()

import ccxt
import time
import os
import numpy
import datetime
import pandas as pd


exchange_class = getattr(ccxt, "binance")
binance = exchange_class()
binance.enableRateLimit = True
binance.RateLimit = 10000
binance.load_markets()

time_frame = "1h"


ticker_list = [
    "ETH/BTC",
    "LTC/BTC",
    "NEO/BTC",
    "GAS/BTC",
    "MCO/BTC",
    "WTC/BTC",
    "LRC/BTC",
    "QTUM/BTC",
    "YOYOW/BTC",
    "OMG/BTC",
    "ZRX/BTC",
    "STRAT/BTC",
    "SNGLS/BTC",
    "BQX/BTC",
    "KNC/BTC",
    "FUN/BTC",
    "SNM/BTC",
    "IOTA/BTC",
    "LINK/BTC",
    "XVG/BTC",
    "MDA/BTC",
    "MTL/BTC",
    "EOS/BTC",
    "SNT/BTC",
    "ETC/BTC",
    "MTH/BTC",
    "ENG/BTC",
    "DNT/BTC",
    "ZEC/BTC",
    "BNT/BTC",
    "AST/BTC",
    "DASH/BTC",
    "OAX/BTC",
    "BTG/BTC",
    "EVX/BTC",
    "REQ/BTC",
    "VIB/BTC",
    "TRX/BTC",
    "POWR/BTC",
    "ARK/BTC",
    "XRP/BTC",
    "ENJ/BTC",
    "STORJ/BTC",
    "KMD/BTC",
    "RCN/BTC",
    "NULS/BTC",
    "RDN/BTC",
    "XMR/BTC",
    "DLT/BTC",
    "AMB/BTC",
    "BAT/BTC",
    "BCPT/BTC",
    "ARN/BTC",
    "GVT/BTC",
    "CDT/BTC",
    "GXS/BTC",
    "POE/BTC",
    "QSP/BTC",
    "BTS/BTC",
    "XZC/BTC",
    "LSK/BTC",
    "TNT/BTC",
    "FUEL/BTC",
    "MANA/BTC",
    "BCD/BTC",
    "ADX/BTC",
    "ADA/BTC",
    "PPT/BTC",
    "CMT/BTC",
    "XLM/BTC",
    "CND/BTC",
    "LEND/BTC",
    "WABI/BTC",
    "TNB/BTC",
    "WAVES/BTC",
    "GTO/BTC",
    "ICX/BTC",
    "OST/BTC",
    "ELF/BTC",
    "AION/BTC",
    "NEBL/BTC",
    "BRD/BTC",
    "NAV/BTC",
    "LUN/BTC",
    "APPC/BTC",
    "VIBE/BTC",
    "RLC/BTC",
    "INS/BTC",
    "PIVX/BTC",
    "IOST/BTC",
    "STEEM/BTC",
    "NANO/BTC",
    "VIA/BTC",
    "BLZ/BTC",
    "AE/BTC",
    "POA/BTC",
    "ZIL/BTC",
    "ONT/BTC",
    "XEM/BTC",
    "WAN/BTC",
    "WPR/BTC",
    "QLC/BTC",
    "SYS/BTC",
    "GRS/BTC",
    "GNT/BTC",
    "LOOM/BTC",
    "REP/BTC",
    "ZEN/BTC",
    "SKY/BTC",
    "CVC/BTC",
    "THETA/BTC",
    "IOTX/BTC",
    "QKC/BTC",
    "AGI/BTC",
    "NXS/BTC",
    "DATA/BTC",
    "SC/BTC",
    "NAS/BTC",
    "ARDR/BTC",
    "HOT/BTC",
    "VET/BTC",
    "DOCK/BTC",
    "POLY/BTC",
    "HC/BTC",
    "GO/BTC",
    "RVN/BTC",
    "DCR/BTC",
    "MITH/BTC",
    "BCH/BTC",
    "REN/BTC",
    "ONG/BTC",
    "FET/BTC",
    "CELR/BTC",
    "MATIC/BTC",
    "ATOM/BTC",
    "PHB/BTC",
    "TFUEL/BTC",
    "ONE/BTC",
    "FTM/BTC",
    "ALGO/BTC",
    "ERD/BTC",
    "DOGE/BTC",
    "DUSK/BTC",
    "ANKR/BTC",
    "COS/BTC",
    "TOMO/BTC",
    "PERL/BTC",
    "CHZ/BTC",
    "BAND/BTC",
    "BEAM/BTC",
    "XTZ/BTC",
    "HBAR/BTC",
    "NKN/BTC",
    "STX/BTC",
    "KAVA/BTC",
    "ARPA/BTC",
    "CTXC/BTC",
    "TROY/BTC",
    "VITE/BTC",
    "FTT/BTC",
    "OGN/BTC",
    "DREP/BTC",
    "TCT/BTC",
    "WRX/BTC",
    "LTO/BTC",
    "MBL/BTC",
    "COTI/BTC",
    "STPT/BTC",
    "SOL/BTC",
    "CTSI/BTC",
    "HIVE/BTC",
    "CHR/BTC",
    "MDT/BTC",
    "STMX/BTC",
    "PNT/BTC",
    "DGB/BTC",
]


def timestamp_to_datetime(timestamp):
    datetimeobj = datetime.datetime.fromtimestamp(timestamp / 1000)
    return datetimeobj


def get_perfomance(trade_log):
    win = []
    lose = []
    risk_free = 0.038 / 365
    avg = numpy.mean(trade_log)
    std = numpy.std(trade_log)
    size = (avg - risk_free) / (std * std)

    for i in range(len(trade_log)):
        if trade_log[i] > 0:
            win.append(trade_log[i])
        elif trade_log[i] < 0:
            lose.append(trade_log[i])

    # print('총거래 : ', len(trade_log))
    print("수익거래수 :", len(win))
    print("손실거래수 :", len(lose))
    # print('평균거래 :',avg)
    # print('평균수익거래 :', numpy.mean(win))
    # print('평균손실거래 :', numpy.mean(lose))
    print("평균손익비 :", -1 * numpy.mean(win) / numpy.mean(lose))
    print("승률 :", int(round(len(win) / len(trade_log), 2) * 100), "%")
    print("포지션 사이징 :", size)
    # print('')


def ATR(data, length):
    TR = []
    for i in range(int(length)):
        TR.append(
            max(
                (data[i - length][2] - data[i - length][3]),
                abs(data[i - length][2] - data[i - length - 1][4]),
                abs(data[i - length][3] - data[i - length - 1][4]),
            )
        )
    ATR = pd.Series(TR).rolling(length).mean()
    # ATR = pd.Series(TR).ewm(length).mean()
    return ATR.tolist()


def ma(data, length):
    result = []
    for i in range(len(data)):
        result.append(data[i][4])
    return pd.Series(result).rolling(length).mean().tolist()


def log_maker_1():
    for j in range(len(ticker_list)):
        if len(price) != 0:  # 못 갖춘 거래라면
            earning = 100 * ((ohlcv[-9][4] / price[0]) * 0.99925 * 0.99925 - 1)
            buy_sell_log.append(earning)
            buy_sell_log2.append(earning)
        price.clear()

        ohlcv = All_ohlcv[j]
        i = 11
        while i < len(ohlcv) - 11:
            i += 1

            if len(price) != 0:
                temp = ohlcv[i - 9 : i]
                target_price = ma(temp, 7)[-1] + (2 * ATR(temp, 7)[-1])
                if ohlcv[i][3] >= target_price:
                    earning = 100 * (
                        (ohlcv[i + 1][1] / price[0]) * 0.99925 * 0.99925 - 1
                    )
                    buy_sell_log.append(earning)
                    buy_sell_log1.append(earning)
                    price.clear()
                    continue
                else:
                    continue

            temp = ohlcv[i - 9 : i]
            target_price = ma(temp, 7)[-1] - (1 * ATR(temp, 7)[-1])
            if ohlcv[i][2] <= target_price:
                price.append(ohlcv[i + 1][1])


for t in range(0, 51):
    day = t

    temp_time = str(
        timestamp_to_datetime(binance.fetch_ohlcv("BTC/USDT", "1d")[-day - 2][0])
    )
    convert = temp_time[:10] + "T" + temp_time[11:19] + "Z"
    timestamp = binance.parse8601(convert)

    print(t)

    All_ohlcv = []
    price = []
    buy_sell_log = []
    buy_sell_log1 = []
    buy_sell_log2 = []

    for i in range(len(ticker_list)):
        temp = binance.fetch_ohlcv(ticker_list[i], time_frame, timestamp)
        All_ohlcv.append(temp)

    # log_maker_1()
    # print('전체거래')
    # get_perfomance(buy_sell_log)
    # print('')
    print("정상거래")
    get_perfomance(buy_sell_log1)
    # print('')
    # print('비정상 거래')
    # get_perfomance(buy_sell_log2)
    # print('')
    print("")
    print("")

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
binance.apiKey = "FRbVseExyAWjQUtYFnS4memLnPCcgNAeRW7HEBrrw9qyIyPUMCTzUKxZKOJIHcfV"
binance.secret = "CbDX3DE5r9ErdLBOphDB4rjCaAaKbUqITbNK05YIitktZ24VfcNrvVRbIgfK6L87"
binance.load_markets()

time_frame = "1h"

day = 50
ticker_list = [
    "XMR/BTC",
    "REP/BTC",
    "SOL/BTC",
    "WNXM/BTC",
    "SUSHI/BTC",
    "ENG/BTC",
    "WAVES/BTC",
    "BAL/BTC",
    "ANT/BTC",
    "BAT/BTC",
    "CRV/BTC",
    "MKR/BTC",
    "VIA/BTC",
    "OCEAN/BTC",
    "LEND/BTC",
    "PAXG/BTC",
    "SNX/BTC",
    "AVA/BTC",
    "BCH/BTC",
    "XRP/BTC",
    "WTC/BTC",
    "XZC/BTC",
    "XTZ/BTC",
    "ZRX/BTC",
    "FIO/BTC",
    "EVX/BTC",
    "ZEC/BTC",
    "FTT/BTC",
    "QTUM/BTC",
    "COMP/BTC",
    "ICX/BTC",
    "STRAT/BTC",
    "KNC/BTC",
    "SRM/BTC",
    "NULS/BTC",
    "NEO/BTC",
    "ZEN/BTC",
    "ARK/BTC",
    "KMD/BTC",
    "IOTA/BTC",
    "PNT/BTC",
    "BAND/BTC",
    "STORJ/BTC",
    "DOT/BTC",
    "GVT/BTC",
    "BNT/BTC",
    "MTL/BTC",
    "RDN/BTC",
    "ETC/BTC",
    "BCD/BTC",
    "HC/BTC",
    "WAN/BTC",
    "ONT/BTC",
    "SXP/BTC",
    "MCO/BTC",
    "YFII/BTC",
    "KSM/BTC",
    "LINK/BTC",
    "OMG/BTC",
    "LUNA/BTC",
    "YFI/BTC",
    "REN/BTC",
    "BNB/BTC",
    "NMR/BTC",
    "NXS/BTC",
    "LTC/BTC",
    "NAS/BTC",
    "TRB/BTC",
    "OGN/BTC",
    "MDA/BTC",
    "RLC/BTC",
    "GAS/BTC",
    "EOS/BTC",
    "DCR/BTC",
    "TOMO/BTC",
    "KAVA/BTC",
    "ATOM/BTC",
    "THETA/BTC",
    "NANO/BTC",
    "ETH/BTC",
    "PPT/BTC",
    "LSK/BTC",
    "BTG/BTC",
    "ALGO/BTC",
    "BZRX/BTC",
    "RUNE/BTC",
    "DASH/BTC",
    "GXS/BTC",
    "SKY/BTC",
]
# ticker_list = ['NEO/BTC', 'DOT/BTC', 'STORJ/BTC', 'EOS/BTC', 'XMR/BTC', 'DASH/BTC', 'BNT/BTC', 'PNT/BTC', 'NMR/BTC', 'TOMO/BTC', 'ZEN/BTC', 'MCO/BTC', 'LRC/BTC', 'RUNE/BTC', 'KAVA/BTC', 'CRV/BTC', 'COMP/BTC', 'REN/BTC', 'LEND/BTC', 'KNC/BTC', 'BAND/BTC', 'ZEC/BTC', 'REP/BTC', 'MKR/BTC', 'IOTA/BTC', 'ICX/BTC', 'XZC/BTC', 'OGN/BTC', 'BZRX/BTC', 'WNXM/BTC', 'DCR/BTC', 'ALGO/BTC', 'NANO/BTC', 'ZRX/BTC', 'SXP/BTC', 'TRB/BTC', 'BAT/BTC', 'LINK/BTC', 'YFII/BTC', 'ANT/BTC', 'ETH/BTC', 'GXS/BTC', 'SOL/BTC', 'THETA/BTC', 'BAL/BTC', 'XTZ/BTC', 'LUNA/BTC', 'SRM/BTC', 'MTL/BTC', 'WAVES/BTC', 'RLC/BTC', 'ETC/BTC', 'OMG/BTC', 'EGLD/BTC', 'NULS/BTC', 'YFI/BTC', 'ONT/BTC', 'OCEAN/BTC', 'QTUM/BTC', 'PAXG/BTC', 'LTC/BTC', 'LSK/BTC', 'STRAT/BTC', 'WAN/BTC', 'BNB/BTC', 'FTT/BTC', 'BCH/BTC', 'WTC/BTC', 'ATOM/BTC', 'HC/BTC', 'SNX/BTC', 'XRP/BTC', 'SUSHI/BTC', 'KMD/BTC']

ticker_list = list(binance.fetch_tickers().keys())


# ticker_list = ['BTC/USDT', 'ETH/USDT', 'BCH/USDT','XRP/USDT', 'XLM/USDT', 'EOS/USDT', 'LTC/USDT', 'TRX/USDT', 'ETC/USDT', 'LINK/USDT', 'ADA/USDT', 'XMR/USDT', 'DASH/USDT', 'ZEC/USDT', 'XTZ/USDT', 'BNB/USDT', 'ATOM/USDT', 'ONT/USDT', 'IOTA/USDT', 'BAT/USDT', 'VET/USDT', 'NEO/USDT', 'QTUM/USDT', 'IOST/USDT', 'THETA/USDT', 'ALGO/USDT', 'ZIL/USDT', 'KNC/USDT', 'ZRX/USDT', 'COMP/USDT', 'OMG/USDT', 'DOGE/USDT', 'SXP/USDT', 'LEND/USDT', 'KAVA/USDT', 'BAND/USDT', 'RLC/USDT', 'WAVES/USDT', 'MKR/USDT', 'SNX/USDT', 'DOT/USDT',  'YFI/USDT', 'BAL/USDT', 'CRV/USDT', 'TRB/USDT', 'YFII/USDT', 'RUNE/USDT', 'SUSHI/USDT', 'SRM/USDT', 'BZRX/USDT']


print(len(ticker_list))


def timestamp_to_datetime(timestamp):
    datetimeobj = datetime.datetime.fromtimestamp(timestamp / 1000)
    return datetimeobj


temp_time = str(
    timestamp_to_datetime(binance.fetch_ohlcv("BTC/USDT", "1d")[-day - 2][0])
)
convert = temp_time[:10] + "T" + temp_time[11:19] + "Z"
timestamp = binance.parse8601(convert)

All_ohlcv = []
price = []
buy_sell_log = []
buy_sell_log1 = []
buy_sell_log2 = []


ticker_list = [
    "BTC/USDT",
    "ETH/USDT",
    "BCH/USDT",
    "XRP/USDT",
    "XLM/USDT",
    "EOS/USDT",
    "LTC/USDT",
    "TRX/USDT",
    "ETC/USDT",
    "LINK/USDT",
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
    "LEND/USDT",
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
]


for i in range(len(ticker_list)):
    temp = binance.fetch_ohlcv(ticker_list[i], time_frame, timestamp)
    All_ohlcv.append(temp)


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

    print("총거래 : ", len(trade_log))
    print("수익거래수 :", len(win))
    print("손실거래수 :", len(lose))
    print("평균거래 :", avg)
    print("평균수익거래 :", numpy.mean(win))
    print("평균손실거래 :", numpy.mean(lose))
    print("평균손익비 :", -1 * numpy.mean(win) / numpy.mean(lose))
    print("승률 :", int(round(len(win) / len(trade_log), 2) * 100), "%")
    print("포지션 사이징 :", size)
    print("")


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
    # ATR = pd.Series(TR).rolling(length).mean()
    ATR = pd.Series(TR).ewm(alpha=1 / length).mean()
    return ATR.tolist()


def ma(data, length):
    result = []
    for i in range(len(data)):
        result.append(data[i][4])
    return pd.Series(result).rolling(length).mean().tolist()


def log_maker_1():
    for j in range(len(ticker_list)):
        if len(price) != 0:  # 못 갖춘 거래라면
            earning = 100 * ((ohlcv[-1][4] / price[0]) * 0.99925 * 0.99925 - 1)
            buy_sell_log.append(earning)
            buy_sell_log2.append(earning)
        price.clear()

        ohlcv = All_ohlcv[j]
        i = 22
        while i < len(ohlcv) - 4:
            i += 1
            """
            if len(price) != 0:
                temp = ohlcv[i-6:i]
                temp2 = ohlcv[i-20:i]
                target_price = ma(temp2, 20)[-1] - (1.7 * ATR(temp, 5)[-1])
                if ohlcv[i][4] <= target_price:
                    earning = 100 * ((ohlcv[i+1][1] / price[0]) * 0.99925 * 0.99925 - 1)
                    buy_sell_log.append(earning)
                    buy_sell_log1.append(earning)
                    price.clear()
                    continue
                else:
                    continue
			"""
            temp = ohlcv[i - 6 : i]
            temp2 = ohlcv[i - 20 : i]
            target_price = ma(temp2, 20)[-1] + (1.7 * ATR(temp, 5)[-1])
            if ohlcv[i][3] >= target_price * 1.03:
                # price.append(ohlcv[i+1][1])
                earning = 100 * (
                    (ohlcv[i + 2][1] / ohlcv[i + 1][1]) * 0.99925 * 0.99925 - 1
                )
                buy_sell_log.append(earning)
                i += 2


log_maker_1()
print("전체거래")
get_perfomance(buy_sell_log)
print("")
print("정상거래")
get_perfomance(buy_sell_log1)
print("")
print("비정상 거래")
get_perfomance(buy_sell_log2)


price = []
buy_sell_log = []
buy_sell_log1 = []
buy_sell_log2 = []

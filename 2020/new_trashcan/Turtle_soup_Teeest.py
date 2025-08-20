import ccxt
import time
import os
import numpy
import datetime


exchange_class = getattr(ccxt, "binance")
binance = exchange_class()
binance.enableRateLimit = True
binance.RateLimit = 10000
binance.apiKey = "FRbVseExyAWjQUtYFnS4memLnPCcgNAeRW7HEBrrw9qyIyPUMCTzUKxZKOJIHcfV"
binance.secret = "CbDX3DE5r9ErdLBOphDB4rjCaAaKbUqITbNK05YIitktZ24VfcNrvVRbIgfK6L87"
binance.load_markets()


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


def timestamp_to_datetime(timestamp):
    datetimeobj = datetime.datetime.fromtimestamp(timestamp / 1000)
    return datetimeobj


def log_maker_1():
    for j in range(len(ticker_list)):
        if len(price) != 0:
            earning = 100 * ((ohlcv[-1][4] / price[0]) * 0.99925 * 0.99925 - 1)
            buy_sell_log.append(earning)
        price.clear()
        ohlcv = All_ohlcv[j]
        # for i in range(0, len(ohlcv)-1):
        i = 20
        while i < len(ohlcv) - 4:
            if len(price) != 0:
                temp = []
                for k in range(-2, 1):
                    temp.append(ohlcv[i + k][3])
                if ohlcv[i][3] == min(temp):
                    i += 1
                    earning = 100 * ((min(temp) / price[0]) * 0.99925 * 0.99925 - 1)
                    buy_sell_log.append(earning)
                    price.clear()
                else:
                    i += 1
                    continue

            temp = []
            for k in range(-20, 0):
                temp.append(ohlcv[i + k][3])

            if ohlcv[i - 1][3] == min(temp):
                if ohlcv[i][3] < min(temp):
                    if ohlcv[i + 1][2] > min(temp):
                        price.append(min(temp))
                        i += 1
                elif ohlcv[i + 1][3] < min(temp):
                    if ohlcv[i + 2][2] > min(temp):
                        price.append(min(temp))
                        i += 2
                elif ohlcv[i + 2][3] < min(temp):
                    if ohlcv[i + 3][2] > min(temp):
                        price.append(min(temp))
                        i += 3
            i += 1


def log_maker_2():
    for j in range(len(ticker_list)):

        ohlcv = All_ohlcv[j]

        i = 20
        while i < len(ohlcv) - 4:
            temp = []
            for k in range(-20, 0):
                temp.append(ohlcv[i + k][3])

            if ohlcv[i - 1][3] == min(temp):
                if ohlcv[i][3] < min(temp):
                    if ohlcv[i + 1][2] > min(temp):
                        earning = 100 * (
                            (ohlcv[i + 2][1] / min(temp)) * 0.99925 * 0.99925 - 1
                        )
                        buy_sell_log.append(earning)
                        i += 2
                elif ohlcv[i + 1][3] < min(temp):
                    if ohlcv[i + 2][2] > min(temp):
                        earning = 100 * (
                            (ohlcv[i + 3][1] / min(temp)) * 0.99925 * 0.99925 - 1
                        )
                        buy_sell_log.append(earning)
                        i += 3
                elif ohlcv[i + 2][3] < min(temp):
                    if ohlcv[i + 3][2] > min(temp):
                        earning = 100 * (
                            (ohlcv[i + 4][1] / min(temp)) * 0.99925 * 0.99925 - 1
                        )
                        buy_sell_log.append(earning)
                        i += 4
            i += 1


# IBS = close - low / high - low

time_frame = "1d"

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
    "LEND/USDT",
]

ticker_list = [
    "ETH/USDT",
    "NEO/USDT",
    "LTC/USDT",
    "QTUM/USDT",
    "ADA/USDT",
    "XRP/USDT",
    "EOS/USDT",
    "IOTA/USDT",
    "XLM/USDT",
    "ONT/USDT",
    "TRX/USDT",
    "ETC/USDT",
    "ICX/USDT",
    "NULS/USDT",
    "VET/USDT",
    "BCH/USDT",
    "LINK/USDT",
    "WAVES/USDT",
    "BTT/USDT",
    "ONG/USDT",
    "HOT/USDT",
    "ZIL/USDT",
    "ZRX/USDT",
    "FET/USDT",
    "BAT/USDT",
    "XMR/USDT",
    "ZEC/USDT",
    "IOST/USDT",
    "CELR/USDT",
    "DASH/USDT",
    "NANO/USDT",
    "OMG/USDT",
    "THETA/USDT",
    "ENJ/USDT",
    "MITH/USDT",
    "MATIC/USDT",
    "ATOM/USDT",
    "TFUEL/USDT",
    "ONE/USDT",
    "FTM/USDT",
    "ALGO/USDT",
    "GTO/USDT",
    "ERD/USDT",
    "DOGE/USDT",
    "DUSK/USDT",
    "ANKR/USDT",
    "WIN/USDT",
    "COS/USDT",
    "NPXS/USDT",
    "COCOS/USDT",
    "MTL/USDT",
    "TOMO/USDT",
    "PERL/USDT",
    "DENT/USDT",
    "MFT/USDT",
    "KEY/USDT",
    "DOCK/USDT",
    "WAN/USDT",
    "FUN/USDT",
    "CVC/USDT",
    "CHZ/USDT",
    "BAND/USDT",
    "BEAM/USDT",
    "XTZ/USDT",
    "REN/USDT",
    "RVN/USDT",
    "HC/USDT",
    "HBAR/USDT",
    "NKN/USDT",
    "STX/USDT",
    "KAVA/USDT",
    "ARPA/USDT",
    "IOTX/USDT",
    "RLC/USDT",
    "MCO/USDT",
    "CTXC/USDT",
    "TROY/USDT",
    "VITE/USDT",
    "FTT/USDT",
    "OGN/USDT",
    "DREP/USDT",
    "TCT/USDT",
    "WRX/USDT",
    "BTS/USDT",
    "LSK/USDT",
    "BNT/USDT",
    "LTO/USDT",
    "STRAT/USDT",
    "AION/USDT",
    "MBL/USDT",
    "COTI/USDT",
    "STPT/USDT",
    "WTC/USDT",
    "DATA/USDT",
    "XZC/USDT",
    "CTSI/USDT",
    "HIVE/USDT",
    "CHR/USDT",
    "BTCUP/USDT",
    "BTCDOWN/USDT",
    "GXS/USDT",
    "ARDR/USDT",
    "LEND/USDT",
    "MDT/USDT",
    "STMX/USDT",
    "KNC/USDT",
    "REP/USDT",
    "LRC/USDT",
    "PNT/USDT",
]

# ticker_list = ['ETH/BTC', 'LTC/BTC', 'NEO/BTC', 'GAS/BTC', 'MCO/BTC', 'WTC/BTC', 'LRC/BTC', 'QTUM/BTC', 'YOYOW/BTC', 'OMG/BTC', 'ZRX/BTC', 'STRAT/BTC', 'SNGLS/BTC', 'BQX/BTC', 'KNC/BTC', 'FUN/BTC', 'SNM/BTC', 'IOTA/BTC', 'LINK/BTC', 'XVG/BTC', 'MDA/BTC', 'MTL/BTC', 'EOS/BTC', 'SNT/BTC', 'ETC/BTC', 'MTH/BTC', 'ENG/BTC', 'DNT/BTC', 'ZEC/BTC', 'BNT/BTC', 'AST/BTC', 'DASH/BTC', 'OAX/BTC', 'BTG/BTC', 'EVX/BTC', 'REQ/BTC', 'VIB/BTC', 'TRX/BTC', 'POWR/BTC', 'ARK/BTC', 'XRP/BTC', 'ENJ/BTC', 'STORJ/BTC', 'KMD/BTC', 'RCN/BTC', 'NULS/BTC', 'RDN/BTC', 'XMR/BTC', 'DLT/BTC', 'AMB/BTC', 'BAT/BTC', 'BCPT/BTC', 'ARN/BTC', 'GVT/BTC', 'CDT/BTC', 'GXS/BTC', 'POE/BTC', 'QSP/BTC', 'BTS/BTC', 'XZC/BTC', 'LSK/BTC', 'TNT/BTC', 'FUEL/BTC', 'MANA/BTC', 'BCD/BTC', 'ADX/BTC', 'ADA/BTC', 'PPT/BTC', 'CMT/BTC', 'XLM/BTC', 'CND/BTC', 'LEND/BTC', 'WABI/BTC', 'TNB/BTC', 'WAVES/BTC', 'GTO/BTC', 'ICX/BTC', 'OST/BTC', 'ELF/BTC', 'AION/BTC', 'NEBL/BTC', 'BRD/BTC', 'NAV/BTC', 'LUN/BTC', 'APPC/BTC', 'VIBE/BTC', 'RLC/BTC', 'INS/BTC', 'PIVX/BTC', 'IOST/BTC', 'STEEM/BTC', 'NANO/BTC', 'VIA/BTC', 'BLZ/BTC', 'AE/BTC', 'POA/BTC', 'ZIL/BTC', 'ONT/BTC', 'XEM/BTC', 'WAN/BTC', 'WPR/BTC', 'QLC/BTC', 'SYS/BTC', 'GRS/BTC', 'GNT/BTC', 'LOOM/BTC', 'REP/BTC', 'ZEN/BTC', 'SKY/BTC', 'CVC/BTC', 'THETA/BTC', 'IOTX/BTC', 'QKC/BTC', 'AGI/BTC', 'NXS/BTC', 'DATA/BTC', 'SC/BTC', 'NAS/BTC', 'ARDR/BTC', 'HOT/BTC', 'VET/BTC', 'DOCK/BTC', 'POLY/BTC', 'HC/BTC', 'GO/BTC', 'RVN/BTC', 'DCR/BTC', 'MITH/BTC', 'BCH/BTC', 'REN/BTC', 'ONG/BTC', 'FET/BTC', 'CELR/BTC', 'MATIC/BTC', 'ATOM/BTC', 'PHB/BTC', 'TFUEL/BTC', 'ONE/BTC', 'FTM/BTC', 'ALGO/BTC', 'ERD/BTC', 'DOGE/BTC', 'DUSK/BTC', 'ANKR/BTC', 'COS/BTC', 'TOMO/BTC', 'PERL/BTC', 'CHZ/BTC', 'BAND/BTC', 'BEAM/BTC', 'XTZ/BTC', 'HBAR/BTC', 'NKN/BTC', 'STX/BTC', 'KAVA/BTC', 'ARPA/BTC', 'CTXC/BTC', 'TROY/BTC', 'VITE/BTC', 'FTT/BTC', 'OGN/BTC', 'DREP/BTC', 'TCT/BTC', 'WRX/BTC', 'LTO/BTC', 'MBL/BTC', 'COTI/BTC', 'STPT/BTC', 'SOL/BTC', 'CTSI/BTC', 'HIVE/BTC', 'CHR/BTC', 'MDT/BTC', 'STMX/BTC', 'PNT/BTC', 'DGB/BTC']


All_ohlcv = []
price = []
buy_sell_log = []


for i in range(len(ticker_list)):
    temp = binance.fetch_ohlcv(ticker_list[i], time_frame)
    All_ohlcv.append(temp)


log_maker_2()
get_perfomance(buy_sell_log)

import ccxt
import time
from pprint import pprint
import datetime
import random
import numpy


def test_trading(day, value, max_num):
    count = 0
    temp = []
    for i, item in enumerate(ticker_list):
        if count == max_num:
            return count, sum(temp), (sum(temp) / count)
        try:
            ohlcv = binance.fetch_ohlcv(item, time_frame)
            PP = (
                ohlcv[-(day + 1)][2] + ohlcv[-(day + 1)][3] + (ohlcv[-(day + 1)][4] * 2)
            ) / 4
            S1_5 = value * PP - ohlcv[-(day + 1)][2]

            S2 = PP - ohlcv[-(day + 1)][2] + ohlcv[-(day + 1)][3]

            # if ohlcv[-day][3] < S1_5:
            #    earning = round(-100 + ohlcv[-day][4]/S1_5*99.985,5)

            if ohlcv[-day][3] < S1_5:
                earning = round(-100 + ohlcv[-day][4] / S1_5 * 99.985, 5)
                # print(item, earning, '%수익')
                # print('buy :',round(S1_5,5), 'sell :',ohlcv[-day][4])
                count += 1
                temp.append(earning)
                buy_and_sell.append(earning)
        except:
            # print(item + '에러-------------------------------------------')
            print("", end="", flush=True)
    if count != 0:
        return count, sum(temp), sum(temp) * (count / max_num)
    else:
        return 0, 0, 0


def position_sizing():
    for i in range(2, 40):
        print("일자 :", i)
        random.shuffle(ticker_list)
        a, b, c = test_trading(i, 1.97, 6)
        # print(c)
        # print('day',i,': ','count =' ,a,'   earining =' , b, '    total = ', c)

    risk_free = 0.038 / 365
    avg = numpy.mean(buy_and_sell)
    std = numpy.std(buy_and_sell)
    result = (avg - risk_free) / (std * std)
    print("총거래 : ", len(buy_and_sell))
    print("일 평균 거래 :", len(buy_and_sell) / 38)
    print("평균수익", avg)
    print("포지션 사이징", result)
    print("")


binance = ccxt.binance(
    {
        "apiKey": "3pFJ5lblk8ff8brlz2plOG2o",
        "secret": "KKFk0a-YvtW8aEcS33HbQlxJ63rHpdA95D7IWNALSOTVraB1",
        "enableRateLimit": True,
        "RateLimit": 10000,
    }
)
binance.load_markets()

time_frame = "1d"
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


for i in range(10):
    buy_and_sell = []
    position_sizing()

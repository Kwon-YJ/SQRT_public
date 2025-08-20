import ccxt
import time
import pandas as pd
import os
from pprint import pprint
from matplotlib import pyplot as plt
import csv


def get_spot_ohlcv(ticker):
    exchange_class = getattr(ccxt, "binance")
    binance = exchange_class()
    binance.enableRateLimit = True
    binance.RateLimit = 10000
    binance.load_markets()
    result = binance.fetch_ohlcv(ticker, timeframe)
    return result


def get_futures_ohlcv(ticker):
    exchange_class = getattr(ccxt, "binance")
    binance = exchange_class(
        {
            "urls": {
                "api": {
                    "public": "https://fapi.binance.com/fapi/v1",
                    "private": "https://fapi.binance.com/fapi/v1",
                },
            }
        }
    )
    binance.enableRateLimit = True
    binance.RateLimit = 10000
    binance.load_markets()
    result = binance.fetch_ohlcv(ticker, timeframe)
    return result


def bb(x, w=20, k=2):  # 볼린저 밴드
    data = []
    for i in range(len(x)):
        data.append(x[i])
    data = pd.Series(data)
    mbb = data.rolling(w).mean()
    lbb = mbb - k * data.rolling(w).std()
    ubb = mbb + k * data.rolling(w).std()
    # return [lbb.tolist()[-1], mbb.tolist()[-1]]

    return lbb.tolist(), mbb.tolist(), ubb.tolist()


spot_ticker = [
    "BTC/USDT",
    "ETH/USDT",
    "BNB/USDT",
    "NEO/USDT",
    "LTC/USDT",
    "QTUM/USDT",
    "ADA/USDT",
    "XRP/USDT",
    "EOS/USDT",
    "TUSD/USDT",
    "IOTA/USDT",
    "XLM/USDT",
    "ONT/USDT",
    "TRX/USDT",
    "ETC/USDT",
    "ICX/USDT",
    "NULS/USDT",
    "VET/USDT",
    "PAX/USDT",
    "BCH/USDT",
    "USDC/USDT",
    "LINK/USDT",
    "WAVES/USDT",
    "BTT/USDT",
    "USDS/USDT",
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
    "BUSD/USDT",
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
    "EUR/USDT",
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
# 116
futures_ticker = [
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
]
# 27

result = []

timeframe = "1h"
for i in range(len(futures_ticker)):
    for j in range(len(spot_ticker)):
        spot_ohlcv = get_spot_ohlcv(spot_ticker[j])
        futures_ohlcv = get_futures_ohlcv(futures_ticker[i])

        if len(spot_ohlcv) > len(futures_ohlcv):
            spot_ohlcv = spot_ohlcv[len(spot_ohlcv) - len(futures_ohlcv) :]
        elif len(spot_ohlcv) < len(futures_ohlcv):
            futures_ohlcv = futures_ohlcv[len(futures_ohlcv) - len(spot_ohlcv) :]

        # synthetic_ohlcv = [spot_ohlcv[s][4] / futures_ohlcv[s][4] for s in range(len(spot_ohlcv))]
        synthetic_ohlcv = [
            futures_ohlcv[s][4] / spot_ohlcv[s][4] for s in range(len(spot_ohlcv))
        ]

        synthetic_L, synthetic_M, synthetic_U = bb(synthetic_ohlcv)
        temp = []
        try:
            for k in range(len(synthetic_ohlcv)):
                if synthetic_ohlcv[k] > synthetic_U[k]:
                    # print('buy :',synthetic_ohlcv[k], 'sell :', synthetic_ohlcv[k+5])
                    # print(round((1 - synthetic_ohlcv[k+5] / synthetic_ohlcv[k]) *100,3),'%')
                    temp.append(
                        round(
                            (1 - synthetic_ohlcv[k + 5] / synthetic_ohlcv[k]) * 100, 3
                        )
                    )
        except:
            print("")

        # print(len(synthetic_ohlcv) ,len(temp), sum(temp))

        result.append(
            [
                "spot :",
                spot_ticker[j],
                "futures :",
                futures_ticker[i],
                len(synthetic_ohlcv),
                len(temp),
                sum(temp),
            ]
        )

        print(i, "-", j)

        print("")


with open(str(os.getcwd()) + "/savedata1107.csv", "w", newline="") as file:
    for i in range(len(result)):
        writer = csv.writer(file)
        writer.writerow(result[i])


"""
spot : ETH/USDT
futures : THETA/USDT
"""

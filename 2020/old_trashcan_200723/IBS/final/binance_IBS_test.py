# -*- coding: utf-8 -*-
import ccxt
import time
import datetime
import pybithumb


exchange_class = getattr(ccxt, "binance")
binance = exchange_class()
binance.enableRateLimit = True
binance.RateLimit = 10000
binance.apiKey = "FRbVseExyAWjQUtYFnS4memLnPCcgNAeRW7HEBrrw9qyIyPUMCTzUKxZKOJIHcfV"
binance.secret = "CbDX3DE5r9ErdLBOphDB4rjCaAaKbUqITbNK05YIitktZ24VfcNrvVRbIgfK6L87"
binance.load_markets()

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


# IBS = close - low / high - low


day = 2

for i, item in enumerate(ticker_list):
    # try:

    ohlcv = binance.fetch_ohlcv(item, "1d")[-day - 1]
    temp = round((float(ohlcv[2] / ohlcv[1] - 1)) * 100, 3)

    if temp < 19.9:
        continue

    IBS0618 = 0.618 * float(ohlcv[2]) + 0.382 * float(ohlcv[3])
    IBS05 = 0.5 * (float(ohlcv[2]) + float(ohlcv[3]))
    IBS0382 = 0.382 * float(ohlcv[2]) + 0.618 * float(ohlcv[3])

    print(item)
    print("상승률 :", temp)
    print("IBS0.6 :", IBS0618)
    print("IBS0.5 :", IBS05)
    print("IBS0.382 :", IBS0382)

    print("")
    # except:
    #    print(item,'에러')
    #    continue

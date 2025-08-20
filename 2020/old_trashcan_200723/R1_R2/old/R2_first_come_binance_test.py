# -*- coding: utf-8 -*-
import ccxt
import time
import datetime


def get_amount(ticker):
    price = binance.fetch_ohlcv(ticker)[-1][4]
    return (today_money * 0.05) / price


def get_time(temp):
    now = temp
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


def buy_order(ticker):
    buy_amount = get_amount(ticker)
    order = binance.create_order(ticker, "market", "buy", buy_amount)
    is_entering[ticker] = float(order["amount"]) * 0.999


def buy_side():
    while True:
        try:
            for i, item in enumerate(ticker_list):
                time.sleep(0.1)

                ohlcv = binance.fetch_ohlcv(item, "1d")
                ohlcv_2ago = ohlcv[-2]
                PP = (ohlcv_2ago[2] + ohlcv_2ago[3] + (ohlcv_2ago[4] * 2)) / 4
                R2 = PP + ohlcv_2ago[2] - ohlcv_2ago[3]

                if ohlcv[-1][4] > R2:
                    buy_order(item)
                    return None

        except Exception as ex:
            print("err")
            time.sleep(3)
            continue


def sell_side():
    while True:
        try:
            time.sleep(0.1)

            ticker = list(is_entering.keys())[0]
            ohlcv = binance.fetch_ohlcv(ticker, "1d")
            ohlcv_2ago = ohlcv[-2]
            PP = (ohlcv_2ago[2] + ohlcv_2ago[3] + (ohlcv_2ago[4] * 2)) / 4
            R3 = 2 * (PP - ohlcv_2ago[3]) + ohlcv_2ago[2]

            if ohlcv[-1][4] > R3:
                sell_amount = is_entering[ticker]
                binance.create_order(ticker, "market", "sell", sell_amount)
                return None

        except Exception as ex:
            time.sleep(3)
            continue


exchange_class = getattr(ccxt, "binance")
binance = exchange_class()
binance.enableRateLimit = True
binance.RateLimit = 10000
binance.apiKey = "FRbVseExyAWjQUtYFnS4memLnPCcgNAeRW7HEBrrw9qyIyPUMCTzUKxZKOJIHcfV"
binance.secret = "CbDX3DE5r9ErdLBOphDB4rjCaAaKbUqITbNK05YIitktZ24VfcNrvVRbIgfK6L87"
binance.load_markets()

# ticker_list = get_tickers('/USDT')

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
today_money = binance.fetch_balance()["USDT"]["total"]
is_entering = {}


while True:
    try:
        for i, item in enumerate(ticker_list):
            time.sleep(0.1)

            ohlcv = binance.fetch_ohlcv(item, "1d")
            ohlcv_2ago = ohlcv[-2]
            PP = (ohlcv_2ago[2] + ohlcv_2ago[3] + (ohlcv_2ago[4] * 2)) / 4
            R2 = PP + ohlcv_2ago[2] - ohlcv_2ago[3]
            R3 = 1.9 * (PP - ohlcv_2ago[3]) + ohlcv_2ago[2]
            R1 = 2 * PP - ohlcv[-2][3]

            print(item)
            print("R2:", R2, "R3:", R3)
            print("예상수익", R3 / R2)
            print("예상손실", 1 - R1 / R2)

    except Exception as ex:
        print("err")
        time.sleep(3)
        continue

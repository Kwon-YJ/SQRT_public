# -*- coding: utf-8 -*-
import ccxt
import time
import datetime


def get_amount(ticker):
    price = binance.fetch_ohlcv(ticker)[-1][4]
    return (today_money * 0.015) / price


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


def exit_ALL():
    for i in range(len(is_entering)):
        ticker = list(is_entering.keys())[i]
        sell_amount = is_entering[ticker]
        binance.create_order(ticker, "market", "sell", sell_amount)
    reset = {}
    return reset


def buy_order(ticker):
    buy_amount = get_amount(ticker)
    order = binance.create_order(ticker, "market", "buy", buy_amount)
    is_entering[ticker] = float(order["amount"]) * 0.999
    banList.append(ticker)


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


today_money = binance.fetch_balance()["USDT"]["total"]
banList = []
is_entering = {}
temp_list = []


# IBS = close - low / high - low


while True:
    for i, item in enumerate(ticker_list):
        try:
            time.sleep(0.1)
            ohlcv = binance.fetch_ohlcv(item, "1d")[-1]
            temp = round((float(ohlcv[2] / ohlcv[1] - 1)) * 100, 3)

            if temp < 19.9:
                continue

            IBS0382 = 0.382 * float(ohlcv[2]) + 0.618 * float(ohlcv[3])

            if ohlcv[4] < IBS0382 and item not in banList:
                buy_order(item)

        except Exception as ex:
            time.sleep(3)
            continue

    for i in range(len(is_entering)):
        try:
            ticker = list(is_entering.keys())[i]
            ohlcv = binance.fetch_ohlcv(item, "1d")[-1]
            IBS0382 = 0.382 * float(ohlcv[2]) + 0.618 * float(ohlcv[3])

            if ohlcv[4] > IBS0382 * 1.01:
                sell_amount = is_entering[ticker]
                binance.create_order(ticker, "market", "sell", sell_amount)
                temp_list.append(ticker)

        except Exception as ex:
            time.sleep(3)
            continue

    for k in range(len(temp_list)):
        del is_entering[temp_list[k]]
    temp_list.clear()

    time_ = get_time(datetime.datetime.now())[1]
    if time_ == "2359":
        is_entering = exit_ALL()
        banList = []
        today_money = binance.fetch_balance()["USDT"]["total"]
        time.sleep(240)

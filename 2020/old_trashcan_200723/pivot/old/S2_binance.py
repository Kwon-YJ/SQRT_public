import ccxt
import time
import pandas as pd
import os
import datetime
from pprint import pprint


def get_amount(ticker):
    price = binance.fetch_ohlcv(ticker)[-1][4]

    if ticker[-4:] == "USDT":
        return (today_money_USDT / 11) / price
    elif ticker[-3:] == "ETH":
        return (today_money_ETH / 11) / price
    elif ticker[-3:] == "BNB":
        return (today_money_BNB / 11) / price


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
        time.sleep(0.7)
        ticker = list(is_entering.keys())[i]
        sell_amount = is_entering[ticker]
        binance.create_order(ticker, "market", "sell", sell_amount)
    reset = {}
    return reset


def buy_order(ticker):
    buy_amount = get_amount(ticker)
    order = binance.create_order(ticker, "market", "buy", buy_amount)
    is_entering[ticker] = float(order["amount"]) * 0.998
    banList.append(ticker)


def get_tickers(base):
    # base = '/USDT' or '/BNB' or '/BTC' or ...
    All_ticker = binance.fetch_tickers().keys()
    tickers = [s for s in All_ticker if base in s]
    result = []
    for i, item in enumerate(tickers):
        ohlcv = binance.fetch_order_book(item)
        if len(ohlcv["bids"]) != 0:
            result.append(item)
    return result


exchange_class = getattr(ccxt, "binance")
binance = exchange_class()
binance.enableRateLimit = True
binance.RateLimit = 10000
binance.apiKey = "FRbVseExyAWjQUtYFnS4memLnPCcgNAeRW7HEBrrw9qyIyPUMCTzUKxZKOJIHcfV"
binance.secret = "CbDX3DE5r9ErdLBOphDB4rjCaAaKbUqITbNK05YIitktZ24VfcNrvVRbIgfK6L87"
binance.load_markets()


# ticker_list = list(set(get_tickers('/ETH')) | set(get_tickers('/BNB')) | set(get_tickers('/USDT')))
ticker_list = [
    "WTC/BNB",
    "GTO/ETH",
    "FTM/BNB",
    "THETA/ETH",
    "XLM/BNB",
    "WIN/USDT",
    "ATOM/USDT",
    "NULS/USDT",
    "XZC/ETH",
    "HC/USDT",
    "KEY/ETH",
    "IOTA/ETH",
    "ZEC/ETH",
    "ADA/ETH",
    "ZEN/ETH",
    "POWR/ETH",
    "LOOM/ETH",
    "TROY/USDT",
    "MFT/ETH",
    "ZIL/USDT",
    "TOMO/BNB",
    "BNB/ETH",
    "ICX/USDT",
    "XRP/USDT",
    "DOCK/USDT",
    "BTCUP/USDT",
    "BQX/ETH",
    "ETC/ETH",
    "WAVES/ETH",
    "NPXS/ETH",
    "HOT/ETH",
    "LEND/USDT",
    "HOT/USDT",
    "ZRX/BNB",
    "WAN/ETH",
    "ALGO/BNB",
    "WRX/BNB",
    "MDT/USDT",
    "ADA/USDT",
    "NULS/ETH",
    "BLZ/ETH",
    "XMR/ETH",
    "COS/BNB",
    "IQ/BNB",
    "PERL/BNB",
    "NPXS/USDT",
    "MCO/USDT",
    "OMG/USDT",
    "FET/USDT",
    "LEND/ETH",
    "EUR/USDT",
    "LTC/ETH",
    "WAVES/USDT",
    "ICX/BNB",
    "NKN/USDT",
    "ZEC/BNB",
    "KEY/USDT",
    "LRC/ETH",
    "LSK/ETH",
    "WIN/BNB",
    "PERL/USDT",
    "ZIL/ETH",
    "MANA/ETH",
    "NEO/BNB",
    "XTZ/BNB",
    "FUN/USDT",
    "THETA/BNB",
    "BNT/ETH",
    "GNT/ETH",
    "TROY/BNB",
    "WTC/USDT",
    "MBL/BNB",
    "STEEM/ETH",
    "RLC/ETH",
    "AION/ETH",
    "DOCK/ETH",
    "CHZ/BNB",
    "CELR/BNB",
    "STX/BNB",
    "LRC/USDT",
    "XRP/ETH",
    "MITH/BNB",
    "BTS/USDT",
    "PAX/USDT",
    "BTT/USDT",
    "ARPA/USDT",
    "BAT/ETH",
    "CTXC/USDT",
    "BTCDOWN/USDT",
    "OST/ETH",
    "DATA/USDT",
    "HIVE/BNB",
    "KAVA/BNB",
    "MCO/ETH",
    "GTO/USDT",
    "ETC/BNB",
    "KAVA/USDT",
    "RLC/USDT",
    "NANO/USDT",
    "ELF/ETH",
    "MFT/USDT",
    "CTSI/USDT",
    "FTT/USDT",
    "SNT/ETH",
    "KNC/ETH",
    "MBL/USDT",
    "ZRX/USDT",
    "XTZ/USDT",
    "BRD/BNB",
    "QKC/ETH",
    "DUSK/USDT",
    "EOS/BNB",
    "STMX/BNB",
    "HBAR/USDT",
    "GXS/ETH",
    "NEO/ETH",
    "QSP/ETH",
    "ADX/ETH",
    "MFT/BNB",
    "MATIC/BNB",
    "NEBL/BNB",
    "REN/USDT",
    "ARDR/USDT",
    "VITE/USDT",
    "XEM/ETH",
    "MDT/BNB",
    "ANKR/BNB",
    "HIVE/USDT",
    "BTT/BNB",
    "ONT/ETH",
    "IOTX/ETH",
    "VET/ETH",
    "ICX/ETH",
    "ARPA/BNB",
    "DREP/USDT",
    "REP/ETH",
    "ZEN/BNB",
    "TUSD/USDT",
    "IOST/ETH",
    "USDC/USDT",
    "EOS/USDT",
    "LSK/USDT",
    "ONT/USDT",
    "XZC/USDT",
    "OGN/BNB",
    "LINK/USDT",
    "DASH/ETH",
    "ARN/ETH",
    "SC/BNB",
    "CTSI/BNB",
    "ETC/USDT",
    "BAT/USDT",
    "SOL/BNB",
    "ENJ/BNB",
    "LTC/USDT",
    "REP/USDT",
    "ONE/BNB",
    "CHR/BNB",
    "BUSD/USDT",
    "MITH/USDT",
    "STORJ/ETH",
    "OGN/USDT",
    "STMX/ETH",
    "XMR/BNB",
    "TRX/USDT",
    "XLM/USDT",
    "ADA/BNB",
    "COTI/BNB",
    "HBAR/BNB",
    "BLZ/BNB",
    "ENJ/USDT",
    "FUN/ETH",
    "NAS/ETH",
    "ONE/USDT",
    "BAT/BNB",
    "CELR/USDT",
    "ZIL/BNB",
    "KNC/USDT",
    "BNB/USDT",
    "TOMO/USDT",
    "ETH/USDT",
    "MATIC/USDT",
    "FTM/USDT",
    "HOT/BNB",
    "IOTA/USDT",
    "COTI/USDT",
    "CMT/ETH",
    "BAND/BNB",
    "DOGE/USDT",
    "AE/ETH",
    "NCASH/ETH",
    "STMX/USDT",
    "GXS/USDT",
    "COS/USDT",
    "VIB/ETH",
    "ERD/BNB",
    "BCH/BNB",
    "BNT/USDT",
    "DASH/USDT",
    "QLC/ETH",
    "BEAM/USDT",
    "EVX/ETH",
    "VET/BNB",
    "NKN/BNB",
    "WAN/USDT",
    "ANKR/USDT",
    "OMG/ETH",
    "STX/USDT",
    "BAND/USDT",
    "NANO/ETH",
    "ENG/ETH",
    "TNT/ETH",
    "ALGO/USDT",
    "DENT/USDT",
    "TCT/USDT",
    "THETA/USDT",
    "NEO/USDT",
    "LINK/ETH",
    "NEBL/ETH",
    "WABI/BNB",
    "LTC/BNB",
    "TFUEL/USDT",
    "ZEC/USDT",
    "KMD/ETH",
    "RLC/BNB",
    "FET/BNB",
    "WAVES/BNB",
    "AION/BNB",
    "IOST/USDT",
    "RVN/USDT",
    "CHR/USDT",
    "ENJ/ETH",
    "BTC/USDT",
    "IOTX/USDT",
    "AION/USDT",
    "CDT/ETH",
    "CVC/ETH",
    "MTL/ETH",
    "COCOS/USDT",
    "COCOS/BNB",
    "XZC/BNB",
    "XRP/BNB",
    "FTT/BNB",
    "QTUM/USDT",
    "XLM/ETH",
    "USDS/USDT",
    "CVC/USDT",
    "STPT/USDT",
    "WTC/ETH",
    "TRX/ETH",
    "DATA/ETH",
    "IOTA/BNB",
    "ERD/USDT",
    "WRX/USDT",
    "STEEM/BNB",
    "STRAT/USDT",
    "CHZ/USDT",
    "BCH/USDT",
    "ATOM/BNB",
    "XVG/ETH",
    "ZRX/ETH",
    "XMR/USDT",
    "EOS/ETH",
    "SC/ETH",
    "VET/USDT",
    "DENT/ETH",
    "PIVX/ETH",
    "BRD/ETH",
    "RVN/BNB",
    "ONT/BNB",
    "TRX/BNB",
    "DASH/BNB",
    "IOST/BNB",
    "QTUM/ETH",
    "LTO/USDT",
    "ONG/USDT",
    "WAN/BNB",
    "MTL/USDT",
    "STRAT/ETH",
]

banList = []
is_entering = {}

today_money_USDT = binance.fetch_balance()["USDT"]["total"]
today_money_ETH = binance.fetch_balance()["ETH"]["total"]
today_money_BNB = binance.fetch_balance()["BNB"]["total"]


while True:
    try:
        for i, item in enumerate(ticker_list):
            time.sleep(0.5)
            time_ = get_time(datetime.datetime.now())[1]
            # if time_ == '0000' or time_ == '0001' or time_ == '0002' or time_ == '0003':
            if time_ == "0000" or time_ == "0001" or time_ == "0002" or time_ == "0003":
                is_entering = exit_ALL()
                banList = []
                today_money_USDT = binance.fetch_balance()["USDT"]["total"]
                today_money_ETH = binance.fetch_balance()["ETH"]["total"]
                today_money_BNB = binance.fetch_balance()["BNB"]["total"]
                time.sleep(179)

            if len(is_entering) > 33 or item in banList:
                time.sleep(40)
                continue



            if ohlcv[-1][4] < S2:
                buy_order(item)

    except Exception as ex:
        print("err", item)
        time.sleep(15)
        continue

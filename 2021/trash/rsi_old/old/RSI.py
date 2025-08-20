# -*- coding: utf-8 -*-
import ccxt
import time
import pandas as pd
import numpy as np
import urllib
import json
import datetime


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


def calcRSI(ticker, period):
    ohlcv = binance.fetch_ohlcv(ticker, "5m")
    df = pd.DataFrame(
        data=np.array(ohlcv),
        columns=["time_stamp", "open", "high", "low", "close", "volume"],
    )
    U = np.where(
        df.diff(1)["close"] > 0, df.diff(1)["close"], 0
    )  # df.diff를 통해 (기준일 종가 - 기준일 전일 종가)를 계산하여 0보다 크면 증가분을 감소했으면 0을 넣어줌
    D = np.where(
        df.diff(1)["close"] < 0, df.diff(1)["close"] * (-1), 0
    )  # df.diff를 통해 (기준일 종가 - 기준일 전일 종가)를 계산하여 0보다 작으면 감소분을 증가했으면 0을 넣어줌
    AU = pd.DataFrame(U).ewm(period).mean()  # AU, period=14일 동안의 U의 평균
    AD = pd.DataFrame(D).ewm(period).mean()  # AD, period=14일 동안의 D의 평균
    RSI = AU / (AD + AU) * 100  # 0부터 1로 표현되는 RSI에 100을 곱함
    # return RSI
    return float(RSI.tail(1)[0])


exchange_class = getattr(ccxt, "binance")
binance = exchange_class()
binance.enableRateLimit = True
binance.RateLimit = 10000
binance.apiKey = "FRbVseExyAWjQUtYFnS4memLnPCcgNAeRW7HEBrrw9qyIyPUMCTzUKxZKOJIHcfV"
binance.secret = "CbDX3DE5r9ErdLBOphDB4rjCaAaKbUqITbNK05YIitktZ24VfcNrvVRbIgfK6L87"
binance.load_markets()


def trade_order(ticker):
    buy_amount = get_amount(ticker)
    order = binance.create_order(ticker, "market", "buy", buy_amount)
    amount_ = float(order["amount"])
    return amount_


def get_amount(ticker):
    price = binance.fetch_ohlcv(ticker)[-1][4]
    today_money = 21
    return today_money / price


# ticker_list = ['BTC/USDT', 'ETH/USDT', 'BCH/USDT', 'LTC/USDT']
# ticker_list = ['BTC/BUSD', 'ETH/BUSD', 'BCH/BUSD', 'LTC/BUSD']
ticker_list = [
    "DOGE/BUSD",
    "XMR/BUSD",
    "ZRX/BUSD",
    "SXP/BUSD",
    "XTZ/BUSD",
    "SUSHI/BUSD",
    "KNC/BUSD",
    "BTC/BUSD",
    "UNI/BUSD",
    "RSR/BUSD",
    "RUNE/BUSD",
    "ALGO/BUSD",
    "ETH/BUSD",
    "LTC/BUSD",
    "MATIC/BUSD",
    "MKR/BUSD",
    "IOTA/BUSD",
    "STORJ/BUSD",
    "ZIL/BUSD",
    "ZEC/BUSD",
    "BAT/BUSD",
    "VET/BUSD",
    "XRP/BUSD",
    "COMP/BUSD",
    "CRV/BUSD",
    "LINK/BUSD",
    "BEL/BUSD",
    "XLM/BUSD",
    "SOL/BUSD",
    "AXS/BUSD",
    "ALPHA/BUSD",
    "ICX/BUSD",
    "FIL/BUSD",
    "BNB/BUSD",
    "SRM/BUSD",
    "CTK/BUSD",
    "ADA/BUSD",
    "FLM/BUSD",
    "NEAR/BUSD",
    "OCEAN/BUSD",
    "SNX/BUSD",
    "AAVE/BUSD",
    "NEO/BUSD",
    "LRC/BUSD",
    "ATOM/BUSD",
    "ETC/BUSD",
    "EOS/BUSD",
    "DASH/BUSD",
    "BZRX/BUSD",
    "SKL/BUSD",
    "TOMO/BUSD",
    "WAVES/BUSD",
    "KSM/BUSD",
    "TRX/BUSD",
    "BAL/BUSD",
    "YFI/BUSD",
    "BLZ/BUSD",
    "TRB/BUSD",
    "QTUM/BUSD",
    "BCH/BUSD",
    "ONT/BUSD",
    "DOT/BUSD",
    "YFII/BUSD",
    "AVAX/BUSD",
    "EGLD/BUSD",
    "ENJ/BUSD",
]


while 1:
    # if int(get_time()[1])%5 != 0:
    #    continue
    for i in range(len(ticker_list)):
        try:
            time.sleep(0.1)
            RSI = calcRSI(ticker_list[i], 11)
            if RSI < 20:
                sell_amount = trade_order(ticker_list[i])
                while 1:
                    try:
                        time.sleep(0.1)
                        RSI = calcRSI(ticker_list[i], 11)
                        if RSI > 45:
                            binance.create_order(
                                ticker_list[i], "market", "sell", sell_amount * 0.99994
                            )
                            break
                    except:
                        time.sleep(1)
                        continue
        except:
            time.sleep(1)
            continue

# -*- coding: utf-8 -*-
import ccxt
import time
import datetime
import telegram
import pandas as pd
import numpy as np


def get_time():
    now = datetime.datetime.now()
    # now = datetime.datetime.now() + datetime.timedelta(seconds=55)
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


def send_MSG(message):
    while True:
        try:
            bot.send_message(chat_id=801167350, text=str(message))
            time.sleep(3)
            return None
        except:
            time.sleep(3)
            continue


def bb(x, w=20, k=2):  # 볼린저 밴드
    data = []
    for i in range(len(x)):
        data.append(x[i][4])
    data = pd.Series(data)
    mbb = data.rolling(w).mean()
    lbb = mbb - k * data.rolling(w).std()
    ubb = mbb + k * data.rolling(w).std()
    return [lbb.tolist()[-5:], mbb.tolist()[-5:], ubb.tolist()[-5:]]


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
binance.apiKey = "FRbVseExyAWjQUtYFnS4memLnPCcgNAeRW7HEBrrw9qyIyPUMCTzUKxZKOJIHcfV"
binance.secret = "CbDX3DE5r9ErdLBOphDB4rjCaAaKbUqITbNK05YIitktZ24VfcNrvVRbIgfK6L87"
binance.enableRateLimit = True
binance.RateLimit = 10000
binance.load_markets()


bot = telegram.Bot(token=my_token)


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
    "KAVA/USDT",
    "BAND/USDT",
    "RLC/USDT",
    "WAVES/USDT",
    "MKR/USDT",
    "SNX/USDT",
    "DOT/USDT",
    "DEFI/USDT",
    "YFI/USDT",
    "BAL/USDT",
    "CRV/USDT",
    "TRB/USDT",
    "YFII/USDT",
    "RUNE/USDT",
    "SUSHI/USDT",
    "SRM/USDT",
    "BZRX/USDT",
    "EGLD/USDT",
    "SOL/USDT",
    "ICX/USDT",
    "STORJ/USDT",
    "BLZ/USDT",
    "UNI/USDT",
    "AVAX/USDT",
    "FTM/USDT",
    "HNT/USDT",
    "ENJ/USDT",
    "FLM/USDT",
    "TOMO/USDT",
    "REN/USDT",
    "KSM/USDT",
    "NEAR/USDT",
    "AAVE/USDT",
    "FIL/USDT",
    "RSR/USDT",
    "LRC/USDT",
    "MATIC/USDT",
    "OCEAN/USDT",
    "CVC/USDT",
    "BEL/USDT",
    "CTK/USDT",
    "AXS/USDT",
    "ALPHA/USDT",
    "ZEN/USDT",
    "SKL/USDT",
    "GRT/USDT",
    "1INCH/USDT",
    "AKRO/USDT",
    "DOTECO/USDT",
    "CHZ/USDT",
    "SAND/USDT",
    "ANKR/USDT",
]


def trade_order(ticker, side):
    sell_amount = get_amount(ticker)
    order = binance.create_order(ticker, "market", side, sell_amount)


def get_amount(ticker):
    price = binance.fetch_ohlcv(ticker)[-1][4]
    today_money = 150
    return today_money / price


def BB_checking(ohlcv15, name):
    BB_value = bb(ohlcv15)  # [lbb, mbb, ubb]
    ohlcv15 = ohlcv15[-5:]
    if ohlcv15[-2][4] > BB_value[1][-2] and ohlcv15[-3][4] < BB_value[1][-3]:
        temp = [i for i in range(len(ohlcv15)) if ohlcv15[i][4] < BB_value[0][i]]
        if len(temp) != 0:
            trade_order(name, "buy")

    elif ohlcv15[-2][4] < BB_value[1][-2] and ohlcv15[-3][4] > BB_value[1][-3]:
        temp = [i for i in range(len(ohlcv15)) if ohlcv15[i][4] > BB_value[2][i]]
        if len(temp) != 0:
            trade_order(name, "sell")
            # print('sell', item)


while 1:
    time.sleep(4)
    temp = int(get_time()[1][2:]) % 5
    if temp == 0:
        ticker_list = list(set(ticker_list))
        for i, item in enumerate(ticker_list):
            ohlcv5 = binance.fetch_ohlcv(ticker_list[i], "5m")
            BB_checking(ohlcv5, ticker_list[i])
        time.sleep(60)

# -*- coding: utf-8 -*-

import ccxt
import time
import datetime
import pandas as pd
import telegram


def bb(x, w=20, k=2):  # 볼린저 밴드
    data = []
    for i in range(len(x)):
        data.append(x[i][4])
    data = pd.Series(data)
    mbb = data.rolling(w).mean()
    lbb = mbb - k * data.rolling(w).std()
    ubb = mbb + k * data.rolling(w).std()
    return [lbb.tolist()[-2], mbb.tolist()[-2], ubb.tolist()[-2]]


def get_decimal(ticker):
    Group_14 = [
        "XRP/USDT",
        "ONT/USDT",
        "IOTA/USDT",
        "BAT/USDT",
        "LEND/USDT",
        "SXP/USDT",
        "OMG/USDT",
        "ZRX/USDT",
        "ALGO/USDT",
        "THETA/USDT",
        "KAVA/USDT",
        "BAND/USDT",
        "RLC/USDT",
        "WAVES/USDT",
    ]
    Group_13 = [
        "EOS/USDT",
        "XTZ/USDT",
        "QTUM/USDT",
        "SNX/USDT",
        "DOT/USDT",
        "BAL/USDT",
        "CRV/USDT",
        "TRB/USDT",
    ]
    Group_05 = [
        "TRX/USDT",
        "XLM/USDT",
        "ADA/USDT",
        "KNC/USDT",
        "ZIL/USDT",
        "RUNE/USDT",
        "SUSHI/USDT",
        "SRM/USDT",
        "BZRX/USDT",
    ]
    Group_06 = ["VET/USDT", "IOST/USDT", "DOGE/USDT"]

    if any(ticker in i for i in Group_14):
        return 1, 4
    elif any(ticker in i for i in Group_13):
        return 1, 3
    elif any(ticker in i for i in Group_05):
        return 0, 5
    elif any(ticker in i for i in Group_06):
        return 0, 6
    elif ticker == "LINK/USDT" or ticker == "COMP/USDT":
        return 2, 3
    elif ticker == "DEFI/USDT" or "YFI/USDT" or "YFII/USDT":
        return 3, 1
    else:  # MKR/USDT, others...
        return 3, 2


def get_amount(ticker):
    price = binance.fetch_ohlcv(ticker)[-1][4]
    # today_money_USDT = float(binance.fetch_balance()['info']['assets'][0]['walletBalance'])
    today_money_USDT = 200
    decimal_amount = get_decimal(ticker)[0]
    result = round(today_money_USDT / price, decimal_amount)
    return result


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


def do_order(ticker):
    ohlcv = binance.fetch_ohlcv(ticker, "1h")
    close_ = ohlcv[-1][4]
    bb_data = bb(ohlcv)
    if bb_data[2] < close_:
        entry_amount = get_amount(ticker)
        order = binance.create_order(ticker, "market", "sell", entry_amount)
        return [ticker, float(order["amount"])]
    return None


bot = telegram.Bot(token=my_token)


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

temp = 0


while 1:
    time_ = get_time()[1][2:]
    if time_ == "00":
        break
    else:
        time.sleep(27)

while True:
    temp = []
    # try:
    time_ = get_time()[1][2:]
    if time_ == "00":
        temp.append(do_order("DOGE/USDT"))
        temp.append(do_order("ETC/USDT"))
    while 1:
        time.sleep(7)
        if get_time()[1][2:] == "59":
            break
    for i in range(len(temp)):
        if temp[i] == None:
            continue
        else:
            order = binance.create_order(temp[i][0], "market", "buy", temp[i][1])
    # except Exception as ex:
    #    continue

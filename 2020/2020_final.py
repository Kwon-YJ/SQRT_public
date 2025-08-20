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
    today_money_USDT = float(
        binance.fetch_balance()["info"]["assets"][0]["walletBalance"]
    )
    decimal_amount = get_decimal(ticker)[0]
    result = round(today_money_USDT / price * 0.21, decimal_amount)
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


def do_order(ticker, side):
    ohlcv = binance.fetch_ohlcv(ticker, "1h")
    close_ = ohlcv[-2][4]
    bb_data = bb(ohlcv)
    if side == "buy":
        target_price = bb_data[0]
        exit_price = round(bb_data[1], get_decimal(ticker)[1])
        if close_ < target_price:
            entry_amount = get_amount(ticker)
            order = binance.create_order(ticker, "market", side, entry_amount)
            binance.create_order(
                ticker, "limit", "sell", float(order["amount"]), exit_price
            )
            return 1
    elif side == "sell":
        target_price = bb_data[2]
        exit_price = round(bb_data[1], get_decimal(ticker)[1])
        if close_ > target_price:
            entry_amount = get_amount(ticker)
            order = binance.create_order(ticker, "market", side, entry_amount)
            binance.create_order(
                ticker, "limit", "buy", float(order["amount"]), exit_price
            )
            return 1
    return 0


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
    try:
        time_ = get_time()[1]
        if time_ == "2358":
            today_money_USDT = float(
                binance.fetch_balance()["info"]["assets"][0]["walletBalance"]
            )
            messege = "margin balance: {ii}\n24H number of trade: {ff}".format(
                ii=today_money_USDT, ff=temp
            )
            bot.send_message(chat_id=801167350, text=messege)
            temp = 0
            time.sleep(60)

        time_ = get_time()[1][2:]
        if time_ == "00":
            a = do_order("BTC/USDT", "buy")
            b = do_order("BNB/USDT", "buy")
            c = do_order("BCH/USDT", "buy")
            d = do_order("LTC/USDT", "buy")
            e = do_order("ADA/USDT", "buy")
            f = do_order("TRX/USDT", "buy")
            h = do_order("DEFI/USDT", "sell")
            temp = temp + a + b + c + d + e + f + h
            time.sleep(60)

        time.sleep(1)

    except Exception as ex:
        time.sleep(3)
        continue

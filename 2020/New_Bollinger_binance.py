# -*- coding: utf-8 -*-
import ccxt
import math
import time
import datetime
import numpy as np
import telegram


def send_err(err_message):
    while True:
        try:
            bot.send_message(chat_id=801167350, text=str(err_message))
            time.sleep(3)
            return None
        except:
            time.sleep(3)
            continue


def bb(x, w, k):  # 볼린저 밴드
    mbb = HMA(x, w)
    lbb = mbb - k * np.std(x[-w:])
    ubb = mbb + k * np.std(x[-w:])
    return lbb[-1] * 0.9975, ubb[-1] * 1.0025


def WMA(df, period):  # 가중이동평균
    result = []
    for epoch in range(len(df) - period + 1):
        value = 0
        for n in range(1, period + 1):
            value = value + ((df[n + epoch - 1]) * n)
        result.append(value / ((period * (period + 1)) / 2))
    return result


def HMA(df, period):  # Hull 이동평균
    data1 = WMA(df, int(period / 2))
    for i in range(0, len(data1)):
        data1[i] = data1[i] * 2
    data2 = WMA(df, period)
    data3 = []
    for i in range(0, len(data2)):
        data3.append(data1[i + len(data1) - len(data2)] - data2[i])
    return WMA(data3, int(math.sqrt(period)))


def convert(ohlcv5):  # convert 5m → 15m
    ohlcv15 = []
    temp = str(datetime.datetime.fromtimestamp(ohlcv5[0][0] / 1000))[14:16]
    if int(temp) % 15 == 5:
        del ohlcv5[0]
        del ohlcv5[1]
    elif int(temp) % 15 == 10:
        del ohlcv5[0]
    for i in range(0, len(ohlcv5) - 2, 3):
        highs = [ohlcv5[i + j][2] for j in range(0, 3) if ohlcv5[i + j][2]]
        lows = [ohlcv5[i + j][3] for j in range(0, 3) if ohlcv5[i + j][3]]
        volumes = [ohlcv5[i + j][5] for j in range(0, 3) if ohlcv5[i + j][5]]
        candle = [
            ohlcv5[i + 0][0],
            ohlcv5[i + 0][1],
            max(highs) if len(highs) else None,
            min(lows) if len(lows) else None,
            ohlcv5[i + 2][4],
        ]
        ohlcv15.append(candle)
    return ohlcv15


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
    today_money_USDT = 600
    decimal_amount = get_decimal(ticker)[0]
    result = round(today_money_USDT / price, decimal_amount)
    return result


def market_order(ticker, side):
    if ticker_list[ticker] == 0:
        amount = get_amount(ticker)
    else:
        amount = ticker_list[ticker] * 2
    order = binance.create_order(ticker, "market", side, amount)
    if side == "sell":
        ticker_list[ticker] = -1 * float(order["amount"])
    else:
        ticker_list[ticker] = float(order["amount"])


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

ticker_list = {
    "BCH/USDT": 0,
    "XRP/USDT": 0,
    "LTC/USDT": 0,
    "ETC/USDT": 0,
    "XLM/USDT": 0,
    "DOGE/USDT": 0,
}
# { 'tickername' = side] } // +1 == buy side position, -1 = sell side position, 0 == first trade


while True:
    time.sleep(9)
    time_ = get_time()[1][2:]
    if time_ == "00" or time_ == "15" or time_ == "30" or time_ == "45":
        time.sleep(11)
        for key, value in ticker_list.items():
            try:
                ohlcv_5 = binance.fetch_ohlcv(key, "5m")
                ohlcv_15 = convert(ohlcv_5)
                ohlcv_15_close = [ohlcv_15[x][4] for x in range(len(ohlcv_15))]
                MA_value = 36
                STD_value = 1.8
                lbb_, ubb_ = bb(ohlcv_15_close, MA_value, STD_value)  # Bollinger_band
                high_ = ohlcv_15[-1][2]
                low_ = ohlcv_15[-1][3]

                if high_ > ubb_ and value > 0:
                    market_order(key, "sell")
                elif low_ < lbb_ and value < 0:
                    market_order(key, "buy")
            except Exception as e:
                time.sleep(2)
                send_err(e)
                continue

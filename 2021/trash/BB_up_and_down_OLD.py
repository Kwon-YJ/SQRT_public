# -*- coding: utf-8 -*-
import ccxt
import time
import datetime
import telegram
import pandas as pd
import numpy as np


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
    return [lbb.tolist()[-20:], mbb.tolist()[-20:], ubb.tolist()[-20:]]


def custom_convert(ticker):  # convert 5m → 15m
    ohlcv5 = binance.fetch_ohlcv(ticker, "5m")
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
        candle = [
            ohlcv5[i + 0][0],
            ohlcv5[i + 0][1],
            max(highs) if len(highs) else None,
            min(lows) if len(lows) else None,
            ohlcv5[i + 2][4],
        ]
        ohlcv15.append(candle)
    if int(temp) % 15 == 0:
        ohlcv15.append(
            [
                ohlcv5[-1][0],
                ohlcv5[-2][1],
                max([ohlcv5[-1][2], ohlcv5[-2][2]]),
                min([ohlcv5[-1][3], ohlcv5[-2][3]]),
                ohlcv5[-1][4],
            ]
        )
    if int(temp) % 15 == 10:
        ohlcv15.append(ohlcv5[-1][:-1])
    return ohlcv15


def calcRSI(ohlcv, period):
    df = pd.DataFrame(
        data=np.array(ohlcv), columns=["time_stamp", "open", "high", "low", "close"]
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


def BB_checking(ohlcv15, name):
    BB_value = bb(ohlcv15)  # [lbb, mbb, ubb]
    ohlcv15 = ohlcv15[-20:]
    if ohlcv15[-1][4] > BB_value[2][-1]:
        temp = [i for i in range(len(BB_value[0])) if ohlcv15[i][4] < BB_value[0][i]]
        if len(temp) != 0:
            msg = "15min  " + name + "  sell entry"
            send_MSG(msg)
            great_escape(1, name)

    elif ohlcv15[-1][4] < BB_value[0][-1]:
        temp = [i for i in range(len(BB_value[0])) if ohlcv15[i][4] > BB_value[2][i]]
        if len(temp) != 0:
            msg = "15min  " + name + "  buy entry"
            send_MSG(msg)
            great_escape(-1, name)


def great_escape(side, ticker_name):
    entry_price = binance.fetch_ohlcv(ticker_name, "5m")[-1][4]
    time.sleep(60)
    count = 0
    # print(entry_price)

    while 1:
        time.sleep(4)
        temp = int(get_time()[1][2:]) % 15
        if temp == 0:
            # if True:
            ohlcv15 = custom_convert(ticker_name)
            if ohlcv15[-2][1] > ohlcv15[-2][4] and side == 1:  # sell entry
                count += 1
                if count == 2:
                    exit_price = binance.fetch_ohlcv(ticker_name, "5m")[-1][4]

                    # print(exit_price)

                    # earning = 100 * (entry_price / exit_price) * 0.9996 * 0.9996 - 1
                    earning = entry_price / exit_price

                    # msg = ticker_name + '  '+ str(round(earning, 2)) + ' exit'
                    msg = ticker_name + "  " + str(earning) + " exit"
                    send_MSG(msg)
                    time.sleep(60)
                    return None
            elif ohlcv15[-2][1] < ohlcv15[-2][4] and side == -1:  # buy enty
                count += 1
                if count == 2:
                    exit_price = binance.fetch_ohlcv(ticker_name, "5m")[-1][4]

                    # print(exit_price)

                    # earning = 100 * (exit_price / entry_price) * 0.9996 * 0.9996 - 1
                    earning = exit_price / entry_price

                    # msg = ticker_name + '  '+ str(round(earning, 2)) + ' exit'
                    msg = ticker_name + "  " + str(earning) + " exit"
                    send_MSG(msg)
                    time.sleep(60)
                    return None
            time.sleep(60)


while 1:
    time.sleep(4)
    temp = int(get_time()[1][2:]) % 15
    if temp == 0:
        ticker_list = list(set(ticker_list))
        for i, item in enumerate(ticker_list):
            ohlcv15 = custom_convert(ticker_list[i])
            RSI = calcRSI(ohlcv15, 14)
            if RSI > 70 or RSI < 30:
                BB_checking(ohlcv15, ticker_list[i])
        time.sleep(60)

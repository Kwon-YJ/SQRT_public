# -*- coding: utf-8 -*-
import ccxt
import time
import pandas as pd
import numpy as np
import urllib
import json
import datetime
import telegram


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


def get_funding_rate(temp):
    target = temp + "/USDT"
    ticker_list = [
        "THETA/USDT",
        "STORJ/USDT",
        "ONT/USDT",
        "ENJ/USDT",
        "LTC/USDT",
        "XRP/USDT",
        "IOST/USDT",
        "DOT/USDT",
        "NEO/USDT",
        "XLM/USDT",
        "CVC/USDT",
        "LINK/USDT",
        "OMG/USDT",
        "EOS/USDT",
        "IOTA/USDT",
        "WAVES/USDT",
        "TRX/USDT",
        "XTZ/USDT",
        "VET/USDT",
        "ICX/USDT",
        "KNC/USDT",
        "ATOM/USDT",
        "ZRX/USDT",
        "SRM/USDT",
        "ZIL/USDT",
        "ADA/USDT",
        "BTC/USDT",
        "KAVA/USDT",
        "ETH/USDT",
        "QTUM/USDT",
        "ETC/USDT",
        "SXP/USDT",
        "BAT/USDT",
        "BCH/USDT",
    ]
    url = "https://fapi.binance.com/fapi/v1/premiumIndex"
    text_data = urllib.request.urlopen(url).read().decode("utf-8")
    tickers = json.loads(text_data)
    EndPoint = len(tickers)
    All_funding_rate = {}
    for i in range(EndPoint):
        # funding_rate = float(tickers[i]['lastFundingRate'])
        ticker = tickers[i]["symbol"][:-4] + "/USDT"
        if ticker in ticker_list:
            All_funding_rate[ticker] = float(tickers[i]["lastFundingRate"])
    return All_funding_rate[target]


def calcRSI(df, period):
    U = np.where(
        df.diff(1)["close"] > 0, df.diff(1)["close"], 0
    )  # df.diff를 통해 (기준일 종가 - 기준일 전일 종가)를 계산하여 0보다 크면 증가분을 감소했으면 0을 넣어줌
    D = np.where(
        df.diff(1)["close"] < 0, df.diff(1)["close"] * (-1), 0
    )  # df.diff를 통해 (기준일 종가 - 기준일 전일 종가)를 계산하여 0보다 작으면 감소분을 증가했으면 0을 넣어줌
    AU = pd.DataFrame(U).ewm(period).mean()  # AU, period=14일 동안의 U의 평균
    AD = pd.DataFrame(D).ewm(period).mean()  # AD, period=14일 동안의 D의 평균
    RSI = AU / (AD + AU) * 100  # 0부터 1로 표현되는 RSI에 100을 곱함
    return RSI  # .tail(1).values[0][0]


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

exchange_class = getattr(ccxt, "upbit")
upbit = exchange_class()
upbit.enableRateLimit = True
upbit.RateLimit = 10000
upbit.load_markets()


bot = telegram.Bot(token=my_token)

ticker_list = [
    "THETA",
    "STORJ",
    "ONT",
    "ENJ",
    "LTC",
    "XRP",
    "IOST",
    "DOT",
    "NEO",
    "XLM",
    "CVC",
    "LINK",
    "OMG",
    "EOS",
    "IOTA",
    "WAVES",
    "TRX",
    "XTZ",
    "VET",
    "ICX",
    "KNC",
    "ATOM",
    "ZRX",
    "SRM",
    "ZIL",
    "ADA",
    "BTC",
    "KAVA",
    "ETH",
    "QTUM",
    "ETC",
    "SXP",
    "BAT",
    "BCH",
]
Alert = []


while 1:
    # print('a')
    for i in range(len(ticker_list)):
        try:
            funding_Rate = get_funding_rate(ticker_list[i])
            ticker = ticker_list[i] + "/KRW"

            temp = upbit.fetch_ohlcv(ticker, "5m")
            # ohlcv = convert(temp)
            ohlcv = temp
            df = pd.DataFrame(
                data=np.array(ohlcv),
                columns=["time_stamp", "open", "high", "low", "close", "1"],
            )
            temp_ = calcRSI(df, 20)
            RSI_15 = int(temp_.tail(1)[0])

            # print(ticker_list[i], RSI_15)

            if RSI_15 > 70 and funding_Rate < 0:
                price = binance.fetch_ohlcv(ticker_list[i] + "/USDT", "1d")[-1][4]
                bot.send_message(
                    chat_id=801167350,
                    text=["SELL", ticker_list[i], price, RSI_15, funding_Rate],
                )
                Alert.append(0)

            if RSI_15 < 30 and funding_Rate > 0:
                price = binance.fetch_ohlcv(ticker_list[i] + "/USDT", "1d")[-1][4]
                bot.send_message(
                    chat_id=801167350,
                    text=["BUY", ticker_list[i], price, RSI_15, funding_Rate],
                )
                Alert.append(0)

        except Exception as ex:
            print(ex)
            continue

    if len(Alert) != 0:
        Alert.clear()
        time.sleep(300)

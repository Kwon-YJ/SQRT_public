# -*- coding: utf-8 -*-
import ccxt
import time
import pandas as pd
import numpy as np
import urllib
import json
import datetime
import telegram


def send_MSG(message):
    while True:
        try:
            bot.send_message(chat_id=801167350, text=str(message))
            time.sleep(3)
            return None
        except:
            time.sleep(3)
            continue


def calcRSI(ohlcv, period):
    df = pd.DataFrame(
        data=np.array(ohlcv),
        columns=["time_stamp", "open", "high", "low", "close", "1"],
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


exchange_class = getattr(ccxt, "upbit")
upbit = exchange_class()
upbit.enableRateLimit = True
upbit.RateLimit = 10000
upbit.load_markets()


ticker_list = [
    "ADA/KRW",
    "ADX/KRW",
    "AERGO/KRW",
    "AHT/KRW",
    "ANKR/KRW",
    "AQT/KRW",
    "ARDR/KRW",
    "ARK/KRW",
    "ATOM/KRW",
    "BAT/KRW",
    "BCH/KRW",
    "BCHA/KRW",
    "BORA/KRW",
    "BSV/KRW",
    "BTC/KRW",
    "BTG/KRW",
    "BTT/KRW",
    "CBK/KRW",
    "CHZ/KRW",
    "CRE/KRW",
    "CRO/KRW",
    "CVC/KRW",
    "DKA/KRW",
    "DMT/KRW",
    "DOT/KRW",
    "EDR/KRW",
    "ELF/KRW",
    "EMC2/KRW",
    "ENJ/KRW",
    "EOS/KRW",
    "ETC/KRW",
    "ETH/KRW",
    "FCT2/KRW",
    "GAS/KRW",
    "GLM/KRW",
    "GRS/KRW",
    "GTO/KRW",
    "HBAR/KRW",
    "HIVE/KRW",
    "HUNT/KRW",
    "ICX/KRW",
    "IGNIS/KRW",
    "IOST/KRW",
    "IOTA/KRW",
    "IQ/KRW",
    "JST/KRW",
    "KAVA/KRW",
    "KMD/KRW",
    "KNC/KRW",
    "LAMB/KRW",
    "LBC/KRW",
    "LINK/KRW",
    "LOOM/KRW",
    "LSK/KRW",
    "LTC/KRW",
    "MANA/KRW",
    "MARO/KRW",
    "MBL/KRW",
    "MED/KRW",
    "META/KRW",
    "MFT/KRW",
    "MLK/KRW",
    "MOC/KRW",
    "MTL/KRW",
    "MVL/KRW",
    "NEO/KRW",
    "NPXS/KRW",
    "OBSR/KRW",
    "OMG/KRW",
    "ONG/KRW",
    "ONT/KRW",
    "ORBS/KRW",
    "OST/KRW",
    "PCI/KRW",
    "PLA/KRW",
    "POLY/KRW",
    "POWR/KRW",
    "PXL/KRW",
    "QKC/KRW",
    "QTCON/KRW",
    "QTUM/KRW",
    "REP/KRW",
    "RFR/KRW",
    "SBD/KRW",
    "SC/KRW",
    "SNT/KRW",
    "SOLVE/KRW",
    "SPND/KRW",
    "SRM/KRW",
    "SRN/KRW",
    "SSX/KRW",
    "STEEM/KRW",
    "STMX/KRW",
    "STORJ/KRW",
    "STPT/KRW",
    "STRAX/KRW",
    "SXP/KRW",
    "TFUEL/KRW",
    "THETA/KRW",
    "Tokamak Network/KRW",
    "TRX/KRW",
    "TSHP/KRW",
    "TT/KRW",
    "UPP/KRW",
    "VET/KRW",
    "WAVES/KRW",
    "WAXP/KRW",
    "XEM/KRW",
    "XLM/KRW",
    "XRP/KRW",
    "XTZ/KRW",
    "ZIL/KRW",
    "ZRX/KRW",
]


bot = telegram.Bot(token=my_token)


while 1:
    for i, item in enumerate(ticker_list):
        time.sleep(0.02)
        # try:
        # ohlcv15_= custom_convert(item)
        RSI = calcRSI(upbit.fetch_ohlcv(item, "5m"), 14)
        if RSI < 30:
            # print(item)
            send_MSG(ticker_list[i])
        # except:
        #    time.sleep(1)
        #    print('err')
        #    continue

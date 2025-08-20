# -*- coding: utf-8 -*-
import pandas as pd
import ccxt
import time
import datetime
import urllib.request
import json


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


def get_funding_rate(ticker):
    ticker = ticker[:-5] + "USDT"
    EndPoint = len(binance.fetch_tickers().keys())
    url = "https://fapi.binance.com/fapi/v1/premiumIndex"
    text_data = urllib.request.urlopen(url).read().decode("utf-8")
    tickers = json.loads(text_data)
    All_funding_rate = {}
    for i in range(EndPoint):
        All_funding_rate[tickers[i]["symbol"]] = float(tickers[i]["lastFundingRate"])
    return All_funding_rate[ticker]


def ATR(data, length):
    TR = []
    for i in range(int(length)):
        TR.append(
            max(
                (data[i - length][2] - data[i - length][3]),
                abs(data[i - length][2] - data[i - length - 1][4]),
                abs(data[i - length][3] - data[i - length - 1][4]),
            )
        )
    ATR = pd.Series(TR).ewm(length).mean()
    return ATR.tolist()


def get_ADX(ohlcv, length):
    DMP = []
    DMM = []
    PDI = []
    MDI = []
    DX = []
    for i in range(1, len(ohlcv)):
        if (ohlcv[i][2] - ohlcv[i - 1][2] > ohlcv[i - 1][3] - ohlcv[i][3]) == True:
            DMP.append(ohlcv[i][2] - ohlcv[i - 1][2])
        else:
            DMP.append(0)

        if (ohlcv[i - 1][3] - ohlcv[i][3] > ohlcv[i][2] - ohlcv[i - 1][2]) == True:
            DMM.append(ohlcv[i - 1][3] - ohlcv[i][3])
        else:
            DMM.append(0)

    smoothTR = ATR(ohlcv, length)
    smoothDMP = pd.Series(DMP).ewm(length).mean().tolist()[-length:]
    smoothDMM = pd.Series(DMM).ewm(length).mean().tolist()[-length:]
    for i in range(len(smoothTR)):
        PDI.append(smoothDMP[i] / smoothTR[i] * 100)
        MDI.append(smoothDMM[i] / smoothTR[i] * 100)
    for i in range(len(smoothTR)):
        DX.append(abs(PDI[i] - MDI[i]) / (PDI[i] + MDI[i]) * 100)
    ADX = pd.Series(DX).ewm(length).mean().tolist()
    return ADX


def get_amount(ticker):
    price = binance.fetch_ohlcv(ticker)[-1][4]
    today_money_USDT = float(
        binance.fetch_balance()["info"]["assets"][0]["walletBalance"]
    )
    decimal_amount = get_decimal(ticker)[0]
    result = round(today_money_USDT / price * 0.058, decimal_amount)
    return result


def entry_order(ticker, exit_price):
    buy_amount = get_amount(ticker)
    order = binance.create_order(ticker, "market", "sell", buy_amount)
    is_entering[ticker] = [float(order["amount"]), exit_price]


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
is_entering = {}


ticker_list = [
    "BTC/USDT",
    "ETH/USDT",
    "BCH/USDT",
    "XRP/USDT",
    "XLM/USDT",
    "EOS/USDT",
    "LTC/USDT",
    "TRX/USDT",
    "ETC/USDT",
    "LINK/USDT",
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
    "LEND/USDT",
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
]


while 1:
    time_ = get_time()[1][2:]
    if time_ == "00":
        break
    else:
        time.sleep(27)

while True:
    temp = []
    time_ = get_time()[1][2:]
    if time_ == "00":
        for i, item in enumerate(ticker_list):
            try:
                if get_funding_rate(item) < 0:
                    continue
                ohlcv = binance.fetch_ohlcv(item, "1h")
                open_ = ohlcv[-2][1]
                high_ = ohlcv[-2][2]
                low_ = ohlcv[-2][3]
                close_ = ohlcv[-2][4]
                ADX = get_ADX(ohlcv, 14)
                IBS = (close_ - low_) / (high_ - low_)
                if high_ - low_ == 0:
                    continue
                if (IBS <= 0.1 and ADX >= 26) and item not in list(is_entering.keys()):
                    if (high_ - low_) * 0.4 < 0.015:
                        exit_price = low_ * 0.985
                    else:
                        exit_price = low_ - (high_ - low_) * 0.4
                    entry_order(item, exit_price)
            except:
                time.sleep(1)
                continue
        time.sleep(59)

    for i in range(len(is_entering)):
        try:
            ticker = list(is_entering.keys())[i]
            now_price = binance.fetch_ohlcv(ticker, "1h")[-1][4]
            exit_price = is_entering[ticker][1]
            if now_price <= exit_price:
                exit_amount = is_entering[ticker][0]
                binance.create_order(ticker, "market", "buy", exit_amount)
                temp.append(ticker)
        except:
            time.sleep(1)
            continue
    for i in range(len(temp)):
        del is_entering[temp[i]]
    time.sleep(6)

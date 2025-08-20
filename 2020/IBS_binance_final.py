import ccxt
import time
import datetime
import urllib.request
import json


def get_funding_rate():
    url = "https://fapi.binance.com/fapi/v1/premiumIndex"
    text_data = urllib.request.urlopen(url).read().decode("utf-8")
    tickers = json.loads(text_data)
    EndPoint = len(tickers)
    All_funding_rate = []
    for i in range(EndPoint):
        funding_rate = float(tickers[i]["lastFundingRate"])
        if funding_rate <= 0.0001 and funding_rate >= -0.0001:
            ticker = tickers[i]["symbol"][:-4] + "/USDT"
            if ticker in ticker_list:
                All_funding_rate.append(ticker)
    return All_funding_rate


def get_amount(ticker):
    price = binance.fetch_ohlcv(ticker)[-1][4]
    today_money_USDT = binance.fetch_balance()["USDT"]["total"]
    size = [
        0.016,
        0.016260163,
        0.016528926,
        0.016806723,
        0.017094017,
        0.017391304,
        0.017699115,
        0.018018018,
        0.018348624,
        0.018691589,
        0.019047619,
        0.019417476,
        0.01980198,
        0.02020202,
        0.020618557,
        0.021052632,
        0.021505376,
        0.021978022,
        0.02247191,
        0.022988506,
        0.023529412,
        0.024096386,
        0.024691358,
        0.025316456,
        0.025974026,
        0.026666667,
        0.02739726,
        0.028169014,
        0.028985507,
        0.029850746,
        0.030769231,
        0.031746032,
        0.032786885,
        0.033898305,
        0.035087719,
        0.036363636,
        0.037735849,
        0.039215686,
        0.040816327,
        0.042553191,
        0.044444444,
        0.046511628,
        0.048780488,
        0.051282051,
        0.054054054,
        0.057142857,
        0.060606061,
        0.064516129,
        0.068965517,
        0.074074074,
        0.08,
    ]
    return (today_money_USDT * size[len(is_entering)]) / price


def buy_order(ticker, sell_price):
    buy_amount = get_amount(ticker)
    order = binance.create_order(ticker, "market", "buy", buy_amount)
    is_entering[ticker] = [float(order["amount"]) * 0.99995, sell_price]


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
binance = exchange_class()
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

global_num = 0


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
        funding_fee = get_funding_rate()
        for i, item in enumerate(funding_fee):
            try:
                ohlcv = binance.fetch_ohlcv(item, "1h")
                open_ = ohlcv[-2][1]
                high_ = ohlcv[-2][2]
                low_ = ohlcv[-2][3]
                close_ = ohlcv[-2][4]

                if high_ - low_ == 0:
                    continue

                IBS = (close_ - low_) / (high_ - low_)

                if IBS < 0.1 and item not in list(is_entering.keys()):
                    buy_order(item, high_ * 1.0014)
                    if global_num == 3:
                        time.sleep(59)
                        global_num = 0
                        break
                    else:
                        global_num += 1
            except:
                time.sleep(1)
                continue
        time.sleep(59)

    for i in range(len(is_entering)):
        try:
            ticker = list(is_entering.keys())[i]
            now_price = binance.fetch_ohlcv(ticker, "1h")[-1][4]
            sell_price = is_entering[ticker][1]
            if sell_price < now_price:
                sell_amount = is_entering[ticker][0]
                binance.create_order(ticker, "market", "sell", sell_amount)
                temp.append(ticker)
        except:
            time.sleep(2)
            continue

    for i in range(len(temp)):
        del is_entering[temp[i]]

    time.sleep(15)

import ccxt
import time
import datetime
import pandas as pd


def get_decimal(ticker):
    Group_14 = [
        "XRP/USDT",
        "LEND/USDT",
        "SXP/USDT",
        "ZRX/USDT",
        "KAVA/USDT",
        "BAND/USDT",
    ]
    Group_13 = ["AAVE/USDT", "TRB/USDT", "CRV/USDT", "SNX/USDT", "BAL/USDT"]
    Group_05 = ["KNC/USDT"]
    Group_06 = ["DOGE/USDT"]
    Group_04 = [
        "UNI/USDT",
        "BZRX/USDT",
        "FLM/USDT",
        "SRM/USDT",
        "RUNE/USDT",
        "SUSHI/USDT",
    ]
    Group_23 = ["COMP/USDT", "LINK/USDT", "BNB/USDT"]
    Group_31 = ["YFI/USDT", "YFII/USDT", "DEFI/USDT"]
    Group_05 = ["LRC/USDT", "REN/USDT", "KNC/USDT", "TRX/USDT"]

    if any(ticker in i for i in Group_14):
        return 1, 4
    elif any(ticker in i for i in Group_13):
        return 1, 3
    elif any(ticker in i for i in Group_05):
        return 0, 5
    elif any(ticker in i for i in Group_06):
        return 0, 6
    elif any(ticker in i for i in Group_04):
        return 0, 4
    elif any(ticker in i for i in Group_23):
        return 2, 3
    elif any(ticker in i for i in Group_31):
        return 3, 1
    elif any(ticker in i for i in Group_05):
        return 0, 5
    else:
        return 3, 2


def bb(x, w=20, k=2):  # 볼린저 밴드
    data = []
    for i in range(len(x)):
        data.append(x[i][4])
    data = pd.Series(data)
    mbb = data.rolling(w).mean()
    lbb = mbb - k * data.rolling(w).std()
    ubb = mbb + k * data.rolling(w).std()
    return [lbb.tolist()[-2], mbb.tolist()[-2], ubb.tolist()[-2]]


def get_amount(ticker):
    price = binance.fetch_ohlcv(ticker)[-1][4]
    # today_money_USDT = float(binance.fetch_balance()['info']['assets'][0]['walletBalance'])
    today_money_USDT = 50
    decimal_amount = get_decimal(ticker)[0]
    result = round(today_money_USDT / price, decimal_amount)
    return result


def long_entry(ticker, exit_price):
    buy_amount = get_amount(ticker)
    order = binance.create_order(ticker, "market", "buy", buy_amount)
    binance.create_order(ticker, "limit", "sell", float(order["amount"]), exit_price)


def short_entry(ticker, exit_price):
    buy_amount = get_amount(ticker)
    order = binance.create_order(ticker, "market", "sell", buy_amount)
    binance.create_order(ticker, "limit", "buy", float(order["amount"]), exit_price)


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


long_ticker_list = [
    "BTC/USDT",
    "ETH/USDT",
    "XRP/USDT",
    "LTC/USDT",
    "BNB/USDT",
    "TRX/USDT",
]

short_ticker_list = [
    "DEFI/USDT",
    "DOGE/USDT",
    "LINK/USDT",
    "UNI/USDT",
    "AAVE/USDT",
    "MKR/USDT",
    "YFI/USDT",
    "COMP/USDT",
    "SNX/USDT",
    "ZRX/USDT",
    "REN/USDT",
    "LRC/USDT",
    "KNC/USDT",
    "SUSHI/USDT",
    "BAND/USDT",
    "RUNE/USDT",
    "BAL/USDT",
    "CRV/USDT",
    "KAVA/USDT",
    "YFII/USDT",
    "SRM/USDT",
    "TRB/USDT",
    "FLM/USDT",
    "BZRX/USDT",
]


while True:
    time.sleep(13)
    time_ = get_time()[1][2:]
    if time_ == "00":
        time.sleep(10)
        for i, item in enumerate(long_ticker_list):
            try:
                ohlcv = binance.fetch_ohlcv(item, "1h")
                bb_ = bb(ohlcv)
                open_ = ohlcv[-2][1]
                high_ = ohlcv[-2][2]
                low_ = ohlcv[-2][3]
                close_ = ohlcv[-2][4]
                if high_ - low_ == 0:
                    continue
                IBS = (close_ - low_) / (high_ - low_)
                if IBS < 0.1 and close_ < bb_[0]:
                    long_entry(item, high_)
            except Exception as ex:
                time.sleep(2)
                continue
        for i, item in enumerate(short_ticker_list):
            try:
                ohlcv = binance.fetch_ohlcv(item, "1h")
                bb_ = bb(ohlcv)
                open_ = ohlcv[-2][1]
                high_ = ohlcv[-2][2]
                low_ = ohlcv[-2][3]
                close_ = ohlcv[-2][4]
                if high_ - low_ == 0:
                    continue
                IBS = (close_ - low_) / (high_ - low_)
                if IBS > 0.9 and close_ > bb_[-1]:
                    short_entry(item, low_)
            except Exception as ex:
                time.sleep(2)
                continue
        time.sleep(59)

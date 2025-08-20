# -*- coding: utf-8 -*-
import ccxt
import time
import datetime
import urllib.request
import json
import pandas as pd
import numpy as np

# from pandas.core.indexing import convert_missing_indexer
import pandas_ta
import parmap


# ccxt ex.fetch_ohlcv() 보다 훨씬 빠르게 ohlcv 얻기
def get_ohlcv(ticker="BTC/USDT", interval="1m", limit=200):
    try:
        temp = ticker.split("/")
        ticker = f"{temp[0]}{temp[1]}"
        url = f"https://fapi.binance.com/fapi/v1/klines?symbol={ticker}&interval={interval}&limit={str(limit)}"  # monitoring
        text_data = urllib.request.urlopen(url).read().decode("utf-8")
        output = json.loads(text_data)
    except Exception as e:
        # print(e, '\n', 'ccxt.base.errors.BadSymbol: binance does not have market symbol {0}'.format(ticker))
        return None
    output = [list(map(float, output[i])) for i in range(len(output))]
    return output


def get_amount(ticker):
    price = binance.fetch_ohlcv(ticker)[-1][4]
    today_money_USDT = (
        float(binance.fetch_balance()["info"]["totalWalletBalance"]) * 0.03
    )
    result = today_money_USDT / price
    return binance.amount_to_precision(ticker, amount=result)


def order(ticker):
    sell_price = get_ohlcv(ticker, "1h", 3)[-2][2]
    buy_amount = get_amount(ticker)
    binance.create_order(ticker, "market", "buy", buy_amount)
    binance.create_order(ticker, "limit", "sell", buy_amount, sell_price)


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


binance = ccxt.binance(
    {
        "options": {"defaultType": "future"},
        "timeout": 30000,
        "apiKey": "yLIufQoCaLdawSTcjQJSuL967AQmKEmItAKR4QtPmksRPrmbnQBNulG6jCh4WYYA",
        "secret": "PHt9lC11jkvDWaMSuMKf1d2Xcz8vAWa7jTlW6rNop0yR4uNZiLVvUA3m8HWui32q",
        "enableRateLimit": False,
    }
)
binance.load_markets()


def get_tickers():
    result = []
    base_ticker = list(binance.fetch_tickers().keys())
    base_ticker = [
        base_ticker[i] for i in range(len(base_ticker)) if "/USDT" in base_ticker[i]
    ]
    base_ticker.remove("BTCDOM/USDT")
    for item in base_ticker:
        time.sleep(0.3)
        try:
            ohlcvs = get_ohlcv(item, "1d", 4)
            if ohlcvs[-2][1] > ohlcvs[-2][4]:
                result.append(item)
        except:
            continue
    return result


# 매수 종목 선정하기
def get_target(item):
    try:
        ohlcv = get_ohlcv(item, "1h", 400)
        df = pd.DataFrame(
            data=np.array(ohlcv),
            columns=["T", "O", "H", "L", "close", "V", "0", "0", "0", "0", "0", "0"],
        )
        EMA_7 = df.ta.ema(length=7).tolist()[-2]
        EMA_25 = df.ta.ema(length=25).tolist()[-2]
        EMA_99 = df.ta.ema(length=99).tolist()[-2]
        if EMA_7 < EMA_25 and EMA_7 < EMA_99 and EMA_25 < EMA_99:
            ohlcv = ohlcv[-2]
            high_ = ohlcv[2]
            low_ = ohlcv[3]
            if high_ - low_ == 0:
                return None
            close_ = ohlcv[4]
            IBS = (close_ - low_) / (high_ - low_)
            if IBS < 0.08:
                return item
    except Exception as e:
        print(item)
        print(e)
        time.sleep(0.1)
        return None
    return None


# ticker_list = get_tickers()
# print(ticker_list)


# today_money_USDT = float(binance.fetch_balance()['info']['availableBalance'])


# Main
if __name__ == "__main__":
    while True:
        time.sleep(2)
        time_ = get_time()[1]
        if time_ == "0903":
            ticker_list = get_tickers()
        if time_[2:] == "00":
            target_list = parmap.map(
                get_target, ticker_list, pm_pbar=False, pm_processes=4
            )
            target_list = list(set(target_list) - set([None]))
            print(target_list)

            money_data = binance.fetch_balance()
            if (
                float(money_data["info"]["availableBalance"])
                < float(money_data["info"]["totalWalletBalance"]) * 0.5
            ):

                for target in target_list:
                    try:
                        order(target)
                    except:
                        print(f"fail buy {target}")
                        time.sleep(0.5)
                        continue
            time.sleep(59)

# -*- coding: utf-8 -*-

import ccxt
import time
import datetime
import urllib.request
import json
import pandas as pd
import numpy as np
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
        time.sleep(0.1)
        return None
    output = [list(map(float, output[i])) for i in range(len(output))]
    return output


def get_amount(ticker):
    price = binance.fetch_ohlcv(ticker)[-1][4]
    today_money_USDT = float(binance.fetch_balance()["info"]["availableBalance"]) * 0.03
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
        "apiKey": "f6LEy0POPdaukqwlrnC4KvJbGWkcXRfVmKbsPmFAaPlyL2Rytswf7ilTa3kAjnQh",
        "secret": "sLvrd7ZT6c49yZVlnFRhPvJcIg8z39S6dVwZcIfPhFueA5BAy5UpTT3ZbVZg9zA2",
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
        time.sleep(0.4)
        try:
            ohlcvs = get_ohlcv(item, "1d", 4)
            if ohlcvs[-2][1] > ohlcvs[-2][4]:
                result.append(item)
        except:
            time.sleep(0.1)
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
        time.sleep(0.1)
        return None
    return None


ticker_list = get_tickers()

if __name__ == "__main__":
    while True:
        time.sleep(2)
        time_ = get_time()[1]
        if time_ == "0915":
            ticker_list = get_tickers()
        if time_[2:] == "00":
            target_list = parmap.map(
                get_target, ticker_list, pm_pbar=False, pm_processes=4
            )
            target_list = list(set(target_list) - set([None]))
            for target in target_list:
                try:
                    order(target)
                except:
                    time.sleep(0.1)
                    continue
            time.sleep(58)

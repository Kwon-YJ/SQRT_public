import ccxt
import time
import numpy as np
import pandas as pd
import datetime
import pandas_ta as ta
import json
import parmap
import urllib
import multiprocessing


# ccxt ex.fetch_ohlcv() 보다 훨씬 빠르게 ohlcv 얻기
def get_ohlcv(ticker="BTC/USDT", interval="1m", limit=200):
    try:
        temp = ticker.split("/")
        ticker = f"{temp[0]}{temp[1]}"
        url = f"https://fapi.binance.com/fapi/v1/klines?symbol={ticker}&interval={interval}&limit={str(limit)}"  # monitoring
        text_data = urllib.request.urlopen(url).read().decode("utf-8")
        output = json.loads(text_data)
    except Exception as e:
        print(
            e,
            "\n",
            "ccxt.base.errors.BadSymbol: binance does not have market symbol {0}".format(
                ticker
            ),
        )
        return None
    output = [list(map(float, output[i])) for i in range(len(output))]
    return output


# get_time()[0] = 오늘 날짜 str
# get_time()[1] = 현재 시각 str
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


# 매수 수량 얻기
def get_amount(ticker):
    price = binance.fetch_ohlcv(ticker)[-1][4]
    result = 69 / price
    return binance.amount_to_precision(ticker, amount=result)


# 매수 주문 실행
def buy_order(ticker):
    try:
        buy_amount = get_amount(ticker)
        order = binance.create_order(ticker, "market", "buy", buy_amount)
        is_entering[ticker] = float(order["amount"])
    except:
        return None


# 매수 종목 선정하기
def get_target(item):
    try:
        ohlcv_temp = get_ohlcv(item, "15m", 800)
        df = pd.DataFrame(
            data=np.array(ohlcv_temp),
            columns=["0", "0", "close", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
        )  ## rsi(15, high)
        rsi_entry = df.ta.rsi(length=15).tolist()
        # if rsi_entry[-2] < 23 and ohlcv_temp[-1][1] > ohlcv_temp[-1][4] and ohlcv_temp[-1][5] > ohlcv_temp[-2][5] and ohlcv_temp[-1][5] > ohlcv_temp[-3][5]:
        if (
            rsi_entry[-3] < 22
            and ohlcv_temp[-2][1] > ohlcv_temp[-2][4]
            and ohlcv_temp[-2][5] > ohlcv_temp[-3][5]
            and ohlcv_temp[-2][5] > ohlcv_temp[-4][5]
        ):
            return item
    except Exception as e:
        print(e)
        time.sleep(0.1)
    return None


def get_tickers():
    base_ticker = list(binance.fetch_tickers().keys())
    base_ticker = [
        base_ticker[i] for i in range(len(base_ticker)) if "/USDT" in base_ticker[i]
    ]
    base_ticker.remove("BTCDOM/USDT")
    return base_ticker


binance = ccxt.binance(
    {
        "options": {"defaultType": "future"},
        "timeout": 30000,
        "apiKey": "bOHcvOmxqFVGN6FPsJwcnh4QOxw0D6oaFGHjEhpU2pby1bt7EJDb6t9TExauOccU",
        "secret": "Yece0g5APcAZR4sXJl1M007tLL9w9bB7Qp2o3fGFYJjN3f6tfx6lOCq1LdmRk4Ob",
        "enableRateLimit": False,
    }
)
binance.load_markets()

is_entering = {}

ticker_list = get_tickers()
print(ticker_list)

if __name__ == "__main__":
    while True:
        time.sleep(2)
        now = int(get_time()[1][-2:])
        if now % 15 == 0:
            break

    while 1:
        temp = []

        target_list = parmap.map(get_target, ticker_list, pm_pbar=False, pm_processes=4)
        target_list = list(set(target_list) - set([None]))
        print(target_list)

        for target in target_list:
            try:
                buy_order(target)
            except:
                time.sleep(2)
                continue

        time.sleep(59.5)

        while True:
            time.sleep(1)
            now = int(get_time()[1][-2:])
            if now % 15 == 0:
                break

        for i in range(len(is_entering)):
            try:
                ticker = list(is_entering.keys())[i]
                ohlcv_temp = get_ohlcv(ticker, "15m", 800)
                df = pd.DataFrame(
                    data=np.array(ohlcv_temp),
                    columns=[
                        "0",
                        "0",
                        "0",
                        "close",
                        "0",
                        "0",
                        "0",
                        "0",
                        "0",
                        "0",
                        "0",
                        "0",
                    ],
                )  ## rsi(8, low)
                rsi_exit = df.ta.rsi(length=8).tolist()
                if rsi_exit[-2] > 38:
                    sell_amount = is_entering[ticker]
                    binance.create_order(
                        ticker,
                        "limit",
                        "sell",
                        sell_amount,
                        binance.fetch_order_book(ticker)["bids"][0][0],
                    )
                    temp.append(ticker)
            except:
                time.sleep(5)
                continue

        for i in range(len(temp)):
            del is_entering[temp[i]]

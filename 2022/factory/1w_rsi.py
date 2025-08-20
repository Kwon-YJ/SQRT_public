import Utils
import pandas as pd
import pandas_ta as ta
import time
import numpy as np

import urllib
import json

import ccxt


def get_cap_rank(ticker):
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"
    text_data = urllib.request.urlopen(url).read().decode("utf-8")
    output = json.loads(text_data)
    for data in output:
        if data["symbol"] == ticker.split("/")[0].lower():
            # print(data["market_cap_rank"])
            return data["market_cap_rank"]
    return None


def symbol_2_id(ticker):
    result = []

    url = "https://api.coingecko.com/api/v3/coins/list"
    text_data = urllib.request.urlopen(url).read().decode("utf-8")
    output = json.loads(text_data)

    for data in output:
        if data["symbol"] == ticker.split("/")[0].lower():
            # id = data["id"]
            result.append(data["id"])

    result = [ticker for ticker in result if "-" not in ticker]

    return result[-1]


"""
ticker = "ETH/USDT"

url = f"https://api.coingecko.com/api/v3/coins/{symbol_2_id(ticker)}/market_chart?vs_currency=usd&days=1"

text_data = urllib.request.urlopen(url).read().decode('utf-8')
output = json.loads(text_data)


print(output["market_caps"][-1][-1])

exit()"""


def remove_None(data):
    return [idx for idx in data if idx != None]


def get_tickers():
    all_ticker_list = list(binance.fetch_tickers().keys())
    std_time_data = Utils.get_ohlcv("BTC/USDT", "1h", 2)[-1][0]
    dropout_delisting = []
    for ticker in all_ticker_list:
        ticker_ohlcv = Utils.get_ohlcv(ticker, "1h", 2)
        if ticker_ohlcv != None and ticker_ohlcv[-1][0] == std_time_data:
            dropout_delisting.append(ticker)
    base_ticker = remove_None(dropout_delisting)

    # busd = [base_ticker[i] for i in range(len(base_ticker)) if '/BUSD' in base_ticker[i]]
    btc = [base_ticker[i] for i in range(len(base_ticker)) if "/BTC" in base_ticker[i]]
    # usdt = [base_ticker[i] for i in range(len(base_ticker)) if '/USDT' in base_ticker[i]]
    # usdt = [usdt[i] for i in range(len(usdt)) if 'DOWN/' not in usdt[i] and 'UP/' not in usdt[i]]
    # eth = [base_ticker[i] for i in range(len(base_ticker)) if '/ETH' in base_ticker[i]]
    # bnb = [base_ticker[i] for i in range(len(base_ticker)) if '/BNB' in base_ticker[i]]
    # return usdt+btc+eth+bnb

    return btc


binance = Utils.use_binance()

ticker_list = get_tickers()

time.sleep(60)

result = []

for i, ticker in enumerate(ticker_list):
    try:
        temp_ohlcv = Utils.get_ohlcv(ticker, "1w", 39)
        if len(temp_ohlcv) != 39:
            print(ticker, len(temp_ohlcv))
            continue
        df = pd.DataFrame(
            data=np.array(temp_ohlcv),
            columns=["0", "0", "0", "0", "close", "0", "0", "0", "0", "0", "0", "0"],
        )  ## rsi(8, low)
        rsi = df.ta.rsi(length=14).tolist()[-1]
        if rsi < 33:
            # print(f"rsi of {ticker} is {rsi}")
            result.append((ticker, rsi, get_cap_rank(ticker)))
    except:
        time.sleep(0.5)
        continue

from pprint import pprint

pprint(result)

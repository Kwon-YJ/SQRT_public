import multiprocessing
import urllib.request
import pandas as pd
import datetime
import operator
import parmap
import ccxt
import time
import json

a = datetime.datetime.now()


def get_ohlcv(ticker="BTC/USDT", interval="1m", limit=200):
    try:
        ticker = ticker[:-5] + "USDT"
        url = "https://fapi.binance.com/fapi/v1/klines?symbol={0}&interval={1}&limit={2}".format(
            ticker, interval, str(limit)
        )
        text_data = urllib.request.urlopen(url).read().decode("utf-8")
        result = json.loads(text_data)
    except:
        time.sleep(0.2)
        print(ticker)
        return None
    return result


def get_data(all_ticker, ticker_list):
    list_ = []

    all_diff = {}
    for i in range(len(all_ticker)):
        ohlcv_ = all_ticker[i]
        price_diff = float(ohlcv_[-2][4]) / float(ohlcv_[-2][1])
        all_diff[ticker_list[i]] = price_diff
        list_.append([ohlcv_[s][4] for s in range(len(ohlcv_))])

    df = pd.DataFrame(list_).T
    corr = df.corr(method="pearson")
    corr.index = ticker_list
    corr.columns = ticker_list

    MDD_ticker = min(all_diff.items(), key=operator.itemgetter(1))[0]
    Decouple_ticker = corr[MDD_ticker].idxmin(axis=0, skipna=True)

    return MDD_ticker, all_diff, Decouple_ticker


# row 생략 없이 출력
pd.set_option("display.max_rows", None)
# col 생략 없이 출력
pd.set_option("display.max_columns", None)

binance = ccxt.binance(
    {
        "options": {"defaultType": "future"},
        "timeout": 30000,
        "apiKey": "FRbVseExyAWjQUtYFnS4memLnPCcgNAeRW7HEBrrw9qyIyPUMCTzUKxZKOJIHcfV",
        "secret": "CbDX3DE5r9ErdLBOphDB4rjCaAaKbUqITbNK05YIitktZ24VfcNrvVRbIgfK6L87",
        "enableRateLimit": True,
    }
)


def get_tickerlist():
    url = "https://fapi.binance.com/fapi/v1/premiumIndex"
    text_data = urllib.request.urlopen(url).read().decode("utf-8")
    result = json.loads(text_data)
    result = [result[s]["symbol"][:-4] + "/USDT" for s in range(len(result))]
    return result


ticker_list = list(binance.fetch_tickers().keys())

# ticker_list = get_tickerlist()


All_ohlcv = {}
for i in range(len(ticker_list)):
    temp = binance.fetch_ohlcv(ticker_list[i], "1h")
    # temp = get_ohlcv(ticker_list[i], '1h')
    if temp != None:
        All_ohlcv[ticker_list[i]] = temp
min_, all_diff, decouple_ticker = get_data(
    list(All_ohlcv.values()), list(All_ohlcv.keys())
)
print(min_, all_diff[min_])  # 최대 하락종목, 하락 폭
print(decouple_ticker)  # 최대 하락 종목과 디커플인 항목


print(datetime.datetime.now() - a)

"""

def add_ohlcv(ticker):
    temp = binance.fetch_ohlcv(ticker, '1h')
    All_ohlcv[ticker_list[i]] = temp


if __name__ == '__main__':
    num_cores = multiprocessing.cpu_count()


    ticker_list = list(binance.fetch_tickers().keys())

    All_ohlcv = {}

    # result_ =sum( parmap.map(log_maker, All_tickers, pm_pbar=True, pm_processes=num_cores), [])
    result_ = parmap.map(add_ohlcv, ticker_list, pm_pbar=True, pm_processes=num_cores)


# https://fapi.binance.com/fapi/v1/klines?symbol=BNBUSDT&interval=1m&limit=1
"""

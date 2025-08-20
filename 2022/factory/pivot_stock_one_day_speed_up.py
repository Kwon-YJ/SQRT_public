import datetime
import pickle
import Utils
import parmap
import time
from pykrx import stock

import urllib
import json


def remove_None(data):
    return [idx for idx in data if idx != None]


def get_result(ticker):
    try:
        name = stock.get_market_ticker_name(ticker)
        if "스팩" in name:
            return None
        df = stock.get_market_ohlcv_by_date("20210401", Today, ticker)
        open = df["시가"].tolist()
        high = df["고가"].tolist()
        low = df["저가"].tolist()
        close = df["종가"].tolist()
        PP = (high[-2] + low[-2] + close[-2]) / 3
        if open[-1] < 1.99 * PP - high[-2] and open[-1] > 1.92 * PP - high[-2]:
            earning = (close[-1] / open[-1] - 1) * 100
            # return [name, open[-1], close[-1], earning]
            return [name, earning]
    except:
        print("", end="")
    return None


def get_all_open_price(url):
    result = {}
    text_data = urllib.request.urlopen(url).read().decode("euc-kr")
    split_newline_data = text_data.split("\n")
    for idx, line in enumerate(split_newline_data):
        if "▼" in line or "▲" in line:
            ticker_line = split_newline_data[idx - 2]
            price_line = split_newline_data[idx - 1]
            ticker = ticker_line.split("title='")[-1].split("'")[0]
            price_with_comma = price_line.split("align='right'>")[-1].split("</td>")[0]
            price = price_with_comma.replace(",", "")
            if (len(ticker) + len(price)) < 21:
                result[ticker] = float(price)
    return result


if __name__ == "__main__":

    while 1:
        print(datetime.datetime.now())

        KOSPI_url = "https://vip.mk.co.kr/newSt/rate/item_all.php"
        KOSDAQ_url = (
            "https://vip.mk.co.kr/newSt/rate/item_all.php?koskok=KOSDAQ&orderBy=upjong"
        )

        KOSPI = get_all_open_price(KOSPI_url)
        KOSDAQ = get_all_open_price(KOSDAQ_url)

        KRX = dict(KOSPI, **KOSDAQ)

        ticker = "102280"  # 쌍방울

        print(KRX[ticker])

        time.sleep(5)

    exit()

    a = datetime.datetime.now()

    Today = Utils.get_time()[0]

    # name = stock.get_market_ticker_name(ticker)

    konex = stock.get_market_ticker_list(market="KONEX")
    ticker_list = list(set(stock.get_market_ticker_list(market="ALL")) - set(konex))
    print(len(ticker_list))

    exit()

    trade_log = parmap.map(get_result, ticker_list, pm_pbar=True, pm_processes=2)

    print(remove_None(trade_log))

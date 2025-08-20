# -*- coding: utf-8 -*-
from pykrx import stock
import time
from datetime import datetime
import multiprocessing
import numpy as np
import parmap
import pandas_ta as ta
from scipy.signal import argrelextrema
import Utils


def get_time(temp):
    now = temp
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


""" 레거시
def get_target_old(ticker_name): 
    try:

        if '스팩' in stock.get_market_ticker_name(ticker_name):
            return None

        Ohlcv = stock.get_market_ohlcv_by_date("20210701", Today, ticker_name)
        Ohlcv.columns = ['Open', 'High', 'Low', 'Close', 'V']
        rsi = Ohlcv.ta.rsi(length=14)
        Ohlcv.insert(5, 'rsi', rsi, True)
        data = Ohlcv.fillna(0)
        
        max_price = argrelextrema(data['Close'].values, np.greater, order=5)[0][-2:]
        min_price = argrelextrema(data['Close'].values, np.less, order=5)[0][-2:]
        max_rsi = argrelextrema(data['rsi'].values, np.greater, order=5)[0][-2:]
        min_rsi = argrelextrema(data['rsi'].values, np.less, order=5)[0][-2:]
        
        if len(max_price) > 1:
            max_before = data.iloc[max_price[0]]
            max_after = data.iloc[max_price[1]]
            if np.array_equal(max_price,max_rsi) and max_price[1] > len(Ohlcv) - 3 and data['rsi'][max_rsi[0]] > 80 and data['rsi'][max_rsi[1]] > 70:
                if max_before['rsi'] > max_after['rsi'] and max_before['Close'] < max_after['Close']:
                    print('overbuy',stock.get_market_ticker_name(ticker_name))


        if len(min_price) > 1:
            min_before = data.iloc[min_price[0]]
            min_after = data.iloc[min_price[1]]
            if np.array_equal(min_price,min_rsi) and min_price[1] > len(Ohlcv) - 3 and data['rsi'][min_rsi[0]] < 20 and data['rsi'][min_rsi[1]] < 30:
                if min_before['rsi'] < min_after['rsi'] and min_before['Close'] > min_after['Close']:
                    print('oversell',stock.get_market_ticker_name(ticker_name))

    except:
        # print(stock.get_market_ticker_name(ticker_name))
        return None
"""


def get_target(ticker_name):
    try:
        if "스팩" in stock.get_market_ticker_name(ticker_name):
            return None
        Ohlcv = stock.get_market_ohlcv_by_date("20210701", Today, ticker_name)
        Ohlcv.columns = ["Open", "High", "Low", "Close", "V"]
        rsi = Ohlcv.ta.rsi(length=14)
        Ohlcv.insert(5, "rsi", rsi, True)
        data = Ohlcv.fillna(0)
        min_price = argrelextrema(data["Close"].values, np.less, order=5)[0][-2:]
        min_rsi = argrelextrema(data["rsi"].values, np.less, order=5)[0][-2:]
        if len(min_price) > 1:
            min_before = data.iloc[min_price[0]]
            min_after = data.iloc[min_price[1]]
            if (
                np.array_equal(min_price, min_rsi)
                and min_price[-1] > len(Ohlcv) - 3
                and data["rsi"][min_rsi[0]] < 20
                and data["rsi"][min_rsi[1]] < 30
            ):
                if (
                    min_before["rsi"] < min_after["rsi"]
                    and min_before["Close"] > min_after["Close"]
                ):
                    print("과매도", stock.get_market_ticker_name(ticker_name))
    except:
        return None


if __name__ == "__main__":
    num_cores = multiprocessing.cpu_count()
    Today = get_time(datetime.now())[0]
    konex = [
        "341310",
        "179530",
        "336040",
        "331660",
        "337840",
        "093510",
        "327970",
        "329050",
        "309900",
        "317860",
        "323350",
        "311840",
        "314130",
        "308700",
        "311060",
        "303360",
        "271780",
        "279060",
        "302920",
        "276240",
        "299480",
        "299670",
        "163430",
        "288490",
        "285770",
        "281310",
        "236030",
        "284420",
        "277880",
        "278990",
        "270020",
        "267060",
        "270660",
        "270210",
        "271850",
        "224880",
        "266170",
        "267810",
        "266870",
        "225860",
        "284610",
        "278380",
        "242350",
        "258250",
        "258540",
        "232830",
        "243870",
        "251280",
        "251960",
        "239890",
        "191600",
        "246250",
        "245450",
        "208850",
        "224020",
        "244880",
        "112190",
        "241510",
        "238500",
        "217910",
        "212310",
        "222160",
        "250030",
        "240340",
        "327610",
        "236340",
        "232530",
        "215570",
        "233990",
        "232680",
        "211050",
        "227420",
        "229500",
        "228180",
        "229000",
        "224760",
        "223220",
        "233250",
        "238170",
        "252370",
        "149300",
        "221800",
        "217880",
        "258050",
        "222670",
        "220110",
        "225220",
        "215050",
        "217950",
        "205290",
        "208890",
        "214610",
        "140610",
        "200580",
        "203400",
        "206950",
        "200350",
        "217320",
        "178600",
        "189330",
        "189540",
        "189350",
        "183350",
        "150440",
        "179720",
        "086080",
        "260870",
        "158300",
        "180060",
        "140290",
        "120780",
        "210120",
        "084440",
        "121060",
        "140660",
        "216280",
        "058970",
        "207490",
        "234070",
        "260970",
        "224810",
        "149010",
        "185190",
        "126340",
        "199290",
        "225850",
        "162120",
        "176750",
        "183410",
        "199150",
        "135160",
        "076340",
        "107640",
        "136660",
        "220250",
        "103660",
        "114920",
        "216400",
        "116100",
        "101360",
        "202960",
        "199800",
        "066830",
        "148780",
        "092590",
        "064850",
        "044990",
        "086460",
        "067370",
        "086220",
    ]
    All_tickers = list(set(stock.get_market_ticker_list()) - set(konex))
    # All_tickers = ['005930']

    # parmap.map(get_target, All_tickers, pm_pbar=False, pm_processes=8)

    for ticker in All_tickers:
        get_target(ticker)

# -*- coding: utf-8 -*-
from pykrx import stock
import time
from datetime import datetime
import numpy


def get_perfomance(trade_log):
    win = []
    lose = []
    risk_free = 0.038 / 365
    avg = numpy.mean(trade_log)
    std = numpy.std(trade_log)
    size = (avg - risk_free) / (std * std)

    for i in range(len(trade_log)):
        if trade_log[i] > 0:
            win.append(trade_log[i])
        elif trade_log[i] < 0:
            lose.append(trade_log[i])

    print("총거래 : ", len(trade_log))
    print("수익거래수 :", len(win))
    print("손실거래수 :", len(lose))
    print("평균거래 :", avg)
    print("평균수익거래 :", numpy.mean(win))
    print("평균손실거래 :", numpy.mean(lose))
    print("평균손익비 :", -1 * numpy.mean(win) / numpy.mean(lose))
    print("승률 :", int(round(len(win) / len(trade_log), 2) * 100), "%")
    print("포지션 사이징 :", size)
    print("")


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


def day_ago(day, ohlcv, ticker):
    a = ticker.tail(day)
    b = a[ohlcv]
    c = b.head(1)
    return c


def get_TR(date, ticker):
    a = day_ago(date, "고가", ticker)
    b = day_ago(date, "저가", ticker)
    c = a.values - b.values

    aa = day_ago(date, "고가", ticker)
    bb = day_ago(date + 1, "종가", ticker)
    cc = abs(aa.values - bb.values)

    aaa = day_ago(date, "저가", ticker)
    bbb = day_ago(date + 1, "종가", ticker)
    ccc = abs(aaa.values - bbb.values)

    return max(c, cc, ccc)


def get_ATR(ticker):
    value = 0
    for i in range(15):
        TR = get_TR(i + 2, ticker)
        value = value + TR
    return value / 15


def log_maker_1():
    print("총", len(All_tickers), "개의 항목")
    for j in range(len(All_tickers)):
        print("현재", j, "번째 항목을 계산하고 있습니다. ")

        ticker = All_tickers[j]

        if stock.get_market_ticker_name(ticker) in "스팩":
            continue

        df = stock.get_market_ohlcv_by_date("20000101", Today, ticker)
        HH_price = 0

        for i in range(15, len(df) - 1):
            now_ohlcv = df.head(i)
            now_close = now_ohlcv.iloc[i - 1]["종가"]

            if HH_price < now_close:
                HH_price = now_close

            if len(price) != 0:
                temp = get_ATR(now_ohlcv)

                if now_close < HH_price - (3 * temp):
                    sell_price = df.head(i + 1).iloc[i - 1]["시가"]
                    earning = 100 * ((sell_price / price[0]) * 0.99925 * 0.99925 - 1)
                    buy_sell_log.append(earning)
                    price.clear()
                continue

            if float(now_close) == 0:
                continue

            if float(max(now_ohlcv["종가"])) == float(now_close):
                buy_price = df.head(i + 1).iloc[i - 1]["시가"]
                price.append(buy_price)


price = []
buy_sell_log = []
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


"""
temp_ticekrs = []
for i in range(len(All_tickers)):
    if i % 31 == 0:
        temp_ticekrs.append(All_tickers[i])
"""

now = datetime.now()
Today = get_time(now)[0]

log_maker_1()
get_perfomance(buy_sell_log)

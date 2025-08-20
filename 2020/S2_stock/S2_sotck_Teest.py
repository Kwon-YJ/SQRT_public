# -*- coding: utf-8 -*-
from pykrx import stock
import time
from datetime import datetime
import multiprocessing
import numpy as np
import parmap
import telegram

"""
def get_perfomance(trade_log):
    win = []
    lose = []
    risk_free = 0.038 / 365
    avg = np.mean(trade_log)
    std = np.std(trade_log)
    size = (avg - risk_free) / (std * std)
    
    for i in range(len(trade_log)):
        if trade_log[i] > 0:
            win.append(trade_log[i])
        elif trade_log[i] < 0:
            lose.append(trade_log[i])
    print('총거래 : ', len(trade_log))
    print('수익거래수 :', len(win))
    print('손실거래수 :', len(lose))
    print('평균거래 :',avg)
    print('평균수익거래 :', np.mean(win))
    print('평균손실거래 :', np.mean(lose))
    print('평균손익비 :', -1 * np.mean(win) / np.mean(lose))
    print('승률 :', int(round(len(win) / len(trade_log),2) * 100), '%')
    print('포지션 사이징 :', size)
    print('')
    result = []
    result.append(['총거래 : ', len(trade_log)])
    result.append(['수익거래수 :', len(win)])
    result.append(['손실거래수 :', len(lose)])
    result.append(['평균거래 :',avg])
    result.append(['평균수익거래 :', np.mean(win)])
    result.append(['평균손실거래 :', np.mean(lose)])
    result.append(['평균손익비 :', -1 * np.mean(win) / np.mean(lose)])
    result.append(['승률 :', int(round(len(win) / len(trade_log),2) * 100), '%'])
    result.append(['포지션 사이징 :', size])
    telegram_send(result)
    print(result)
"""


def get_perfomance(trade_log):
    if len(trade_log) == 0:
        return None
    win = []
    lose = []
    risk_free = 0.038 / 365
    avg = np.mean(trade_log)
    std = np.std(trade_log)
    size = (avg - risk_free) / (std * std)

    for i in range(len(trade_log)):
        if trade_log[i] > 0:
            win.append(trade_log[i])
        elif trade_log[i] < 0:
            lose.append(trade_log[i])

    print("총거래 : ", len(trade_log))
    print("수익거래수 :", len(win))
    print("손실거래수 :", len(lose))
    print("평균손익 :", avg)
    print("평균수익거래 :", np.mean(win))
    print("평균손실거래 :", np.mean(lose))
    avg_W_L_ratio = -1 * np.mean(win) / np.mean(lose)
    print("평균손익비 :", avg_W_L_ratio)
    win_rate = int(round(len(win) / len(trade_log), 2) * 100)
    print("승률 :", win_rate, "%")
    if len(lose) > 0:
        # print(lose)
        print("MDD :", min(lose))
    print("시그마 포지션 사이징 :", size)
    win_rate = win_rate * 0.01
    temp = (1 - win_rate) / avg_W_L_ratio
    kelly = win_rate - temp
    print("켈리 레이쇼 :", kelly)


def telegram_send(data):
    bot = telegram.Bot(token=my_token)
    if type(data) != "str":
        data = str(data)
    while 1:
        try:
            bot.send_message(chat_id=801167350, text=data)
            time.sleep(3)
            return None
        except:
            continue


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


def log_maker(ticker):
    pass



Today = get_time(datetime.now())[0]


if __name__ == "__main__":
    num_cores = multiprocessing.cpu_count()
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
    # All_tickers = All_tickers[:int(len(All_tickers))]
    # All_tickers = ['005930']
    a = time.time()
    result_ = sum(parmap.map(log_maker, All_tickers, pm_pbar=True, pm_processes=2), [])
    b = time.time()
    print(b - a)
    print(len(result_))
    get_perfomance(result_)

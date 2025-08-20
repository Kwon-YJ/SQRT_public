# -*- coding: utf-8 -*-

from pykrx import stock
import time
from datetime import datetime
import numpy as np
import parmap
import pandas as pd
from tabulate import tabulate
import telegram

# import multiprocessing


def get_time():
    now = datetime.now()
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


"""
def Result_output(ticker):
    df = stock.get_market_ohlcv_by_date("20000101", Today, ticker)
    try:
        if float(max(df['종가'])) == float(df['종가'].tail(1)):
            return (stock.get_market_ticker_name(ticker))
    except:
        print('', end='')
    return 'pass'
"""


def Result_output(ticker):
    try:
        name = stock.get_market_ticker_name(ticker)
        if "스팩" in name:
            return "pass"
        df = stock.get_market_ohlcv_by_date("20000101", Today, ticker)
        temp_list = df["종가"].tolist()
        if len(temp_list) < 270:
            return "pass"
        sorted_list = sorted(temp_list)
        if temp_list[-1] == sorted_list[-1] and temp_list[-2] != sorted_list[-2]:
            cap = stock.get_market_cap_by_ticker(Today).loc[ticker, "시가총액"]
            # return [name, max(temp_list)/min(temp_list), cap, df['종가'].tolist()[-1]]
            return [
                name,
                max(temp_list[-250:]) / min(temp_list[-250:]),
                cap,
                df["종가"].tolist()[-1],
            ]
    except:
        print("", end="")
    return "pass"


def print_result(input_list):
    temp_list = [[], [], [], []]

    for idx, item in enumerate(input_list):
        temp_list[0].append(item[0])
        temp_list[1].append(item[1])
        temp_list[2].append(item[2])
        temp_list[3].append(item[3])

    df = pd.DataFrame(
        {
            "name": temp_list[0],
            "high_low_gap": temp_list[1],
            "cap": temp_list[2],
            "price": temp_list[3],
        }
    )
    df["rank_gap"] = df["high_low_gap"].rank(method="min")
    df["rank_cap"] = df["cap"].rank(method="min", ascending=False)
    df["gap + cap"] = df["rank_gap"] + df["rank_cap"]

    return tabulate(df, headers="keys", tablefmt="psql")


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


if __name__ == "__main__":
    global Today
    Today = get_time()[0]
    # Today = '20210710'
    # num_cores = multiprocessing.cpu_count()
    # bot = telegram.Bot(token = my_token)

    konex = stock.get_market_ticker_list(market="KONEX")
    tickers = list(set(stock.get_market_ticker_list(market="ALL")) - set(konex))
    result_ = parmap.map(Result_output, tickers, pm_pbar=True, pm_processes=10)

    while 1:
        try:
            result_.remove("pass")
        except:
            break

    print(result_)

    print(print_result(result_))

    telegram_send(result_)

    telegram_send(print_result(result_))

    # bot.send_message(chat_id = 801167350, text = message)

# -*- coding: utf-8 -*-

from pykrx import stock
import parmap
import pandas as pd
from tabulate import tabulate
import Utils
import pandas_ta as ta


def get_position_size(dataframe):
    close = dataframe["종가"].tolist()[-1]
    dataframe.rename(
        columns={"종가": "close", "고가": "high", "저가": "low"}, inplace=True
    )
    atr = dataframe.ta.atr(length=14).tail(1).tolist()[0] * 2
    position_size = f"{round(0.02/(atr/close)*100,2)}%"
    return position_size


def get_result(ticker):
    try:
        name = stock.get_market_ticker_name(ticker)
        if "스팩" in name:
            return "pass"
        df = stock.get_market_ohlcv_by_date("20000101", Today, ticker)
        temp_list = df["종가"].tolist()
        if len(temp_list) < 270:
            return "pass"
        sorted_list = sorted(temp_list)
        if temp_list[-1] == sorted_list[-1] and sorted_list[-2] not in temp_list[-30:]:
            cap = int(
                stock.get_market_cap("20220101", Today, ticker)["시가총액"].tail(1)
            )
            cap = 0
            size = get_position_size(df)
            return [
                name,
                round(max(temp_list[-250:]) / min(temp_list[-250:]), 1),
                cap,
                size,
            ]
    except:
        print("err", end="")
    return "pass"


def print_result(input_list):
    temp_list = [[], [], [], [], []]

    for idx, item in enumerate(input_list):
        temp_list[0].append(item[0])
        temp_list[1].append(item[1])
        temp_list[2].append(item[2])
        temp_list[3].append(item[3])

    df = pd.DataFrame(
        {
            "name": temp_list[0],
            "max/min": temp_list[1],
            "cap": temp_list[2],
            "size": temp_list[3],
        }
    )
    df["R_gap"] = df["max/min"].rank(method="min")
    df["R_cap"] = df["cap"].rank(method="min", ascending=False)
    df["gap+cap"] = df["R_gap"] + df["R_cap"]

    return tabulate(df, headers="keys", tablefmt="psql")


def get_target_list_sub(ticker):
    try:
        name = stock.get_market_ticker_name(ticker)
        if "스팩" in name:
            return None
        df = stock.get_market_ohlcv_by_date("20000301", Today, ticker)
        temp_list = df["종가"].tolist()
        sorted_list = sorted(temp_list)
        if temp_list[-1] > temp_list[-2] and temp_list[-1] * 1.3 > sorted_list[-1]:
            return ticker
    except:
        return None


def get_target_list():
    konex = stock.get_market_ticker_list(market="KONEX")
    tickers = list(set(stock.get_market_ticker_list(market="ALL")) - set(konex))
    # result_ = parmap.map(get_result, tickers , pm_pbar=True, pm_processes=2)
    result_ = parmap.map(get_target_list_sub, tickers, pm_pbar=True, pm_processes=2)
    while 1:
        try:
            result_.remove(None)
        except:
            break
    return result_


if __name__ == "__main__":
    global Today
    Today = Utils.get_time()[0]
    # Today = '20210710'

    result_ = get_target_list()

    print(result_)
    print(len(result_))
    # print(print_result(result_))
    # Utils.telegram_send(result_)
    # Utils.telegram_send(print_result(result_))

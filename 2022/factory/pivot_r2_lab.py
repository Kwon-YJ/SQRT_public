# -*- coding:utf-8 -*-
import Utils
import time
import random


def log_maker(day):
    temp = []
    for i in range(len(All_ohlcv)):
        ohlcv = All_ohlcv[i]
        open, high, low, close = ohlcv[-(day + 1)][1:5]  # D-1 ohlc

        high = max((ohlcv[-(day + 2)][2], ohlcv[-(day + 1)][2]))
        low = min((ohlcv[-(day + 2)][3], ohlcv[-(day + 1)][3]))

        if open < close:  # 양봉
            value = 2.4
        else:
            value = 2.15

        PP = (high + low + (close * 4)) / 6
        R2 = value * PP - low
        if ohlcv[-day][2] > R2:
            entry_price = ohlcv[-day][4]
            exit_price = R2
            earning = (exit_price / entry_price * Slippage - 1) * 100
            trade_time = Utils.timestamp_to_datetime(ohlcv[-day][0])[1]
            print(
                f"{  ticker_list[i]} {trade_time} short : {round(exit_price, 8)}  //  exit : {round(entry_price, 8)}   {round(earning, 2)}"
            )
            temp.append(earning)
    upper_limit = 999
    if len(temp) != 0:
        for i in range(len(temp)):
            if i == upper_limit:
                break
            popped_item = temp.pop(random.randint(0, len(temp) - 1))
            buy_sell_log.append(popped_item)
    """upper_limit = 999
    if len(temp) != 0:
        sorted_list = sorted(temp)
        for i in range(len(sorted_list)):
            if i == upper_limit:
                break
            buy_sell_log.append(sorted_list[i])"""


if __name__ == "__main__":
    binance = Utils.use_binance("future")
    All_ohlcv = []
    buy_sell_log = []
    Slippage = 0.9982 * 0.9982
    performance = Utils.Performance()
    # value = 2.1
    value = 2.15
    ticker_list = list(binance.fetch_tickers().keys())
    ticker_list = [ticker for ticker in ticker_list if "/USDT" in ticker]
    del_list = []
    temp_time = Utils.timestamp_to_datetime(
        binance.fetch_ohlcv("BTC/USDT", "1d")[int(-102 * 4)][0]
    )[
        2
    ]  # 1h 기준 40의 배수
    convert = temp_time[:10] + "T" + temp_time[11:19] + "Z"
    timestamp = binance.parse8601(convert)
    for ticker in ticker_list:
        try:
            ohlcv = binance.fetch_ohlcv(ticker, "4h", timestamp, 605)
        except:
            time.sleep(0.1)
            continue
        if len(ohlcv) == 605:
            All_ohlcv.append(ohlcv)
        else:
            print(len(ohlcv))
            del_list.append(ticker)
    for ticker in del_list:
        ticker_list.remove(ticker)

    for day in range(600, 0, -1):
        log_maker(day)
        performance.calculating(buy_sell_log)
        buy_sell_log.clear()
    print(performance.zero_trade_log)
    performance.total_calculating()

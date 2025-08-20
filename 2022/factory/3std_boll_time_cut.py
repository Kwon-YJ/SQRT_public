#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import Utils
import numpy as np
import time
import pandas_ta as ta
import pandas as pd


def get_bband(
    ohlcv,
) -> list:  # [lower band, ma, upper band, band width, min-max scale percentage]
    if len((ohlcv[0])) != 6:
        ohlcv = [item[:6] for item in ohlcv]
    data = pd.DataFrame(
        data=np.array(ohlcv), columns=["Time", "Open", "High", "Low", "Close", "V"]
    )  ## rsi(15, high)
    result = data.ta.bbands(std=3, length=20).values.tolist()[-1]
    return result


def log_maker(day):
    for i in range(len(All_ohlcv)):
        ohlcv = All_ohlcv[i]
        high, low, close = ohlcv[-day][2:5]
        # bband = get_bband(ohlcv[-day-20:-day]) # [-day-20:-day] : D-1까지 종가의 BB, [-day-19:-day+1] : D-day까지 종가의 BB
        # bband = get_bband(ohlcv[-day-19:-day+1]) # [-day-20:-day] : D-1까지 종가의 BB, [-day-19:-day+1] : D-day까지 종가의 BB

        ohlcv_for_bband = ohlcv[-day - 19 : -day + 1]
        bband_for_entry_price = get_bband(ohlcv_for_bband)

        ohlcv_for_bband[-1][4] = ohlcv_for_bband[-1][2]
        bband_for_check = get_bband(
            ohlcv_for_bband
        )  # [-day-20:-day] : D-1까지 종가의 BB, [-day-19:-day+1] : D-day까지 종가의 BB

        if bband_for_check == None:
            continue
        lower_band = bband_for_check[0]
        upper_band_for_check = bband_for_check[2]
        upper_band_for_price = bband_for_entry_price[2]
        if high > upper_band_for_check:
            exit_price = upper_band_for_price
            entry_price = close
            trade_time = Utils.timestamp_to_datetime(ohlcv[-day][0])[1]
            earning = (exit_price / entry_price * Slippage - 1) * 100
            print(
                f"{  ticker_list[i]} {trade_time} short : {round(exit_price, 8)}  //  exit : {round(entry_price, 8)}   {round(earning, 2)}"
            )
            buy_sell_log.append(earning)
        elif low < lower_band:
            continue
            entry_price = lower_band
            exit_price = close
            trade_time = Utils.timestamp_to_datetime(ohlcv[-day][0])[1]
            earning = (exit_price / entry_price * Slippage - 1) * 100
            print(
                f"{  ticker_list[i]} {trade_time} long : {round(exit_price, 8)}  //  exit : {round(entry_price, 8)}   {round(earning, 2)}"
            )
            buy_sell_log.append(earning)


if __name__ == "__main__":
    binance = Utils.use_binance("future")
    All_ohlcv = []
    buy_sell_log = []
    Slippage = 0.9982 * 0.9982
    performance = Utils.Performance()
    ticker_list = list(binance.fetch_tickers().keys())
    ticker_list = [ticker for ticker in ticker_list if "/USDT" in ticker]
    del_list = []
    # temp_time = Utils.timestamp_to_datetime(binance.fetch_ohlcv('BTC/USDT','1d')[-105][0])[2] # 1h 기준 40의 배수
    temp_time = Utils.timestamp_to_datetime(
        binance.fetch_ohlcv("BTC/USDT", "1d")[-50][0]
    )[
        2
    ]  # 1h 기준 40의 배수
    convert = temp_time[:10] + "T" + temp_time[11:19] + "Z"
    timestamp = binance.parse8601(convert)
    candle_length = 200
    time_frame = "15m"
    # standard_ohlcv = binance.fetch_ohlcv('BTC/USDT', time_frame, timestamp, candle_length)
    standard_ohlcv = binance.fetch_ohlcv("BTC/USDT", time_frame, None, candle_length)
    standard_length = len(standard_ohlcv)
    standard_filanl_timestamp = standard_ohlcv[-1][0]
    for ticker in ticker_list:
        try:
            ohlcv = binance.fetch_ohlcv(ticker, time_frame, None, candle_length)
            # ohlcv = binance.fetch_ohlcv(ticker, time_frame,timestamp,candle_length)
        except:
            time.sleep(0.1)
            continue

        if ohlcv[-1][0] == standard_filanl_timestamp and len(ohlcv) == standard_length:
            All_ohlcv.append(ohlcv)
        else:
            print(len(ohlcv))
            del_list.append(ticker)
    for ticker in del_list:
        ticker_list.remove(ticker)
    # for day in range(standard_length-21, 0, -1):
    for day in range(standard_length - 21, 1, -1):
        log_maker(day)
        performance.calculating(buy_sell_log)
        buy_sell_log.clear()
    performance.total_calculating()
    print(performance.zero_trade_log)
    print(f"{int(performance.money_simulation())}")

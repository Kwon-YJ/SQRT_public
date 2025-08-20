# -*- coding: utf-8 -*- 
import ccxt
import time
import pandas as pd
import os
import datetime
import pyupbit


def get_decimal(target_price, sample_data):
    integral_part = max(len(str(int(sample_data[1]))), len(str(int(sample_data[2]))), len(str(int(sample_data[2]))), len(str(int(sample_data[2]))))
    if integral_part >= 3:
        return int(target_price)
    elif integral_part == 2:
        return round(target_price, 1)
    elif integral_part == 1:
        return round(target_price, 2)

def get_time(temp):
    now = temp
    YYYY = str(now.year)
    MM = str(now.month)
    DD = str(now.day)
    hh = str(now.hour)
    mm = str(now.minute)

    if len(MM) != 2:
        MM = '0' + MM
    if len(DD) != 2:
        DD = '0' + DD
    if len(hh) != 2:
        hh = '0' + hh
    if len(mm) != 2:
        mm = '0' + mm

    return YYYY + MM + DD, hh + mm

def exit_ALL():
    for i in range(len(is_entering)):
        time.sleep(0.7)
        unit = upbit2.get_balance(is_entering[i])
        upbit2.sell_market_order(is_entering[i], unit)
    reset = []
    return reset


upbit = ccxt.upbit({
    'enableRateLimit': True,
    'RateLimit': 10000
})
upbit.load_markets()



def get_tickers():
    temp = upbit.fetch_tickers().keys()
    all_tickers = [s for s in temp if 'KRW' in s]
    growth_rate = {}
    for idx, item in enumerate(all_tickers):
        time.sleep(1)
        ohlcv = upbit.fetch_ohlcv(item, '1d')
        growth_rate[item] = ohlcv[-1][4] / ohlcv[-8][4]
    result = sorted(growth_rate.items(), key = lambda item: item[1], reverse = True)[:7] 
    
    return [result[i][0] for i in range(len(result))]


tickers = get_tickers()
today_KRW = upbit.fetch_balance()['KRW']['free']

print(tickers)

'''
while(True):
    time_ = get_time(datetime.datetime.now())[1]
    if time_ == '0858':
        break
    tiem.sleep(25)
'''

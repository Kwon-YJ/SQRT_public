import ccxt
import time
from pprint import pprint
import datetime
import random
import numpy
import pybithumb


def test_trading(day, value, max_num):
    count = 0
    temp = []
    for i, item in enumerate(ticker_list):
        if count == max_num:
            return count, sum(temp), (sum(temp) / count)
        try:
            ohlcv = pybithumb.get_candlestick(item).tail(day + 1)
            D_1 = ohlcv.iloc[0]
            D_day = ohlcv.iloc[1]

            PP = (D_1["high"] + D_1["low"] + 2 * D_1["close"]) / 4
            S1_5 = value * PP - D_1["high"]

            if D_day["low"] < S1_5:
                earning = round(-100 + D_day["close"] / S1_5 * 99.5, 5)
                print(item, earning, "%수익")
                # print('buy :',round(S1_5,5), 'sell :', D_day['close'])
                count += 1
                temp.append(earning)
                buy_and_sell.append(earning)
        except:
            # print(item + '에러-------------------------------------------')
            print("", end="", flush=True)
    if count != 0:
        return count, sum(temp), sum(temp) * (count / max_num)
    else:
        return 0, 0, 0


def position_sizing():
    for i in range(41, 70):
        print("일자 :", i)
        random.shuffle(ticker_list)
        a, b, c = test_trading(i, 1.97, 6)
        print(c)
        # print('day',i,': ','count =' ,a,'   earining =' , b, '    total = ', c)

    risk_free = 0.14
    avg = numpy.mean(buy_and_sell)
    std = numpy.std(buy_and_sell)
    result = (avg - risk_free) / (std * std)
    print("평균수익", avg)
    print("포지션 사이징", result)
    print("")


time_frame = "1d"
ticker_list = pybithumb.get_tickers()

for i in range(10):
    buy_and_sell = []
    position_sizing()

import datetime
import pickle
import Utils
import parmap
import time
from pykrx import stock
import pandas as pd
import pandas_ta as ta
import numpy as np


def get_atr(loop):
    data = pd.DataFrame(data=np.array(loop), columns=["Close"])
    return data.ta.rsi(length=14).tolist()


def exit_logic(loop, i):
    triger = 0
    after_entry = loop[i:]  # 진입후 모든종가
    for k in range(1, len(after_entry) - 2, 1):  # 매도를 위한 반복
        if after_entry[k - 1] > after_entry[k]:  # 하락 시
            triger -= 1  # 트리거 -1
        else:
            triger += 1  # 상승 시 트리거 + 1

        if triger > 5:  # 트리거가 6이라면
            return after_entry[k + 1]  # 내일 종가에 매도
    return after_entry[-1]


def exit_logic2(loop, i):
    after_entry = loop[i - 300 :]
    atr = get_atr(after_entry)
    for k in range(301, len(after_entry) - 2, 1):
        exit_target = max(after_entry[:k]) - 10 * atr[k]
        if after_entry[k] < exit_target:
            return after_entry[k + 1]
    return after_entry[-1]


def log_maker(ticker_name):
    ticker_close = result[ticker_name]  # 한 종목의 모든 종가 불러오기

    return_data = []  # 리턴에 사용할 리스트

    if len(ticker_close) < 500:  # 상장한지 500 영업일 이내 종목 컷
        return None

    for i in range(
        365, len(ticker_close) - 3, 1
    ):  # 역대 고점은 적어도 상장기간 365 영업일 이상부터 시작

        close_sample = ticker_close[:i]  # 상장후 i 영업일이 지난 후 까지의 종가
        sorted_sample = sorted(close_sample)  # 정렬

        if close_sample[-1] == sorted_sample[-1]:  # 역대 고점인가

            # if max(sorted_sample[-250:]) / min(sorted_sample[-250:]) > 2: # 연간 최고/최저 갭이 50퍼 초과 컷
            #    continue

            entry_price = ticker_close[i]  # 진입가

            exit_price = exit_logic(ticker_close, i)
            earning = (exit_price / entry_price - 1) * 100
            # earning = (exit_price / entry_price - 1) * 100 # 손익
            return_data.append(earning)  # 손익 저장
            # return_data.append(k)

    return return_data


def name_to_ticker(name):
    df = stock.get_market_price_change("20180301", "20180310")
    return df.loc[df["종목명"] == name].index[0]


a = datetime.datetime.now()

with open("stock_close_data.pickle", "rb") as fr:
    result = pickle.load(fr)

ticker_list = list(result.keys())

trade_log = parmap.map(log_maker, ticker_list, pm_pbar=False, pm_processes=23)

print("done")
result = []
i = 0
while 1:
    try:
        if type(trade_log[i]) == list:
            for log in trade_log[i]:
                result.append(log)
        elif trade_log[i] != None:
            result.append(trade_log[i])
        i += 1
    except:
        time.sleep(1)
        break


# print(sum(result)/len(result));print(sorted(result)[int(len(result)/2)]) ;exit()

performance = Utils.Performance()
performance.calculating(result)

print(datetime.datetime.now() - a)

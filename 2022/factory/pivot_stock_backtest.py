import datetime
import pickle
import Utils
import parmap
import time
from pykrx import stock
import gzip


def log_maker(ticker_name):
    ohlcvs = result[ticker_name]  # 한 종목의 모든 ohlcv 불러오기
    return_data = []  # 리턴에 사용할 리스트
    for i in range(10, len(ohlcvs) - 3, 1):
        open, high, low, close = ohlcvs[i - 1]
        PP = (high + low + close) / 3
        if (
            ohlcvs[i][0] < 1.99 * PP - high and ohlcvs[i][0] > 1.92 * PP - high
        ):  # 시가가 어떤 범위에 존재할 때 매수
            entry_price = ohlcvs[i][0]  # 진입가
            exit_price = ohlcvs[i][3]  # 청산가, 당일 종가 일괄 매도
            try:
                earning = (exit_price / entry_price - 1) * 100
            except:
                continue
            # earning = (exit_price / entry_price - 1) * 100 # 손익
            return_data.append(earning)  # 손익 저장
            # return_data.append(k)
    return return_data


"""
def log_maker(ticker_name):
    ohlcvs = result[ticker_name] # 한 종목의 모든 ohlcv 불러오기
    return_data = [] # 리턴에 사용할 리스트
    for i in range(10, len(ohlcvs)-3, 1): 
        open, high, low, close = ohlcvs[i]
        try:
            earning = (close / open -1 ) * 100
        except:
            continue
        return_data.append(earning) # 손익 저장  
    return return_data
"""


def name_to_ticker(name):
    df = stock.get_market_price_change("20180301", "20180310")
    return df.loc[df["종목명"] == name].index[0]


if __name__ == "__main__":
    a = datetime.datetime.now()

    with gzip.open("stock_ohlcv_data.pickle", "rb") as fr:
        result = pickle.load(fr)
    ticker_list = list(result.keys())

    # trade_log = parmap.map(log_maker, ticker_list, pm_pbar=False, pm_processes=23)
    trade_log = parmap.map(log_maker, ticker_list, pm_pbar=False, pm_processes=10)

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

    performance = Utils.Performance()
    performance.calculating(result)

    print(datetime.datetime.now() - a)

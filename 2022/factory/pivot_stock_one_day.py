import datetime
import pickle
import Utils
import parmap
import time
from pykrx import stock


def remove_None(data):
    return [idx for idx in data if idx != None]


def get_result(ticker):
    day = 0  # 0 = today, 1 = d-1
    try:
        name = stock.get_market_ticker_name(ticker)
        if "스팩" in name:
            return None
        df = stock.get_market_ohlcv_by_date("20210401", Today, ticker)
        open = df["시가"].tolist()
        high = df["고가"].tolist()
        low = df["저가"].tolist()
        close = df["종가"].tolist()
        # PP = (high[-2-day] + low[-2-day] + (close[-2-day]*4) ) / 6
        PP = (high[-2 - day] + low[-2 - day] + close[-2 - day]) / 3
        if (
            open[-1 - day] < 1.99 * PP - high[-2 - day]
            and open[-1 - day] > 1.92 * PP - high[-2 - day]
        ):
            # if open[-1-day] < PP - high + low:
            earning = (close[-1 - day] / open[-1 - day] - 1) * 100
            # return [name, open[-1-day], close[-1-day], earning]
            return [name, earning]
    except:
        print("", end="")
    return None


if __name__ == "__main__":
    a = datetime.datetime.now()

    Today = Utils.get_time()[0]

    konex = stock.get_market_ticker_list(market="KONEX")
    ticker_list = list(set(stock.get_market_ticker_list(market="ALL")) - set(konex))
    trade_log = parmap.map(get_result, ticker_list, pm_pbar=True, pm_processes=2)

    print(remove_None(trade_log))

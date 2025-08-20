from pykrx import stock
import time
import csv
import datetime
import pandas as pd
import pandas_ta as ta
from pykiwoom.kiwoom import *
from pprint import pprint

import pickle
import os

def get_balance():  # opw00001
	df = kiwoom.block_request("opw00001",
	                          계좌번호=stock_account,
	                          비밀번호="",
	                          비밀번호입력매체구분="00",
	                          조회구분=2,
	                          output="예수금상세현황",
	                          next=0)

	balance = int(df['100%종목주문가능금액'][0])
	return balance


kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)
accounts = kiwoom.GetLoginInfo("ACCNO")
stock_account = accounts[0]


def get_time():
    now = datetime.datetime.now()
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

def get_qty(ticker):
    accounts = kiwoom.GetLoginInfo("ACCNO")
    stock_account = accounts[0]

    today_var = str(datetime.datetime.now()).split(" ")[0].replace("-", "")

    start_time = datetime.datetime.now() - datetime.timedelta(5)
    start_time = str(start_time).split(" ")[0].replace("-", "")
    df = stock.get_market_ohlcv(start_time, today_var, ticker)

    money = stock_account
    price = df.tail(1)["종가"].values
    qty = int(money / price[0])
    return qty


def exit_side():
    now = datetime.datetime.now()
    with open('./data.pickle', 'rb') as f:
        data = pickle.load(f)
        for ticker, positions in data.items():
            for i, position in enumerate(positions):
                today_var = str(now).split(" ")[0].replace("-", "")
                start_time = now - datetime.timedelta(5)
                df = stock.get_market_ohlcv(start_time, today_var, ticker).tail(1)
                if isinstance(position[-1], dict):
                    entry_time = position[-1]["entry_time"]
                    param = position[-1]["exit_param"]
                    if now + datetime.timedelta(hours=9) > entry_time:
                        open_price = df["시가"].values
                        take_profit_price = open_price + param
                        data[ticker][i][-1] = float(take_profit_price[0]) 
                else:
                    current_price = df["종가"].values
                    sl, qty, tp = position
                    if current_price < sl:
                        kiwoom.SendOrder("시장가매도", "0101", stock_account, 2, ticker, qty, 0, "03", "") # 시장가는 0, "03"
                        print("손절")
                    if current_price > tp:
                        kiwoom.SendOrder("시장가매도", "0101", stock_account, 2, ticker, qty, 0, "03", "") # 시장가는 0, "03"
                        print("익절")
                    data[ticker].pop(i)

    with open('./data.pickle', 'wb') as f:
        pickle.dump(data, f)


def get_daily_data():
    result_dict = {}
    today_var = str(datetime.datetime.now()).split(" ")[0].replace("-", "")
    start_time = datetime.datetime.now() - datetime.timedelta(300)
    start_time = str(start_time).split(" ")[0].replace("-", "")
    ticker_list = stock.get_market_ticker_list(today_var, market="ALL")
    for ticker in ticker_list:
        df = stock.get_market_ohlcv(start_time, today_var, ticker)
        df["ema8"] = ta.ema(df["종가"], length=8)
        df["ema16"] = ta.ema(df["종가"], length=16)
        df['tail_d'] = df[['시가', '종가']].max(axis=1) - df['저가']
        df["body_d"] = abs(df['종가'] - df['시가'])
        result_dict[ticker] = df
    return result_dict


if os.path.isfile("./data.pickle") == False:
    with open('./data.pickle', 'wb') as f:
        pickle.dump({}, f)



if __name__ == "__main__":

    while True:
        entry_positions = {}

        if get_time()[-1] != "1518":
            exit_side()
            time.sleep(10)
            continue

        daily_data = get_daily_data()

        for i, ticker in enumerate(daily_data.keys()):
            if "스팩" in ticker:
                continue
            daily_ohlcv = daily_data[ticker].iloc[-1].tolist()
            o, h, l, c, v, _, ema_8, ema_16, tail_d, body_d = daily_ohlcv
            try:
                if l < ema_8 and min(c, o) > ema_8 and ema_8 > ema_16:
                    param_1, param_2, _, __ = list(map(float, pd.read_csv(f"../post_result/{ticker}.csv", header = None).iloc[-1].tolist()))
                    if tail_d * param_1 < tail_d:
                        qty = get_qty(ticker)
                        if qty < 1:
                            continue
                        else:
                            ticker_name = stock.get_market_ticker_name(ticker)
                            print(f"{ticker_name} 시장가 {qty}주 매수")   
                            kiwoom.SendOrder("시장가매수", "0101", stock_account, 1, ticker, qty, 0, "03", "") # 시장가는 0, "03"
                            stop_loss_price = l
                            take_prof_data = {"entry_time": datetime.datetime.now(), "exit_param":param_2 * abs((l-max(c, o)))} 
                            if ticker in entry_positions.keys():
                                entry_positions[ticker].append([stop_loss_price, qty, take_prof_data])
                            else:
                                entry_positions[ticker] = [[stop_loss_price, qty, take_prof_data]]
            except Exception as e:
                print(e)
                continue

        with open('./data.pickle', 'rb') as f:
            data = pickle.load(f)

        combined_dict = {**data, **entry_positions}

        with open('./data.pickle', 'wb') as f:
            pickle.dump(combined_dict, f)



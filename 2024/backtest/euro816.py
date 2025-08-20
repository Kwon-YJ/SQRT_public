import pandas as pd
import pandas_ta as ta
import argparse
import math


import numpy as np
from abc import *


def TW(odd):
    return np.round(-np.log(0.99) / (np.log(1 + 0.01 * odd) - np.log(0.99)), 4)


def shortest_distance(odd, winrate, n=100000):
    lins = np.linspace(0, 10, n)
    y = TW(lins)
    least_distance = 1e100
    for i in range(n):
        dx = lins[i] - odd
        dy = y[i] - winrate
        distance = np.sqrt(dx**2 + dy**2)
        if distance < least_distance:
            least_distance = distance
    if winrate > TW(odd):
        return np.round(least_distance, 10)
    else:
        return -1 * np.round(least_distance, 10)


def get_perfomance(trade_log):
    if len(trade_log) == 0:
        return None
    win = []
    lose = []
    risk_free = 0.038 / 365
    avg = np.mean(trade_log)
    std = np.std(trade_log)

    for i in range(len(trade_log)):
        if trade_log[i] > 0:
            win.append(trade_log[i])
        elif trade_log[i] < 0:
            lose.append(trade_log[i])

    avg_W_L_ratio = -1 * np.mean(win) / np.mean(lose)
    total_perform = shortest_distance(avg_W_L_ratio, len(win) / len(trade_log))
    # total_perform = Utils.shortest_distance(avg_W_L_ratio, len(win) / len(trade_log))
    size = (avg - risk_free) / (std * std)
    print("총거래 : ", len(trade_log))
    print("수익거래수 :", len(win))
    print("손실거래수 :", len(lose))
    print("평균거래 :", avg)
    print("평균수익거래 :", np.mean(win))
    print("평균손실거래 :", np.mean(lose))
    print("평균손익비 :", avg_W_L_ratio)
    win_rate = int(round(len(win) / len(trade_log), 2) * 100)
    print("승률 :", win_rate, "%")
    print("포지션 사이징 :", size)
    if len(lose) > 0:
        print("최대 손실 :", min(lose))
    print(total_perform)
    print("")


class Performance:
    def __init__(self):
        self.zero_trade_log = 0  # 해당 기간동안 매매를 안한 횟수 기록
        self.total_trade_log = []  # 누적 로그
        self.risk_free = 0.038 / 365  # 무위험 수익률
        self.max_trade_count = 0

    def TW(self, odd):
        return np.round(-np.log(0.99) / (np.log(1 + 0.01 * odd) - np.log(0.99)), 4)

    def shortest_distance(self, odd, winrate, n=100000):
        lins = np.linspace(0, 10, n)
        y = TW(lins)
        least_distance = 1e100
        for i in range(n):
            dx = lins[i] - odd
            dy = y[i] - winrate
            distance = np.sqrt(dx**2 + dy**2)
            if distance < least_distance:
                least_distance = distance
        if winrate > TW(odd):
            return np.round(least_distance, 10)
        else:
            return -1 * np.round(least_distance, 10)

    def calculating(self, trade_log):
        if len(trade_log) == 0:
            self.zero_trade_log += 1
            return None

        if self.max_trade_count < len(trade_log):
            self.max_trade_count = len(trade_log)

        trade_count = len(trade_log)  # 총 거래 수
        win = [item for item in trade_log if item > 0]  # 수익을 낸 경우
        lose = [item for item in trade_log if item < 0]  # 손실을 낸 경우
        win_count = len(win)  # 수익 거래 수
        avg = np.mean(trade_log)  # 평균 손익률
        avg_win = np.mean(win)  # 평균 수익률
        avg_lose = np.mean(lose)  # 평균 손실률
        std = np.std(trade_log)  # trade_log의 편차
        avg_W_L_ratio = -1 * np.mean(win) / np.mean(lose)  # 평균 손익비
        win_rate = int(win_count / trade_count * 100)  # 승률
        # sharp = (avg - self.risk_free) / (std ** 2)
        std_lose = np.std(lose)
        sharp = (avg - self.risk_free) / std
        sortino = (avg - self.risk_free) / std_lose
        total_perform = shortest_distance(avg_W_L_ratio, win_count / trade_count)

        risk_free = 0.038 / 365

        size = (avg - risk_free) / (std * std)

        print(f"총 거래 수 : {trade_count}")
        print(f"수익 거래 수 : {win_count}")
        print(f"손실 거래 수 : {len(lose)}")
        print(f"평균 손익률 : {avg}%")
        print(f"평균 수익률 : {avg_win}%")
        print(f"평균 손실률 : {avg_lose}%")
        print(f"평균 손익비 : {avg_W_L_ratio}")
        print(f"승 률 : {win_rate}%")

        print("포지션 사이징 :", size)

        print(f"sharp ratio : {sharp}%")
        print(f"sortino ratio : {sortino}")
        if lose != []:
            print(f"최대 손실 : {min(lose)}%")
        print(f"{total_perform}\n")

        self.total_trade_log += trade_log

    def total_calculating(self):
        print(f"max : {self.max_trade_count}")
        final_wallet_balance = self.money_simulation()
        self.calculating(self.total_trade_log)
        print(f"{final_wallet_balance}")

    def money_simulation(self):
        money = 0
        bet = 264
        print(len(self.total_trade_log))
        for earn in self.total_trade_log:
            # bet = money * 0.03
            earn *= 47
            result = bet * (1 + earn / 100)
            money = money - bet + result
        return money


def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-T",
        "--time_frame",
        default="1d",
        help='select time frame {"1m", "5m", "30m", "1h", "1d"}',
    )


def load_data(data_dir="../../data/", file_name="E6_1d.CSV"):
    csv_data = pd.read_csv(data_dir + file_name, header=None)
    try:
        csv_data.columns = ["t", "o", "h", "l", "c", "v", "none"]
    except:
        csv_data.columns = ["t", "o", "h", "l", "c", "v"]
    ema_8 = ta.ema(csv_data["c"], length=8)
    ema_16 = ta.ema(csv_data["c"], length=16)

    return csv_data, ema_8.values.tolist(), ema_16.values.tolist()


# ohlc, ema_8, ema_16 = load_data(file_name="E6_1h.CSV")
ohlc, ema_8, ema_16 = load_data(file_name="E6_1d.CSV")


open_data = ohlc["o"].values.tolist()
high_data = ohlc["h"].values.tolist()
low_data = ohlc["l"].values.tolist()
close_data = ohlc["c"].values.tolist()

time_data = ohlc["t"].values.tolist()

is_long = False
is_short = False

short_sl = []
short_tp = []

trade_log = []

slippage = 1

long_entry_price = []
long_entry_time = []

short_entry_price = []
short_entry_time = []


long_sl = []
long_tp = []

for i in range(1, len(ohlc) - 1):

    high_ = high_data[i]
    low_ = low_data[i]
    close_ = close_data[i]

    short_ema = ema_8[i]
    long_ema = ema_16[i]

    open_ = open_data[i]

    if math.isnan(long_ema) == True:
        continue

    # long case
    if is_long == False:
        if (
            low_ < long_ema
            and low_ < short_ema
            and min(close_, open_) > short_ema
            and short_ema > long_ema
        ):

            tail_d = min(close_, open_) - low_
            body_d = abs(close_ - open_)
            if body_d * 2.52 < tail_d:
                is_long = True
                long_entry_price.append(open_data[i + 1])
                long_sl.append(low_)
                long_tp.append(
                    open_data[i + 1] + 1.66 * abs((low_ - max(close_, open_)))
                )

                long_entry_time = time_data[i + 1]
    else:
        if low_ < long_sl[-1]:
            is_long = False
            earning = 100 * (long_sl[-1] / long_entry_price[-1] * slippage - 1)
            text = f"LSL / {long_entry_time} ~ {time_data[i]} long : {long_entry_price[-1]} exit : {long_sl[-1]} earn : {earning}"
            print(text)
            trade_log.append(earning)
        elif high_ > long_tp[-1]:
            is_long = False
            earning = 100 * (long_tp[-1] / long_entry_price[-1] * slippage - 1)
            text = f"LTP / {long_entry_time} ~ {time_data[i]} long : {long_entry_price[-1]} exit : {long_sl[-1]} earn : {earning}"
            print(text)
            trade_log.append(earning)

    # short case
    if is_short == False:

        if (
            high_ > long_ema
            and high_ > short_ema
            and long_ema > short_ema
            and short_ema > close_
            and short_ema > open_
        ):
            tail_d = high_ - max(close_, open_)
            body_d = abs(close_ - open_)
            if body_d * 3 < tail_d:

                is_short = True
                short_entry_price.append(open_data[i + 1])
                short_sl.append(high_)
                short_tp.append(
                    open_data[i + 1] - 1.5 * abs((high_ - min(close_, open_)))
                )
                short_entry_time.append(time_data[i + 1])

    else:
        if high_ > short_sl[-1]:
            is_short = False

            earning = -100 * (short_sl[-1] / short_entry_price[-1] / slippage - 1)
            # text = f"SSL / {short_entry_time[-1]} ~ {time_data[i]} short : {short_entry_price[-1]} exit : {short_sl[-1]} earn : {earning}"
            text = f"SSL / {short_entry_time[-1]} ~ {time_data[i]} short : {short_entry_price[-1]} exit : {short_sl[-1]} earn : {earning}"
            print(text)
            trade_log.append(earning)

        elif low_ < short_tp[-1]:
            is_short = False

            earning = -100 * (short_tp[-1] / short_entry_price[-1] / slippage - 1)
            text = f"STP / {short_entry_time[-1]} ~ {time_data[i]} short : {short_entry_price[-1]} exit : {short_tp[-1]} earn : {earning}"
            print(text)
            trade_log.append(earning)


# get_perfomance(trade_log)

total_perform = Performance()

total_perform.calculating(trade_log)

result = total_perform.money_simulation()

print(result)

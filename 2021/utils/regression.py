# -*- coding: utf-8 -*-
import ccxt
import time
import datetime
import pandas as pd
import numpy as np


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
    size = (avg - risk_free) / (std * std)

    for i in range(len(trade_log)):
        if trade_log[i] > 0:
            win.append(trade_log[i])
        elif trade_log[i] < 0:
            lose.append(trade_log[i])

    avg_W_L_ratio = -1 * np.mean(win) / np.mean(lose)
    total_perform = shortest_distance(avg_W_L_ratio, len(win) / len(trade_log))

    print("총거래 : ", len(trade_log))
    print("수익거래수 :", len(win))
    print("손실거래수 :", len(lose))
    print("평균손익 :", avg)
    print("평균수익거래 :", np.mean(win))
    print("평균손실거래 :", np.mean(lose))
    print("평균손익비 :", avg_W_L_ratio)
    win_rate = int(round(len(win) / len(trade_log), 2) * 100)
    print("승률 :", win_rate, "%")
    if len(lose) > 0:
        # print(lose)
        print("MDD :", min(lose))
    print("시그마 포지션 사이징 :", size)
    win_rate = win_rate * 0.01
    temp = (1 - win_rate) / avg_W_L_ratio
    kelly = win_rate - temp
    print("켈리 레이쇼 :", kelly)

    print("성능 지수 :", total_perform)

    if len(trade_log) == 0:
        return None

    if len(lose) == 0:
        temp_temp_.append(0.25)
    elif len(win) == 0:
        temp_temp_.append(-0.25)
    else:
        temp_temp_.append(total_perform)

    # base_return = ((1+ (np.mean(win)*0.01)) ** win_rate) * ((1- (np.mean(lose)*-0.01)) ** (1-win_rate))
    # print('매매 당 기대 수익률 :', (base_return-1) * kelly)
    # print('총 수익률 :', (base_return-1) * kelly * len(trade_log))
    print("")


def get_tickers():
    result = []
    base_ticker = list(binance.fetch_tickers().keys())
    base_ticker = [
        base_ticker[i] for i in range(len(base_ticker)) if "/USDT" in base_ticker[i]
    ]
    base_ticker.remove("BTCDOM/USDT")
    return base_ticker

    for item in base_ticker:
        time.sleep(0.3)
        try:
            ohlcvs = get_ohlcv(item, "1d", 4)
            if ohlcvs[-2][1] > ohlcvs[-2][4]:
                result.append(item)
        except:
            continue
    return result


# 매수 종목 선정하기
def get_target(item):
    try:
        ohlcv = get_ohlcv(item, "1h", 400)
        df = pd.DataFrame(
            data=np.array(ohlcv),
            columns=["T", "O", "H", "L", "close", "V", "0", "0", "0", "0", "0", "0"],
        )
        EMA_7 = df.ta.ema(length=7).tolist()[-2]
        EMA_25 = df.ta.ema(length=25).tolist()[-2]
        EMA_99 = df.ta.ema(length=99).tolist()[-2]
        if EMA_7 < EMA_25 and EMA_7 < EMA_99 and EMA_25 < EMA_99:
            ohlcv = ohlcv[-2]
            high_ = ohlcv[2]
            low_ = ohlcv[3]
            if high_ - low_ == 0:
                return None
            close_ = ohlcv[4]
            IBS = (close_ - low_) / (high_ - low_)
            # if IBS < 0.08:
            if IBS < 0.1:
                return item
    except Exception as e:
        print(item)
        print(e)
        time.sleep(0.1)
        return None
    return None


if __name__ == "__main__":
    binance = ccxt.binance(
        {
            "options": {"defaultType": "future"},
            "timeout": 30000,
            "apiKey": "bOHcvOmxqFVGN6FPsJwcnh4QOxw0D6oaFGHjEhpU2pby1bt7EJDb6t9TExauOccU",
            "secret": "Yece0g5APcAZR4sXJl1M007tLL9w9bB7Qp2o3fGFYJjN3f6tfx6lOCq1LdmRk4Ob",
            "enableRateLimit": False,
        }
    )
    binance.load_markets()

    ticker_list = get_tickers()
    print(ticker_list)

    while True:
        time.sleep(2)

        target_list = parmap.map(get_target, ticker_list, pm_pbar=False, pm_processes=4)
        target_list = list(set(target_list) - set([None]))
        print(target_list)
        for target in target_list:
            try:
                order(target)
            except:
                print(f"fail buy {target}")
                time.sleep(0.5)
                continue
        time.sleep(59)

import pandas as pd
import datetime
import ccxt
import time
import urllib
import json
from Decimal_update import get_decimal
from all_func import send_MSG, get_time


def ema(data, length):
    result = []
    for i in range(len(data)):
        result.append(data[i][4])
    return pd.Series(result).ewm(span=length, adjust=True).mean().tolist()


def get_size(ticker, side, time_frame):
    temp = binance.fetch_ohlcv(ticker, time_frame)
    if side == "long":
        entry_price = temp[-1][4]
        exit_price = ema(temp, 50)[-1]
    else:
        entry_price = ema(temp, 50)[-1]
        exit_price = temp[-1][4]

    money = binance.fetch_balance()["USDT"]["total"]
    size = (money * 0.025) / (entry_price - exit_price)
    size = round(size, get_decimal(ticker)[0])
    return size, entry_price, exit_price


binance = ccxt.binance(
    {
        "options": {"defaultType": "future"},
        "timeout": 30000,
        "apiKey": "FRbVseExyAWjQUtYFnS4memLnPCcgNAeRW7HEBrrw9qyIyPUMCTzUKxZKOJIHcfV",
        "secret": "CbDX3DE5r9ErdLBOphDB4rjCaAaKbUqITbNK05YIitktZ24VfcNrvVRbIgfK6L87",
        "enableRateLimit": True,
    }
)

ticker_list = list(binance.fetch_tickers().keys())
ticker_list = list(set(ticker_list) - set(["BTCUSDT_210625, ETHUSDT_210625"]))


def main(time_frame):
    for i in range(len(ticker_list)):
        up_count = 0
        down_count = 0
        temp = binance.fetch_ohlcv(ticker_list[i], time_frame)

        if temp == None:
            continue

        ema_25 = ema(temp, 25)[-10:]
        ema_50 = ema(temp, 50)[-10:]
        ema_99 = ema(temp, 99)[-10:]
        for j in range(len(ema_99) - 1):
            try:
                if (
                    temp[-10 + j][4] > ema_25[j]
                    and ema_25[j] > ema_50[j]
                    and ema_50[j] > ema_99[j]
                ):
                    up_count += 1
                if (
                    temp[-10 + j][4] < ema_25[j]
                    and ema_25[j] < ema_50[j]
                    and ema_50[j] < ema_99[j]
                ):
                    down_count += 1
            except:
                continue
        if up_count == 9 and temp[-1][4] < ema_25[-1]:
            size_, entry_price, exit_price = get_size(
                ticker_list[i], "long", time_frame
            )
            print("up", ticker_list[i], size_, entry_price, exit_price)
            send_MSG([ticker_list[i], time_frame, "up", size_, entry_price, exit_price])
        if down_count == 9 and temp[-1][4] > ema_25[-1]:
            size_, entry_price, exit_price = get_size(
                ticker_list[i], "short", time_frame
            )
            print("down", ticker_list[i], size_, entry_price, exit_price)
            send_MSG(
                [ticker_list[i], time_frame, "down", size_, entry_price, exit_price]
            )
        up_count = 0
        down_count = 0


if __name__ == "__main__":
    while True:
        time.sleep(11)
        if (get_time()[1]) == "0000":
            print("새 하루의 시작")
            main("1h")
            main("1d")
        if (get_time()[1][2:]) == "00":
            print("새 한시간의 시작")
            main("1h")

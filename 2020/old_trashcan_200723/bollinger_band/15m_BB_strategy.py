# -*- coding: utf-8 -*-
import ccxt
import time
import datetime
import telegram
import pandas as pd


def bb(x, w=20, k=2):  # 볼린저 밴드
    data = []
    for i in range(len(x)):
        data.append(x[i][4])
    data = pd.Series(data)
    mbb = data.rolling(w).mean()
    lbb = mbb - k * data.rolling(w).std()
    return [lbb.tolist()[-1], mbb.tolist()[-1]]


def reset():
    global bot, binance, tickers, ban_ticker, temp_ticker, today_money
    binance = ccxt.binance(
        {
            "apiKey": "nQhztY2hEGYUyPRzViv55tnh1hGw01Vdlb3TglBlpJwzn4ZRsvfEfa0txp4X0rZR",
            "secret": "MwGFSgoVb3zoZYWgk3OEvRpVeWkck1I88eTAZOJlaeMrhrYBAzRcaUBkOKWGiAWi",
            "enableRateLimit": True,
        }
    )
    tickers = [
        "BTC/USDT",
        "ETH/USDT",
        "BCH/USDT",
        "LTC/USDT",
        "EOS/USDT",
        "XRP/USDT",
        "LINK/USDT",
        "XTZ/USDT",
        "ETC/USDT",
        "TRX/USDT",
        "ADA/USDT",
        "ATOM/USDT",
        "NEO/USDT",
        "VET/USDT",
        "DASH/USDT",
        "XLM/USDT",
        "XMR/USDT",
        "ZEC/USDT",
        "ONT/USDT",
        "QTUM/USDT",
        "BAT/USDT",
        "IOST/USDT",
        "IOTA/USDT",
    ]
    ban_ticker = []
    temp_ticker = []
    today_money = binance.fetch_balance()["USDT"]["total"]
    bot.send_message(chat_id=801167350, text="금일잔고 : " + str(today_money))


def convert(ohlcv5):  # convert 5m → 15m
    ohlcv15 = []
    temp = str(datetime.datetime.fromtimestamp(ohlcv5[0][0] / 1000))[14:16]
    if int(temp) % 15 == 5:
        del ohlcv5[0]
        del ohlcv5[1]
    elif int(temp) % 15 == 10:
        del ohlcv5[0]
    for i in range(0, len(ohlcv5) - 2, 3):
        highs = [ohlcv5[i + j][2] for j in range(0, 3) if ohlcv5[i + j][2]]
        lows = [ohlcv5[i + j][3] for j in range(0, 3) if ohlcv5[i + j][3]]
        volumes = [ohlcv5[i + j][5] for j in range(0, 3) if ohlcv5[i + j][5]]
        candle = [
            ohlcv5[i + 0][0],
            ohlcv5[i + 0][1],
            max(highs) if len(highs) else None,
            min(lows) if len(lows) else None,
            ohlcv5[i + 2][4],
        ]
        ohlcv15.append(candle)
    return ohlcv15


reset()

while True:
    for i in range(len(tickers)):
        try:
            # 0 = 타임프레임 | 1 = 시가 | 2 = 고가 | 3 = 저가 | 4 = 종가 | 5 = 거래량
            temp = convert(binance.fetch_ohlcv(tickers[i], "5m"))
            if (
                (bb(temp)[0] > temp[-1][4])
                and (temp[-1][1] > temp[-1][4])
                and (tickers[i] not in ban_ticker)
            ):
                now_current_p = float(binance.fetch_order_book(tickers[i])["bids"][1])
                unit = (today_money / now_current_p) * 0.08
                order = binance.create_limit_buy_order(tickers[i], unit, now_current_p)
                bot.send_message(
                    chat_id=801167350,
                    text="buy " + tickers[i] + "  " + str(order["price"]),
                )
                ban_ticker.append(tickers[i])
        except:
            print("에러 Line 56 ~ 64", end="", flush=True)
    for i in range(len(ban_ticker)):
        try:
            temp = convert(binance.fetch_ohlcv(ban_ticker[i], "5m"))
            if bb(temp)[1] < temp[-1][4]:
                balance = binance.fetch_balance()
                order = binance.create_market_sell_order(
                    ban_ticker[i], balance[ban_ticker[i][0:-5]]["free"]
                )
                bot.send_message(
                    chat_id=801167350,
                    text="sell " + ban_ticker[i] + "  " + str(order["price"]),
                )
                temp_ticker.append(ban_ticker[i])
        except:
            print("에러 Line 66 ~ 74", end="", flush=True)
    ban_ticker = list(set(ban_ticker) - set(temp_ticker))
    reset_time = "%s%s" % (datetime.datetime.now().hour, datetime.datetime.now().minute)
    if reset_time[0:-1] == "090":  # 현재 시간이 GMT 기준 자정이라면
        reset()
        time.sleep(600)

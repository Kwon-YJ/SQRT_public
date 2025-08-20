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
    return [lbb.tolist()[-2], mbb.tolist()[-2]]


def reset():
    global bot, binance, all_ticker, tickers, ban_ticker, temp_ticker, today_money
    binance = ccxt.binance(
        {
            "enableRateLimit": True,
        }
    )
    all_ticker = list(binance.fetch_tickers().keys())
    tickers = [
        s for s in all_ticker if "/BTC" in s
    ]  # 분모에 BTC : 더 많은 유동성, 더 많은 시장 종목 // USDT : 기초자산의 가격 변동 X
    ban_ticker = []
    temp_ticker = []
    today_money = binance.fetch_balance()["BTC"]["total"]
    bot.send_message(chat_id=801167350, text="금일잔고 : " + str(today_money))


reset()
while True:
    for i in range(len(tickers)):
        try:
            # 0 = 타임프레임 | 1 = 시가 | 2 = 고가 | 3 = 저가 | 4 = 종가 | 5 = 거래량
            temp = binance.fetch_ohlcv(tickers[i], "1h")
            if (
                (bb(temp)[0] > temp[-2][4])
                and (temp[-2][1] > temp[-2][4])
                and (tickers[i] not in ban_ticker)
            ):
                unit = (today_money / temp[-1][4]) * 0.08
                order = binance.create_market_buy_order(tickers[i], unit)
                bot.send_message(
                    chat_id=801167350,
                    text="buy " + tickers[i] + "  " + str(order["price"]),
                )
                ban_ticker.append(tickers[i])
        except:
            print("에러 Line 35 ~ 44", end="", flush=True)
    for i in range(len(ban_ticker)):
        try:
            temp = binance.fetch_ohlcv(ban_ticker[i], "1h")
            if bb(temp)[1] < temp[-1][4]:
                balance = binance.fetch_balance()
                order = binance.create_market_sell_order(
                    ban_ticker[i], balance[ban_ticker[i][0:-4]]["free"]
                )
                bot.send_message(
                    chat_id=801167350,
                    text="sell " + ban_ticker[i] + "  " + str(now_current_p),
                )
                temp_ticker.append(ban_ticker[i])
        except:
            print("에러 Line 46 ~ 54", end="", flush=True)
    ban_ticker = list(set(ban_ticker) - set(temp_ticker))
    reset_time = "%s%s" % (datetime.datetime.now().hour, datetime.datetime.now().minute)
    if reset_time[0:-1] == "090":  # 현재 시간이 GMT 기준 자정이라면
        reset()
        time.sleep(600)

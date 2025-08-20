# -*- coding: utf-8 -*-
import ccxt
import time
import datetime
import telegram

bot = telegram.Bot(token=my_token)

binance = ccxt.binance(
    {
        "enableRateLimit": True,
    }
)

all_ticker = list(binance.fetch_tickers().keys())
tickers = [
    s for s in all_ticker if "/BTC" in s
]  # 분모에 BTC : 더 많은 유동성, 더 많은 시장 종목 // USDT : 기초자산의 가격 변동 X
info_ticker = []
info_price = []
today_money = binance.fetch_balance()["BTC"]["total"]
bot.send_message(chat_id=801167350, text="금일잔고 : " + str(today_money))
temp_ticker = []
data = []

try:
    for i in range(len(tickers)):
        # time.sleep(0.5)
        data.append(binance.fetch_ohlcv(tickers[i], "1d")[-2])
except:
    print("", end="", flush=True)

while True:
    reset_time = "%s%s" % (datetime.datetime.now().hour, datetime.datetime.now().minute)
    if reset_time[0:-1] == "090":
        balance = binance.fetch_balance()
        if len(info_ticker) != 0:
            for i in range(len(info_ticker)):
                order = binance.create_market_sell_order(
                    info_ticker[i], balance[info_ticker[i][0:-4]]["free"]
                )
        all_ticker = list(binance.fetch_tickers().keys())
        tickers = [
            s for s in all_ticker if "/BTC" in s
        ]  # 분모에 BTC : 더 많은 유동성, 더 많은 시장 종목 // USDT : 기초자산의 가격 변동 X
        info_ticker = []
        info_price = []
        today_money = binance.fetch_balance()["BTC"]["total"]
        bot.send_message(chat_id=801167350, text="금일잔고 : " + str(today_money))
        temp_ticker = []
        data = []
        try:
            for i in range(len(tickers)):
                data.append(binance.fetch_ohlcv(tickers[i], "1d")[-2])
        except:
            print("", end="", flush=True)
        time.sleep(599)
    else:
        for i in range(len(tickers)):
            try:
                # 0 = 타임프레임 | 1 = 시가 | 2 = 고가 | 3 = 저가 | 4 = 종가
                temp = abs(data[i][2] - data[i][3])
                entry_price = data[i][2] + abs(data[i][1] - data[i][4])
                now_current_p = binance.fetch_ticker(tickers[i])["close"]
                if now_current_p > entry_price and tickers[i] not in info_ticker:
                    unit = (today_money / now_current_p) * 0.06
                    order = binance.create_market_buy_order(tickers[i], unit)
                    bot.send_message(
                        chat_id=801167350,
                        text="buy " + tickers[i] + "  " + str(order["price"]),
                    )
                    info_price.append(order["price"])  # // 실제 거래
                    # info_price.append(now_current_p) # // 테스트 거래
                    info_ticker.append(tickers[i])
            except:
                time.sleep(0.7)
                print("에러", end="", flush=True)
        if len(info_ticker) == 0:
            continue
        else:
            for i in range(len(info_ticker)):
                temp = abs(
                    binance.fetch_ohlcv(info_ticker[i], "1d")[-2][2]
                    - binance.fetch_ohlcv(info_ticker[i], "1d")[-2][3]
                )
                exit_price1 = info_price[i] + temp * 0.7
                exit_price2 = info_price[i] - temp * 0.3
                now_current_p = binance.fetch_ticker(info_ticker[i])["close"]
                if (
                    now_current_p > exit_price1 or now_current_p < exit_price2
                ) and info_ticker[i] not in temp_ticker:
                    balance = binance.fetch_balance()
                    order = binance.create_market_sell_order(
                        info_ticker[i], balance[info_ticker[i][0:-4]]["free"]
                    )
                    bot.send_message(
                        chat_id=801167350,
                        text="sell " + info_ticker[i] + "  " + str(now_current_p),
                    )
                    temp_ticker.append(info_ticker[i])

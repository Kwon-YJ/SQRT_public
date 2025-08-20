# -*- coding: utf-8 -*-
import ccxt
import time
import datetime

binance = ccxt.binance(
    {
        "enableRateLimit": True,
    }
)

# print(binance.fetch_tickers().keys())

basetime_ = str(datetime.datetime.now() - datetime.timedelta(hours=16))
convert_time = basetime_[0:10] + "T" + basetime_[11:19]
all_ticker = list(binance.fetch_tickers().keys())
tickers = [
    s for s in all_ticker if "/USDT" in s
]  # 분모에 BTC : 더 많은 유동성, 더 많은 시장 종목 // USDT : 기초자산의 가격 변동 X
info_ticker = []
info_price = []
today_USDT = binance.fetch_balance()["USDT"]["total"]
temp_ticker = []
temp_price = []

while True:
    reset_time = "%s%s" % (datetime.datetime.now().hour, datetime.datetime.now().minute)
    if reset_time[0:-1] == "090":
        # for i in range(len(info_ticker)):
        # 	order = binance.create_market_sell_order(info_ticker[0], balance[info_ticker[0][0:-5]]['free'])
        basetime_ = str(datetime.datetime.now() - datetime.timedelta(hours=16))
        convert_time = basetime_[0:10] + "T" + basetime_[11:19]
        all_ticker = list(binance.fetch_tickers().keys())
        tickers = [
            s for s in all_ticker if "/USDT" in s
        ]  # 분모에 BTC : 더 많은 유동성, 더 많은 시장 종목 // USDT : 기초자산의 가격 변동 X
        info_ticker = []
        info_price = []
        today_USDT = binance.fetch_balance()["USDT"]["total"]
        temp_ticker = []
        time.sleep(599)
    else:
        for i in range(len(tickers)):
            a = binance.fetch_ohlcv(tickers[i], "1d")
            try:
                b = binance.fetch_ohlcv(
                    tickers[i], "5m", binance.parse8601(convert_time)
                )
                data = []
                data.append(a[-1][4])  # 현재가
                data.append(a[-2][4])  # 전일종가
                data.append(b[-2])  # 5분봉 D-1
                data.append(b[-3])  # 5분봉 D-2
                data.append(b[-4])  # 5분봉 D-3
                if (
                    float(data[4][4]) > float(data[4][1])
                    and float(data[3][4]) > float(data[3][1])
                    and float(data[2][4]) > float(data[2][1])
                    and float(data[0]) > (float(data[1]) * 1.08)
                ):
                    # unit = (today_USDT / binance.fetch_ticker(tickers[i])['close']) * 0.1
                    unit = (today_USDT / a[-1][-4]) * 0.1
                    # order = binance.create_market_buy_order(tickers[i], unit)
                    print("매수(5m)" + tickers[i], a[-1][4])
                    # info_price.append(order['price']) // 실제 거래
                    info_price.append(a[-1][4])  # // 테스트 거래
                    info_ticker.append(tickers[i])
            except:
                print("", end="", flush=True)
        tickers = [i for i in tickers if i not in set(info_ticker)]
        if len(info_ticker) == 0:
            continue
        else:
            for i in range(len(info_ticker)):
                if (
                    binance.fetch_ticker(info_ticker[i])["close"] > info_price[i] * 1.09
                    or binance.fetch_ticker(info_ticker[i])["close"]
                    < info_price[i] * 0.975
                ):
                    # order = binance.create_market_sell_order(info_ticker[0], balance[info_ticker[0][0:-5]]['free'])
                    print(
                        "매도(5m)" + info_ticker[i],
                        binance.fetch_ticker(info_ticker[i])["close"],
                    )
                    temp_price.append(info_price[i])
                    temp_ticker.append(info_ticker[i])
            info_ticker = [i for i in info_ticker if i not in set(temp_ticker)]
            info_price = [i for i in info_price if i not in set(temp_price)]

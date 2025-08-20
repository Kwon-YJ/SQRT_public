# -*- coding: utf-8 -*-
import ccxt
import time
import datetime
import pybithumb


exchange_class = getattr(ccxt, "bithumb")
bithumb2 = exchange_class()
bithumb2.enableRateLimit = True
bithumb2.RateLimit = 10000
bithumb2.apiKey = "06a2eaefc7956173bbd9f7b47c850786"
bithumb2.secret = "322d44201a7894e3cc2c64cadad673c0"
bithumb2.load_markets()


con_key = "06a2eaefc7956173bbd9f7b47c850786"
sec_key = "322d44201a7894e3cc2c64cadad673c0"
bithumb = pybithumb.Bithumb(con_key, sec_key)


ticker_list = pybithumb.get_tickers()


# IBS = close - low / high - low

day = 0


for i, item in enumerate(ticker_list):
    try:
        time.sleep(1)
        ohlcv = pybithumb.get_candlestick(item).tail(day + 1).iloc[0]
        temp = round((float(ohlcv["high"] / ohlcv["open"] - 1)) * 100, 3)

        if temp < 19.9:
            continue

        IBS0618 = 0.618 * float(ohlcv["high"]) + 0.382 * float(ohlcv["low"])
        IBS05 = 0.5 * (float(ohlcv["high"]) + float(ohlcv["low"]))
        IBS0382 = 0.382 * float(ohlcv["high"]) + 0.618 * float(ohlcv["low"])

        print(item)
        print("상승률 :", temp)
        print("IBS0.6 :", IBS0618)
        print("IBS0.5 :", IBS05)
        print("IBS0.382 :", IBS0382)

        print("")
    except:
        print(item, "에러")
        continue

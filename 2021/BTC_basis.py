# -*- coding: utf-8 -*-
import ccxt
import time
import pandas as pd
import numpy as np

# import matplotlib as plt
from matplotlib import pyplot as plt


def get_tickers():
    base_ticker = list(binance.fetch_tickers().keys())
    base_ticker = [
        base_ticker[i] for i in range(len(base_ticker)) if "/USDT" in base_ticker[i]
    ]
    base_ticker.remove("BTCDOM/USDT")
    return base_ticker


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
            if IBS < 0.1:
                return item
    except Exception as e:
        print(item)
        print(e)
        time.sleep(0.1)
        return None
    return None


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


def get_coin_m(ticker_name):
    binance = ccxt.binance(
        {
            "options": {"defaultType": "delivery"},
            "timeout": 30000,
            "apiKey": "bOHcvOmxqFVGN6FPsJwcnh4QOxw0D6oaFGHjEhpU2pby1bt7EJDb6t9TExauOccU",
            "secret": "Yece0g5APcAZR4sXJl1M007tLL9w9bB7Qp2o3fGFYJjN3f6tfx6lOCq1LdmRk4Ob",
            "enableRateLimit": False,
        }
    )
    binance.load_markets()

    result = binance.fetch_ohlcv(ticker_name, time_frame, None, limit_count)
    return result


# base_ticker = list(binance.fetch_tickers().keys())
# print(base_ticker)


result = []

limit_count = 188  # 31 == day

time_frame = "4h"

denominator = binance.fetch_ohlcv("BTCUSDT_211231", time_frame, None, limit_count)
numerator = binance.fetch_ohlcv("BTCUSDT", time_frame, None, limit_count)


# denominator = binance.fetch_ohlcv('ETHUSDT_211231', time_frame, None, limit_count)
# numerator = binance.fetch_ohlcv('ETHUSDT', time_frame, None, limit_count)

print(denominator[0][0])

# denominator = get_coin_m('BTC/USD')
# numerator = binance.fetch_ohlcv('BTCUSDT', time_frame, None, limit_count)


print(len(denominator), len(numerator))

for i in range(len(denominator)):
    gap = numerator[i][4] / denominator[i][4]
    result.append(round(gap, 3))

print(result)


plt.plot(result)
plt.savefig("test123.png", dpi=300)

exit()

# -*- coding: utf-8 -*-
import ccxt
import time
from matplotlib import pyplot as plt


def get_ETH_ETC_spread():
    timeframe = "1m"
    ETH_ohlcv = binance.fetch_ohlcv("ETH/USDT", timeframe)
    ETC_ohlcv = binance.fetch_ohlcv("ETC/USDT", timeframe)

    spread = [ETH_ohlcv[i][4] / ETC_ohlcv[i][4] for i in range(500)]
    # 스토캐스틱N = (현재 가격 - N일중 최저가)/(N일중 최고가 - N일중 최저가)
    spread_stochastic = [
        (spread[i] - min(spread)) / (max(spread) - min(spread)) for i in range(500)
    ]
    plt.plot(spread_stochastic)
    plt.show()
    # return spread_stochastic[-1]


exchange_class = getattr(ccxt, "binance")
binance = exchange_class(
    {
        "urls": {
            "api": {
                "public": "https://fapi.binance.com/fapi/v1",
                "private": "https://fapi.binance.com/fapi/v1",
            },
        }
    }
)
binance.enableRateLimit = True
binance.RateLimit = 10000
binance.apiKey = "FRbVseExyAWjQUtYFnS4memLnPCcgNAeRW7HEBrrw9qyIyPUMCTzUKxZKOJIHcfV"
binance.secret = "CbDX3DE5r9ErdLBOphDB4rjCaAaKbUqITbNK05YIitktZ24VfcNrvVRbIgfK6L87"
binance.load_markets()


get_ETH_ETC_spread()

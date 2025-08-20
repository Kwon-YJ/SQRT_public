# -*- coding: utf-8 -*-
import ccxt
import time


def get_ETH_ETC_spread():
    timeframe = "1m"
    ETH_ohlcv = binance.fetch_ohlcv("ETH/USDT", timeframe)
    ETC_ohlcv = binance.fetch_ohlcv("ETC/USDT", timeframe)
    spread = [ETH_ohlcv[i][4] / ETC_ohlcv[i][4] for i in range(500)]
    # 스토캐스틱N = (현재 가격 - N일중 최저가)/(N일중 최고가 - N일중 최저가)
    spread_stochastic = [
        (spread[i] - min(spread)) / (max(spread) - min(spread)) for i in range(500)
    ]
    return spread_stochastic[-1]


def order():
    if mode_switch == True:
        ETH_side = "buy"
        ETC_side = "sell"
    else:
        ETH_side = "sell"
        ETC_side = "buy"

    if len(amount) == 0:
        # ETH_amount = round(wallet_balance / binance.fetch_ohlcv("ETH/USDT")[-1][-4] * 9, 2)
        # ETC_amount = round(wallet_balance / binance.fetch_ohlcv("ETC/USDT")[-1][-4] * 9, 3)
        ETH_amount = round(
            wallet_balance / binance.fetch_ohlcv("ETH/USDT")[-1][-4] * 0.3, 2
        )
        ETC_amount = round(
            wallet_balance / binance.fetch_ohlcv("ETC/USDT")[-1][-4] * 0.3, 3
        )
        amount.append(ETH_amount)
        amount.append(ETC_amount)
    else:
        ETH_amount = amount[0] * 2
        ETC_amount = amount[1] * 2

    # binance.create_order('ETH/USDT' , 'market', ETH_side, ETH_amount, None, {'leverage': 23})
    # binance.create_order('ETC/USDT', 'market', ETC_side, ETC_amount, None, {'leverage': 23})
    binance.create_order(
        "ETH/USDT", "market", ETH_side, ETH_amount, None, {"leverage": 4}
    )
    binance.create_order(
        "ETC/USDT", "market", ETC_side, ETC_amount, None, {"leverage": 4}
    )

    time.sleep(60)


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

wallet_balance = float(binance.fetch_balance()["info"]["assets"][1]["walletBalance"])
amount = []

data = get_ETH_ETC_spread()
if data > 0.5:
    mode_switch = False
    order()
    mode_switch = True
else:
    mode_switch = True
    order()
    mode_switch = False

while 1:
    data = get_ETH_ETC_spread()

    if data == 1 and mode_switch == False:
        order()
        mode_switch = True

    elif data == 0 and mode_switch == True:
        order()
        mode_switch = False

    time.sleep(30)

# $409

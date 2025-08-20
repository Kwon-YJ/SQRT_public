# -*- coding: utf-8 -*-
import ccxt
import time
import datetime


def Bitmex_time_parameter():
    temp_time = str(
        datetime.datetime.now()
        - datetime.timedelta(minutes=100)
        - datetime.timedelta(hours=9)
    )
    convert = temp_time[:10] + "T" + temp_time[11:19]
    timestamp = bitmex.parse8601(convert)
    return timestamp


def get_BTC_XBT_spread():
    timeframe = "1h"
    XBT_ohlcv = bitmex.fetch_ohlcv("BTC/USD", timeframe, Bitmex_time_parameter())
    BTC_ohlcv = binance.fetch_ohlcv("BTC/USDT", timeframe)
    return BTC_ohlcv[-1][4] - XBT_ohlcv[-1][4]


def order():
    XBT_amount = 102
    BTC_amount = 0.006
    if mode_switch == False:
        BTC_side = "buy"
        XBT_side = "sell"
    else:
        BTC_side = "sell"
        XBT_side = "buy"

    if is_first_trade == False:
        BTC_amount = BTC_amount * 2
    binance.create_order(
        "BTC/USDT", "market", BTC_side, BTC_amount, None, {"leverage": 3}
    )
    bitmex.create_order(
        "BTC/USD", "market", XBT_side, XBT_amount, None, {"leverage": 3}
    )
    time.sleep(3)


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


bitmex = ccxt.bitmex(
    {
        "apiKey": "3pFJ5lblk8ff8brlz2plOG2o",
        "secret": "KKFk0a-YvtW8aEcS33HbQlxJ63rHpdA95D7IWNALSOTVraB1",
        "enableRateLimit": True,
        "RateLimit": 10000,
    }
)
bitmex.load_markets()
"""

bitmex = ccxt.bitmex({
    'apiKey': 'qlMFMLdQ7t2K7C4syVWS4Ia_',
    'secret': 'CHAfO5s1qzAdgImnTxiGZHq07t3jc9HTs-g50KiHPGDY6xS8',
})
if 'test' in bitmex.urls:
    bitmex.urls['api'] = bitmex.urls['test'] # ←----- switch the base URL to testnet
bitmex.load_markets()
"""

# bitmex case : x2 short or noting
# binance case : x1 long or 1x short

mode_switch = False
is_first_trade = True

XBT_amount = 102
BTC_amount = 0.006

params = {"execInst": "ParticipateDoNotInitiate", "leverage": 3}


while 1:
    data = get_BTC_XBT_spread()
    if data < 2 and mode_switch == False:
        BTC_side = "buy"
        XBT_side = "sell"
        price = bitmex.fetch_order_book("BTC/USD")["asks"][0][0]
        order = bitmex.create_order(
            "BTC/USD", "limit", XBT_side, XBT_amount, price, params
        )
        time.sleep(7)
        state = bitmex.fetch_order_status(order["info"]["orderID"])
        if state == "closed":
            if is_first_trade == False:
                BTC_amount = BTC_amount * 2
            binance.create_order(
                "BTC/USDT", "market", BTC_side, BTC_amount, None, {"leverage": 3}
            )
            mode_switch = True
            is_first_trade = False
        elif state != "canceled":
            bitmex.cancel_order(order["info"]["orderID"], "BTC/USDT")

    elif data > 6 and mode_switch == True:
        BTC_side = "sell"
        XBT_side = "buy"
        price = bitmex.fetch_order_book("BTC/USD")["bids"][0][0]
        time.sleep(7)
        order = bitmex.create_order(
            "BTC/USD", "limit", XBT_side, XBT_amount, price, params
        )
        state = bitmex.fetch_order_status(order["info"]["orderID"])
        if state == "closed":
            if is_first_trade == False:
                BTC_amount = BTC_amount * 2
                binance.create_order(
                    "BTC/USDT", "market", BTC_side, BTC_amount, None, {"leverage": 3}
                )
            mode_switch = False
            is_first_trade = False
        elif state != "canceled":
            bitmex.cancel_order(order["info"]["orderID"], "BTC/USDT")
    time.sleep(1.5)

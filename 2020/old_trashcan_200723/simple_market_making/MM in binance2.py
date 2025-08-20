# -*- coding: utf-8 -*-
import ccxt
import time
import telegram

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


symbol = "ETH/USDT"
size = 1


while True:
    try:
        binance.enableRateLimit = True
        binance.RateLimit = 10000
        binance.apiKey = (
            "FRbVseExyAWjQUtYFnS4memLnPCcgNAeRW7HEBrrw9qyIyPUMCTzUKxZKOJIHcfV"
        )
        binance.secret = (
            "CbDX3DE5r9ErdLBOphDB4rjCaAaKbUqITbNK05YIitktZ24VfcNrvVRbIgfK6L87"
        )
        binance.load_markets()
        bot = telegram.Bot(token=my_token)
        time.sleep(0.1)

        data = binance.fetch_order_book(symbol)
        target_ask = data["asks"][3][0]
        target_bid = data["bids"][2][0]
        PNL = target_ask / target_bid * 0.9998 * 0.9998  # BNB 할인 시 0.99982
        if PNL > 1:
            order2 = binance.create_order(
                symbol, "limit", "buy", size, target_bid, {"leverage": 25}
            )
            order1 = binance.create_order(
                symbol, "limit", "sell", size, target_ask, {"leverage": 25}
            )
            time.sleep(144)
    except Exception as ex:
        bot.send_message(chat_id=801167350, text=str(ex))
        continue

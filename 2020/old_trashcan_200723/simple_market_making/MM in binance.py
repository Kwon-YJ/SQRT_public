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


symbol = "XRP/USDT"
size = 100


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
        time.sleep(2)

        data = binance.fetch_order_book(symbol)
        target_ask = data["asks"][1][0]
        target_bid = data["bids"][1][0]
        PNL = target_ask / target_bid * 0.99964 * 0.99982
        if PNL > 1:
            order2 = binance.create_order(
                symbol, "limit", "buy", size, target_bid, {"leverage": 11}
            )
            order1 = binance.create_order(
                symbol, "limit", "sell", size, target_ask, {"leverage": 11}
            )
            time.sleep(144)
    except Exception as ex:
        bot.send_message(chat_id=801167350, text=str(ex))
        continue

"""


while(True):

	binance.enableRateLimit = True
	binance.RateLimit = 10000
	binance.apiKey = "FRbVseExyAWjQUtYFnS4memLnPCcgNAeRW7HEBrrw9qyIyPUMCTzUKxZKOJIHcfV"
	binance.secret = "CbDX3DE5r9ErdLBOphDB4rjCaAaKbUqITbNK05YIitktZ24VfcNrvVRbIgfK6L87"
	binance.load_markets()
	bot = telegram.Bot(token = my_token)
	time.sleep(2)
	
	data = binance.fetch_order_book(symbol)
	data2 = binance.fetch_order_book("ETH/USDT")
	target_ask = data['asks'][1][0]
	target_bid = data['bids'][1][0]

	ta2 = data2['asks'][4][0]
	tb2 = data2['bids'][4][0]

	PNL = target_ask / target_bid * 0.99964 * 0.99982
	PNL2 = ta2 / tb2 * 0.99964 * 0.99982

	print(PNL, 'XRP')
	print(PNL2, 'ETH')

"""

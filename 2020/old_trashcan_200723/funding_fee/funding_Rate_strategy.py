# -*- coding: utf-8 -*-
import urllib.request
from pprint import pprint
import json
import time
import ccxt


def get_decimal(ticker):
    Group_14 = ["XRP/USDT", "ONT/USDT", "IOTA/USDT", "BAT/USDT"]
    Group_13 = ["EOS/USDT", "XTZ/USDT", "QTUM/USDT"]
    Group_05 = ["TRX/USDT", "XLM/USDT", "ADA/USDT"]
    Group_06 = ["VET/USDT", "IOST/USDT"]

    if any(ticker in i for i in Group_14):
        return 1, 4
    elif any(ticker in i for i in Group_13):
        return 1, 3
    elif any(ticker in i for i in Group_05):
        return 0, 5
    elif any(ticker in i for i in Group_06):
        return 0, 6
    elif ticker == "LINK/USDT":
        return 2, 3
    else:
        return 3, 2


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


# 절대값이 가장 큰 한 종목을 찾아내서
# 그 종목을 펀딩피가 지급되기 15초 전에 시장가로 진입 한 뒤 펀딩피 지급 5초 후 지정가로 청산(거래 비용만큼 지정가를 높여서)
# 펀딩피 양수 = 롱 포지션이 숏포지션에게 지급 (숏이 받음)
# 펀딩피 음수 = 숏 포지션이 롱 포지션에게 지급 (롱이 받음)

"""
while(True):
	time.sleep(3)
	
	url = 'https://fapi.binance.com/fapi/v1/premiumIndex'
	text_data = urllib.request.urlopen(url).read().decode('utf-8')
	tickers = json.loads(text_data)
	time_diff = (float(tickers[0]['nextFundingTime']) - float(tickers[0]['time']))/1000
	funding_rate = [abs(float(tickers[i]['lastFundingRate'])) for i in range(24)]
	best_ticker = [[tickers[i]['symbol'],tickers[i]['lastFundingRate']] for i, value in enumerate(funding_rate) if max(funding_rate) == value]
	if time_diff < 12:
		if float(best_ticker[0][1]) > 0:
			side1 = 'sell'
			side2 = 'buy'
		else:
			side1 = 'buy'
			side2 = 'sell'
		ticker_name = best_ticker[0][0][:-4]+'/'+best_ticker[0][0][-4:]
		wallet_balance = float(binance.fetch_balance()['info']['assets'][1]['walletBalance'])
		decimal_amount, decimal_price  = get_decimal(ticker_name)
		amount = round(wallet_balance / binance.fetch_ohlcv(ticker_name)[-1][-4] * 0.48, decimal_amount)
		
		order1 = binance.create_order(ticker_name, 'market', side1, amount, None, {'leverage': 1})
		time.sleep(3)

		price = round(binance.fetch_closed_orders(ticker_name)[-1]['average'] * 1.00058, decimal_price)
		time.sleep(12)
		
		order2 = binance.create_order(ticker_name, 'limit', side2, float(order1['amount']), price, {'leverage': 1})
"""

EndPoint = len(binance.fetch_tickers().keys())

"""
url = 'https://fapi.binance.com/fapi/v1/premiumIndex'
text_data = urllib.request.urlopen(url).read().decode('utf-8')
tickers = json.loads(text_data)
funding_rate = [abs(float(tickers[i]['lastFundingRate'])) for i in range(EndPoint)]
ticker_name = [tickers[i]['symbol'] for i in range(EndPoint)]
print(ticker_name)
print(funding_rate)




for i in range(EndPoint):
	temp[tickers[i]['symbol']] = abs(float(tickers[i]['lastFundingRate']))

print(temp)
"""


def get_funding_rate(ticker):
    ticker = ticker[:-5] + "USDT"
    EndPoint = len(binance.fetch_tickers().keys())
    url = "https://fapi.binance.com/fapi/v1/premiumIndex"
    text_data = urllib.request.urlopen(url).read().decode("utf-8")
    tickers = json.loads(text_data)
    All_funding_rate = {}
    for i in range(EndPoint):
        All_funding_rate[tickers[i]["symbol"]] = float(tickers[i]["lastFundingRate"])
    pprint(All_funding_rate)
    return All_funding_rate[ticker]


aa_ = get_funding_rate("BTC/USDT")

print(aa_ + 1000)

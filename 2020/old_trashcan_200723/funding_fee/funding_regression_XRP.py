# -*- coding: utf-8 -*-
import urllib.request
from pprint import pprint
import json
import time
import ccxt


def get_funding_rate(ticker):
    url = "https://fapi.binance.com/fapi/v1/premiumIndex"
    text_data = urllib.request.urlopen(url).read().decode("utf-8")
    All_tickers = json.loads(text_data)
    for i in range(len(All_tickers)):
        if All_tickers[i]["symbol"] == "XRPUSDT":
            result = float(All_tickers[i]["lastFundingRate"])
            return result


def get_time_diff():
    url = "https://fapi.binance.com/fapi/v1/premiumIndex"
    text_data = urllib.request.urlopen(url).read().decode("utf-8")
    All_tickers = json.loads(text_data)
    time_diff = (
        float(All_tickers[0]["nextFundingTime"]) - float(All_tickers[0]["time"])
    ) / 1000
    return time_diff


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

is_first_trade = True
last_FR = 0

while True:
    try:
        if is_first_trade == True:
            size = 10
        else:
            size = 20

        XRP_FR = get_funding_rate("XRPUSDT")
        time_diff = get_time_diff()

        if time_diff < 20:
            if XRP_FR > 0 and last_FR <= 0:
                side = "sell"
                binance.create_order(
                    "XRP/USDT", "market", side, size, None, {"leverage": 2}
                )
                last_FR = 1
                is_first_trade = False
            elif XRP_FR < 0 and last_FR >= 0:
                side = "buy"
                binance.create_order(
                    "XRP/USDT", "market", side, size, None, {"leverage": 2}
                )
                last_FR = -1
                is_first_trade = False

        time.sleep(3)
    except:
        time.sleep(6)
        continue

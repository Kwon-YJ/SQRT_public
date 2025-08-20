import enum
import time
import datetime
import ccxt
import urllib
import json

from numpy import DataSource

binance = ccxt.binance(
    {
        # "options": {"defaultType": "future"},
        "timeout": 30000,
        "apiKey": "f6LEy0POPdaukqwlrnC4KvJbGWkcXRfVmKbsPmFAaPlyL2Rytswf7ilTa3kAjnQh",
        "secret": "sLvrd7ZT6c49yZVlnFRhPvJcIg8z39S6dVwZcIfPhFueA5BAy5UpTT3ZbVZg9zA2",
        "enableRateLimit": True,
    }
)


# 빌트인 함수보다 훨씬 빠르게 ohlcv 얻기
def get_ohlcv(ticker="BTC/USDT", interval="1m", limit=200):
    try:
        temp = ticker.split("/")
        ticker = f"{temp[0]}{temp[1]}"
        url = f"https://api.binance.com/api/v3/klines?symbol={ticker}&interval={interval}&limit={str(limit)}"
        text_data = urllib.request.urlopen(url).read().decode("utf-8")
        result = json.loads(text_data)
    except Exception as e:
        # print(e, '\n', 'ccxt.base.errors.BadSymbol: binance does not have market symbol {0}'.format(ticker))
        return [[0]]
    result = [list(map(float, result[i])) for i in range(len(result))]
    return result


# 호가 스프레드 계산
def calc_spread(data):
    total = {}
    for ticker in data:
        temp = ticker.split("/")
        ticker = f"{temp[0]}{temp[1]}"
        url = f"https://api.binance.com/api/v3/depth?symbol={ticker}"
        text_data = urllib.request.urlopen(url).read().decode("utf-8")
        text_data = json.loads(text_data)
        b = float(text_data["bids"][0][0])
        c = float(text_data["asks"][0][0])
        total[f"{temp[0]}/{temp[1]}"] = c / b
    return total


# 신뢰 가능한 종목 얻기 : 평균 거래대금 하위 n퍼센트 절삭, 호가 갭 상위 20퍼 제외
def get_ticker_list(target="/USDT"):
    total = {}
    temp_list = list(binance.fetch_tickers().keys())
    # temp_list = [ticker for ticker in temp_list if '/ETH' in ticker or '/USDT' in ticker or '/BNB' in ticker or '/BTC' in ticker]
    temp_list = [ticker for ticker in temp_list if target in ticker]
    std_time_data = binance.fetch_ohlcv("BTC/USDT", "1d")[-1][0]
    dropout_delisting = [
        ticker
        for ticker in temp_list
        if get_ohlcv(ticker, "1d", 2)[-1][0] == std_time_data
    ]  # 상폐 종목 제외
    for i in range(len(dropout_delisting)):  # 전 종목 거래대금 구하기
        temp__ = get_ohlcv(dropout_delisting[i], "1h", 500)
        vol_temp = [item[5] for idx, item in enumerate(temp__)]
        avg_vol = sum(vol_temp) / len(vol_temp)
        market_type = dropout_delisting[i].split("/")[1]
        if market_type == "USDT":
            value_ = temp__[-1][4] * avg_vol
        else:
            price = get_ohlcv(market_type + "/USDT", "1h", 2)[-1][4]
            value_ = price * avg_vol
        total[dropout_delisting[i]] = value_

    sort_total = sorted(total.items(), key=lambda item: item[1])
    dropout_undervalue = sort_total[int(len(sort_total) * 0.1) :]  # 하위 10프로 제외
    temp_result = [dropout_undervalue[s][0] for s in range(len(dropout_undervalue))]
    get_spread = calc_spread(temp_result)
    result = sorted(get_spread.items(), key=lambda item: item[1])
    result = result[: int(len(result) * 0.5)]  # 상위 50프로 제외
    # aaaa = [result[s][1] for s in range(len(result))]
    # print(max(aaaa))
    # print(min(aaaa))
    # print(sum(aaaa)/len(aaaa))
    result = [result[s][0] for s in range(len(result))]

    return result


if __name__ == "__main__":
    a = get_ticker_list("/ETH")
    print(len(a))
    print(a)

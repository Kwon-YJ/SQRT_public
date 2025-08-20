import ccxt
import time
import urllib
import parmap
import ccxt
import json


# 호가 갭 계산
def calc_spread(data):
    total = {}
    # cdef float bids = 0.0
    # cdef float asks = 0.0
    for ticker in data:
        try:
            temp = ticker.split("/")
            ticker = f"{temp[0]}{temp[1]}"
            url = f"https://api.binance.com/api/v3/depth?symbol={ticker}"
            text_data = urllib.request.urlopen(url).read().decode("utf-8")
            text_data = json.loads(text_data)
            b = float(text_data["bids"][0][0])
            c = float(text_data["asks"][0][0])
            total[f"{temp[0]}/{temp[1]}"] = c / b
        except:
            # print(ticker, text_data)
            time.sleep(0.5)
            continue
    return total


# get_ticker_list() 의 상폐 종목 제외를 위한 '멀티'프로세싱용 서브 루틴
def discard_delisting(ticker):
    ohlcv = get_ohlcv(ticker, "1d", 30)
    if ohlcv[-1][0] == std_time_data and len(ohlcv) > 25:
        return ticker
    return None


# get_ticker_list() 의 상폐 종목 제외를 위한 '싱글'프로세싱용 서브 루틴
def discard_delisting_single(ticker):
    try:
        valid = binance.fetch_order_book(ticker)
        if len(valid["bids"]) == 100:
            return True
        else:
            return None
    except:
        return None


# 신뢰 가능한 종목 얻기 : 평균 거래대금 하위 10퍼센트 제외, 호가 갭 상위 50퍼센트 제외
def get_ticker_list(target="/USDT"):  # use only '/USDT', '/BTC', '/ETH', '/BNB'
    # cdef float avg_bol = 0.0
    # cdef float value_ = 0.0
    # cdef float price = 0.0
    # cdef int i = 0
    # cdef int s = 0

    total = {}
    temp_list = list(binance.fetch_tickers().keys())
    time.sleep(60)
    temp_list = [ticker for ticker in temp_list if target in ticker]
    # global std_time_data # 멀티프로세싱 참조 용 글로벌
    std_time_data = get_ohlcv("BTC/USDT", "1d", 2)[-1][0]
    # dropout_delisting = [ticker for ticker in temp_list if get_ohlcv(ticker, '1d', 2)[-1][0] == std_time_data] # 상폐 종목 제외 single
    dropout_delisting = [
        ticker for ticker in temp_list if discard_delisting_single(ticker) == True
    ]  # 상폐 종목 제외 single
    # dropout_delisting = parmap.map(discard_delisting, temp_list, pm_pbar=True, pm_processes = 4) # 상폐 종목 제외 multi
    # dropout_delisting = list(set(dropout_delisting) - set([None])) # 싱글 케이스는 이 곳을 주석 처리
    for i in range(len(dropout_delisting)):  # 전 종목 거래대금 구하기 루프
        temp__ = get_ohlcv(dropout_delisting[i], "1h", 500)
        # print(dropout_delisting[i],len(temp__))
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
    dropout_undervalue = sort_total[
        int(len(sort_total) * 0.1) :
    ]  # 거래대금 하위 10프로 제외
    temp_result = [dropout_undervalue[s][0] for s in range(len(dropout_undervalue))]
    get_spread = calc_spread(temp_result)
    result = sorted(get_spread.items(), key=lambda item: item[1])
    # result = result[:int(len(result) * 0.5)] # 호가 갭 상위 50프로 제외
    result = result[: int(len(result) * 0.8)]  # 호가 갭 상위 50프로 제외
    result = [result[s][0] for s in range(len(result))]
    return result


# ccxt ex.fetch_ohlcv() 보다 훨씬 빠르게 ohlcv 얻기
def get_ohlcv(ticker="BTC/USDT", interval="1m", limit=200):
    # cdef int i = 0
    try:
        temp = ticker.split("/")
        ticker = f"{temp[0]}{temp[1]}"
        url = f"https://api.binance.com/api/v3/klines?symbol={ticker}&interval={interval}&limit={str(limit)}"
        text_data = urllib.request.urlopen(url).read().decode("utf-8")
        result = json.loads(text_data)
    # except Exception as e:
    except:
        # print(e, '\n', 'ccxt.base.errors.BadSymbol: binance does not have market symbol {0}'.format(ticker))
        return [[0]]
    result = [list(map(float, result[i])) for i in range(len(result))]
    return result


binance = ccxt.binance(
    {
        # "options": {"defaultType": "future"},
        "timeout": 30000,
        # "apiKey":"",
        # "secret": "",
        "enableRateLimit": False,
    }
)
binance.load_markets()

if __name__ == "__main__":
    ticker_list = get_ticker_list("/BNB")
    print(ticker_list)

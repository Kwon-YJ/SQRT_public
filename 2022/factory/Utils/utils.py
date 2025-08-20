import ccxt
import time
import numpy as np

# import pandas as pd
import datetime

# import pandas_ta as ta
import urllib
import json
import telegram


upbit = ccxt.upbit(
    {
        "timeout": 30000,
        "apiKey": "xuTwrDh8DG0pXJNT0mGkkqFCA8kA7CA09QZ7qKMQ",
        "secret": "ntpBwLjtMCh9uA9W9CUKmyITQSgUL50xiJ5pti9Y",
        "enableRateLimit": True,
    }
)


bithumb = ccxt.bithumb(
    {
        "timeout": 30000,
        "apiKey": "6f0f6da344472cee0e78594a5e2e0cad",
        "secret": "b82826545009d1132a5de460e2bbad64",
        "enableRateLimit": True,
    }
)


def use_binance(options="spot"):
    if options == "test":
        binance = ccxt.binance(
            {
                "apiKey": "a8e1a769ccf507113fb84616f1999f34147f6d8ca4a4263ff0a37a9461b359ea",
                "secret": "605f78a26c51981f4a2bbac852661b538027be99924866dc28096efa7b36be01",
                "enableRateLimit": False,  # https://github.com/ccxt/ccxt/wiki/Manual#rate-limit
                "options": {
                    "defaultType": "future",
                },
            }
        )
        binance.set_sandbox_mode(True)  # comment if you're not using the testnet
    else:
        binance = ccxt.binance(
            {
                # "options": {"defaultType": "future"},
                "options": {"defaultType": options},
                "timeout": 30000,
                "apiKey": "bOHcvOmxqFVGN6FPsJwcnh4QOxw0D6oaFGHjEhpU2pby1bt7EJDb6t9TExauOccU",
                "secret": "Yece0g5APcAZR4sXJl1M007tLL9w9bB7Qp2o3fGFYJjN3f6tfx6lOCq1LdmRk4Ob",
                "enableRateLimit": False,
            }
        )
    binance.load_markets()
    return binance


def get_tickers():
    result = []
    binance = use_binance("future")
    base_ticker = list(binance.fetch_tickers().keys())
    base_ticker = [
        base_ticker[i] for i in range(len(base_ticker)) if "/USDT" in base_ticker[i]
    ]
    time.sleep(60)
    for ticker in base_ticker:
        try:
            order_book = binance.fetch_order_book(ticker)
            result.append(ticker)
        except:
            continue
    return result


def get_time():
    now = datetime.datetime.now()
    YYYY = str(now.year)
    MM = str(now.month)
    DD = str(now.day)
    hh = str(now.hour)
    mm = str(now.minute)

    if len(MM) != 2:
        MM = "0" + MM
    if len(DD) != 2:
        DD = "0" + DD
    if len(hh) != 2:
        hh = "0" + hh
    if len(mm) != 2:
        mm = "0" + mm

    return YYYY + MM + DD, hh + mm


def timestamp_to_datetime(timestamp):
    datetimeobj = datetime.datetime.fromtimestamp(timestamp / 1000)
    original_time_data = str(datetimeobj)
    entry_time_data = str(datetimeobj)[11:-3]
    exit_time_data = str(datetimeobj)[5:-3]
    return entry_time_data, exit_time_data, original_time_data


# 업비트 KRW 가격 순 정렬
def get_ticekrs_upbit():
    tickers = list(upbit.fetch_tickers().keys())
    tickers = [tickers[s] for s in range(len(tickers)) if "/KRW" in tickers[s]]
    ticekrs_with_price = []
    for ticker in tickers:
        currency_price = upbit.fetch_ohlcv(ticker)[-1][4]
        ticekrs_with_price.append([ticker, currency_price])
    price = [ticekrs_with_price[i][1] for i in range(len(ticekrs_with_price))]
    result = []
    while len(price) != 0:
        max_price = max(price)
        for i in range(len(ticekrs_with_price)):
            if max_price == ticekrs_with_price[i][1]:
                result.append(ticekrs_with_price[i][0])
                price.remove(max_price)
    return result


def custom_convert(ohlcv5):  # convert 5m → 15m
    # if len(ohlcv5) < 2000:
    #     return None
    if len(ohlcv5) == 0:
        return None
    ohlcv15 = []
    temp = str(datetime.datetime.fromtimestamp(ohlcv5[0][0] / 1000))[14:16]
    if int(temp) % 15 == 5:
        del ohlcv5[0]
        del ohlcv5[1]
    elif int(temp) % 15 == 10:
        del ohlcv5[0]
    for i in range(0, len(ohlcv5) - 2, 3):
        highs = [ohlcv5[i + j][2] for j in range(0, 3) if ohlcv5[i + j][2]]
        lows = [ohlcv5[i + j][3] for j in range(0, 3) if ohlcv5[i + j][3]]
        candle = [
            ohlcv5[i + 0][0],
            ohlcv5[i + 0][1],
            max(highs) if len(highs) else None,
            min(lows) if len(lows) else None,
            ohlcv5[i + 2][4],
            ohlcv5[i][5] + ohlcv5[i + 1][5] + ohlcv5[i + 2][5],
        ]
        ohlcv15.append(candle)
    return ohlcv15


def TW(odd):
    return np.round(-np.log(0.99) / (np.log(1 + 0.01 * odd) - np.log(0.99)), 4)


def shortest_distance(odd, winrate, n=100000):
    lins = np.linspace(0, 10, n)
    y = TW(lins)
    least_distance = 1e100
    for i in range(n):
        dx = lins[i] - odd
        dy = y[i] - winrate
        distance = np.sqrt(dx**2 + dy**2)
        if distance < least_distance:
            least_distance = distance
    if winrate > TW(odd):
        return np.round(least_distance, 10)
    else:
        return -1 * np.round(least_distance, 10)


"""
def get_perfomance(trade_log):
    if len(trade_log) == 0:
        return None
    win = []
    lose = []
    risk_free = 0.038 / 365
    avg = np.mean(trade_log)
    std = np.std(trade_log)

    for i in range(len(trade_log)):
        if trade_log[i] > 0:
            win.append(trade_log[i])
        elif trade_log[i] < 0:
            lose.append(trade_log[i])

    avg_W_L_ratio = -1 * np.mean(win) / np.mean(lose)
    total_perform = shortest_distance(avg_W_L_ratio, len(win) / len(trade_log))
    # total_perform = Utils.shortest_distance(avg_W_L_ratio, len(win) / len(trade_log))
    size = (avg - risk_free) / (std * std)
    print('총거래 : ', len(trade_log))
    print('수익거래수 :', len(win))
    print('손실거래수 :', len(lose))
    print('평균거래 :',avg)
    print('평균수익거래 :', np.mean(win))
    print('평균손실거래 :', np.mean(lose))
    print('평균손익비 :', avg_W_L_ratio)
    win_rate = int(round(len(win) / len(trade_log),2) * 100)
    print('승률 :',win_rate , '%')
    print('포지션 사이징 :', size)
    if len(lose) > 0:
        print('최대 손실 :', min(lose))
    print(total_perform)
    print('')
"""


# ccxt ex.fetch_ohlcv() 보다 훨씬 빠르게 ohlcv 얻기
def get_ohlcv(ticker="BTC/USDT", interval="1m", limit=200):
    try:
        temp = ticker.split("/")
        ticker = f"{temp[0]}{temp[1]}"
        # url = f'https://fapi.binance.com/fapi/v1/klines?symbol={ticker}&interval={interval}&limit={str(limit)}' # monitoring
        url = f"https://api.binance.com/api/v3/klines?symbol={ticker}&interval={interval}&limit={str(limit)}"
        text_data = urllib.request.urlopen(url).read().decode("utf-8")
        output = json.loads(text_data)
    except Exception as e:
        # print(e)
        time.sleep(0.5)
        return None
    output = [list(map(float, output[i])) for i in range(len(output))]
    return output


def telegram_send(data):
    bot = telegram.Bot(token=my_token)
    if type(data) != "str":
        data = str(data)
    while 1:
        try:
            bot.send_message(chat_id=801167350, text=data)
            time.sleep(3)
            return None
        except:
            continue


"""
# 신뢰 가능한 종목 얻기 : 평균 거래대금 하위 n퍼센트 절삭, 호가 갭 상위 20퍼 제외 
def get_ticker_list(target = '/USDT'):
    total = {}
    temp_list = list(binance.fetch_tickers().keys())
    # temp_list = [ticker for ticker in temp_list if '/ETH' in ticker or '/USDT' in ticker or '/BNB' in ticker or '/BTC' in ticker]
    temp_list = [ticker for ticker in temp_list if target in ticker]
    global std_time_data # 멀티프로세싱 용
    std_time_data = get_ohlcv('BTC/USDT', '1d', 2)[-1][0]
    # dropout_delisting = [ticker for ticker in temp_list if get_ohlcv(ticker, '1d', 2)[-1][0] == std_time_data] # 상폐 종목 제외 single
    dropout_delisting = parmap.map(discard_delisting, temp_list, pm_pbar=True, pm_processes=num_cores) # 상폐 종목 제외 multi
    dropout_delisting = list(set(dropout_delisting) - set([None]))
    for i in range(len(dropout_delisting)): # 전 종목 거래대금 구하기
        temp__ = get_ohlcv(dropout_delisting[i], '1h', 500)
        vol_temp = [item[5] for idx, item in enumerate(temp__)]
        avg_vol = sum(vol_temp) / len(vol_temp)
        market_type = dropout_delisting[i].split('/')[1]
        if market_type == 'USDT':
            value_ = temp__[-1][4] * avg_vol
        else:
            price = get_ohlcv(market_type + '/USDT', '1h', 2)[-1][4]
            value_ = price * avg_vol
        total[dropout_delisting[i]] = value_
    sort_total = sorted(total.items(), key = lambda item: item[1])
    dropout_undervalue = sort_total[int(len(sort_total) * 0.1):] # 거래대금 하위 10프로 제외
    temp_result = [dropout_undervalue[s][0] for s in range(len(dropout_undervalue))]
    get_spread = calc_spread(temp_result)
    result = sorted(get_spread.items(), key = lambda item: item[1])
    result = result[:int(len(result) * 0.5)] # 호가 갭 상위 50프로 제외
    result = [result[s][0] for s in range(len(result))]
    return result
"""

import time
import telegram
import datetime
import ccxt
import urllib
import json

binance = ccxt.binance(
    {
        # "options": {"defaultType": "future"},
        "timeout": 30000,
        "apiKey": "f6LEy0POPdaukqwlrnC4KvJbGWkcXRfVmKbsPmFAaPlyL2Rytswf7ilTa3kAjnQh",
        "secret": "sLvrd7ZT6c49yZVlnFRhPvJcIg8z39S6dVwZcIfPhFueA5BAy5UpTT3ZbVZg9zA2",
        "enableRateLimit": True,
    }
)

"""
# 빌트인 함수보다 훨씬 빠르게 ohlcv 얻기
def get_ohlcv(ticker='BTC/USDT', interval='1m', limit=200, default = 'futures'):
    try:
        ticker = ticker[:-5] + 'USDT'
        if default == 'futures':
            url = 'https://fapi.binance.com/fapi/v1/klines?symbol={0}&interval={1}&limit={2}'.format(ticker, interval, str(limit))
        else:
            url = 'https://api.binance.com/api/v3/klines?symbol={0}&interval={1}&limit={2}'.format(ticker, interval, str(limit))
        text_data = urllib.request.urlopen(url).read().decode('utf-8')
        result = json.loads(text_data)
    except Exception as e:
        time.sleep(0.2)
        print(e)
        print('ccxt.base.errors.BadSymbol: binance does not have market symbol {0}'.format(ticker))
        exit()
    result = [list(map(float,result[i])) for i in range(len(result))]
    return result
"""


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


# 신뢰 가능한 종목 얻기 : 평균 거래대금 하위 n퍼센트 절삭, 호가 갭 상위 20퍼 제외
def get_ticker_list(target="/USDT"):
    total = {}
    temp_list = list(binance.fetch_tickers().keys())
    # temp_list = [ticker for ticker in temp_list if '/ETH' in ticker or '/USDT' in ticker or '/BNB' in ticker or '/BTC' in ticker]
    temp_list = [ticker for ticker in temp_list if target in ticker]
    global std_time_data  # 멀티프로세싱 용
    std_time_data = get_ohlcv("BTC/USDT", "1d", 2)[-1][0]
    # dropout_delisting = [ticker for ticker in temp_list if get_ohlcv(ticker, '1d', 2)[-1][0] == std_time_data] # 상폐 종목 제외 single
    dropout_delisting = parmap.map(
        discard_delisting, temp_list, pm_pbar=True, pm_processes=num_cores
    )  # 상폐 종목 제외 multi
    dropout_delisting = list(set(dropout_delisting) - set([None]))
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
    dropout_undervalue = sort_total[
        int(len(sort_total) * 0.1) :
    ]  # 거래대금 하위 10프로 제외
    temp_result = [dropout_undervalue[s][0] for s in range(len(dropout_undervalue))]
    get_spread = calc_spread(temp_result)
    result = sorted(get_spread.items(), key=lambda item: item[1])
    result = result[: int(len(result) * 0.5)]  # 호가 갭 상위 50프로 제외
    result = [result[s][0] for s in range(len(result))]
    return result


# API 적힌 텍스트 파일 읽어오기 (API.txt)
def get_API():
    f = open("./API.txt", "r")
    public = f.readline()
    secret = f.readline()
    f.close()
    return public[:-1], secret[:-1]


# 현물 시장에서 거래 가능한 소숫점 임계 구하기
def get_dec(ticker):
    temp = binance.fetch_order_book(ticker)["bids"][0][1]
    result = str(temp).split(".")
    if len(result[1]) == 1:
        return 0
    else:
        return len(result[1])


# 충돌없이 무조건 메시지 보내기
def send_MSG(message):
    bot = telegram.Bot(token=my_token)
    while True:
        try:
            bot.send_message(chat_id=801167350, text=str(message))
            time.sleep(3)
            return None
        except Exception as e:
            print(e)
            time.sleep(3)
            continue


# get_time()[0] = 오늘 날짜 str
# get_time()[1] = 현재 시각 str
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


# ccxt 전용 5분봉 3개를 합쳐 15분봉으로 바꿔주는 함수
def custom_convert(ohlcv5):  # convert 5m → 15m
    time_mm = get_time()[1][2:]
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
        ]
        ohlcv15.append(candle)
    div_case = str(int(time_mm) // 5)
    # print(div_case)
    safe_case = ["2", "5", "8", "11"]
    add_one_case = ["0", "3", "6", "9"]
    add_two_case = ["1", "4", "7", "10"]
    if any(div_case in idx for idx in safe_case):
        # print('safe_case')
        return ohlcv15
    elif any(div_case in idx for idx in add_one_case):
        # print('add_one_case')
        temp = [
            ohlcv5[-1][0],
            ohlcv5[-1][1],
            ohlcv5[-1][2],
            ohlcv5[-1][3],
            ohlcv5[-1][4],
        ]
        ohlcv15.append(temp)
        return ohlcv15
    elif any(div_case in idx for idx in add_two_case):
        # print('add_two_case')
        temp = [
            ohlcv5[-2][0],
            ohlcv5[-2][1],
            max(ohlcv5[-2][2], ohlcv5[-1][2]),
            min(ohlcv5[-2][3], ohlcv5[-1][3]),
            ohlcv5[-1][4],
        ]  # , sum(ohlcv5[-2][5], ohlcv5[-1][5])
        ohlcv15.append(temp)
        return ohlcv15


def get_volume_based_chart(target_ohlcv):
    target_V = [target_ohlcv[i][5] for i in range(len(target_ohlcv))]
    V_threshold = max(target_V) * 1.5
    result = []
    step = 0
    while True:
        try:
            V_value = 0
            lenght_ = 0
            for lenght_ in range(len(target_V)):
                V_value += target_V[lenght_ + step]
                if V_value > V_threshold:
                    break
            highs = [
                target_ohlcv[step + j][2]
                for j in range(0, lenght_)
                if target_ohlcv[step + j][2]
            ]
            lows = [
                target_ohlcv[step + j][3]
                for j in range(0, 3)
                if target_ohlcv[step + j][3]
            ]
            candle = [
                target_ohlcv[step][0],
                target_ohlcv[step][1],
                max(highs) if len(highs) else None,
                min(lows) if len(lows) else None,
                target_ohlcv[lenght_ + step][4],
                V_value,
            ]
            result.append(candle)
            step += lenght_
        except:
            highs = []
            lows = []
            V_value = []
            for i in range(1, lenght_ + 1):
                highs.append(target_ohlcv[-i][2])
                lows.append(target_ohlcv[-i][3])
                V_value.append(target_ohlcv[-i][5])
            candle = [
                target_ohlcv[-lenght_][0],
                target_ohlcv[-lenght_][1],
                max(highs),
                min(lows),
                target_ohlcv[-1][4],
                sum(V_value),
            ]
            result.append(candle)
            break
        return result


def timestamp_to_datetime(timestamp):
    datetimeobj = datetime.datetime.fromtimestamp(timestamp / 1000)
    original_time_data = str(datetimeobj)
    entry_time_data = str(datetimeobj)[11:-3]
    exit_time_data = str(datetimeobj)[5:-3]
    return entry_time_data, exit_time_data, original_time_data


""" 
# not used
# 볼린저 밴드 상단, 하단에 벗어나기위한 최소한의 가격변동 계산
def get_target_price(ohlcv, multiple):
    data = [ohlcv[i][4] for i in range(len(ohlcv))]
    data = pd.Series(data)
    result = []
    for i in range(100000):
        price = ohlcv[-1][4]
        temp_list = data
        temp_list[-1] = price - (price*i*0.0001)
        temp = tuple([data[-1]])
        mbb = data.rolling(20).mean()
        lbb = mbb - multiple * data.rolling(20).std()
        if temp[-1] < lbb.tolist()[-1]:
            result.append(temp[-1])
            break
    for i in range(100000):
        price = ohlcv[-1][4]
        temp_list = data
        temp_list[-1] = price + (price*i*0.0001)
        temp = tuple([data[-1]])
        mbb = data.rolling(20).mean()
        ubb = mbb + multiple * data.rolling(20).std()
        if temp[-1] > ubb.tolist()[-1]:
            result.append(temp[-1])
            break
    return result
"""

import ccxt
import json
import urllib
import datetime


binance = ccxt.binance(
    {
        "options": {"defaultType": "future"},
        "timeout": 30000,
        "apiKey": "f6LEy0POPdaukqwlrnC4KvJbGWkcXRfVmKbsPmFAaPlyL2Rytswf7ilTa3kAjnQh",
        "secret": "sLvrd7ZT6c49yZVlnFRhPvJcIg8z39S6dVwZcIfPhFueA5BAy5UpTT3ZbVZg9zA2",
        "enableRateLimit": False,
    }
)
binance.load_markets()


# ccxt ex.fetch_ohlcv() 보다 훨씬 빠르게 ohlcv 얻기
def get_ohlcv(ticker="BTC/USDT", interval="1m", limit=200):
    # cdef int i = 0
    try:
        temp = ticker.split("/")
        ticker = f"{temp[0]}{temp[1]}"
        # url = f'https://api.binance.com/api/v3/klines?symbol={ticker}&interval={interval}&limit={str(limit)}'
        # url = f'https://api.binance.com/api/v3/klines?symbol={ticker}&interval={interval}&startTime={startTime}&endTime={endTime}&limit={str(limit)}'
        # url = f'https://fapi.binance.com/fapi/v1/klines?symbol={ticker}&interval={interval}&startTime={startTime}&limit={str(limit)}'
        url = f"https://fapi.binance.com/fapi/v1/klines?symbol={ticker}&interval={interval}&limit={str(limit)}"
        text_data = urllib.request.urlopen(url).read().decode("utf-8")
        buy_sell_log = json.loads(text_data)
    # except Exception as e:
    except Exception as e:
        print(
            e,
            "\n",
            "ccxt.base.errors.BadSymbol: binance does not have market symbol {0}".format(
                ticker
            ),
        )
        # return [[0]]
        return None
    buy_sell_log = [list(map(float, buy_sell_log[i])) for i in range(len(buy_sell_log))]
    return buy_sell_log


target_ohlcv = get_ohlcv("BTC/USDT", "1m", 1000)
# target_ohlcv = binance.fetch_ohlcv('BTC/USDT', '1m')


########################################################################################
########################################################################################
########################################################################################


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


result = get_volume_based_chart(target_ohlcv)


print(result)
print(len(result))


print(timestamp_to_datetime(target_ohlcv[0][0]))
print("##########################")

for i in range(len(result)):
    print(timestamp_to_datetime(result[i][0])[2])
print("##########################")
"""
for i in range(len(result)):
    print(int(result[i][5]))
"""

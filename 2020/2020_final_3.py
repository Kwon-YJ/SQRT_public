import ccxt
import datetime
import time
import telegram


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

bot = telegram.Bot(token=my_token)

tickers = list(binance.fetch_tickers().keys())


idx = 1

while 1:
    result = []
    # if get_time()[1][2:] != '58':
    #    time.sleep(7)
    #    continue
    try:
        for i in range(len(tickers)):
            ohlcv = binance.fetch_ohlcv(tickers[i], "1h")
            open_ = ohlcv[-1 - idx][1]
            high_ = ohlcv[-1 - idx][2]
            low_ = ohlcv[-1 - idx][3]
            close_ = ohlcv[-1 - idx][4]
            if high_ - low_ == 0:
                print("pass")
                continue
            IBS = (close_ - low_) / (high_ - low_)
            if IBS < 0.07:
                trust_rate = abs(open_ - close_) / abs(high_ - low_)
                result.append([tickers[i], round(trust_rate, 2), "buy"])
            if IBS > 0.93:
                trust_rate = abs(open_ - close_) / abs(high_ - low_)
                result.append([tickers[i], round(trust_rate, 2), "sell"])
        bot.send_message(chat_id=801167350, text=str(result))
        time.sleep(60)
    except:
        print("err")
        time.sleep(1)
        continue

import ccxt
import time
import datetime
import telegram


def get_time(temp):
    now = temp
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


def get_futures_wallet_balance():
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

    binance.load_markets()

    # wallet_balance = float(binance.fetch_balance()['info']['assets'][1]['walletBalance'])
    # today_money_USDT = float(binance.fetch_balance()['info']['assets'][0]['walletBalance'])
    # return today_money_USDT
    wallet_data = binance.fetch_balance()["info"]["assets"]

    for data in wallet_data:
        if data["asset"] == "USDT":
            return data["availableBalance"]


def get_spot_wallet_balance():
    exchange_class = getattr(ccxt, "binance")
    binance = exchange_class()
    binance.enableRateLimit = True
    binance.RateLimit = 10000

    binance.load_markets()

    wallet_balance = binance.fetch_balance()["USDT"]["free"]
    return wallet_balance


bot = telegram.Bot(token=my_token)


futures = get_futures_wallet_balance()

print(futures)


exit()

while True:
    time.sleep(13)
    now = get_time(datetime.datetime.now())
    try:
        if now[1] == "0901":
            # spot = get_spot_wallet_balance()
            futures = get_futures_wallet_balance()
            # messege = ['spot : ', spot , 'futures : ', futures]
            messege = ["futures : ", futures]
            bot.send_message(chat_id=801167350, text=str(messege))
            time.sleep(120)
    except:
        time.sleep(1)
        continue

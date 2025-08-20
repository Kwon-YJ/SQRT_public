import ccxt
import datetime
import time
import telegram


def get_decimal(ticker):
    Group_14 = [
        "XRP/USDT",
        "ONT/USDT",
        "IOTA/USDT",
        "BAT/USDT",
        "LEND/USDT",
        "SXP/USDT",
        "OMG/USDT",
        "ZRX/USDT",
        "ALGO/USDT",
        "THETA/USDT",
        "KAVA/USDT",
        "BAND/USDT",
        "RLC/USDT",
        "WAVES/USDT",
    ]
    Group_13 = [
        "EOS/USDT",
        "XTZ/USDT",
        "QTUM/USDT",
        "SNX/USDT",
        "DOT/USDT",
        "BAL/USDT",
        "CRV/USDT",
        "TRB/USDT",
    ]
    Group_05 = [
        "TRX/USDT",
        "XLM/USDT",
        "ADA/USDT",
        "KNC/USDT",
        "ZIL/USDT",
        "RUNE/USDT",
        "SUSHI/USDT",
        "SRM/USDT",
        "BZRX/USDT",
    ]
    Group_06 = ["VET/USDT", "IOST/USDT", "DOGE/USDT"]

    if any(ticker in i for i in Group_14):
        return 1, 4
    elif any(ticker in i for i in Group_13):
        return 1, 3
    elif any(ticker in i for i in Group_05):
        return 0, 5
    elif any(ticker in i for i in Group_06):
        return 0, 6
    elif ticker == "LINK/USDT" or ticker == "COMP/USDT":
        return 2, 3
    elif ticker == "DEFI/USDT" or "YFI/USDT" or "YFII/USDT":
        return 3, 1
    else:  # MKR/USDT, others...
        return 3, 2


def get_amount(ticker):
    price = binance.fetch_ohlcv(ticker)[-1][4]
    today_money_USDT = float(
        binance.fetch_balance()["info"]["assets"][0]["walletBalance"]
    )
    decimal_amount = get_decimal(ticker)[0]
    result = round(today_money_USDT / price * 0.004, decimal_amount)
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


def convert(ohlcv5):  # convert 5m → 15m
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
        volumes = [ohlcv5[i + j][5] for j in range(0, 3) if ohlcv5[i + j][5]]
        candle = [
            ohlcv5[i + 0][0],
            ohlcv5[i + 0][1],
            max(highs) if len(highs) else None,
            min(lows) if len(lows) else None,
            ohlcv5[i + 2][4],
        ]
        ohlcv15.append(candle)
    return ohlcv15


def get_HA_ohlcv(ticker, time_frame):
    ohlcv = binance.fetch_ohlcv(ticker, time_frame)
    if time_frame == "15m":
        ohlcv = convert(binance.fetch_ohlcv(ticker, "5m"))

    ha_ohlcv = []
    for i in range(1, len(ohlcv)):
        if i == 1:
            ha_open = (ohlcv[i - 1][1] + ohlcv[i - 1][4]) / 2
        else:
            ha_open = (ha_ohlcv[i - 2][1] + ha_ohlcv[i - 2][4]) / 2
        timestamp = ohlcv[i][0]
        ha_close = (ohlcv[i][1] + ohlcv[i][2] + ohlcv[i][3] + ohlcv[i][4]) / 4
        ha_high = max(ohlcv[i][2], ha_close, ha_open)
        ha_low = min(ohlcv[i][3], ha_close, ha_open)
        ha_ohlcv.append(
            [
                timestamp,
                round(ha_open, 8),
                round(ha_high, 8),
                round(ha_low, 8),
                round(ha_close, 8),
            ]
        )
    return ha_ohlcv


def check_match(item):
    _15m_data = get_HA_ohlcv(item, "15m")[-1]  # 15분 전
    _5m_data = get_HA_ohlcv(item, "5m")[-2]  # 5분 전

    if _15m_data[1] < _15m_data[4] and _5m_data[1] < _5m_data[4]:
        return "buy"
    if _15m_data[1] > _15m_data[4] and _5m_data[1] > _5m_data[4]:
        return "sell"
    return None


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

futuers_tickers = ["YFI/USDT"]
position_size = [0]
prices = []

while 1:
    last_position = [
        check_match(futuers_tickers[i]) for i in range(len(futuers_tickers))
    ]
    print(last_position)
    if last_position[0] == None:
        print("start!")
        break
    time.sleep(17)

while 1:
    for i, item in enumerate(futuers_tickers):
        try:
            time.sleep(23)
            if int(get_time()[1]) % 5 != 0:
                continue
            temp = check_match(item)
            price = binance.fetch_ohlcv(item, "5m")[-1][4]
            if last_position[i] == None and temp == "buy":
                prices.append(price)
                last_position[i] = temp
            if last_position[i] == None and temp == "sell":
                prices.append(price)
                last_position[i] = temp
            if last_position[i] == "sell" and temp == None:
                earning = round(-100 + prices[0] / price * 99.985, 2)
                messege = ["buy exit", price, earning]
                bot.send_message(chat_id=801167350, text=str(messege))
                last_position[i] = None
                position_size[i] = 0
                prices.clear()
            if last_position[i] == "buy" and temp == None:
                earning = round(-100 + price / prices[0] * 99.985, 2)
                messege = ["sell exit", price, earning]
                bot.send_message(chat_id=801167350, text=str(messege))
                last_position[i] = None
                position_size[i] = 0
                prices.clear()
        except:
            continue

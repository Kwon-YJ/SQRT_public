import numpy as np
import ccxt

# from matplotlib import pyplot as plt
import pandas as pd
import math
import time
import datetime
import telegram


def calc_std(ohlcv, slope, intercept):  # 볼린저 밴드
    result = 0
    for i in range(0, len(ohlcv)):
        result += math.pow(ohlcv[i][4] - (i * slope + intercept), 2)

    return math.sqrt(result / len(ohlcv))


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


def qr_householder(A):
    m, n = A.shape
    Q = np.eye(m)  # Orthogonal transform so far
    R = A.copy()  # Transformed matrix so far

    for j in range(n):
        # Find H = I - beta*u*u' to put zeros below R[j,j]
        x = R[j:, j]
        normx = np.linalg.norm(x)
        rho = -np.sign(x[0])
        u1 = x[0] - rho * normx
        u = x / u1
        u[0] = 1
        beta = -rho * u1 / normx

        R[j:, :] = R[j:, :] - beta * np.outer(u, u).dot(R[j:, :])
        Q[:, j:] = Q[:, j:] - beta * Q[:, j:].dot(np.outer(u, u))

    return Q, R


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


bot = telegram.Bot(token=my_token)


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


def get_data(ticker):
    temp = binance.fetch_ohlcv(ticker, "5m")[-101:-1]
    close_ = temp[-1][4]
    temp = [[i + 1, temp[i][4]] for i in range(len(temp))]
    data = np.array(temp)

    m, n = data.shape
    A = np.array([data[:, 0], np.ones(m)]).T
    b = data[:, 1]

    Q, R = qr_householder(A)
    b_hat = Q.T.dot(b)

    R_upper = R[:n, :]
    b_upper = b_hat[:n]

    x = np.linalg.solve(R_upper, b_upper)
    slope, intercept = x
    # print(slope, intercept)

    mid = slope * 101 + intercept
    temp = binance.fetch_ohlcv(ticker, "5m")[-101:-1]
    bb_ = calc_std(temp, slope, intercept)
    upper = mid + 2 * bb_
    lower = mid - 2 * bb_
    print(ticker, upper, mid, lower)
    if close_ > upper:
        # print(ticker, 'upper')
        messege = [ticker, "upper"]
        # result.append(messege)
        bot.send_message(chat_id=801167350, text=str(messege))
    elif close_ < lower:
        # print(ticker, 'lower')
        messege = [ticker, "lower"]
        # result.append(messege)
        bot.send_message(chat_id=801167350, text=str(messege))


def get_data_2(ticker):
    print("get_data_2 start")
    ohlcv5 = binance.fetch_ohlcv(ticker, "5m")
    temp = convert(ohlcv5)[-100:-1]
    close_ = ohlcv5[-1][4]
    temp = [[i + 1, temp[i][4]] for i in range(len(temp))]
    temp.append([100, close_])
    data = np.array(temp)

    m, n = data.shape
    A = np.array([data[:, 0], np.ones(m)]).T
    b = data[:, 1]

    Q, R = qr_householder(A)
    b_hat = Q.T.dot(b)

    R_upper = R[:n, :]
    b_upper = b_hat[:n]

    x = np.linalg.solve(R_upper, b_upper)
    slope, intercept = x
    # print(slope, intercept)

    mid = slope * 101 + intercept
    # temp = slope * 98 + intercept
    # print(temp)
    temp = convert(binance.fetch_ohlcv(ticker, "5m"))[-101:-1]
    bb_ = calc_std(temp, slope, intercept)
    upper = (
        mid + 2 * bb_
    )  # -----------------------------------------------------------------------------
    lower = (
        mid - 2 * bb_
    )  # -----------------------------------------------------------------------------
    # print(ticker, upper , mid, lower)
    if close_ > upper:
        # print(ticker, 'upper')
        # messege = [ticker, 'upper']
        result.append(close_)
        time.sleep(60)
        send_result("sell")
        # result.append(messege)
        # bot.send_message(chat_id = 801167350, text = str(messege))
    elif close_ < lower:
        # print(ticker, 'lower')
        # messege = [ticker, 'lower']
        result.append(close_)
        time.sleep(60)
        send_result("buy")
        # result.append(messege)
        # bot.send_message(chat_id = 801167350, text = str(messege))


ticker_list = list(binance.fetch_tickers().keys())


result = []


def send_result(side):
    print("send_result start", side, get_time()[1])
    count_ = 0
    while 1:
        time.sleep(1)
        time_ = get_time()[1][2:]
        if int(time_) % 15 == 0:
            time.sleep(1)
            ohlcv5 = binance.fetch_ohlcv("FIL/USDT", "5m")
            temp = convert(ohlcv5)
            open_ = temp[-1][1]
            close_ = temp[-1][4]
            if side == "buy" and open_ < close_:
                print("count up")
                count_ = count_ + 1
                time.sleep(60)
            elif side == "sell" and open_ > close_:
                print("count down")
                count_ = count_ - 1
                time.sleep(60)
        if count_ > 2:
            print("count finished", get_time()[1])
            earning = 100 * (close_ / result[0]) * 0.99925 * 0.99925 - 1
            messege = ["buy_entry", earning]
            bot.send_message(chat_id=801167350, text=str(messege))
            result.clear()
            return None
        if count_ < -2:
            print("count finished", get_time()[1])
            earning = 100 * (result[0] / close_) * 0.99925 * 0.99925 - 1
            messege = ["sell_entry", earning]
            bot.send_message(chat_id=801167350, text=str(messege))
            result.clear()
            return None


while True:
    time.sleep(27)
    time_ = get_time()[1][2:]
    if int(time_) % 15 == 0:
        get_data_2("FIL/USDT")


"""
while(True):
    time.sleep(1)
    time_ = get_time()[1][2:]
    if int(time_) % 5 == 0:
        for i in range(len(ticker_list)):
            get_data(ticker_list[i])
        bot.send_message(chat_id = 801167350, text = str(result))
        result.clear()
        time.sleep(61)
"""


# -----------------------------# -----------------------------# -----------------------------# -----------------------------
# -----------------------------# -----------------------------# -----------------------------# -----------------------------
# -----------------------------# -----------------------------# -----------------------------# -----------------------------


"""

def on_sell_mode(ticker):
	price = get_sell_price()
	order = bitmex.create_order(ticker, 'limit', 'sell', size, price, params)
	time.sleep(3)

	while(True):
		time.sleep(0.5)
		state = bitmex.fetch_order_status(order['info']['orderID'])
		now = int(datetime.datetime.now().second)
		if now > 3:
			continue
		if state == 'closed':
			return None
		else:
			time.sleep(3)
			state = bitmex.fetch_order_status(order['info']['orderID'])
			if state != 'canceled':
				bitmex.cancel_order(order['info']['orderID'], ticker)

			price = get_sell_price()
			order = bitmex.create_order(ticker, 'limit', 'sell', size, price, params)
			continue		




while(True):
    time.sleep(13)
    time_ = get_time()[1][2:]
    if time_ == '00':
        time.sleep(10)
        for i, item in enumerate(long_ticker_list):
            try:
                ohlcv = binance.fetch_ohlcv(item, "1h")
                bb_ = bb(ohlcv)
                open_ = ohlcv[-2][1]
                high_ = ohlcv[-2][2]
                low_ = ohlcv[-2][3]
                close_ = ohlcv[-2][4]
                if high_ - low_ == 0:
                    continue
                IBS = (close_ - low_) / (high_ - low_)
                if IBS < 0.1 and close_ < bb_[0]:
                    long_entry(item, high_)
            except Exception as ex:
                time.sleep(2)
                continue
        for i, item in enumerate(short_ticker_list):
            try:
                ohlcv = binance.fetch_ohlcv(item, "1h")
                bb_ = bb(ohlcv)
                open_ = ohlcv[-2][1]
                high_ = ohlcv[-2][2]
                low_ = ohlcv[-2][3]
                close_ = ohlcv[-2][4]
                if high_ - low_ == 0:
                    continue
                IBS = (close_ - low_) / (high_ - low_)
                if IBS > 0.9 and close_ > bb_[-1]:
                    short_entry(item, low_)
            except Exception as ex:
                time.sleep(2)
                continue
        time.sleep(59)

"""

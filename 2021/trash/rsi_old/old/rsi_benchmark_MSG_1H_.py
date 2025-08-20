import datetime
import time
import telegram
import ccxt
import pandas as pd
import numpy as np


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


def send_MSG(message):
    while True:
        try:
            bot.send_message(chat_id=801167350, text=str(message))
            time.sleep(3)
            return None
        except:
            time.sleep(3)
            continue


def calcRSI(ohlcv, period):
    df = pd.DataFrame(
        data=np.array(ohlcv),
        columns=["time_stamp", "open", "high", "low", "close", "1"],
    )
    U = np.where(
        df.diff(1)["close"] > 0, df.diff(1)["close"], 0
    )  # df.diff를 통해 (기준일 종가 - 기준일 전일 종가)를 계산하여 0보다 크면 증가분을 감소했으면 0을 넣어줌
    D = np.where(
        df.diff(1)["close"] < 0, df.diff(1)["close"] * (-1), 0
    )  # df.diff를 통해 (기준일 종가 - 기준일 전일 종가)를 계산하여 0보다 작으면 감소분을 증가했으면 0을 넣어줌
    AU = pd.DataFrame(U).ewm(period).mean()  # AU, period=14일 동안의 U의 평균
    AD = pd.DataFrame(D).ewm(period).mean()  # AD, period=14일 동안의 D의 평균
    RSI = AU / (AD + AU) * 100  # 0부터 1로 표현되는 RSI에 100을 곱함
    return RSI
    # return float(RSI.tail(1)[0])


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

ticker_list = [
    "BTC/USDT",
    "ETH/USDT",
    "BCH/USDT",
    "XRP/USDT",
    "EOS/USDT",
    "LTC/USDT",
    "TRX/USDT",
    "ETC/USDT",
    "LINK/USDT",
    "XLM/USDT",
    "ADA/USDT",
    "XMR/USDT",
    "DASH/USDT",
    "ZEC/USDT",
    "XTZ/USDT",
    "BNB/USDT",
    "ATOM/USDT",
    "ONT/USDT",
    "IOTA/USDT",
    "BAT/USDT",
    "VET/USDT",
    "NEO/USDT",
    "QTUM/USDT",
    "IOST/USDT",
    "THETA/USDT",
    "ALGO/USDT",
    "ZIL/USDT",
    "KNC/USDT",
    "ZRX/USDT",
    "COMP/USDT",
    "OMG/USDT",
    "DOGE/USDT",
    "SXP/USDT",
    "KAVA/USDT",
    "BAND/USDT",
    "RLC/USDT",
    "WAVES/USDT",
    "MKR/USDT",
    "SNX/USDT",
    "DOT/USDT",
    "DEFI/USDT",
    "YFI/USDT",
    "BAL/USDT",
    "CRV/USDT",
    "TRB/USDT",
    "YFII/USDT",
    "RUNE/USDT",
    "SUSHI/USDT",
    "SRM/USDT",
    "BZRX/USDT",
    "EGLD/USDT",
    "SOL/USDT",
    "ICX/USDT",
    "STORJ/USDT",
    "BLZ/USDT",
    "UNI/USDT",
    "AVAX/USDT",
    "FTM/USDT",
    "HNT/USDT",
    "ENJ/USDT",
    "FLM/USDT",
    "TOMO/USDT",
    "REN/USDT",
    "KSM/USDT",
    "NEAR/USDT",
    "AAVE/USDT",
    "FIL/USDT",
    "RSR/USDT",
    "LRC/USDT",
    "MATIC/USDT",
    "OCEAN/USDT",
    "CVC/USDT",
    "BEL/USDT",
    "CTK/USDT",
    "AXS/USDT",
    "ALPHA/USDT",
    "ZEN/USDT",
    "SKL/USDT",
    "GRT/USDT",
    "1INCH/USDT",
]


bot = telegram.Bot(token=my_token)

up = []
down = []
all_ = []

if __name__ == "__main__":
    while 1:
        time.sleep(5)
        temp = int(get_time()[1][2:])
        if temp == 0:
            up.clear()
            down.clear()
            all_.clear()
            for i, item in enumerate(ticker_list):
                try:
                    ohlcv = binance.fetch_ohlcv(item, "1h")
                    RSI = calcRSI(ohlcv, 11)
                    temp = RSI.tail(2)
                    now = float(temp.iloc[1])
                    # D_1 = float(temp.iloc[0])
                    all_.append(now)
                    if now > 70:
                        up.append(item)
                    if now < 30:
                        down.append(item)
                except:
                    time.sleep(3)
                    continue
            if len(up) > 0 or len(down) > 0:
                avg = sum(all_) / len(all_)
                # send_MSG(['up :', len(up), up, 'down :', len(down), down, 'avg :', avg])
                send_MSG(["up :", len(up), "down :", len(down), "avg :", avg])
            time.sleep(60)

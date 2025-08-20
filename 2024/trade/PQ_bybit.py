from pybit.unified_trading import WebSocket
from pybit.unified_trading import HTTP
from time import sleep
from collections import deque
import numpy as np
import ccxt
import telegram
import datetime
import time

import json

import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


global global_dict
global_dict = {
    "1h": [],
    "2h": [],
    "4h": [],
    "6h": [],
    "8h": [],
    "12h": [],
}


last_callback_time = 0


class Data_struct:
    def __init__(
        self,
        target_price,
        order_dict,
        money,
    ):
        self.target_price = target_price
        self.order_dict = order_dict
        self.money = money




def get_time():
    result = str(datetime.datetime.utcfromtimestamp(time.time()))
    return result[14:16]


def telegram_send(data):
    bot = telegram.Bot(token=my_token)
    if type(data) != "str":
        data = str(data)
    while 1:
        # try:
        bot.send_message(chat_id=801167350, text=data)
        sleep(3)
        return None
    # except:
    #    continue


def exit_side(data):
    for ticker in list(data.keys()):
        try:
            bybit.create_market_sell_order(ticker, data[ticker])
        except Exception as e:
            telegram_send(f"PQ exit_side error {ticker} {e}")
            sleep(1)


def precision_optimize(ticker, amount, price):
    ticker = ticker.split("/")[0] + "USDT"
    session = HTTP(testnet=False)
    market_info = session.get_instruments_info(
        category="linear",
        symbol=ticker,
    )
    amount = round(
        amount,
        len(
            market_info["result"]["list"][0]["lotSizeFilter"]["minOrderQty"].split(".")[
                -1
            ]
        ),
    )
    price = round(
        price,
        len(market_info["result"]["list"][0]["priceFilter"]["tickSize"].split(".")[-1])
        - 1,
    )
    return amount, price


def get_amount(ticker, money):
    price = bybit.fetch_ohlcv(ticker, "1m", limit=2)[-1][4]
    amount = money / price
    amount, price = precision_optimize(ticker, amount, price)
    return amount, price


def timestamp_to_datetime(timestamp):
    datetimeobj = datetime.datetime.fromtimestamp(timestamp / 1000)
    original_time_data = str(datetimeobj)
    return original_time_data


def entry_side_P(current_price, ticker, time_data):
    pass


def entry_side_Q(current_price, ticker, time_data):
    pass


# elastic_data_Q = [1+0.2*(i-1) for i in range(1,200)]
# elastic_data_Q = [1+0.21*(i-1) for i in range(1,200)]
elastic_data_Q = [1 + 0.205 * (i - 1) for i in range(1, 200)]
# elastic_data_P = [1.0006, 1.0006, 1.0006, 1.0006, 1.0006, 1.0036, 1.0042, 1.0048, 1.0054, 1.006, 1.0066, 1.03, 1.03255, 1.0348, 1.03705, 1.0393, 1.04155, 1.0438, 1.04605, 1.0483, 1.05055, 1.0528, 1.05505, 1.0573, 1.05955, 1.294, 1.303, 1.312, 1.321, 1.33, 1.339, 1.348, 1.357, 1.366, 1.375, 1.384, 1.393, 1.402, 1.411, 1.42, 1.429, 1.438, 1.447, 1.456, 1.465, 1.474, 1.483, 1.492, 1.501, 1.51, 1.519, 1.528, 1.537, 1.546, 1.555, 1.564, 1.573, 1.582, 1.591, 1.6, 1.609, 1.618, 1.627, 1.636, 1.645, 1.654, 1.663, 1.672, 1.681, 1.69, 1.699, 1.708, 1.717, 1.726, 1.735, 1.744, 1.753, 1.762, 1.771, 1.78, 1.789, 1.798, 1.807, 1.816, 1.825, 1.834, 1.843, 1.852, 1.861, 1.87, 1.879, 1.888, 1.897, 1.906, 1.915, 1.924, 1.933, 1.942, 1.951, 1.96]
elastic_data_P = [
    1.0006,
    1.0006,
    1.0006,
    1.0006,
    1.0006,
    1.0036,
    1.0042,
    1.0048,
    1.0054,
    1.006,
    1.0066,
    1.03,
    1.03255,
    1.0348,
    1.03705,
    1.0393,
    1.04155,
    1.0438,
    1.04605,
    1.0483,
    1.05055,
    1.0528,
    1.05505,
    1.0573,
    1.05955,
    1.294,
    1.303,
    1.312,
    1.321,
    1.33,
    1.339,
    1.348,
    1.357,
    1.366,
    1.375,
    1.384,
    1.393,
    1.4020000000000001,
    1.411,
    1.42,
    1.4289999999999998,
    1.438,
    1.447,
    1.456,
    1.4649999999999999,
    1.474,
    1.483,
    1.492,
    1.501,
    1.51,
    1.519,
    1.528,
    1.537,
    1.546,
    1.555,
    1.564,
    1.573,
    1.582,
    1.591,
    1.6,
    1.609,
    1.6179999999999999,
    1.627,
    1.6360000000000001,
    1.645,
    1.654,
    1.663,
    1.6720000000000002,
    1.681,
    1.69,
    1.699,
    1.708,
    1.717,
    1.726,
    1.7349999999999999,
    1.744,
    1.7530000000000001,
    1.762,
    1.771,
    1.78,
    1.7890000000000001,
    1.798,
    1.807,
    1.816,
    1.8250000000000002,
    1.834,
    1.843,
    1.8519999999999999,
    1.861,
    1.8699999999999999,
    1.879,
    1.888,
    1.897,
    1.906,
    1.915,
    1.924,
    1.933,
    1.942,
    1.951,
    1.96,
]


bybit = ccxt.bybit(
    {
        "options": {
            "defaultType": "future",
        },
        "timeout": 30000,
        "apiKey": "ldbPGPjWisdJVVGii4",
        "secret": "FxxmGghYqYiipXEOlchBxzRDf5Qwh3JZ0nBu",
        "enableRateLimit": False,
    }
)


global _6h_data
# _6h_data = Data_struct(data_init_P("6h", True), {}, 715)
_6h_data = Data_struct(data_init_P("6h", True), {}, 1100)

global _12h_data
# _12h_data = Data_struct(data_init_Q("12h"), {}, 100)
_12h_data = Data_struct(data_init_Q("12h"), {}, 200)


ticker_list = get_tickers_bybit()


def handle_message(message):
    global last_callback_time
    last_callback_time = time.time()
    current_time = get_time()
    if current_time in {"59", "00", "01", "02"}:
        return None

    data = message["data"][0]
    time_ = message["ts"]
    ticker = data["s"][:-4] + "/USDT:USDT"
    price = data["p"]
    # try:
    entry_side_P(price, ticker, time_)
    entry_side_Q(price, ticker, time_)
    # except Exception as e:
    #    logger.info(e)


ticker_list_ws = [
    "TRXUSDT",
    "BAKEUSDT",
    "SOLUSDT",
    "SPELLUSDT",
    "RADUSDT",
    "SSVUSDT",
    "ARUSDT",
    "TOMOUSDT",
    "ARBUSDT",
    "LRCUSDT",
    "DOGEUSDT",
    "NEOUSDT",
    "GALAUSDT",
    "SUIUSDT",
    "MANAUSDT",
    "LTCUSDT",
    "LEVERUSDT",
    "BLURUSDT",
    "COMPUSDT",
    "VETUSDT",
    "LUNA2USDT",
    "CTKUSDT",
    "MASKUSDT",
    "PEOPLEUSDT",
    "TRUUSDT",
    "DARUSDT",
    "C98USDT",
    "ENSUSDT",
    "AAVEUSDT",
    "COMBOUSDT",
    "CKBUSDT",
    "KSMUSDT",
    "ALPHAUSDT",
    "CRVUSDT",
    "LDOUSDT",
    "SKLUSDT",
    "HFTUSDT",
    "OPUSDT",
    "DGBUSDT",
    "QNTUSDT",
    "ADAUSDT",
    "HOTUSDT",
    "IOSTUSDT",
    "IOTXUSDT",
    "CTSIUSDT",
    "ACHUSDT",
    "UMAUSDT",
    "MATICUSDT",
    "PERPUSDT",
    "THETAUSDT",
    "STORJUSDT",
    "SANDUSDT",
    "JOEUSDT",
    "HBARUSDT",
    "BNBUSDT",
    "INJUSDT",
    "ZRXUSDT",
    "DASHUSDT",
    "REEFUSDT",
    "GALUSDT",
    "AMBUSDT",
    "FETUSDT",
    "FLOWUSDT",
    "WAVESUSDT",
    "RVNUSDT",
    "CFXUSDT",
    "SXPUSDT",
    "EGLDUSDT",
    "API3USDT",
    "ROSEUSDT",
    "EOSUSDT",
    "XTZUSDT",
    "AVAXUSDT",
    "ICPUSDT",
    "SNXUSDT",
    "RENUSDT",
    "XLMUSDT",
    "1000PEPEUSDT",
    "FTMUSDT",
    "WOOUSDT",
    "KAVAUSDT",
    "ZENUSDT",
    "AUDIOUSDT",
    "IDUSDT",
    "ONEUSDT",
    "OGNUSDT",
    "ARPAUSDT",
    "RDNTUSDT",
    "BCHUSDT",
    "CHZUSDT",
    "MKRUSDT",
    "KLAYUSDT",
    "KEYUSDT",
    "UNIUSDT",
    "HOOKUSDT",
    "CELOUSDT",
    "ETCUSDT",
    "STGUSDT",
    "LINAUSDT",
    "ONTUSDT",
    "ATOMUSDT",
    "ASTRUSDT",
    "BATUSDT",
    "QTUMUSDT",
    "SFPUSDT",
    "ATAUSDT",
    "MINAUSDT",
    "SUSHIUSDT",
    "RUNEUSDT",
    "RSRUSDT",
    "ZECUSDT",
    "TLMUSDT",
    "RLCUSDT",
    "FXSUSDT",
    "APTUSDT",
    "ANTUSDT",
    "BLZUSDT",
    "DENTUSDT",
    "XEMUSDT",
    "BALUSDT",
    "MTLUSDT",
    "HIGHUSDT",
    "DUSKUSDT",
    "JASMYUSDT",
    "GTCUSDT",
    "XVSUSDT",
    "ANKRUSDT",
    "PHBUSDT",
    "COTIUSDT",
    "XMRUSDT",
    "DOTUSDT",
    "KNCUSDT",
    "OMGUSDT",
    "GMTUSDT",
    "UNFIUSDT",
    "AGIXUSDT",
    "TRBUSDT",
    "GRTUSDT",
    "BELUSDT",
    "ENJUSDT",
    "AXSUSDT",
    "FILUSDT",
    "ALGOUSDT",
    "DYDXUSDT",
    "CVXUSDT",
    "LPTUSDT",
    "STXUSDT",
    "TUSDT",
    "RNDRUSDT",
    "APEUSDT",
    "IDEXUSDT",
    "BANDUSDT",
    "1000XECUSDT",
    "IMXUSDT",
    "LQTYUSDT",
    "LINKUSDT",
    "1000FLOKIUSDT",
    "OCEANUSDT",
    "ZILUSDT",
    "IOTAUSDT",
    "EDUUSDT",
    "FLMUSDT",
    "STMXUSDT",
    "CELRUSDT",
    "NEARUSDT",
    "GMXUSDT",
    "1INCHUSDT",
    "ALICEUSDT",
    "XRPUSDT",
    "MAGICUSDT",
    "ICXUSDT",
    "LITUSDT",
    "BNXUSDT",
    "ETHUSDT",
    "1000LUNCUSDT",
    "CHRUSDT",
    "NKNUSDT",
]


async def websocket_handler():
    while True:
        ws = WebSocket(testnet=False, channel_type="linear")
        ws.trade_stream(ticker_list_ws, handle_message)
        await asyncio.sleep(10)
        while True:
            global last_callback_time
            await asyncio.sleep(0.001)
            if time.time() - last_callback_time > 60:
                time_var = str(datetime.datetime.utcfromtimestamp(time.time()))
                try:
                    ws.exit()
                except:
                    pass
                logger.info(f"reconnected at {time_var}")
                break


async def main_loop():
    task = asyncio.create_task(
        websocket_handler()
    )  # websocket_handler를 백그라운드 태스크로 실행

    while True:
        await asyncio.sleep(1)
        current_time = get_time()

        if current_time == "00":
            global _6h_data
            global _12h_data

            await asyncio.sleep(10)
            now = datetime.datetime.utcfromtimestamp(time.time())
            hh = str(now.hour)

            if int(hh) in [6, 12, 18, 0, 24]:
                exit_side(_6h_data.order_dict)
                _6h_data = Data_struct(data_init_P("6h", True), {}, 715)

            if int(hh) in [12, 0, 24]:
                exit_side(_12h_data.order_dict)
                now = datetime.datetime.utcfromtimestamp(time.time())
                logger.info(f"exit at {now}")
                break  # asyncio의 루프 내에서는 exit() 대신 break를 사용

            await asyncio.sleep(50)
            time_var = str(datetime.datetime.utcfromtimestamp(time.time()))
            logger.info(f"bybit {time_var}")


asyncio.run(main_loop())

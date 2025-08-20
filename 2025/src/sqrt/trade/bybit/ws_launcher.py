"""퀵 터틀 실행파일"""

import asyncio
import platform
import logging
import time
import datetime
import crypto

if platform.system() == "Darwin":
    import sys

    sys.modules["Crypto"] = crypto

from pybit.unified_trading import WebSocket


from sqrt.trade.crypto.bybit.quick_turtle import *
from sqrt.trade.crypto.bybit.quick_turtle import (
    get_data_struct,
    get_time,
    update_data_struct,
    all_exit,
    get_amount,
    bybit,
    timestamp_to_datetime,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

temp_dict = {}


def handle_message(message: dict) -> None:
    """
    웹소켓 콜백함수
    """
    global LAST_CALLBACK_TIME
    LAST_CALLBACK_TIME = time.time()
    current_time = get_time()
    if current_time in {"59", "00", "01", "02"}:
        return None

    data = message["data"][0]
    time_ = message["ts"]
    ticker = data["s"]  # [:-4] + "/USDT:USDT"
    price = float(data["p"])


    # print(data)
    # try:

    verbose = False
    if ticker in temp_dict.keys():
        if temp_dict[ticker] > price:
            temp_dict[ticker] = price
            logger.info("UTC %s UPDATE %s %s", LAST_CALLBACK_TIME, ticker, price)
            logger.info(temp_dict)
            verbose = True
    else:
        temp_dict[ticker] = price
        logger.info("UTC %s ADD %s %s", LAST_CALLBACK_TIME, ticker, price)
        logger.info(temp_dict)
        verbose = True

    global data_struct

    for key, vlaue in data_struct.items():
        if ticker not in vlaue.ticker_list:
            continue
        if ticker in vlaue.order_dict:
            continue


        current_order_count = len(vlaue.order_dict)
        target_price = vlaue.target_price[ticker][current_order_count]

        if verbose == True:
            logger.info(
                f"{ticker} {key} current_price {price} target_price {target_price}"
            )

        if price < target_price:
            # try:

            symbol = _get_symbol_from_ticker(ticker)

            trade_amount, _ = get_amount(symbol, vlaue.money)

            bybit.create_market_buy_order(symbol, trade_amount)
            # vlaue[key].order_dict[ticker] = trade_amount # err point
            vlaue.order_dict[ticker] = trade_amount # err point

            time_var = str(datetime.datetime.utcfromtimestamp(time.time()))
            logger.info("%s\n%s\n%s\n%s\n", ticker, timestamp_to_datetime(time_), time_var, trade_amount)
            logger.info(f"{ticker} BUY {key} qty : {trade_amount}")
            # telegram_send(f"{ticker} BUY {key} qty : {trade_amount}")

            # except Exception as e:
            #    telegram_send(f"PQ entry_side_P error {ticker} {e}")
            #    sleep(1)

    # except Exception as e:
    #    logger.info(e)


async def websocket_handler() -> None:
    """웹소켓 수신부, 콜백함수에서 엔트리 처리"""
    logger.info("websocket start.")
    # fmt: off
    ticker_list_ws = ["MYROUSDT", "BEAMUSDT", "TIAUSDT", "JUPUSDT", "WIFUSDT", "ARKMUSDT", "ENAUSDT", "AXLUSDT", "ZETAUSDT", "WUSDT", "1000BONKUSDT", "INJUSDT", "ORDIUSDT", "JTOUSDT", "XAIUSDT", "PYTHUSDT", "MEMEUSDT", "BOMEUSDT", "METISUSDT", "STRKUSDT", "POWRUSDT", "ONDOUSDT", "PENDLEUSDT", "ILVUSDT", "XVGUSDT", "TOKENUSDT", "NTRNUSDT", "GLMUSDT", "WLDUSDT", "BICOUSDT", "SEIUSDT", "1000PEPEUSDT", "YFIUSDT", "AIUSDT", "10000SATSUSDT", "DYMUSDT", "MKRUSDT", "POLYXUSDT", "CYBERUSDT", "BSVUSDT", "PIXELUSDT", "ALTUSDT", "BIGTIMEUSDT", "ARBUSDT", "NFPUSDT", "STXUSDT", "REZUSDT", "BLURUSDT", "MOVRUSDT", "ETHWUSDT", "1000LUNCUSDT", "VANRYUSDT", "USTCUSDT", "SPELLUSDT", "ETHFIUSDT", "AEVOUSDT", "NMRUSDT", "AUCTIONUSDT", "STEEMUSDT", "SUIUSDT", "OPUSDT", "MTLUSDT", "SSVUSDT", "MAVUSDT", "LSKUSDT", "TAOUSDT", "OXTUSDT", "IMXUSDT", "GALAUSDT", "SUPERUSDT", "QNTUSDT", "DYDXUSDT", "AGLDUSDT", "DOGEUSDT", "HFTUSDT", "THETAUSDT", "HBARUSDT", "TWTUSDT", "CELRUSDT", "HOTUSDT", "ENSUSDT", "HIFIUSDT", "YGGUSDT", "HIGHUSDT", "LDOUSDT", "CKBUSDT", "PEOPLEUSDT", "FETUSDT", "ROSEUSDT", "MINAUSDT", "API3USDT", "SOLUSDT", "SFPUSDT", "RONINUSDT", "PHBUSDT", "TRUUSDT", "BNTUSDT", "APTUSDT", "SAGAUSDT", "ICPUSDT", "WAXPUSDT", "DODOUSDT", "RLCUSDT", "XRPUSDT", "OMNIUSDT", "OGNUSDT", "ASTRUSDT", "JASMYUSDT", "TONUSDT", "OMUSDT", "ARKUSDT", "GASUSDT", "ONGUSDT", "KSMUSDT", "ANKRUSDT", "TUSDT", "KNCUSDT", "RDNTUSDT", "NEARUSDT", "ETCUSDT", "NEOUSDT", "UNIUSDT", "GRTUSDT", "BANDUSDT", "LRCUSDT", "RIFUSDT", "ATOMUSDT", "ONTUSDT", "VETUSDT", "ALPHAUSDT", "SNXUSDT", "SKLUSDT", "JOEUSDT", "HOOKUSDT", "QTUMUSDT", "ZILUSDT", "MASKUSDT", "GTCUSDT", "ALGOUSDT"]
    # fmt: on

    while True:
        global LAST_CALLBACK_TIME
        ws = WebSocket(testnet=False, channel_type="linear")
        ws.trade_stream(ticker_list_ws, handle_message)
        await asyncio.sleep(10)
        while True:
            await asyncio.sleep(0.01)
            # logger.info(time.time() - LAST_CALLBACK_TIME)
            if time.time() - LAST_CALLBACK_TIME > 60:
                time_var = str(datetime.datetime.utcfromtimestamp(time.time()))
                try:
                    ws.exit()
                except:
                    pass
                logger.info("reconnected at %s", time_var)
                break


async def main_loop() -> None:
    """
    핵심 비동기 함수
    """
    task = asyncio.create_task(
        websocket_handler()
    )  # websocket_handler를 백그라운드 태스크로 실행

    global data_struct
    while True:
        await asyncio.sleep(1)
        current_time = get_time()
        if current_time == "00":
            all_exit(data_struct)
            await asyncio.sleep(20)
            data_struct = update_data_struct(data_struct)
            if data_struct == {}:
                now = datetime.datetime.utcfromtimestamp(time.time())
                logger.info("exit at %s", str(now))
                break

            await asyncio.sleep(50)
            time_var = str(datetime.datetime.utcfromtimestamp(time.time()))
            logger.info("bybit %s", time_var)


def _get_symbol_from_ticker(ticker):
    """ticker -> symbol 변환 캐시"""
    if ticker not in _ticker_symbol_cache:
        _ticker_symbol_cache[ticker] = ticker[:-4] + "/USDT:USDT"
    return _ticker_symbol_cache[ticker]

if __name__ == "__main__":
    _ticker_symbol_cache = {}  # ticker -> symbol 변환 캐시

    global LAST_CALLBACK_TIME
    LAST_CALLBACK_TIME = 0

    global data_struct
    data_struct = get_data_struct()

    asyncio.run(main_loop())

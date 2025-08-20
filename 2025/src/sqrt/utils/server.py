"""rye run uvicorn server:app --reload"""

import ccxt
from fastapi import FastAPI
from typing import Union
from dotenv import load_dotenv
import os
import telegram
import ast
import datetime

load_dotenv()


def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance


@singleton
class Exchanges:
    def __init__(self) -> None:
        self.master_key = {
            "binance_spot": ccxt.binance(
                {
                    "options": {"defaultType": "spot"},
                    "apiKey": os.getenv("binance_pub"),
                    "secret": os.getenv("binance_sec"),
                }
            ),
            "binance_future": ccxt.binance(
                {
                    "options": {"defaultType": "future"},
                    "apiKey": os.getenv("binance_pub"),
                    "secret": os.getenv("binance_sec"),
                }
            ),
            "bybit_spot": ccxt.bybit(
                {
                    "options": {"defaultType": "spot"},
                    "apiKey": os.getenv("bybit_pub"),
                    "secret": os.getenv("bybit_sec"),
                }
            ),
            "bybit_future": ccxt.bybit(
                {
                    "options": {"defaultType": "future"},
                    "apiKey": os.getenv("bybit_pub"),
                    "secret": os.getenv("bybit_sec"),
                }
            ),
            "gateio_spot": ccxt.gateio(
                {
                    "options": {"defaultType": "spot"},
                    "rateLimit": 64,
                    # "apiKey": os.getenv("bybit_pub"),
                    # "secret": os.getenv("bybit_sec"),
                }
            ),
            "gateio_future": ccxt.gateio(
                {
                    "options": {"defaultType": "swap"},
                    "rateLimit": 20,
                    # "apiKey": os.getenv("bybit_pub"),
                    # "secret": os.getenv("bybit_sec"),
                }
            ),
        }
        [
            self.master_key[exchange].load_markets()
            for exchange in self.master_key.keys()
        ]


def invoke_exchange_api(exchange: str, method: str, *args, **kwargs):
    exchanges = Exchanges()
    try:
        print(datetime.datetime.now())
        return getattr(exchanges.master_key[exchange], method)(*args, **kwargs)
    except AttributeError:
        return f"method {method} is not found."
    except Exception as e:
        return f"unknown err : {e}"


exchanges = Exchanges()
app = FastAPI()


# @app.get("/")
# def read_root(exchange: str, method: str, args: Union[str, None] = None):
#     return invoke_exchange_api(exchange, method, *eval(args) if args else ())
#     # usage: http://127.0.0.1:8000/?exchange=binance_spot&method=fetch_ohlcv&args='BTC/USDT','1h'


@app.get("/")
def read_root(
    exchange: str,
    method: str,
    args: str = "()",
    kwargs: str = "{}",
):
    """
    Usage:
    http://127.0.0.1:8000/?exchange=binance_future&method=fetch_ohlcv&args=('APT/USDT:USDT','1d')&kwargs={'limit':1499}
    """
    # parsed_args = ast.literal_eval(args)
    # parsed_kwargs = ast.literal_eval(kwargs)

    parsed_args = ast.literal_eval(args)
    parsed_kwargs = ast.literal_eval(kwargs)

    return invoke_exchange_api(exchange, method, *parsed_args, **parsed_kwargs)


@app.get("/telegram")
def send_telegram_message(message: str):
    bot = telegram.Bot(token=os.getenv("telegram_token"))
    if type(message) != "str":
        message = str(message)
    try:
        result = bot.send_message(chat_id=os.getenv("telegram_id"), text=message)
    except:
        result = bot.send_message(chat_id=os.getenv("telegram_id"), text=message)
        return {}
    return {}

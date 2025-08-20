"""KRX LS증권 EMA 816 전략 실행"""

import datetime
import time
import os
import pickle
import subprocess
from pykrx import stock
from utils import LSSecuritiesAPI
from utils import *
from pandas import DataFrame


def set_upper_pirce(pickle_data: dict) -> None:
    for ticker in ORDERD_DICT.keys():
        qty, upper, lower = ORDERD_DICT[ticker]
        if upper < 0:
            new_upper = get_ohlcv(ticker).iloc[-1]["시가"] + (-1 * upper)
            ORDERD_DICT[ticker] = [qty, new_upper, lower]
    with open("ORDERD_DICT.pickle", "wb") as f:
        pickle.dump(ORDERD_DICT, f)
    return ORDERD_DICT


def exit_side(LS_api: LSSecuritiesAPI) -> dict[str, list]:
    """
    조건 해당하는 종목 매도 수행하는 함수
    """
    del_list = []
    for code in ORDERD_DICT.keys():
        time.sleep(0.3)
        qty, upper, lower = ORDERD_DICT[code]
        current_price = LS_api.get_current_price(shcode=code)
        if current_price > upper:
            LS_api.place_order(
                isu_no=code,
                ord_qty=qty,
                ord_prc=0,
                bns_tp_code="1",
                ordprc_ptn_code="03",
                acnt_no=20717606604,
                acnt_pwd=8524,
            )
            del_list.append(code)
        elif current_price < lower:
            LS_api.place_order(
                isu_no=code,
                ord_qty=qty,
                ord_prc=0,
                bns_tp_code="1",
                ordprc_ptn_code="03",
                acnt_no=20717606604,
                acnt_pwd=8524,
            )
            del_list.append(code)

    for ticker in del_list:
        del ORDERD_DICT[ticker]

    if len(del_list) != 0:
        with open("ORDERD_DICT.pickle", "wb") as f:
            pickle.dump(ORDERD_DICT, f)
    return ORDERD_DICT


def get_ohlcv(ticker: str) -> DataFrame:
    start_time = str(datetime.datetime.now() - datetime.timedelta(300))
    start_time = (start_time).split(" ", maxsplit=1)[0].replace("-", "")
    end_time = get_time()[0]
    return stock.get_market_ohlcv(start_time, end_time, ticker)


if __name__ == "__main__":
    ORDERD_DICT: dict[str, list] = {}
    if os.path.isfile("ORDERD_DICT.pickle"):
        with open("ORDERD_DICT.pickle", "rb") as f:
            ORDERD_DICT = pickle.load(f)
    ORDERD_DICT = set_upper_pirce(ORDERD_DICT)

    APPKEY = ""
    APPSECRETKEY = ""
    api: LSSecuritiesAPI = LSSecuritiesAPI(APPKEY, APPSECRETKEY)

    if api.authenticate() != True:
        print("fail auth!")
        exit()

    while 1:
        time.sleep(1)
        ORDERD_DICT = exit_side(api)

        if get_time()[-1] == "1515":
            result = subprocess.run(
                ["python3", "entry_module.py"], capture_output=True, text=True
            )
            print(result.stdout)
            exit()

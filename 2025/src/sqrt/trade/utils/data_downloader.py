"""코인, 주식 데이터 저장"""

import os
from time import sleep
from pykrx import stock
from tqdm import tqdm

# pylint: disable=E0611
from julia import Main as julia_space  # type: ignore

from .time_tool import get_time


def krx_saver() -> None:
    """
    오늘자 기준, 코스피, 코스닥 상장사 일봉 데이터 저장
    """
    os.makedirs("./src/data/krx", exist_ok=True)
    today: str = get_time()[0]
    tickers: list = stock.get_market_ticker_list(today, market="ALL")
    for ticker in tqdm(tickers):
        ticker_name = stock.get_market_ticker_name(ticker)
        df = stock.get_market_ohlcv("20001210", today, ticker)
        df.to_csv(f"./src/data/krx/{ticker_name}.csv")
        sleep(1)


def binance_saver() -> None:
    """
    오늘자 기준, binance futuers 티커 데이터 저장
    """
    julia_space.include("./src/sqrt/utils/jl_module/utils.jl")
    tickers: list[str] = julia_space.get_tickers()

    for ticker in tqdm(tickers):
        os.system(
            f"julia ./src/sqrt/utils/jl_module/crypto_module.jl --ticker {ticker}"
        )
